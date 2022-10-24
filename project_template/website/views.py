from dataclasses import dataclass
from datetime import datetime
from django.shortcuts import render
from flask import Blueprint, render_template, request, flash, current_app as app, redirect, url_for
from flask_login import login_required, current_user
from .models import Trip, User
from . import db
import json, os
from .read_trip_suggestions import get_json
import folium
from flask_sqlalchemy import SQLAlchemy

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html")

@views.route('events', methods=['GET', 'POST'])
@login_required
def events():
    if request.method == 'POST':
        if request.form['submit_button'] == 'create trip':
            date_in = request.form.get('tripDate')
            time_in = request.form.get('tripTime')
            name_in = request.form.get('name')
            desc_in = request.form.get('desc')
            lat_in = request.form.get('lat')
            lon_in = request.form.get('lon')
            tripType_in = request.form.get('tripType')
            num_people_in = request.form.get('num_people')
            date_time = datetime.strptime(date_in + " " + time_in,"%Y-%m-%d %H:%M")
            if len(name_in) < 1:
                flash('Trip name is too short!', category='error')
            else:
                new_trip = Trip(name = name_in, desc = desc_in, trip_type = tripType_in, date = date_time, num_people = num_people_in, user_id=current_user.id, latitude = lat_in, longitude = lon_in)
                db.session.add(new_trip)
                db.session.commit()
                flash('Trip added!', category='success')

    return render_template("events.html", user=current_user)

@views.route('/map')
def index():
    start_coords = (35, -83)
    folium_map = folium.Map(min_zoom = 4, center=start_coords,tiles="Stamen Terrain")
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
                
            folium.Marker(location = marker_coords,popup=f'<a href="/trip-summary/{item.id}"> {item.name}</a>', icon = folium.Icon(color = icon_color, icon = "info-sign") ).add_to(folium_map)
    return folium_map._repr_html_()

@views.route('/profile/', methods = ['GET', 'POST'])
@login_required
def profile():
    return render_template("profile.html", user=current_user)


@views.route('suggestions')
def suggestions():
    data = get_json()
    return render_template("trip_suggestions.html", data=data)
