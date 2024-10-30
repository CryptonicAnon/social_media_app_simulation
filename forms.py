from flask_wtf import Form
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Regexp, ValidationError, Email, Length, EqualTo
from models import User

def used_email(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError("Account with that email already exists.")
def used_username(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError("Account with that username already exists.")

class regForm(Form):
    username = StringField('Username',validators=[DataRequired(), Regexp(r'[^a-zA-Z0-9_]+$', message=("Username can only include valid characters.")),used_username])
    email = StringField('Email',validators=[DataRequired(), Email(), used_email])
    password = PasswordField('Password',validators=[DataRequired(), Length(min=8),EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm Password',validators=[DataRequired()])

class loginForm(Form):
    email= StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password',validators=[DataRequired()])

class PostForm(Form):
    content = TextAreaField("Post here:", validators=[DataRequired()])