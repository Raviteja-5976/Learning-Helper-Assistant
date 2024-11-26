
import sqlite3

def init_db():
    conn = sqlite3.connect('learning_helper_assistant.db')
    cursor = conn.cursor()
    
    # Drop existing users table if it exists
    # cursor.execute('DROP TABLE IF EXISTS users')
    
    # Create new users table
    cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        Name TEXT NOT NULL,
        Age INTEGER NOT NULL,
        gender TEXT,
        email TEXT UNIQUE NOT NULL,
        Profession TEXT
    )
    ''')

    # cursor.execute("DELETE FROM users WHERE username = 'raviteja_5312'")
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()