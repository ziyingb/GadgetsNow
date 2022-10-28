import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mysqldb import MySQL
from flask_mail import Mail
from random import randint


base = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config.from_object('app.config.Config')
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root' 
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'gadgetsnow'

# CAPTCHA
app.config["RECAPTCHA_PUBLIC_KEY"] = "6Lf6IroiAAAAACdelIAKuPCl-DwfF6XcC_BZpTC0"
app.config["RECAPTCHA_PRIVATE_KEY"] = "6Lf6IroiAAAAAGKFOtWU5skNH7-QjQ4Fg9jWQ-BK"

# Email Verification
mail= Mail(app)
app.config["MAIL_SERVER"]='smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"]='gadgetsnow3103@gmail.com'
app.config['MAIL_PASSWORD']='texgdnpwcxxpjbhs'   
# app.config['MAIL_PASSWORD']='dwuxiliefpxpmjrq'   

app.config['MAIL_DEFAULT_SENDER'] = 'GadgetsNow'                 
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail=Mail(app)
otp= randint(000000,999999)

# Initialization
mysql = MySQL(app)
bcrypt = Bcrypt(app)
sa = SQLAlchemy(app)
lm = LoginManager()
lm.session_protection = "strong"
lm.login_view = "login"
lm.login_message_category = "info"
lm.init_app(app)

from .views import views
from .auth import auth

app.register_blueprint(views, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')

app.config['STRIPE_PUBLIC_KEY'] = 'pk_test_51LudtbH9RvLfX3o6FSoGYQxQisM9hz1chTbZl761XDY4HhHcaEWYpKtIXZmqjmm6zSTVuXQpISLh0Q8ZJTqDciby002Py4s5oS'
app.config['STRIPE_SECRET_KEY'] = 'sk_test_51LudtbH9RvLfX3o6zVrWW3RfRkvJjWPNOWzghcgRpr6jxjpWOXKYfi7aVJFjENmA06YKrENcwJOthOWQKhNKK9fU00lpcXpJsJ'

# Set up SQLITE - Temp***
@app.before_first_request
def init_db():
    sa.create_all()

from app import views, auth, models
