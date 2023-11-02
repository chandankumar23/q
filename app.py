from flask import Flask, render_template, request, redirect, url_for, session, json, jsonify

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Mock user database
users = {'john': 'password', 'jane': '12345'}


practice_papers_list = ["New ISEB Practice Test  1","New ISEB Practice Test  2","New ISEB Practice Test  3", "New ISEB Practice Test 4 "]
subjects_list = ['English', 'Maths','Science', 'History']
user_answers = []

with open('questions.json') as file:
    question_list = json.load(file)
# question_list = [
#         {
#             "question": "What is capital of India?",
#             "choices": ["New Delhi", "Mumbai", "Chennai", "Kolkata"],
#             "answer": "New Delhi",
#             "explaination": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
#         },
#         {
#             "question": "What is the value of 3^2?",
#             "choices": ["81", "9", "27", "64"],
#             "answer": "9",
#              "explaination": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."

#         },
#         {
#             "question": "What is state of water at 100 degree celsius?",
#             "choices": ["Solid", "Ice", "Vapour", "None of the above"],
#             "answer": "Vapour",
#              "explaination": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."

#         }
#     ]


# Initialize selected answers

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


@app.route('/practice-papers/<paper_name>/subjects/<subject>/questions', methods=['GET','POST'])
def questions(paper_name, subject):
    username = "John Doe" 
    answers = request.form
    score = 0
    # print(score)
    # for key , value in answers.items():
    #     print(answers.items)
    #     for question in question_list :
    #         if question['question'] == key:
    #             if value == question['answer'] :
    #                 print(value)
    #                 score = +1
    #                 print(score)


    with open('questions.json', 'r') as file:
        question_list = json.load(file)
        print(question_list)
    current_question_index = int(request.args.get('current_question_index', 0))
    total_questions = len(question_list)
    current_question = question_list[current_question_index]
    has_prev = current_question_index > 0
    has_next = current_question_index < total_questions - 1
    # print(total_questions)

    return render_template('questions.html', username=username, paper_name=paper_name, subject=subject, current_question=current_question, current_question_index=current_question_index, total_questions=total_questions, has_prev=has_prev, has_next=has_next)


@app.route('/review/<int:index>', methods=['GET'])
def review_page(index):
    if 0 <= index < len(question_list):
        question = question_list[index]
        return render_template('review.html', question=question, index=index, total=len(question_list))
    else:
        return "Question not found!"
    
@app.route('/practice-papers/subjects/<subject>/review', methods=['GET', 'POST'])
def review( subject):
    print(subject)
    subject = subject  # Replace with the actual subject
    # review_questions = [
    #     {
    #         "question": "What is capital of India?",
    #         "choices": ["New Delhi", "Mumbai", "Chennai", "Kolkata"],
    #         "answer": "New Delhi",
    #         "explaination": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
    #     },
    #     {
    #         "question": "What is the value of 3^2?",
    #         "choices": ["81", "9", "27", "64"],
    #         "answer": "9",
    #          "explaination": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."

    #     },
    #     {
    #         "question": "What is state of water at 100 degree celsius?",
    #         "choices": ["Solid", "Ice", "Vapour", "None of the above"],
    #         "answer": "Vapour",
    #          "explaination": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."

    #     }
    # ]  # Replace with your actual questions data
    with open('questions.json', 'r') as file:
        question_list = json.load(file)
        # print(question_list)
    # current_question_index = int(request.args.get('current_question_index', 0))
    # total_questions = len(question_list)
    # current_question = question_list[current_question_index]
    # has_prev = current_question_index > 0
    # has_next = current_question_index < total_questions - 1
    # print(total_questions)

    # return render_template('review.html',subject=subject, current_question=current_question, current_question_index=current_question_index, total_questions=total_questions, has_prev=has_prev, has_next=has_next)
    return render_template('review.html', subject=subject, questions=question_list)


@app.route('/question/<test>/<int:qid>', methods=['GET', 'POST'], endpoint='question')
def question(test, qid):
    print(test , qid )
    if 'username' in session:
        if test in question_list and qid < len(question_list[test]):
            if request.method == 'POST':
                user_answer = request.form['answer']
                print(user_answer)
                user_answers.setdefault(test, {})[qid] = user_answer
                print(user_answers)
                next_qid = qid + 1
                if next_qid < len(questions[test]):
                    return redirect(url_for('question', test=test, qid=next_qid))
                else:
                    return redirect(url_for('result', test=test))
            return render_template('question.html', test=test, qid=qid, question=questions[test][qid])
    return redirect(url_for('login'))


# @app.route('/submit/<paper_name>/<subject>', methods=['POST'])
# def result (paper_name,  subject):
#     if 'username' in session:
#         user_answers = request.form:
#         correct_answers = questions['answer']
#         score=0
#         total_questions = len(correct_answers)

#         for index, (question, correct_answer) in enumerate(zip(papers[paper][subject]['questions'], correct_answers)):
#             user_answer = user_answers.get(f'answer_{index + 1}')
#             if user_answer == correct_answer:
#                 score += 1

#         return render_template('score.html', username=session['username'], score=score, total_questions=total_questions)
#     return redirect(url_for('login'))


@app.route('/<username>/<subject>/submit', methods=['GET', 'POST'])
def submit(username, subject):
        if 'username' in session:            
            username = username 
            subject = subject
            score = 80
            total_questions = len(question_list)
        # return f"Your Score: {score}/{total_questions}
        return render_template('result.html',usernmae =username, score=score,subject=subject )

# @app.route('/<test>/result', methods=['GET', 'POST'])
# def result(test):
#     if 'username' in session:
#         correct_count = 0
#         for qid, question in enumerate(question[test]):
#             if selected_answers.get(test, {}).get(qid) == question_list['answer']:
#                 correct_count += 1
#         score = f'{correct_count} out of {len(question_list[test])}'
#         return render_template('result.html', test=test, score=score)
#     return redirect(url_for('login'))


@app.route('/test', methods =['GET', 'POST'])
def test():
    with open('questions.json', 'r') as file:
        question_list = json.load(file)
        print(question_list)
    return jsonify(question_list)

# @app.route('/review', methods=['GET','POST'])
# def review():
#     if 'username' in session:
#         # return render_template('review.html',username=username, questions=questions[test], selected_answers=selected_answers.get(test, {}))
#         return render_template('review.html')

#     return redirect(url_for('login'))

# @app.route("/editprofile")
# def edit_profile():
#     return render_template("index.html", title="Second page")

if __name__ == '__main__':
    app.run(debug=True)
