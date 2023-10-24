from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Mock user database
users = {'john': 'password', 'jane': '12345'}

# Sample questions
questions = {
    'English': [
        {
            'id': 1,
            'question': 'What is the capital of India?',
            'choices': ['Delhi', 'Kolkata', 'Chennai', 'Mumbai'],
            'answer': 'Delhi'
        },
        {
            'id': 2,
            'question': 'Which is capital of Karnataka?',
            'choices': ['Tumkur', 'Hubli', 'Mysore', 'Bangalore'],
            'answer': 'Bangalore'
        },
        {
            'id': 3,
            'question': 'Identify the noun in "India is a beautiful country"',
            'choices': ['A', 'Country', 'India', 'Beautiful'],
            'answer': 'Bhutan'
        },
        {
            'id': 4,
            'question': 'Which of these is a common noun?',
            'choices': ['Acting', 'John', 'Beautiful', 'She'],
            'answer': 'She'
        }
    ],
    'History': [
        {
            'id': 1,
            'question': 'When did World War II end?',
            'choices': ['1943', '1944', '1945', '1946'],
            'answer': '1945'
        },
        {
            'id': 2,
            'question': 'Who was the first president of the United States?',
            'choices': ['George Washington', 'Thomas Jefferson', 'John Adams', 'Abraham Lincoln'],
            'answer': 'George Washington'
        }
    ]
}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        username = session['username']
        return render_template('dashboard.html', username=username, tests=questions.keys())
    return redirect(url_for('login'))


@app.route('/practice/<test>')
def practice(test):
    if 'username' in session:
        if test in questions:
            session['test'] = test
            session['question_number'] = 0
            return redirect(url_for('next_question'))
        return 'Test not found'
    return redirect(url_for('login'))


@app.route('/next_question', methods=['GET', 'POST'])
def next_question():
    if 'username' in session and 'test' in session:
        test = session['test']
        question_number = session['question_number']
        if question_number < len(questions[test]):
            question = questions[test][question_number]
            if request.method == 'POST':
                answer = request.form['answer']
                # save the answer somewhere if needed
                return redirect(url_for('next_question'))
            session['question_number'] += 1
            return render_template('question.html', question=question)
        else:
            return redirect(url_for('result'))
    return redirect(url_for('login'))


@app.route('/result', methods=['GET', 'POST'])
def result():
    if 'username' in session and 'test' in session:
        test = session['test']
        answers = session.get('answers', {})
        score = 0
        for question in questions[test]:
            user_answer = answers.get(str(question['id']), None)
            if user_answer and user_answer == question['answer']:
                score += 1
        return render_template('result.html', test=test, score=score, total=len(questions[test]))
    return redirect(url_for('login'))


@app.route('/review_answers', methods=['GET', 'POST'])
def review_answers():
    if 'username' in session and 'test' in session:
        test = session['test']
        answers = session.get('answers', {})
        score = 0
        for question in questions[test]:
            user_answer = answers.get(str(question['id']), None)
            if user_answer and user_answer == question['answer']:
                score += 1
        return render_template('review.html', questions=questions[test], answers=answers, score=score, total=len(questions[test]))
    return redirect(url_for('login'))




if __name__ == '__main__':
    app.run(debug=True)
