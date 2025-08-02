from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
#hashing a password
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__) 

#login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # check if email is valid - querying database for specific entry lookup
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully.', category='success')
                # log in user, remember they're logged in until browser is cleared or web server restarts
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password. Please try again.', category='error')
        else:
            flash('Email is not registered.', category='error')
        
    return render_template("login.html", user=current_user)

#logout
@auth.route('/logout')
# must be logged in to log out
@login_required
def logout():
    logout_user()
    # return user to login page
    flash('Successfully logged out!', category='success')
    return redirect(url_for('auth.login'))

#sign up
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        # make sure user is not trying to register with an already established email
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already registered. Please enter a different email.', category='error')
        elif len(email) < 4:
            flash('Email must be at least 4 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be at least 2 character.', category='error')
        elif password1 != password2:
            flash('Passwords do not match.', category='error')
        elif len(password1) < 7:
            flash('Passwords must be at least 7 characters.', category='error')
        else:
            # create a new user
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            # add user to database
            db.session.add(new_user)
            # commit to database
            db.session.commit()
            login_user(user, remember=True)
            flash('Account successfully created!', category='success')
            # redirect to home page
            return redirect(url_for('views.home'))
            
    return render_template("signup.html", user=current_user)