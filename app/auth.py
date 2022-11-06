from re import S
from flask import Blueprint, render_template, request, flash, redirect, url_for, abort, session
from flask_login import login_user, logout_user, current_user, login_required
from itsdangerous import BadTimeSignature, URLSafeTimedSerializer, SignatureExpired
from app.models import User, UserInformation, ShoppingCart
from app import app, lm, bcrypt, mail
from flask_mail import Message
from app.src.utility import *
from .forms import *
from datetime import datetime
import flask
import stripe
import pyotp


auth = Blueprint('auth', __name__)
s = URLSafeTimedSerializer('GadgetsNow3103TimedSerializer!')
uid_private_key = '$2a$12$nimtZBhjl.7PTRdnoQ/viOWz200MV9eYAIp.OAb71MpR7rygDVZt6' 
password_private_key = '$2a$12$6uFb4m9raet4ofAgIIrQmuXVF7NTlKiXNHydqi/B5YjhllBlYHghC' 

# provide login manager with load_user callback
@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if not current_user.is_authenticated:
        session['login_failure_count'] = 0
        # Declare the login form
        form = LoginForm(request.form)
        # Flask message injected into the page, in case of any errors
        msg = None
        if request.method == 'POST':
            # check if both http method is POST and form is valid on submit
            if form.validate_on_submit():
                if session['login_failure_count'] >= 3:
                    msg = "Too many failed attempts. Please try again after 30 minutes."
                    return render_template( 'login.html', form=form, msg=msg )
                else:
                    # assign form data to variables
                    usernameoremail = request.form.get('usernameoremail', '', type=str)
                    password = request.form.get('password', '', type=str) 
                    if bcrypt.check_password_hash(password_private_key, password) and bcrypt.check_password_hash(uid_private_key ,usernameoremail):
                        session['priviledge'] = 'admin'
                        return redirect(url_for('views.adminDashboard'))
                    remember_me = request.form.get('remember_me', '', type=bool)
                    # filter User out of database through email
                    user_by_email = User.query.filter_by(email=usernameoremail).first()
                    user_by_username = User.query.filter_by(username=usernameoremail).first()
                    if user_by_username:
                        password = password + user_by_username.salt
                        if bcrypt.check_password_hash(user_by_username.password, password):
                            session['user_tobevalidated'] = usernameoremail
                            session['remember_me_input'] = remember_me
                            # login_user(user_by_username, remember_me)
                            session['login_failure_count'] = 0
                            # flask.flash('Logged in successfully. (Username)')
                            # return redirect(url_for('auth.login_2fa'))
                            return redirect(url_for('views.index'))
                        else:
                            session['login_failure_count'] += 1
                            msg = "Invalid Credentials. Please try again!"
                    elif user_by_email:
                        password = password + user_by_email.salt
                        if bcrypt.check_password_hash(user_by_email.password, password):
                            session['user_tobevalidated'] = usernameoremail
                            session['remember_me_input'] = remember_me
                            # login_user(user_by_email, remember_me)
                            session['login_failure_count'] = 0
                            # flask.flash('Logged in successfully. (Email)')
                            # return redirect(url_for('auth.login_2fa'))
                            return redirect(url_for('views.index'))
                        else:
                            session['login_failure_count'] += 1
                            msg = "Invalid Credentials. Please try again!"
                    else:
                        session['login_failure_count'] += 1
                        msg = "Invalid Credentials. Please try again!"
        return render_template( 'login.html', form=form, msg=msg )
    else:
        flask.flash('Please logout before proceeding.')
        return redirect(url_for('views.index'))



@auth.route('/login/2fa')
def login_2fa():
    #global secret
    secret = pyotp.random_base32()
    #if secret is None:
#         secret = pyotp.random_base32()
    return render_template('login_2fa.html', secret=secret)


