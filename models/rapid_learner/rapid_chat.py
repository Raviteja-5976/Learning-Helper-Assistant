from flask import render_template, Blueprint, request, session, redirect, url_for, flash
from groq import Groq
import json

rapid_chat = Blueprint('rapid_chat', __name__, template_folder='templates')
client = Groq(api_key='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')

@rapid_chat.route('/popup', methods=['GET', 'POST'])
def rapid_chat_popup():
    if 'user' not in session:
        flash('You need to login first!', 'error')
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        session['topic'] = request.form['topic']
        session['goals'] = request.form['goals']
        session['prior_knowledge'] = request.form['prior_knowledge']
        
        system_message = {
            "role": "system",
            "content": f"You are a helpful learning assistant. The topic is {session['topic']}. "\
                      f"The learning goals are: {session['goals']}. "\
                      f"The student's prior knowledge is: {session['prior_knowledge']}"\
                      f"First give me the main important topics that to be learnt about this topic and goals"
        }
        session['messages'] = [system_message]
        
        try:
            completion = client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=session['messages'],
                temperature=0.7,
                max_tokens=1024,
                top_p=1,
                stream=False
            )
            
            session['messages'].append({
                "role": "assistant",
                "content": completion.choices[0].message.content
            })
            session.modified = True
            
        except Exception as e:
            flash(f"Error: {str(e)}")
        
        return redirect(url_for('rapid_chat.chat'))
    return render_template('rapid_chat_popup.html')

@rapid_chat.route('/new_topic', methods=['POST'])
def new_topic():
    session.pop('topic', None)
    session.pop('goals', None)
    session.pop('prior_knowledge', None)
    session.pop('messages', None)
    return redirect(url_for('rapid_chat.rapid_chat_popup'))

@rapid_chat.route('/chat', methods=['GET', 'POST'])
def chat():
    if not all(key in session for key in ['topic', 'goals', 'prior_knowledge']):
        return redirect(url_for('rapid_chat.rapid_chat_popup'))
    
    if 'messages' not in session:
        session['messages'] = []
        system_message = {
            "role": "system",
            "content": f"You are a helpful learning assistant. The topic is {session['topic']}. "\
                      f"The learning goals are: {session['goals']}. "\
                      f"The student's prior knowledge is: {session['prior_knowledge']}"
        }
        session['messages'] = [system_message]
        session.modified = True
    
    if request.method == 'POST':
        user_message = request.form.get('message')
        if user_message:
            messages_to_send = session['messages'].copy()
            messages_to_send.append({"role": "user", "content": user_message})
            
            try:
                completion = client.chat.completions.create(
                    model="mixtral-8x7b-32768",
                    messages=messages_to_send,
                    temperature=0.7,
                    max_tokens=1024,
                    top_p=1,
                    stream=False
                )
                
                session['messages'].append({"role": "user", "content": user_message})
                session['messages'].append({
                    "role": "assistant",
                    "content": completion.choices[0].message.content
                })
                session.modified = True
                
            except Exception as e:
                flash(f"Error: {str(e)}")
                
    return render_template('rapid_chat.html', messages=session.get('messages', [])[1:])

