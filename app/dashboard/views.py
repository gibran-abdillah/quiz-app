
from flask import (redirect, 
                   url_for, 
                   abort, 
                   render_template, 
                   session)
from app.dashboard.forms import QuizForm, ChangePwForm

from app.dashboard import dashboard_blueprint as dashboard 
from app.db import quiz, db
from app.modules.decorators import login_required
from app.modules.utils import json_decoder

@dashboard.route('/')
@login_required
def dashboard_index():
    print(quiz.find_one())
    return render_template('dashboard/index.html')

@dashboard.route('/manage-quiz')
@login_required
def manage_quiz():
    result = json_decoder([x for x in quiz.find({'author':session.get('username')})])
    

    
    list_id = [x['code'] for x in result if x.get('code')]

    list_quiz = [x['quiz_title'] for x in result 
                for y in list_id 
                if x.get('code') == y]

    data = zip(list_quiz, list_id)
    return render_template('dashboard/manage-quiz.html', data=data)

@dashboard.route('/change-password')
@login_required
def change_password():
    form = ChangePwForm()

    return render_template('dashboard/change-password.html', form=form)

@dashboard.route('/edit-quiz/<code>')
@login_required
def edit_quiz(code):
    
    check = json_decoder(quiz.find_one({'code':code}))
    if check and session.get('username') == check['author']:
        forms = []
        for data in check['data']:
            form = QuizForm()
            
            form.a_option.data = check['data'][data].get('a_option')
            form.b_option.data = check['data'][data].get('b_option')
            form.c_option.data = check['data'][data].get('c_option')
            form.d_option.data = check['data'][data].get('d_option')
            form.e_option.data = check['data'][data].get('e_option')
            form.question.data = check['data'][data].get('question')
            form.answer.data = check['data'][data].get('answer')
            forms.append(form)

        return render_template('dashboard/add-quizes.html', forms=forms)

@dashboard.route('/scores')
@login_required
def scores():
    return render_template('dashboard/users-scores.html')


@dashboard.route('/users-scores')
@login_required
def users_scores():
    return render_template('dashboard/users-scores.html')

@dashboard.route('/upload-quiz')
@login_required
def upload_quiz():
    return render_template('dashboard/csv-upload.html')

@dashboard.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('auth.login_page'))

@dashboard.route('/add-quizes')
@login_required
def add_quizes():
    form = QuizForm()
    return render_template('dashboard/add-quizes.html', form=form)

