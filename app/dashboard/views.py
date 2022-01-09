from flask import (redirect, 
                   url_for, 
                   Response,
                   abort, 
                   render_template, 
                   session, 
                   request)

from app.dashboard.forms import QuizForm, ChangePwForm, DashProfile
from app.dashboard import dashboard_blueprint as dashboard 
from app.db import quiz, db
from app.modules.decorators import login_required
from app.modules.utils import json_decoder

import io, json 

@dashboard.route('/')
@login_required
def dashboard_index():
    return render_template('dashboard/index.html')


@dashboard.route('/quiz/download/<code>')
@login_required
def download_quiz(code):
    """
    function to export quiz from json to download for users
    """
    result = quiz.aggregate([
        {'$match':{
            'code':code
        }},
        {'$group':{
            '_id':'$code',
            'data':{
                '$first':'$data'
            }
        }}
    ])

    list_result = [_ for _ in result]
    if list_result:
        data_result = json.dumps(list_result[-1]['data'])
        
        return Response(
            io.StringIO(data_result), status=200,
            mimetype='application/json',
            headers={'Content-Disposition':'attachment;filename={}.json'.format(code)}
        )


@dashboard.route('/manage-quiz')
@login_required
def manage_quiz():

    author = {'$exists':True} if session.get('type') == 1 else session.get('username')

    result = [x for x in quiz.find({'author':author})]
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
    if check and (session.get('username') == check['author'] or session.get('type') == 1):
        forms = []
        for data in range(len(check['data'])):
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
    abort(403)

@dashboard.route('/profile')
@login_required
def profile_page():
    form = DashProfile()

    form.full_name.data = session.get('name')
    form.username.data = session.get('username')
    form.email.data = session.get('email')
    return render_template('dashboard/profile.html', form=form)

@dashboard.route('/delete-quiz/<code>')
@login_required
def delete_quiz(code):
    result = json_decoder(quiz.find_one({'code':code}))
    if result:
        if result.get('author') == session.get('username') or session.get('type') == 1:
            quiz.delete_one({'code':code})
    return redirect(url_for('dashboard.manage_quiz'))

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


@dashboard.route('/export-quiz/<code>')
def export_quiz(code):
    check_exists = quiz.find_one({'code':code})
    if check_exists:
        resp = Response(json_decoder(check_exists), mimetype='application/csv')
        resp.headers['Content-Disposition'] = 'attachment: filename={}.csv'.format(code)
        resp.headers['Content-Length'] = len(check_exists)
        return resp
    return 'no'
