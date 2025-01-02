import sqlite3
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from groq import Groq
# import os
from models.my_courses.course_embed import process_file  # Import the process_file function
import PyPDF2
import re
import time
from models.my_courses.course_chat import get_chat_response, get_chat_history, get_suggested_questions, imp_chat_response # Import the chat processing function
from datetime import datetime
from models.my_courses.course_podcast import generate_podcast as generate_podcast_audio, check_podcast_status
from models.my_courses.course_exam import generate_exam, evaluate_exam  # Import exam functions


client = Groq(api_key='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')

courses = Blueprint('courses', __name__, template_folder='templates')

@courses.route('/my_courses')
def my_courses():
    if 'user' not in session:
        flash('You need to login first!', 'error')
        return redirect(url_for('auth.login'))
    
    conn = sqlite3.connect('learning_helper_assistant.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT title
        FROM user_courses
        WHERE username = ?
    ''', (session['user'],))
    titles = cursor.fetchall()
    
    courses_with_progress = []
    for (title,) in titles:
        cursor.execute('''
            SELECT COUNT(*) FROM user_topics
            WHERE username = ? AND title = ?
        ''', (session['user'], title))
        total_topics = cursor.fetchone()[0]
        cursor.execute('''
            SELECT COUNT(*) FROM user_topics
            WHERE username = ? AND title = ? AND completed = 1
        ''', (session['user'], title))
        completed_topics = cursor.fetchone()[0]
        courses_with_progress.append((title, completed_topics, total_topics))
    
    conn.close()
    return render_template('courses.html', courses=courses_with_progress)




@courses.route('/upload_course', methods=['GET', 'POST'])
def upload_course():
    if request.method == 'POST':
        title = request.form['title']
        file = request.files['file']
        index_checked = request.form['index_checked'] == 'true'
        
        if index_checked:
            start_page = int(request.form['start_page']) - 1  # Adjust for zero-based index
            end_page = int(request.form['end_page'])
            reader = PyPDF2.PdfReader(file)

            # Extract index text
            index_text = ''
            for page_num in range(start_page, end_page):
                index_text += reader.pages[page_num].extract_text()

            # Extract full PDF text
            full_text = ''
            for page in reader.pages:
                full_text += page.extract_text()

            # Save full text into user_courses
            conn = sqlite3.connect('learning_helper_assistant.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO user_courses (username, title, content)
                VALUES (?, ?, ?)
            ''', (session['user'], title, full_text))
            conn.commit()

            # Generate topics based on index text
            completion = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {
                        "role": "system",
                        "content": f'''
                                    Extract the main topics listed in the following index text for the title: {title}.
                                    Provide an array of topics in the format: ['topic1', 'topic2', 'topic3'].
                                    If the data is not clear, provide main topics based on the title: {title}. It can be some extra topics.
                                    Caution : Only provide an array like the given example with the relavant title: ex: ['topic1', 'topic2', 'topic3']
                                    \nIndex text: {index_text}
                                '''
                    }
                ],
                temperature=0.7,
                max_tokens=8192,
                top_p=1,
                stream=False,
                stop=None,
            )
            response = completion.choices[0].message.content
            match = re.search(r'\[(.*?)\]', response)
            if match:
                array_string = match.group(1)
                array_string = array_string.replace("'", "").replace('"', '')
                array_list = [item.strip() for item in array_string.split(',')]
                array = array_list
                for topic in array:
                    cursor.execute('''
                        INSERT INTO user_topics (username, title, topic)
                        VALUES (?, ?, ?)
                    ''', (session['user'], title, topic))
                    conn.commit()
            conn.close()

            # Process full text with process_file
            db_name = f"{session['user']}_{title}.db"
            process_file(full_text, db_name)

            flash('Course uploaded successfully!', 'success')
            return redirect(url_for('courses.my_courses'))

        else:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
            
            conn = sqlite3.connect('learning_helper_assistant.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO user_courses (username, title, content)
                VALUES (?, ?, ?)
            ''', (session['user'], title, text))
            conn.commit()
            
            # Summarize the PDF in chunks to reduce context window
            summaries = []
            chunk_size = 2000  # Adjusted chunk size to control token usage
            max_tokens_per_request = 800  # Adjusted max_tokens per request
            requests_made = 0
            tokens_used = 0
            start_time = time.time()

            for i in range(0, len(text), chunk_size):
                chunk = text[i:i+chunk_size]
                estimated_input_tokens = len(chunk) // 4  # Approximate conversion: 1 token ≈ 4 characters
                estimated_tokens = estimated_input_tokens + max_tokens_per_request

                # Rate limiting for tokens per minute
                tokens_used += estimated_tokens
                elapsed_time = time.time() - start_time
                if tokens_used > 30000:
                    sleep_time = 60 - elapsed_time
                    if sleep_time > 0:
                        time.sleep(sleep_time)
                    tokens_used = 0
                    start_time = time.time()

                # Rate limiting for requests per minute
                requests_made += 1
                if requests_made > 29:
                    sleep_time = 60 - elapsed_time
                    if sleep_time > 0:
                        time.sleep(sleep_time)
                    requests_made = 0
                    start_time = time.time()

                summary_completion = client.chat.completions.create(
                    model="llama3-8b-8192",
                    messages=[
                        {
                            "role": "system",
                            "content": f"Summarize the following text of what is the main topic specifically covered in this data :\n\n{chunk}"
                        }
                    ],
                    temperature=2,
                    max_tokens=max_tokens_per_request,
                    top_p=1,
                    stream=False,
                    stop=None,
                )
                summary = summary_completion.choices[0].message.content.strip()
                summaries.append(summary)

            combined_summary = ' '.join(summaries)
            
            # Use the combined summary to get the topics array
            completion = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {
                        "role": "system",
                        "content": f'''
                        Give me the best roadmap or course outline for the given title: {title} and the data is {combined_summary}. 
                        Give me the main topics to cover in an array format and make sure of the square brackets of the array and the comma separation.
                        If the data is not clear, Then provide the main topics based on the title: {title}
                        Caution : Only provide an array like the given example with the relavant title: ex: ['topic1', 'topic2', 'topic3']
                        '''
                    }
                ],
                temperature=0.7,
                max_tokens=8192,
                top_p=1,
                stream=False,
                stop=None,
            )
            response = completion.choices[0].message.content
            print(response)
            # Initialize array with default topics based on title
            array = [title, "Introduction", "Basic Concepts", "Advanced Topics", "Summary"]
            
            match = re.search(r'\[(.*?)\]', response)
            print(match)
            if match:
                array_string = match.group(1)
                print(array_string)
                array_string = array_string.replace("'", "").replace('"', '')
                print(array_string)
                array_list = [item.strip() for item in array_string.split(',')]
                if array_list and len(array_list) > 0:  # Only update array if we got valid topics
                    array = array_list
                print(array)

            # Add error handling around database operations
            try:
                for topic in array:
                    if topic:  # Only insert non-empty topics
                        cursor.execute('''
                            INSERT INTO user_topics (username, title, topic)
                            VALUES (?, ?, ?)
                        ''', (session['user'], title, topic))
                conn.commit()
            except sqlite3.Error as e:
                print(f"Database error: {e}")
                flash('Error saving topics, but course was uploaded', 'warning')

            conn.close()


            db_name = f"{session['user']}_{title}.db"
            process_file(text, db_name)


            flash('Course uploaded successfully!', 'success')
            print('Course uploaded successfully!')
            return redirect(url_for('courses.my_courses'))
    
    return render_template('courses_popup.html')

@courses.route('/course/<title>')
def course_description(title):
    conn = sqlite3.connect('learning_helper_assistant.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT topic, completed
        FROM user_topics
        WHERE username = ? AND title = ?
    ''', (session['user'], title))
    topics = cursor.fetchall()
    conn.close()
    return render_template('course_desc.html', title=title, topics=topics)

