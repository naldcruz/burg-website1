# ty 

from flask import render_template, request, Blueprint, redirect, url_for, flash, session
from .models import User 
from . import db 
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash 

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user: 
            if check_password_hash(user.pword, password):
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else: 
                flash('Wrong PW.', category='error')
        else: 
            flash('Email does not exist.', category='error')

    return render_template('login.html', error='test')

@auth.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        fName = request.form['fName']
        lName = request.form['lName']
        email = request.form['email']
        password1 = request.form['password1']
        password2 = request.form['password2']

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exist.', category='error')
        elif len(email) < 10: 
            flash('Email must be at least 10.', category='error')
        elif len(fName)  < 2: 
            flash('First name must be at least 2.', category='error')
        elif len(lName) < 2: 
            flash('last name must be at least 2', category='error')
        elif len(password1) < 7: 
            flash('Password must be at least 7.', category='error')
        elif password1 != password2:
            flash('Passwords do not match.', category='error')
        else: 
            new_user = User(fName=fName, lName=lName, email=email, pword=generate_password_hash(password1))
            db.session.add(new_user)
            db.session.commit() 

            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))
    
    return render_template('signup.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('auth.login'))

