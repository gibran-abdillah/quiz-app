from sys import meta_path
from app.auth import auth_blueprint as auth 
from flask import render_template, request
from app import csrf_protect
from flask_wtf.csrf import CSRFError, validate_csrf
from .forms import LoginForm, RegisterForm

@auth.route('/')
def auth_index():
    return render_template('auth/index.html')

@auth.route('/login')
def login_page():
    form = LoginForm()
    return render_template('auth/login.html', form=form)

@auth.route('/register')
def register_page():
    form = RegisterForm()
    return render_template('auth/register.html', form=form)
