import sqlite3

def create_tables():
    conn = sqlite3.connect('learning_helper.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        name TEXT NOT NULL,
        age INTEGER,
        gender TEXT,
        email TEXT,
        profession TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_courses (
        username TEXT,
        title TEXT,
        content BLOB,
        created_at TIMESTAMP,
        FOREIGN KEY (username) REFERENCES users(username)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_topics (
        username TEXT,
        title TEXT,
        topic TEXT,
        completed BOOLEAN,
        FOREIGN KEY (username) REFERENCES users(username)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS chat_history (
        username TEXT,
        title TEXT,
        topic TEXT,
        role TEXT,
        content TEXT,
        timestamp TIMESTAMP,
        FOREIGN KEY (username) REFERENCES users(username)
    )
    ''')


    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
