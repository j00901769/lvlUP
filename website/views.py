from flask import Blueprint, render_template, session, g, redirect
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("lvlUP_home.html", user = current_user)

@views.route('/account', methods = ['GET', 'POST'])
def account():
    if 'user' not in session:
        return redirect('/login')
    name, email, user_type, username = session['user']
    return render_template("lvlUP_account.html",
                           name = name, email = email,
                           user_type = user_type,
                           username = username)

@views.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

@views.route('/about')
def about():
    return render_template("lvlUP_about.html")

@views.route('/contact')
def contact():
    return render_template("lvlUP_contact.html")
