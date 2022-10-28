import os
from decouple import config

basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    CSRF_ENABLED = True
    FLASK_DEBUG  = True
    TESTING = False
    # Set up the App SECRET_KEY
    SECRET_KEY = config('SECRET_KEY', default='secretkey3103')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
