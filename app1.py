from flask import Flask, render_template, request, Response, redirect, url_for
from captcha_parse import generate_session, get_timetable
import re

app = Flask(__name__)

# Dummy user credentials for demonstration purposes
valid_credentials = {
    'username': 'admin',
    'password': 'password123'
}

def generate_output(keyword):
    for i in (f"22BCE{x}" for x in range(7200, 9999)):
        sess, valid = generate_session(i, "vitap12345")
        days = get_timetable(sess, i)
        if re.findall(keyword, days):
            yield f"{i}\n"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == valid_credentials['username'] and password == valid_credentials['password']:
            return redirect(url_for('index'))
        else:
            # Add an error message for invalid credentials
            error = 'Invalid username or password. Please try again.'
            return render_template('login.html', error=error)
    
    return render_template('login.html')

@app.route('/runcode', methods=['POST'])
def run_code():
    keyword = request.json['keyword']
    output = generate_output(keyword)
    return Response(output, mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True)