# 2FA form route
# 2FA form route
@auth.route('/login/2fa', methods=["POST"])
def login_2fa_form():

     # getting secret key used by user
    secret = request.form.get("secret")
    # getting OTP provided by user
    otp = int(request.form.get("otp"))

    # verifying submitted OTP with PyOTP
    if pyotp.TOTP(secret).verify(otp):
        # inform users if OTP is valid
        flash("The TOTP 2FA token is valid","success")
        ####### redirect to home page
        return redirect(url_for('views.index'))
    else:
        # inform users if OTP is invalid
        flash("You have supplied an invalid 2FA token!","danger")
        return redirect(url_for('auth.login_2fa'))

@auth.route('/verify_account/<token>')
def verify_account(token):
    try:
        email = s.loads(token, salt = "verify_account", max_age=300)
        now = datetime.now()
        user_by_email = User.query.filter_by(email=email).first()
        if user_by_email.verified_dt == None:
            user_by_email.set_verified()
            ui = UserInformation(user_by_email.id, now)
            ui.save()
            msg = "Account has been successfully verified."
        else:
            msg = "Account is already verified."
        return render_template('verify_account_success.html', msg = msg)
    except SignatureExpired:
        return render_template('verify_account_unsuccessful.html')
    except BadTimeSignature:
        return render_template('verify_account_unsuccessful.html')


@auth.route('/shopping_cart', methods = ['GET', 'POST'])
def cart():
    if current_user.is_authenticated:
        if request.method == 'POST':
            if 'prod_id' in request.form:
                uid = session['_id']
                prod_id = request.form['prod_id']
                print(uid, prod_id)
                cart_item = ShoppingCart.query.filter_by(uid = uid, prod_id = prod_id).first()
                cart_item.delete()
        products = ShoppingCart.query.filter_by(uid = session['_id']).all()
        line_items = []
        for item in products:
            tempdict = {'price' : item.prod_price_stripe,
                        'quantity' : item.quantity}
            line_items.append(tempdict)
        if products:
            stripe.api_key = app.config['STRIPE_SECRET_KEY']
            ss = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items = line_items,
                mode='payment',
                success_url = url_for('views.success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url = url_for('views.unsuccessful', _external=True),
            )
            return render_template('shopping_cart.html', checkout_session_id=ss['id'],checkout_public_key=app.config['STRIPE_PUBLIC_KEY'], products = products)
        else:
            return render_template('shopping_cart.html', products = products)
    else:
        return redirect(url_for('auth.login'))


@auth.route('/logout')
def logout():
    logout_user()
    session.clear()
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
                flash('Error: User already exists!','danger')
            elif len(password) < 10:
                flash('Password must be at least 10 characters.','danger')
            elif re.search('[0-9]',password) is None:
                flash('Make sure your password has a number in it','danger')
            elif re.search('[A-Z]',password) is None: 
                flash('Make sure your password has a capital letter in it','danger')
            elif re.search('[^a-zA-Z0-9]',password) is None: 
                flash('Make sure your password has a special character in it','danger')
            else:
                token = s.dumps(email, salt='verify_account')
                message = Message('Confirm Email', sender='gadgetsnow3x03@fastmail.com', recipients = [email])
                link = url_for('auth.verify_account', token=token, external=True)
                message.body = "Your verification link is https://www.gadgetsnow.tk{}".format(link) 
                # Need to set to whatever URL
                mail.send(message)
                salt = get_random_string()
                password = password + salt
                pw_hash = bcrypt.generate_password_hash(password)
                while True:
                    temp_id = generateID()
                    tuser = User.query.filter_by(id = temp_id).first()
                    if not tuser:
                        user = User(temp_id, username, email, pw_hash, salt)
                        user.save()
                        flash('User created! Please check your email to verify the account.','success')    
                        success = True
                        break
        else:
            msg = 'Input error'    
        return render_template('register.html', form=form, msg=msg, success=success )
    else:
        flask.flash('Please logout before proceeding.')
        return redirect(url_for('views.index'))


