from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from app.models import User, UserInformation
from app import app, lm, sa, bcrypt
from .forms import *

auth = Blueprint('auth', __name__)

# provide login manager with load_user callback
@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth.route('/login', methods=['GET', 'POST'])
def login():
     # Declare the login form
    form = LoginForm(request.form)
    # Flask message injected into the page, in case of any errors
    msg = None
    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():

        # assign form data to variables
        usernameoremail = request.form.get('usernameoremail', '', type=str)
        password = request.form.get('password', '', type=str) 
        # filter User out of database through email
        user_by_email = User.query.filter_by(email=usernameoremail).first()
        user_by_username = User.query.filter_by(username=usernameoremail).first()
        if user_by_username:
            if bcrypt.check_password_hash(user_by_username.password, password):
                login_user(user_by_username)
                return redirect(url_for('views.index'))
            else:
                msg = "Wrong password. Please try again."
        else:
            msg = "Unknown user"


        if user_by_email:
            if bcrypt.check_password_hash(user_by_email.password, password):
                login_user(user_by_email)
                return redirect(url_for('views.index'))
            else:
                msg = "Wrong password. Please try again."
        else:
            msg = "Unknown user"

    return render_template( 'login.html', form=form, msg=msg )


@auth.route('/logout')
def logout():
    pass


@auth.route('/register', methods=['GET','POST'])
def register():
    # declare the Registration Form
    form = RegisterForm(request.form)
    msg     = None
    success = False
    if request.method == 'GET':
        return render_template( 'register.html', form=form, msg=msg )
    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():
        # assign form data to variables
        username = request.form.get('username', '', type=str)
        password = request.form.get('password', '', type=str) 
        email    = request.form.get('email'   , '', type=str) 
        # filter User out of database through username
        user = User.query.filter_by(username=username).first()
        # filter User out of database through username
        user_by_email = User.query.filter_by(email=email).first()
        if user or user_by_email:
            msg = 'Error: User exists!'
        else:         
            pw_hash = bcrypt.generate_password_hash(password)
            user = User(username, email, pw_hash, 'salt', False)
            user.save()
            msg     = 'User created, please <a href="' + url_for('auth.login') + '">login</a>'     
            success = True
    else:
        msg = 'Input error'    
    return render_template( 'register.html', form=form, msg=msg, success=success )