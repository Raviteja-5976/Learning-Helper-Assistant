import sqlite3
from groq import Groq
import re

client = Groq(api_key='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')

def generate_exam(username, title, topic, difficulty):
    # Fetch the assistant's first response from the chat history
    query = '''
    SELECT content FROM chat_history WHERE username = ? AND title = ? AND topic = ? AND role = 'assistant' 
    ORDER BY timestamp ASC LIMIT 1'''
    conn = sqlite3.connect('learning_helper_assistant.db')
    cursor = conn.cursor()
    cursor.execute(query, (username, title, topic))
    response = cursor.fetchone()
    conn.close()
    
    if not response:
        return None  # No content to generate exam
    
    # Generate exam questions using AI
    completion = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[
            {
                "role": "user",
                "content": f"""
                Provide 5 {difficulty.lower()} questions based on the content: {response[0]}.
                Each question should be unique and focused on {topic} in {title}.
                Return the questions as a list of strings.
                """
            }
        ],
        temperature=1,
        max_tokens=5000,
        top_p=0.7,
        stream=False,
        stop=None,
    )

    # Parse and return the list of questions
    response = completion.choices[0].message.content
    match = re.search(r'\[(.*?)\]', response, re.DOTALL)
    if match:
        array_string = match.group(1)
        array_string = array_string.replace("'", "").replace('"', '')
        array_list = [item.strip() for item in array_string.split(',')]
    else:
        # If no match, attempt to parse numbered questions
        array_list = re.findall(r'\d+\.\s*(.*?)\n', response)
        if not array_list:
            # Fallback: split by newlines
            array_list = [line.strip('- ').strip() for line in response.strip().split('\n') if line.strip()]
    return array_list


def evaluate_exam(question, answer):
    # Evaluate the student's answer to the exam question
    completion = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[
            {
                "role": "user",
                "content": f"""
                Evaluate the following:
                Question: {question}
                Answer: {answer}
                Provide feedback indicating correctness and any improvements needed.
                """
            }
        ],
        temperature=0.8,
        max_tokens=500,
        top_p=1,
        stream=False,
        stop=None,
    )
    
    return completion.choices[0].message.content

