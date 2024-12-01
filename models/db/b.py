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

# # Delete all data in podcasts table
# cursor.execute('''
#     DELETE FROM podcasts
# ''')

# # Delete form users
# cursor.execute('''
#     DELETE FROM users
# ''')

# # Delete form users_topics
# cursor.execute('''
#     DELETE FROM user_topics
# ''')

# # Delete form users_podcasts
# cursor.execute('''
#     DELETE FROM podcasts
# ''')

# # Delete form chat_history
# cursor.execute('''
#     DELETE FROM chat_history
# ''')

# # Delete form user_courses
# cursor.execute('''
#     DELETE FROM user_courses
# ''')

# # Delete form sqlite_sequence
# cursor.execute('''
#     DELETE FROM sqlite_sequence
# ''')

# From user_courses delete vRetrieval_Agumented_Generation 
cursor.execute('''
    DELETE FROM user_courses WHERE title = 'Retrieval_Agumented_Generation'
''')

# From user_topics delete course = Retrieval_Agumented_Generation
cursor.execute('''
    DELETE FROM user_topics WHERE title = 'Retrieval_Agumented_Generation'
''')

# from chat_history delete title = Retrieval_Agumented_Generation
cursor.execute('''
    DELETE FROM chat_history WHERE title = 'Retrieval_Agumented_Generation'
''')

conn.commit()
conn.close()
