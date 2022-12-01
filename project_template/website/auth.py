from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, UserBio, gearItems, Trip, tripTypes, Menu, menuTypes, menuItems
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
            flash('Username does not exist.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/trip-summary-map/<tripId>', methods=['GET', 'POST'])
def trip_summary_map(tripId):
    trip = Trip.query.filter_by(id = tripId).first()
    start_coords = (trip.latitude, trip.longitude)
    folium_map = folium.Map(min_zoom = 6, center=start_coords,tiles="OpenStreetMap")
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
        item = request.form.get('item')
        trip = Trip.query.filter_by(id = tripId).first()
        quantity = request.form.get('quantity')
        if len(item) < 1:
            flash('Not valid gear item', category = 'error')
        else: 
            new_gearItem = gearItems(name=item, trip_id = trip.id, quantity = quantity)
            db.session.add(new_gearItem)
            db.session.commit()

    trip = Trip.query.filter_by(id = tripId).first()
    type = tripTypes.query.filter_by(id = trip.trip_type).first()
    gear_items = gearItems.query.filter_by(trip_id = trip.id)

    return render_template("trip_summary.html", trip = trip, gear_items = gear_items, type = type)

@auth.route('/menu-summary/<menuId>', methods=['GET', 'POST'])
def menu_summary(menuId):

    if request.method == 'POST':
        item = request.form.get('item')
        menu = Menu.query.filter_by(id = menuId).first()
        quantity = request.form.get('quantity')
        if len(item) < 1:
            flash('Not valid menu item', category = 'error')
        else:
            new_menuItem = menuItems(name=item, menu_id = menu.id, quantity = quantity)
            db.session.add(new_menuItem)
            db.session.commit()

    menu = Menu.query.filter_by(id = menuId).first()
    #type = menuTypes.query.filter_by(id = menu.menu_type).first()
    #menu_items = menuItems.query.filter_by(menu_id = menu.id)

    #return render_template("menu_summary.html", menu = menu, menu_items = menu_items, type = type)
    return render_template("menu_summary.html", menu = menu)

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

        if len(email) < 5:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character', category='error')
        elif len(last_name) < 2:
            flash('Last name must be greater than 1 character', category='error')
        elif len(username) < 5:
            flash('Username must be greater than 4 characters', category='error')
        elif User.query.filter_by(username = username).first() != None:
            flash('Username is taken', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            #add user to database
            new_user = User(email=email, first_name=first_name, last_name=last_name, username=username, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            new_user_bio = UserBio(user_id = new_user.id)
            db.session.add(new_user_bio)
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
        if len(email) < 5:
            flash('Email must be greater than 4 characters.', category='error')
        else:
            tmp = User.query.filter_by(id = userId).first()
            tmp.email = email
            db.session.commit()
            return redirect(url_for('auth.login')) # redirect to login page after email reset
    return render_template("email_reset.html", user=current_user)

@auth.route('/username_reset/<userId>', methods = ['GET', 'POST'])
@login_required
def username_reset(userId):
    if request.method == 'POST':
        username = request.form.get('username')
        if len(username) < 5:
            flash('Username must be greater than 4 characters.', category='error')
        else:
            tmp = User.query.filter_by(id = userId).first()
            tmp.username = username
            db.session.commit()
            return redirect(url_for('auth.login')) # redirect to login page after email reset
    return render_template("username_reset.html", user=current_user)
