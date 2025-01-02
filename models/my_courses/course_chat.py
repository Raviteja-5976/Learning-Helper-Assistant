from groq import Groq
import sqlite3
import time
from datetime import datetime
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from models.config import GROQ_API_KEY_COURSE_CHAT

client = Groq(api_key=GROQ_API_KEY_COURSE_CHAT)

PROMPT_TEMPLATE = """
Answer the question based only on the following context and format your response using markdown:

{context}
--------

Question about {topic} from {title}: {question}

Provide a detailed response using the context above. If the context doesn't contain relevant information,
respond based on general knowledge about the topic. Use markdown formatting for better readability.
"""

def get_rag_response(username: str, title: str, topic: str, query: str):
    # Construct the database path for this specific course
    db_path = f"chroma/{username}_{title}.db"
    
    # Setup embedding function and load course-specific database
    embedding_function = OllamaEmbeddings(model='nomic-embed-text')
    db = Chroma(persist_directory=db_path, embedding_function=embedding_function)

    # Perform similarity search
    results = db.similarity_search_with_score(query, k=3)
    context_text = "\n\n --- \n\n".join([doc.page_content for doc, _score in results])

    # Format prompt with context and query
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(
        context=context_text,
        title=title,
        topic=topic,
        question=query
    )

    # Get response from Groq
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful teaching assistant. Use markdown formatting in your responses. Just give your answer no need to mention the user question again."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_tokens=8192,
        top_p=1,
        stream=False,
        stop=None,
    )
    
    return completion.choices[0].message.content.strip()

def get_simple_chat_response(title: str, topic: str, query: str):
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                "content": f"You are a helpful teaching assistant explaining about {topic} from {title}. Use markdown formatting in your responses."
            },
            {
                "role": "user",
                "content": query
            }
        ],
        temperature=0.7,
        max_tokens=8192,
        top_p=1,
        stream=False,
        stop=None,
    )
    
    return completion.choices[0].message.content.strip()

def get_initial_overview(username: str, title: str, topic: str):
    # First try RAG to get context-specific overview
    context_query = f"What are the main points to cover about {topic} in {title}? Include definitions and key concepts."
    response = get_rag_response(username, title, topic, context_query)
    
    # If RAG response is too short, fall back to general overview
    if len(response.strip()) < 100:
        response = get_simple_chat_response(title, topic, context_query)
    
    return response

def get_chat_history(username, title, topic, limit=50):
    conn = sqlite3.connect('learning_helper_assistant.db')
    cursor = conn.cursor()
    
    # Check if there are any existing messages
    cursor.execute('''
        SELECT COUNT(*) FROM chat_history
        WHERE username = ? AND title = ? AND topic = ?
    ''', (username, title, topic))
    message_count = cursor.fetchone()[0]
    
    # If no messages exist, create initial overview
    if message_count == 0:
        initial_response = get_initial_overview(username, title, topic)
        store_chat_message(username, title, topic, 'assistant', initial_response)
    
    # Get chat history
    cursor.execute('''
        SELECT role, content FROM chat_history
        WHERE username = ? AND title = ? AND topic = ?
        ORDER BY timestamp ASC LIMIT ?
    ''', (username, title, topic, limit))
    messages = cursor.fetchall()
    conn.close()
    return [{'role': role, 'content': content} for role, content in messages]

def store_chat_message(username, title, topic, role, content):
    conn = sqlite3.connect('learning_helper_assistant.db')
    cursor = conn.cursor()
    
    # Check for duplicate message
    cursor.execute('''
        SELECT id FROM chat_history 
        WHERE username = ? AND title = ? AND topic = ? AND role = ? AND content = ?
        ORDER BY timestamp DESC LIMIT 1
    ''', (username, title, topic, role, content))
    
    existing_message = cursor.fetchone()
    
    if not existing_message:  # Only insert if not a duplicate
        cursor.execute('''
            INSERT INTO chat_history (username, title, topic, role, content)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, title, topic, role, content))
        conn.commit()
    
    conn.close()

def generate_suggested_question(title: str, topic: str, last_response: str):
    prompt = f"""Based on this response about {topic} from {title}, suggest one natural follow-up question:
    
Response: {last_response}

Generate only one question that would help deepen understanding or explore a related concept.
Make sure the question is clear and focused."""

    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful teaching assistant. Generate one clear follow-up question."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.8,
        max_tokens=100,
        top_p=1,
        stream=False,
        stop=None,
    )
    
    return completion.choices[0].message.content.strip()

def get_suggested_questions(title: str, topic: str, last_response: str, num_questions=3):
    questions = []
    for _ in range(num_questions):
        question = generate_suggested_question(title, topic, last_response)
        questions.append(question)
    return questions

def get_chat_response(username, title, topic, user_message, use_rag=True):
    # Store user message
    store_chat_message(username, title, topic, 'user', user_message)
    time.sleep(1)  # Sleep for 1 second before AI response

    # Get response based on mode
    if use_rag:
        response = get_rag_response(username, title, topic, user_message)
    else:
        response = get_simple_chat_response(title, topic, user_message)

    # Store AI response
    store_chat_message(username, title, topic, 'assistant', response)

    return response

def imp_chat_response(username, title, topic):
    # Get the first bot response
    query = """
    SELECT content FROM chat_history WHERE username = ? AND title = ? AND topic = ? AND role = 'assistant' 
    ORDER BY timestamp ASC LIMIT 1"""
    conn = sqlite3.connect('learning_helper_assistant.db')
    cursor = conn.cursor()
    cursor.execute(query, (username, title, topic))
    response = cursor.fetchone()
    conn.close()
    return response[0]
