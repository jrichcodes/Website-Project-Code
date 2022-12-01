from dataclasses import dataclass
from datetime import datetime
from django.shortcuts import render
from flask import Blueprint, render_template, request, flash, current_app as app, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Trip, UserBio, User, gearItems, Menu, tripTypes, Friends, menuTypes, menuItems
from . import db
import json, os
import folium
from flask_sqlalchemy import SQLAlchemy
from . import time_till
from . import friendsfuncs
import uuid
from .general import ret_location, get_json, get_recipes

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        return render_template("home.html", check = 1)
    else: 
        return render_template("home.html", check = 0)

@views.route('events', methods=['GET', 'POST'])
@login_required
def events():
    continent = request.args.get('continent', "")
    name = request.args.get('name', "")
    description = request.args.get('description', "")

    if request.method == 'POST':
        if request.form['submit_button'] == 'create trip':
            date_in = request.form.get('tripDate')
            time_in = request.form.get('tripTime')
            name_in = request.form.get('name')
            desc_in = request.form.get('desc')
            location = ret_location(request.form.get('location_name'))
            lat_in = location[0]
            lon_in = location[1]
            tripType_in = request.form.get('tripType')
            num_people_in = request.form.get('num_people')
            date_time = datetime.strptime(date_in + " " + time_in,"%Y-%m-%d %H:%M")
            
            if int(tripType_in) == 5:
                other_name = request.form.get('otherType')
                other_Type = tripTypes(type=other_name)
                db.session.add(other_Type)
                db.session.commit()
                type = db.session.query(tripTypes).filter(tripTypes.type == other_name).first()
                tripType_in = type.id
            
            if len(name_in) < 1:
                flash('Trip name is too short!', category='error')
            else:
                new_trip = Trip(name = name_in, desc = desc_in, trip_type = tripType_in, date = date_time, num_people = num_people_in, user_id=current_user.id, latitude = lat_in, longitude = lon_in, id = uuid.uuid1().hex)
                db.session.add(new_trip)
                db.session.commit()
                flash('Trip added!', category='success')

    return render_template("events.html", user=current_user, time_till=time_till.count_time, continent=continent, name=name, description=description)

@views.route('/friends', methods=['GET', 'POST'])
@login_required
def friends():
    if request.method == 'POST':
        if request.form['Add_friend_button'] == 'Add Friend':
            username_in = request.form.get('username')
            if len(username_in) < 1:
                flash('Username is too short!', category='error')
            else:
                friend2 = User.query.filter_by(username = username_in).first()
                if friend2:
                    new_friends1 = Friends(friend1_id = current_user.id, friend2_id = friend2.id, status = 2)
                    new_friends2 = Friends(friend2_id = current_user.id, friend1_id = friend2.id, status = 1)
                    db.session.add(new_friends1)
                    db.session.add(new_friends2)
                    db.session.commit()
                    new_friends1.partner_link = new_friends2.id
                    new_friends2.partner_link = new_friends1.id
                    db.session.commit()
                else:
                    flash('not found', category='error')

    return render_template("friends.html", user=current_user, getfriend = friendsfuncs.getfriend)

@views.route('/friend/<friendship_id>', methods=['GET', 'POST'])
def friend(friendship_id):
    friendship = Friends.query.filter_by(id = friendship_id).first()
    friend2 = User.query.filter_by(id = friendship.friend2_id).first()
    friend_bio = UserBio.query.filter_by(user_id = friend2.id).first()

    if request.method == 'POST':
        if request.form['Friendship_Button'] == 'Accept':
            friendsfuncs.acceptfriend(friendship_id)
        elif request.form['Friendship_Button'] == 'Reject':
            friendsfuncs.rejectfriend(friendship_id)
            return redirect(url_for('views.friends'))

    return render_template("friend.html", friendship = friendship, friend2 = friend2, time_till=time_till.count_time, friend_bio = friend_bio)

