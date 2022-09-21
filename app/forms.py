from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired
from .validators import *

class LoginForm(FlaskForm):
	usernameoremail = StringField  (u'UsernameOrEmail' , validators=[DataRequired()])
	password = PasswordField(u'Password' , validators=[DataRequired()])
	remember_me = BooleanField()

class RegisterForm(FlaskForm):
	username = StringField  (u'Username' , validators=[DataRequired()])
	password = PasswordField(u'Password' , validators=[DataRequired()])
	email = StringField  (u'Email' , validators=[DataRequired(), Email()])
