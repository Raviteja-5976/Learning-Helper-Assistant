from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import os
from models.authentication.auth import auth
from models.rapid_learner.rapid_chat import rapid_chat
from models.my_courses.courses import courses

app = Flask(__name__)


app.secret_key = 'super_secret_key'
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(rapid_chat, url_prefix='/rapid')
app.register_blueprint(courses, url_prefix='/courses')

@app.route('/')
def home():
    return render_template('index.html')
    

if __name__ == '__main__':
    app.run(debug=True)