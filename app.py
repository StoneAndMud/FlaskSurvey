from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, Survey, satisfaction_survey, personality_quiz, surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "survey123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)
RESPONSES_KEY = "responses"


@app.route('/')
def home_page():
    satisfaction_survey_title = satisfaction_survey.title
    satisfaction_survey_instructions = satisfaction_survey.instructions
    return render_template('home.j2', survey_title=satisfaction_survey_title, survey_instructions=satisfaction_survey_instructions)


@app.route('/questions/<int:number>')
def do_form(number):
    question = satisfaction_survey.questions[number]
    responses = session.get(RESPONSES_KEY)
    response_len = len(responses)

    if responses is None:
        return redirect("/")
    if response_len == len(satisfaction_survey.questions):
        return redirect("/thanks")
    if response_len != number:
        return redirect(f"/questions/{response_len}")

    return render_template('questions.j2', question=question, number=number, responses=responses)


@app.route("/answer", methods=["POST"])
def add_answer():
    answer = request.form['answer']
    responses = session[RESPONSES_KEY]
    responses.append(answer)
    session[RESPONSES_KEY] = responses
    response_len = len(responses)

    if (response_len == len(satisfaction_survey.questions)):
        return redirect("/thanks")
    else:
        return redirect(f"/questions/{response_len}")


@app.route("/thanks")
def finish_survey():
    return render_template("thank-you.j2")


@app.route("/start", methods=["POST"])
def clear_session():
    session[RESPONSES_KEY] = []
    return redirect("/questions/0")
