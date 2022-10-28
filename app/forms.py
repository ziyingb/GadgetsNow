from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired
from .validators import *

class LoginForm(FlaskForm):
	recaptcha = RecaptchaField()
	usernameoremail = StringField  (u'UsernameOrEmail' , validators=[DataRequired()])
	password = PasswordField(u'Password' , validators=[DataRequired()])
	remember_me = BooleanField()

class RegisterForm(FlaskForm):
	recaptcha = RecaptchaField()
	username = StringField  (u'Username' , validators=[DataRequired()])
	password = PasswordField(u'Password' , validators=[DataRequired()])
	email = StringField  (u'Email' , validators=[DataRequired(), Email()])

class VerifyUser(FlaskForm):
	otp_code = StringField  (u'Verification' , validators=[DataRequired()])
	