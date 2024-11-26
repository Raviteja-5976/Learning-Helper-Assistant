import sqlite3
from flask import Blueprint, render_template, request, redirect, url_for, flash, session


courses = Blueprint('courses', __name__, template_folder='templates')

@courses.route('/my_courses')
def my_courses():
    if 'user' not in session:
        flash('You need to login first!', 'error')
        return redirect(url_for('auth.login'))
    
    conn = sqlite3.connect('learning_helper_assistant.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT title
        FROM user_courses
        WHERE username = ?
    ''', (session['user'],))
    titles = cursor.fetchall()
    
    conn.close()
    return render_template('courses.html', courses=titles)

@courses.route('/upload_course', methods=['GET', 'POST'])
def upload_course():
    # if request.method == 'POST':
    #     # Handle form submission
    #     # ...process form data...
    #     pass
    return render_template('courses_popup.html')