from flask import Flask, render_template, request, jsonify
from captcha_parse import generate_session, get_timetable
import re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/runcode', methods=['POST'])
def run_code():
    keyword = request.json['keyword']

    output = []
    for i in (f"21BCE{x}" for x in range(7000, 9999)):
        sess, valid = generate_session(i, "vitap12345")
        days = get_timetable(sess, i)
        if re.findall(keyword, days):
            output.append(f"{i} True")

    return jsonify({'output': '\n'.join(output)})

if __name__ == '__main__':
    app.run(debug=True)