@courses.route('/<title>/<topic>/chat', methods=['GET', 'POST'])
def chat(title, topic):
    if 'user' not in session:
        flash('You need to login first!', 'error')
        return redirect(url_for('auth.login'))
    
    user = session['user']
    session_key = f'messages_{user}_{title}_{topic}'
    toggle_key = f'use_rag_{user}_{title}_{topic}'

    if request.method == 'POST':
        user_message = request.form.get('message', '')
        if not user_message:
            user_message = request.form.get('suggested_question', '')
        
        if user_message:  # Only process if there's actually a message
            use_rag = 'use_rag' in request.form
            session[toggle_key] = use_rag
            
            response = get_chat_response(user, title, topic, user_message, use_rag)
            messages = get_chat_history(user, title, topic)
            session[session_key] = messages
        
        return redirect(url_for('courses.chat', title=title, topic=topic))

    messages = get_chat_history(user, title, topic)
    use_rag = session.get(toggle_key, True)
    
    suggested_questions = []
    for message in reversed(messages):
        if message['role'] == 'assistant':
            last_response = message['content']
            suggested_questions = get_suggested_questions(title, topic, last_response)
            break

    # Fetch podcast URL from the database
    conn = sqlite3.connect('learning_helper_assistant.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT podcast_url FROM podcasts
        WHERE username = ? AND title = ? AND topic = ?
        ORDER BY time_created DESC LIMIT 1
    ''', (user, title, topic))
    result = cursor.fetchone()
    podcast_url = result[0] if result else None
    conn.close()
    
    return render_template('course_chat.html', 
                           title=title, 
                           topic=topic, 
                           messages=messages, 
                           use_rag=use_rag,
                           suggested_questions=suggested_questions,
                           podcast_url=podcast_url)

@courses.route('/<title>/<topic>/generate_podcast', methods=['POST'])
def generate_podcast(title, topic):
    user = session['user']
    podcast_url = generate_podcast_audio(user, title, topic)
    
    if podcast_url:
        # Store the podcast URL in the database
        conn = sqlite3.connect('learning_helper_assistant.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO podcasts (username, title, topic, podcast_url, time_created)
            VALUES (?, ?, ?, ?, ?)
        ''', (user, title, topic, podcast_url, datetime.now()))
        conn.commit()
        conn.close()
    
    return redirect(url_for('courses.chat', title=title, topic=topic))

