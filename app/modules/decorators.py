from functools import wraps
from flask import session, redirect, flash, url_for

def login_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        if not session.get('username'):
            flash('login first ')
            return redirect(url_for('auth.login_page'))
        return f(*args, **kwargs)
    return function

def admin_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        if not session.get('username') or not session.get('type') == 1:
            return redirect(url_for('dashboard.dashboard_index'))
        return f(*args, **kwargs)
    return function
