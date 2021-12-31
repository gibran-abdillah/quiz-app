from flask import request, jsonify, abort, session
from flask.helpers import url_for
from werkzeug.utils import redirect
from app.api import api_blueprint as api 
from app import csrf_protect
from app.auth.forms import RegisterForm, LoginForm
from app.dashboard.forms import ChangePwForm, DashProfile
from app.db import db, quiz
from app.modules.decorators import admin_required, login_required

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
            new_data['email'] = data.get('email')

            # type 0 means its not admin
            new_data['type'] = 0

            insert_data = db.users.insert_one(new_data)
            if insert_data.inserted_id:
                return jsonify(status='success')
            return jsonify(status='fail', errors='unkown failure')
        except Exception as e:
            return jsonify(status='fail', errors='<p>{}'.format(e))

    return jsonify(status='fail', 
                   errors='<p>'.join(form.errors[x][0] for x in form.errors))

@api.route('/manage-users', methods=['POST','GET'])
@admin_required
def manage_users():
    request_data = request.get_json()
    if request_data.get('option') and request_data.get('data'):
        option = request_data.get('option')
        data = request_data.get('data')
        if option == 'delete':
            db.users.delete_many({'username':{'$in':data}})
        elif option == 'promote':
            db.users.update_many({'username':{'$in':data}}, {'$set':{'type':1}})
        elif option == 'unpromote':
            db.users.update_many({'username':{'$in':data}}, {"$set":{'type':0}})
        return jsonify(status='success', message='Task Done!')
    return jsonify(status='failed', message='what are you doing here?')

@api.route('/users')
def show_users():
    result = [x for x in db.users.find({})]
    for y in result:
        y.pop('_id')
        y.pop('password')
        _ = y.pop('email') if y.get('email') else ''
    return jsonify(data=json_decoder(result))

@api.route('/login', methods=['POST'])
def api_login():
    data = request.get_json()
    form = LoginForm(data=data)
    if form.validate():
        fetch_data = db.users.find_one({'username':data['username']})
        if fetch_data and check_password(fetch_data['password'], data['password']):
            session['username'] = data['username']
            session['name'] = fetch_data['full_name']
            session['type'] = fetch_data.get('type')
            session['email'] = fetch_data.get('email')
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

@api.route('/edit-profile', methods=['POST','GET'])
@login_required
def edit_profile():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    if username != session.get('username'):
        if db.users.find_one({'username':username}):
            return jsonify(status='failed', message='Username already registered')
    if email != session.get('email'):
        if db.users.find_one({'email':email}):
            return jsonify(status='failed', message='Email Already registered')
    db.users.update_one({'username':session.get('username')}, {'$set':data})
    session['username'] = username 
    session['email'] = email
    return jsonify(status='success', message='Changed')