@views.route('/map')
def index():
    start_coords = (35, -83)
    folium_map = folium.Map(min_zoom = 4, center=start_coords,tiles="OpenStreetMap")
    list = Trip.query.filter_by(user_id=current_user.id).order_by(Trip.id).all()
    for item in list:
        if item.latitude != None and item.longitude != None:
            marker_coords = (item.latitude,item.longitude)
            if item.trip_type == 1:
                icon_color = "red"
            elif item.trip_type == 2:
                icon_color = "blue"
            elif item.trip_type == 3:
                icon_color = "green"
            elif item.trip_type == 4:
                icon_color = "purple"
            else:
                icon_color = "yellow"
                
            folium.Marker(location = marker_coords,popup=f'<a href="/trip-summary/{item.id}"> {item.name}</a>', 
            icon = folium.Icon(color = icon_color, icon = "info-sign") ).add_to(folium_map)
    return folium_map._repr_html_()

@views.route('/profile/', methods = ['GET', 'POST'])
@login_required
def profile():
    curbio = UserBio.query.filter_by(user_id=User.id).first()
    bio = curbio.bio
    d_d_a = curbio.dream_dest_array

    if request.method == 'POST':
        if request.form['submit_button'] =='submit bio':
            bio_in = request.form.get('bio')
            d_d_a_in = request.form.get('d_d_a')

            curbio.bio = bio_in
            curbio.dream_dest_array = d_d_a_in
            db.session.commit()
            return redirect(url_for('views.profile'))

    return render_template("profile.html", user=current_user,  d_d_a = d_d_a, bio = bio)

@views.route('menu', methods=['GET', 'POST'])
@login_required
def menu():
    name = request.args.get('name', "")
    desc = request.args.get('desc', "")
    menuType = request.args.get('menuType', "")
    num_servings = request.args.get('num_servings', "")

    if request.method == 'POST':
        if request.form['submit_button'] == 'create meal':
            name_in = request.form.get('name')
            desc_in = request.form.get('desc')
            menuType_in = request.form.get('menuType')
            num_servings_in = request.form.get('num_servings')
            if len(name_in) < 1:
                flash('Meal name is too short!', category='error')
            else:
                new_menu = Menu(name = name_in, m_desc = desc_in, menu_type = menuType_in, num_servings = num_servings_in, user_id=current_user.id)
                db.session.add(new_menu)
                db.session.commit()
                flash('Meal added!', category='success')

    return render_template("menu.html", user=current_user, name=name, desc=desc, menuType=menuType, num_servings=num_servings)

@views.route('suggestions', methods=['GET', 'POST'])
def suggestions():
    continent = request.args.get('continent', "")
    data = get_json()
    return render_template("trip_suggestions.html", data=data, place=continent)

@views.route('/recipes', methods=['GET', 'POST'])
def recipes():
    data = get_recipes()
    return render_template("recipes.html", data=data)

@views.route('/single-recipe', methods=['GET','POST'])
def single_recipe():
    recipe_in = request.args.get('recipe', "")
    data = get_recipes()
    for recipe in data:
        if recipe['name'] == recipe_in:
            recipe_out = recipe
    return render_template("single-recipe.html", recipe = recipe_out)
    
@views.route('/delete-gearitem', methods=['POST'])
def delete_gearitem():
    if request.method == 'POST':
        Item = json.loads(request.data)
        gearid = Item['gearItemId']
        Item = gearItems.query.get(gearid)
        if Item:
            db.session.delete(Item)
            db.session.commit()
    return jsonify({})

@views.route('/delete-trip',methods=['POST'])
def delete_trip():
    if request.method == 'POST':
        delete_trip = json.loads(request.data)
        tripId = delete_trip['tripId']
        delete_trip = Trip.query.get(tripId)
        if delete_trip:
            db.session.delete(delete_trip)
            db.session.commit()
    return jsonify({})

@views.route('/delete-menu', methods=['POST'])
def delete_menu():
    if request.method == 'POST':
        delete_menu = json.loads(request.data)
        menuId = delete_menu['menuId']
        delete_menu = Menu.query.get(menuId)
        if delete_menu:
            db.session.delete(delete_menu)
            db.session.commit()
    return jsonify({})

@views.route('/delete-menuitem', methods=['POST'])
def delete_menuitem():
    if request.method == 'POST':
        item = json.loads(request.data)
        menuId = item['menuItemId']
        item = menuItems.query.get(menuId)
        if item:
            db.session.delete(item)
            db.session.commit()
    return jsonify({})
