from wtforms.fields import StringField, PasswordField
from flask_wtf import FlaskForm
from wtforms.validators import ValidationError

from app.db import db
from app.modules.utils import check_password
from app.auth.forms import PasswordForm, ProfileForm
from flask import session

class QuizForm(FlaskForm):
    question = StringField(
        'question',
        render_kw={'class':'questions','placeholder':'Question','id':'question'}
    )
    a_option = StringField( 
        'A Option',
        render_kw={'class':'answer_option','placeholder':'A Option'}
    )
    b_option = StringField(render_kw={'class':'answer_option', 'placeholder':'B Option'})
    c_option = StringField(render_kw={'class':'answer_option', 'placeholder':'C Option'})
    d_option = StringField(render_kw={'placeholder':'D Option', 'class':'answer_option'})
    e_option = StringField(render_kw={'placeholder':'E Option', 'class':'E Option'})
    answer = StringField(render_kw={'placeholder':'answer (eg : A )', 'class':'answer'})

class ChangePwForm(FlaskForm, PasswordForm):
    old_password = PasswordField('old password')

    def validate_old_password(self, old_password):
        old_pw = db.users.find_one({'username':session.get('username')})
        if not old_pw or not check_password(old_pw.get('password'), old_password.data):
            raise ValidationError('invalid old password')

class DashProfile(ProfileForm, FlaskForm):
    pass 
