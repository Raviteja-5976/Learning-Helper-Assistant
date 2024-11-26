import sqlite3

conn = sqlite3.connect('learning_helper_assistant.db')

c = conn.cursor()


c.execute('''CREATE TABLE user_topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    title TEXT NOT NULL,
    topic TEXT NOT NULL
)''')

c.execute('''CREATE TABLE user_courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    title TEXT NOT NULL,
    content BLOB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)''')

# c.execute("DROP TABLE IF EXISTS user_topics")
# c.execute("DROP TABLE IF EXISTS user_courses")

conn.commit()