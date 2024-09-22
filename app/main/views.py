from functools import wraps
from flask import render_template, session, redirect, url_for, request, flash
from . import main

from ..fb_functions import create_user, login_with_email_password, verify_id_token

# LoginRequired Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print("im gay")
        uid = session.get('uid')
        if uid is None:
            flash("You need to login first")
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return decorated_function


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Call login_with_email_password function
        token = login_with_email_password(email, password)
        if token:
            # Store the token in the session
            uid = verify_id_token(token)
            session['uid'] = uid
            return redirect(url_for('main.index'))
        else:
            flash("Invalid Credentials")
            return redirect(url_for('main.login'))
    return render_template('login.html')

@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        password = request.form['password']
        license_no = request.form['license']
        contact = request.form['contact']
        create_user(email, password, name, license_no, contact)
        return redirect(url_for('main.login'))
    return render_template('signup.html')

@main.route('/uid')
def return_uid():
    uid = session.get('uid')
    return f"UID: {uid}"

@main.route('/logout')
@login_required
def logout():
    session.pop('uid', None)
    return redirect(url_for('main.index'))