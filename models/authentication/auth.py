import sqlite3
from flask import render_template, url_for, session, request, redirect, Blueprint, flash
from datetime import timedelta
# from models.authentication import user_db
# from models.authentication.user_db import get_db_connection
# import hashlib

auth = Blueprint('auth', __name__, template_folder='templates')

def init_session_config(app):
    app.permanent_session_lifetime = timedelta(hours=1)
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        try:
            conn = sqlite3.connect('learning_helper_assistant.db')
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
            user = cursor.fetchone()
            
            if user:
                session['user'] = username
                session['user_id'] = user[0]  # Store user_id in session
                flash('Login successful!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Invalid username or password', 'error')
        except sqlite3.Error as e:
            flash(f'Login error: {str(e)}', 'error')
        finally:
            conn.close()
        
    return render_template('login.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = {
            'username': request.form['username'],
            'password': request.form['password'],
            'name': request.form['name'],
            'age': request.form['age'],
            'gender': request.form['gender'],
            'email': request.form['email'],
            'profession': request.form['profession']
        }
        try:
            conn = sqlite3.connect('learning_helper_assistant.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (username, password, Name, Age, gender, email, Profession)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                data['username'], data['password'], data['name'], data['age'],
                data['gender'], data['email'], data['profession']
            ))
            conn.commit()
            # user_db.user_test_info(data['username'], conn)   # Pass conn to the function
            # user_db.user_test_result(data['username'], conn) # Pass conn to the function
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))
        except sqlite3.Error as e:
            flash(f'Registration error: {str(e)}', 'error')
            return render_template('register.html')
            
    return render_template('register.html')


@auth.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('auth.login'))



