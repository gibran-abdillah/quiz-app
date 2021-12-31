from wtforms import ValidationError

from wtforms.fields import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField
)
from wtforms.validators import ( 
    DataRequired, 
    EqualTo,
    Length
)

from flask_wtf import FlaskForm
from app.db import db 
import re 


EMAIL_REGEX = r'[\w\d\-]+@[\w\d\-\.]+\.[\w]{2,4}'

class LoginForm(FlaskForm):
    username = StringField('username')
    password = PasswordField('password')

class PasswordForm:
    password = PasswordField('Password', validators=[
                            DataRequired('Password is required'),
                            Length(min=5, max=100,message='password length must be between 5 to 100 characters'), 
                            EqualTo('password_confirmation', message='invalid confirmation password')],
                            render_kw={'placeholder':'password'})

    password_confirmation = PasswordField('Confirm Password', 
                            validators=[
                                DataRequired('Enter confirm password')],
                            render_kw={'placeholder':'Confirm Password'})    
        

class ProfileForm:
    full_name = StringField('Full Name',
                    validators=[DataRequired(),
                                Length(min=4, max=100, message='full name length must be between 4 to 100 characters')],
                    render_kw={'placeholder':'Full Name'})

    email = StringField('Email', validators=[DataRequired('Email required')], render_kw={'placeholder':'Email'})

    username = StringField('Username ', 
                            validators=[DataRequired(message='Username is required'), Length(min=4, max=14, message='Username length must be between 4 to 14 characters')],
                            render_kw={'placeholder':'username'})
    
    
    def validate_full_name(self, full_name):
        if re.findall('([\d_.]+)', full_name.data):
            raise ValidationError('numeric / symbol not allowed in your name')
    
    def validate_username(self, username):
        if re.findall(' ', username.data) or re.findall('([A-Z])', username.data):
            raise ValidationError('invalid username, space or uppercase not allowed')
        
        if db.users.find_one({'username':username.data}):
            raise ValidationError('Username already registered')
    
    def validate_email(self, email):
        if db.users.find_one({'email':email.data}):
            raise ValidationError('Email already registered')
        
        if not re.match(EMAIL_REGEX, email.data):
            raise ValidationError('Invalid Email Address')

class RegisterForm(FlaskForm, PasswordForm, ProfileForm):
    pass 