import sqlite3

conn = sqlite3.connect('learning_helper_assistant.db')

c = conn.cursor()

# Create chat_history table
c.execute('''CREATE TABLE IF NOT EXISTS chat_history
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
             username TEXT NOT NULL,
             title TEXT NOT NULL,
             topic TEXT NOT NULL,
             role TEXT NOT NULL,
             content TEXT NOT NULL,
             timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')

conn.commit()
conn.close()