@courses.route('/<title>/<topic>/check_podcast_status/<job_id>', methods=['GET'])
def check_podcast_status_route(title, topic, job_id):
    podcast_url = check_podcast_status(job_id)
    if podcast_url:
        return redirect(podcast_url)
    return redirect(url_for('courses.chat', title=title, topic=topic))
    
@courses.route('/<title>/<topic>/imp_chat_response')
def get_imp_chat_response(title, topic):
    if 'user' not in session:
        return '', 403  # Forbidden if not logged in

    user = session['user']
    response = imp_chat_response(user, title, topic)
    return response

@courses.route('/<title>/<topic>/complete_topic', methods=['POST'])
def complete_topic(title, topic):
    user = session['user']
    conn = sqlite3.connect('learning_helper_assistant.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE user_topics
        SET completed = 1
        WHERE username = ? AND title = ? AND topic = ?
    ''', (user, title, topic))
    conn.commit()
    conn.close()
    flash('You have completed this topic!', 'success')
    return redirect(url_for('courses.course_description', title=title, topic=topic))

@courses.route('/<title>/<topic>/test', methods=['GET', 'POST'])
def take_test(title, topic):
    user = session['user']
    difficulty = request.args.get('difficulty')
    if request.method == 'GET':
        if not difficulty:
            return redirect(url_for('courses.chat', title=title, topic=topic))
        else:
            questions = generate_exam(user, title, topic, difficulty)
            return render_template('course_exam.html', title=title, topic=topic, questions=questions)
    else:
        user_answers = request.form.getlist('answers')
        questions = request.form.getlist('questions')
        evaluations = []
        for question, answer in zip(questions, user_answers):
            evaluation = evaluate_exam(question, answer)
            evaluations.append({'question': question, 'answer': answer, 'evaluation': evaluation})
        return render_template('course_exam.html', title=title, topic=topic, evaluations=evaluations)




