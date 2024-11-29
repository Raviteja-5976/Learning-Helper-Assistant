from groq import Groq
import sqlite3
import time
from datetime import datetime
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate

client = Groq(api_key='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')

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
                "content": "You are a helpful teaching assistant. Use markdown formatting in your responses."
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

def get_chat_history(username, title, topic, limit=3):
    conn = sqlite3.connect('learning_helper_assistant.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT role, content FROM chat_history
        WHERE username = ? AND title = ? AND topic = ?
        ORDER BY timestamp DESC LIMIT ?
    ''', (username, title, topic, limit*2))  # limit*2 because each exchange has 2 messages
    messages = cursor.fetchall()
    conn.close()
    return [{'role': role, 'content': content} for role, content in reversed(messages)]

def store_chat_message(username, title, topic, role, content):
    conn = sqlite3.connect('learning_helper_assistant.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO chat_history (username, title, topic, role, content)
        VALUES (?, ?, ?, ?, ?)
    ''', (username, title, topic, role, content))
    conn.commit()
    conn.close()

def get_chat_response(username, title, topic, user_message):
    # Store user message
    store_chat_message(username, title, topic, 'user', user_message)
    time.sleep(1)  # Sleep for 1 second before AI response
    
    # Get RAG-enhanced response
    response = get_rag_response(username, title, topic, user_message)
    
    # Store AI response
    store_chat_message(username, title, topic, 'assistant', response)
    
    return response
