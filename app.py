from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Mock user database
users = {'john': 'password', 'jane': '12345'}


practice_papers_list = ["New ISEB Practice Test  1","New ISEB Practice Test  2","New ISEB Practice Test  3", "New ISEB Practice Test 4 "]
subjects_list = ['English', 'Maths','Science', 'History']




# Initialize selected answers
selected_answers = {}
selected_practice = {}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
            # return redirect(url_for(practice_papers(username)))
        return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')



@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        username = session['username']
        return render_template('dashboard.html', username=username, practice_papers=practice_papers_list)
    return redirect(url_for('login'))


@app.route('/practice-papers/<paper_name>/subjects')
def subjects( paper_name):
    return render_template('subjects.html', paper_name=paper_name, subjects=subjects_list)


@app.route('/practice-papers/<paper_name>/subjects/<subject>/questions', methods=['GET'])
def questions(paper_name, subject):
    username = "John Doe"  # Replace with the actual username
    questions = [
        {
            "question": "What is capital of India?",
            "choices": ["New Delhi", "Mumbai", "Chennai", "Kolkata"],
            "answer": "New Delhi",
            "explaination": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
        },
        {
            "question": "What is the value of 3^2?",
            "choices": ["81", "9", "27", "64"],
            "answer": "9",
             "explaination": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."

        },
        {
            "question": "What is state of water at 100 degree celsius?",
            "choices": ["Solid", "Ice", "Vapour", "None of the above"],
            "answer": "Vapour",
             "explaination": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."

        }
    ]  # Replace with your actual questions data

    current_question_index = int(request.args.get('current_question_index', 0))
    total_questions = len(questions)
    current_question = questions[current_question_index]
    has_prev = current_question_index > 0
    has_next = current_question_index < total_questions - 1

    return render_template('questions.html', username=username, paper_name=paper_name, subject=subject, current_question=current_question, current_question_index=current_question_index, total_questions=total_questions, has_prev=has_prev, has_next=has_next)


@app.route('/review', methods=['GET', 'POST'])
def review():

    username = "John"
    paper_name = "Sample Paper" # Replace with the actual paper name
    subject = "Sample Subject"  # Replace with the actual subject
    questions = [
        {
            "question": "What is capital of India?",
            "choices": ["New Delhi", "Mumbai", "Chennai", "Kolkata"],
            "answer": "New Delhi",
            "explaination": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
        },
        {
            "question": "What is the value of 3^2?",
            "choices": ["81", "9", "27", "64"],
            "answer": "9",
             "explaination": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."

        },
        {
            "question": "What is state of water at 100 degree celsius?",
            "choices": ["Solid", "Ice", "Vapour", "None of the above"],
            "answer": "Vapour",
             "explaination": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."

        }
    ]  # Replace with your actual questions data

    return render_template('review.html', username=username, paper_name=paper_name, subject=subject, questions=questions)




# @app.route('/practice-papers/<paper_name>/subjects/<subject>/questions')
# def questions(paper_name, subject):
#     questions = [
#         {
#             "question": "What is question 1?",
#             "choices": ["Choice 1", "Choice 2", "Choice 3", "Choice 4"],
#             "answer": "Choice 1"
#         },
#         {
#             "question": "What is question 2?",
#             "choices": ["Choice 1", "Choice 2", "Choice 3", "Choice 4"],
#             "answer": "Choice 2"
#         },
#         {
#             "question": "What is question 3?",
#             "choices": ["Choice 1", "Choice 2", "Choice 3", "Choice 4"],
#             "answer": "Choice 3"
#         }
#     ]  # Replace with your actual questions data

#     return render_template('questions.html',paper_name=paper_name, subject=subject, questions=questions)




@app.route('/practice/<test>')
def practice(test):
    if 'username' in session:
        if test in questions:
            selected_answers[test] = {}
            return redirect(url_for('question', test=test, qid=0))
        return 'Test not found'
    return redirect(url_for('login'))

@app.route('/question/<test>/<int:qid>', methods=['GET', 'POST'], endpoint='question')
def question(test, qid):
    if 'username' in session:
        if test in questions and qid < len(questions[test]):
            if request.method == 'POST':
                selected_answer = request.form['answer']
                selected_answers.setdefault(test, {})[qid] = selected_answer
                next_qid = qid + 1
                if next_qid < len(questions[test]):
                    return redirect(url_for('question', test=test, qid=next_qid))
                else:
                    return redirect(url_for('result', test=test))
            return render_template('question.html', test=test, qid=qid, question=questions[test][qid])
    return redirect(url_for('login'))

@app.route('/result/test', methods=['GET', 'POST'])
def result(test):
    if 'username' in session:
        correct_count = 0
        for qid, question in enumerate(questions[test]):
            if selected_answers.get(test, {}).get(qid) == question['answer']:
                correct_count += 1
        score = f'{correct_count} out of {len(questions[test])}'
        return render_template('result.html', test=test, score=score)
    return redirect(url_for('login'))



# @app.route('/review', methods=['POST'])
# def review(test):
#     if 'username' in session:
#         return render_template('review.html', test=test, questions=questions[test], selected_answers=selected_answers.get(test, {}))
#     return redirect(url_for('login'))

@app.route("/editprofile")
def edit_profile():
    return render_template("index.html", title="Second page")

if __name__ == '__main__':
    app.run(debug=True)
