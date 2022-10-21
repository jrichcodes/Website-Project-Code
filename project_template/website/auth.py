from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, gearItems, Trip, tripTypes
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, login_required, logout_user, current_user
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.events'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/new-trip', methods=['GET', 'POST'])
def new_trip():
    if request.method == 'POST':
        return redirect(url_for('views.home')) #redirect to home page after new account created
    return render_template("new_trip.html")

@auth.route('/trip-summary/<tripId>', methods=['GET', 'POST'])
def trip_summary(tripId):
    trip = Trip.query.filter_by(id = tripId).first()
    type = tripTypes.query.filter_by(id = trip.trip_type).first()
    gear_items = gearItems.query.filter_by(trip_type_id = trip.trip_type)
    return render_template("trip_summary.html", trip = trip, gear_items = gear_items, type =type)

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character', category='error')
        elif len(last_name) < 2:
            flash('Last name must be greater than 1 character', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            #add user to database
            new_user = User(email=email, first_name=first_name, last_name=last_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='sucess')
            return redirect(url_for('auth.login')) # redirect to events page after new account created


    return render_template("sign_up.html", user=current_user)
