from re import S
from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from flask_login import login_user, logout_user, current_user, login_required
from itsdangerous import BadTimeSignature, URLSafeTimedSerializer, SignatureExpired
from app.models import User, UserInformation
from app import app, lm, bcrypt, mail
from flask_mail import Message
from app.src.utility import *
from .forms import *
import flask
import stripe
from datetime import datetime


auth = Blueprint('auth', __name__)
s = URLSafeTimedSerializer('GadgetsNow3103TimedSerializer!')


# provide login manager with load_user callback
@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if not current_user.is_authenticated:
        # Declare the login form
        form = LoginForm(request.form)
        # Flask message injected into the page, in case of any errors
        msg = None
        if request.method == 'POST':
            # check if both http method is POST and form is valid on submit
            if form.validate_on_submit():
                # assign form data to variables
                usernameoremail = request.form.get('usernameoremail', '', type=str)
                password = request.form.get('password', '', type=str) 
                remember_me = request.form.get('remember_me', '', type=bool)
                # filter User out of database through email
                user_by_email = User.query.filter_by(email=usernameoremail).first()
                user_by_username = User.query.filter_by(username=usernameoremail).first()
                if user_by_username:
                    password = password + user_by_username.salt
                    if bcrypt.check_password_hash(user_by_username.password, password):
                        login_user(user_by_username, remember_me)
                        flask.flash('Logged in successfully. (Username)')
                        return redirect(url_for('views.index'))
                    else:
                        msg = "Invalid Credentials. Please try again!"
                elif user_by_email:
                    password = password + user_by_email.salt
                    if bcrypt.check_password_hash(user_by_email.password, password):
                        login_user(user_by_email)
                        flask.flash('Logged in successfully. (Email)')
                        return redirect(url_for('views.index'))
                    else:
                        msg = "Invalid Credentials. Please try again!"
                else:
                    msg = "Invalid Credentials. Please try again!"
        return render_template( 'login.html', form=form, msg=msg )
    else:
        flask.flash('Please logout before proceeding.')
        return redirect(url_for('views.index'))

@auth.route('/verify_account/<token>')
def verify_account(token):
    try:
        email = s.loads(token, salt = "verify_account", max_age=300)
        now = datetime.now()
        user_by_email = User.query.filter_by(email=email).first()
        user_by_email.set_verified(1, now)
        return render_template('verify_account_success.html')
    except SignatureExpired:
        return render_template('verify_account_unsuccessful.html')
    except BadTimeSignature:
        return render_template('verify_account_unsuccessful.html')


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/register', methods=['GET','POST'])
def register():
    if not current_user.is_authenticated:
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
                msg = 'Error: User already exists!'
            else:         
                token = s.dumps(email, salt='verify_account')
                message = Message('Confirm Email', sender='GadgetsNow3103@gmail.com', recipients = [email])
                link = url_for('auth.verify_account', token=token, external=True)
                message.body = "Your verification link is 127.0.0.1/{}".format(link)
                mail.send(message)
                salt = get_random_string()
                password = password + salt
                pw_hash = bcrypt.generate_password_hash(password)
                user = User(username, email, pw_hash, salt, 0)
                user.save()
                msg = 'User created! Please check your email to verify the account.'     
                success = True
        else:
            msg = 'Input error'    
        return render_template( 'register.html', form=form, msg=msg, success=success )
    else:
        flask.flash('Please logout before proceeding.')
        return redirect(url_for('views.index'))
        


@auth.route('/checkout', methods=['GET', 'POST'])
def checkout():
    stripe.api_key = app.config['STRIPE_SECRET_KEY']
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items = [{
            'price': 'price_1LufGYH9RvLfX3o6QqrFdeyi',
            'quantity': 5,
        }],
        mode='payment',
        success_url = url_for('views.success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url = url_for('views.unsuccessful', _external=True),
    )
    return render_template('checkout.html', checkout_session_id=session['id'],checkout_public_key=app.config['STRIPE_PUBLIC_KEY'])


@app.route('/stripe_webhook', methods=['POST'])
def stripe_webhook():
    print('WEBHOOK CALLED')
    if request.content_length > 1024 * 1024:
        print('REQUEST TOO BIG')
        abort(400)
    payload = request.get_data()
    sig_header = request.environ.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = 'YOUR_ENDPOINT_SECRET'
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        print('INVALID PAYLOAD')
        return {}, 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print('INVALID SIGNATURE')
        return {}, 400
    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print(session)
        line_items = stripe.checkout.Session.list_line_items(session['id'], limit=1)
        print(line_items['data'][0]['description'])
    return {}