@auth.route('/personal_information', methods=['GET', 'POST'])
def userInformation():
    if current_user.is_authenticated:
        # Assign form data to variables
        id = session['_user_id']
        # filter User out of database through username
        userInfo = UserInformation.query.filter_by(user_id=id).first()
        # declare the Registration Form
        form = UpdateProfile(request.form)
        msg     = None
        success = False
        if request.method == 'GET':
            return render_template( 'user_information.html', form=form, msg=msg, success=success, userInfo = userInfo)
        # check if both http method is POST and form is valid on submit
        if form.validate_on_submit():
            first_name = request.form.get('first_name', '', type=str)
            last_name = request.form.get('last_name', '', type=str)
            mobile_no = request.form.get('mobile_no', '', type=str)
            country = request.form.get('country', '', type=str)
            address = request.form.get('address', '', type=str)
            city = request.form.get('city', '', type=str)
            postal_code = request.form.get('postal_code', '', type=str)
            last_modified_dt = datetime.now()
            userInfo.update_information(first_name, last_name, mobile_no, address, country, city, postal_code, last_modified_dt)
            flash('Profile updated successfully.','success')
        else:
            msg = 'Input error'
        return render_template( 'user_information.html', form=form, msg=msg, success=success, userInfo = userInfo)
    else:
        flask.flash('Please login before proceeding.')
        return redirect(url_for('auth.login'))


# @auth.route('/checkout', methods=['GET', 'POST'])
# def checkout():
#     stripe.api_key = app.config['STRIPE_SECRET_KEY']
#     session = stripe.checkout.Session.create(
#         payment_method_types=['card'],
#         line_items = [{
#             'price': 'price_1LufGYH9RvLfX3o6QqrFdeyi',
#             'quantity': 5,
#         }],
#         mode='payment',
#         success_url = url_for('views.success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
#         cancel_url = url_for('views.unsuccessful', _external=True),
#     )
#     return render_template('checkout.html', checkout_session_id=session['id'],checkout_public_key=app.config['STRIPE_PUBLIC_KEY'])


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
        line_items = stripe.checkout.Session.list_line_items(session['id'], limit=1)
        print(line_items['data'][0]['description'])

    return {}


@auth.route('/forget_password', methods = ['POST', 'GET'])
def forgetpassword():
    if not current_user.is_authenticated:
        msg     = None
        if request.method == 'POST':
            usernameoremail = request.form.get('usernameoremail', '', type=str)
            # filter User out of database through username
            user = User.query.filter_by(username=usernameoremail).first()
            # filter User out of database through username
            user_by_email = User.query.filter_by(email=usernameoremail).first()
            email = ""
            if user:
                email = user.email
            elif user_by_email:
                email = user_by_email.email
                
            if email != "":
                token = s.dumps(email, salt='reset_password')
                message = Message('Reset Password', sender='gadgetsnow3x03@fastmail.com', recipients = [email])
                link = url_for('auth.reset_password', token=token, external=True)
                message.body = "Your verification link is https://www.gadgetsnow.tk{}".format(link) 
                # Need to set to whatever URL
                mail.send(message)
                flash("Please check your email to reset your password!",'warning')
            else:
                flash("This email or username does not exist!",'danger')
        form = ForgetPasswordForm(request.form)
        return render_template('forgetpassword.html', form=form, msg = msg)
    else:
        return redirect(url_for('views.index'))


@auth.route('/reset_password/<token>', methods=['GET','POST'])
def reset_password(token):
    if not current_user.is_authenticated:
        msg     = None
        if request.method == 'POST':
            password = request.form.get('password', '', type=str) 
            passwordCheck = request.form.get('passwordCheck', '', type=str) 
            if password != passwordCheck:
                msg = "Passwords do not match! Please try again."
            else:
                email = s.loads(token, salt = "reset_password", max_age=300)
                user_by_email = User.query.filter_by(email=email).first()
                salt = get_random_string()
                password = password + salt
                pw_hash = bcrypt.generate_password_hash(password)
                if user_by_email.changepassword(pw_hash, salt):
                    msg = "Password has been reset. Click <a href='/login'>here</a> to login."
    form = ResetPasswordForm(request.form)
    return render_template('reset_password.html', form = form, msg = msg)

# Use special @app.errorhandler() decorator for 404 errors.
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

# This one relates to app.route 500 below
@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500
