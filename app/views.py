from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template("home.html")


@views.route('/success')
def success():
    return render_template('success.html')


@views.route('/unsuccessful')
def unsuccessful():
    return render_template('unsuccessful.html')