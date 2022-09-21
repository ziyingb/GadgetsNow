import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

base = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config.from_object('app.config.Config')

# Initialization
bcrypt = Bcrypt(app)
sa = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)

from .views import views
from .auth import auth

app.register_blueprint(views, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')

# Set up SQLITE - Temp***
@app.before_first_request
def init_db():
    sa.create_all()

from app import views, auth, models
