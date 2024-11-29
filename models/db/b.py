import sqlite3

conn = sqlite3.connect('learning_helper_assistant.db')
cursor = conn.cursor()

# Create podcasts table
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS podcasts (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         username TEXT NOT NULL,
#         title TEXT NOT NULL,
#         topic TEXT NOT NULL,
#         podcast_url TEXT NOT NULL,
#         time_created TIMESTAMP NOT NULL
#     )
# ''')

# Delete all data in podcasts table
cursor.execute('''
    DELETE FROM podcasts
''')

conn.commit()
conn.close()
