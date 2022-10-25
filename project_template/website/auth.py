from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, gearItems, Trip, tripTypes
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, login_required, logout_user, current_user
import folium
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        # email = request.form.get('email')
        # email = email.lower()
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
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

@auth.route('/trip-summary-map/<tripId>', methods=['GET', 'POST'])
def trip_summary_map(tripId):
    trip = Trip.query.filter_by(id = tripId).first()
    start_coords = (trip.latitude, trip.longitude)
    folium_map = folium.Map(min_zoom = 6, center=start_coords,tiles="Stamen Terrain")
    if trip.trip_type == 1:
        icon_color = "red"
    elif trip.trip_type == 2:
        icon_color = "blue"
    elif trip.trip_type == 3:
        icon_color = "green"
    elif trip.trip_type == 4:
        icon_color = "purple"
    else:
        icon_color = "yellow"
    folium.Marker(location = start_coords,popup=f'<p>{trip.name}</p>', 
    icon = folium.Icon(color = icon_color, icon = "info-sign") ).add_to(folium_map)
    return folium_map._repr_html_()

@auth.route('/trip-summary/<tripId>', methods=['GET', 'POST'])
def trip_summary(tripId):

    if request.method == 'POST':
        print('here')
        item = request.form.get('item')
        trip = Trip.query.filter_by(id = tripId).first()
        trip_type = trip.trip_type
        if len(item) < 1:
            flash('Not valid gear item', category = 'error')
        else: 
            new_gearItem = gearItems(name=item, trip_type_id = trip_type)
            db.session.add(new_gearItem)
            db.session.commit()
            flash('Gear Item added!', category='success')

    trip = Trip.query.filter_by(id = tripId).first()
    type = tripTypes.query.filter_by(id = trip.trip_type).first()
    gear_items = gearItems.query.filter_by(trip_type_id = trip.trip_type)

    return render_template("trip_summary.html", trip = trip, gear_items = gear_items, type = type)

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        email = email.lower()
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character', category='error')
        elif len(last_name) < 2:
            flash('Last name must be greater than 1 character', category='error')
        elif len(username) < 5:
            flash('Username must be greater than 4 characters', category='error')
        elif User.query.filter_by(username = username).first() != None:
            flash('Username already in use')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            #add user to database
            new_user = User(email=email, first_name=first_name, last_name=last_name, username=username, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='sucess')
            return redirect(url_for('auth.login')) # redirect to login page after new account created
    return render_template("sign_up.html", user=current_user)

@auth.route('/password_reset/<userId>', methods = ['GET', 'POST'])
@login_required
def password_reset(userId):
    if request.method == 'POST':
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if password1 != password2:
            flash('Passwords don\'t match', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            tmp = User.query.filter_by(id = userId).first()
            tmp.password = generate_password_hash(password1, method='sha256')
            db.session.commit()
            return redirect(url_for('auth.login')) # redirect to login page after password reset
    return render_template("password_reset.html", user=current_user)

@auth.route('/email_reset/<userId>', methods = ['GET', 'POST'])
@login_required
def email_reset(userId):
    if request.method == 'POST':
        email = request.form.get('email')
        email = email.lower()
        if len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        else:
            tmp = User.query.filter_by(id = userId).first()
            tmp.email = email
            db.session.commit()
            return redirect(url_for('auth.login')) # redirect to login page after email reset
    return render_template("email_reset.html", user=current_user)