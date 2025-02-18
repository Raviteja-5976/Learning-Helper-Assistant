import sqlite3

def create_tables():
    conn = sqlite3.connect('learning_helper_assistant.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        Name TEXT NOT NULL,
        Age INTEGER,
        gender TEXT,
        email TEXT,
        Profession TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        title TEXT,
        content BLOB,
        created_at TIMESTAMP
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_topics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        title TEXT,
        topic TEXT,
        completed BOOLEAN
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        title TEXT,
        topic TEXT,
        role TEXT,
        content TEXT,
        timestamp TIMESTAMP
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS podcasts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        title TEXT,  
        topic TEXT,
        podcast_url TEXT,
        time_created TIMESTAMP      
    )
    ''')


    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
