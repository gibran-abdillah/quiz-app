from app.quiz import quiz_blueprint as quiz 
from flask import render_template

@quiz.route('/start/<code>')
def quiz_homepage(code):
    return render_template('quiz/index.html')
    
@quiz.route('/')
def index_quiz():
    return render_template('quiz/landing-page.html')