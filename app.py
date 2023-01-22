from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, Survey, satisfaction_survey, personality_quiz, surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "survey123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)
RESPONSES = []


@app.route('/')
def home_page():
    satisfaction_survey_title = satisfaction_survey.title
    satisfaction_survey_instructions = satisfaction_survey.instructions
    return render_template('home.j2', survey_title=satisfaction_survey_title, survey_instructions=satisfaction_survey_instructions)


@app.route('/questions/<int:number>')
def do_form(number):
    question = satisfaction_survey.questions[number]
    response_len = len(RESPONSES)

    if response_len is None:
        return redirect("/")
    if response_len == len(satisfaction_survey.questions):
        return redirect("/thanks")
    if response_len != number:
        return redirect(f"/questions/{response_len}")

    return render_template('questions.j2', question=question, number=number)


@app.route("/answer", methods=["POST"])
def add_answer():
    answer = request.form['answer']
    response_len = len(RESPONSES)
    RESPONSES.append(answer)

    if (response_len == len(satisfaction_survey.questions)):
        return redirect("/thanks")
    else:
        return redirect(f"/questions/{response_len}")


@app.route("/thanks")
def finish_survey():
    return render_template("thank-you.j2")
