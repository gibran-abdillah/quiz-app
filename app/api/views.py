from flask import request, jsonify, abort, session
from app.api import api_blueprint as api 
from app import csrf_protect
from app.auth.forms import RegisterForm, LoginForm
from app.dashboard.forms import ChangePwForm
from app.db import db, quiz
from app.modules.decorators import login_required

from app.modules.utils import (
                            generate_code, 
                            generate_password, 
                            check_password, 
                            json_decoder)

from datetime import datetime

@api.route('/add-account', methods=['POST'])
def add_account():
    """
    function for register 
    """
    csrf_protect.protect()
    data = request.get_json()
    form = RegisterForm(data=data)
    if form.validate():
        try:
            new_data = {}
            new_data['full_name'] = data['full_name']
            new_data['username'] = data['username']
            new_data['password'] = generate_password(data['password'])
            new_data['joined_at'] = datetime.utcnow()
            new_data['type'] = 0

            insert_data = db.users.insert_one(new_data)
            if insert_data.inserted_id:
                return jsonify(status='success')
            return jsonify(status='fail', errors='unkown failure')
        except Exception as e:
            return jsonify(status='fail', errors='<p>{}'.format(e))

    return jsonify(status='fail', 
                   errors='<p>'.join(form.errors[x][0] for x in form.errors))

@api.route('/login', methods=['POST'])
def api_login():
    data = request.get_json()
    form = LoginForm(data=data)
    if form.validate():
        fetch_data = db.users.find_one({'username':data['username']})
        if fetch_data and check_password(fetch_data['password'], data['password']):
            session['username'] = data['username']
            session['name'] = fetch_data['full_name']
            return jsonify(status='success')
            
    return jsonify(status='fail', errors='invalid username / password')

@api.route('/change-password', methods=['POST'])
def change_password():
    if not session.get('username', None):
        return jsonify(status='fail', message='not logged in')
    json_request = request.get_json()
    form = ChangePwForm(data=json_request)
    if form.validate() and json_request.get('password'):
        user = db.users.update_one({'username':session.get('username')}, 
                                   {'$set':{'password':generate_password(json_request.get('password'))}})
        return jsonify(status='success', message='password changed')

    return jsonify(status='fail', message='<p>'.join([values[0] 
                                           for key, values in form.errors.items() 
                                           if len(values) != 0]))

@api.route('/asal')
def asal():
    cek = quiz.find_one({'data':{'$exists':True}})
    return jsonify(json_decoder(cek))

@api.route('/delete-all')
def api_delete_all():
    quiz.delete_many({})
    return jsonify(
        json_decoder([x for x in quiz.find()])
    )
