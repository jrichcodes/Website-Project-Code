from dataclasses import dataclass
from datetime import datetime
from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .models import Trip
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html")

@views.route('events', methods=['GET', 'POST'])
@login_required
def events():
    if request.method == 'POST':
        date_in = request.form.get('tripDate')
        time_in = request.form.get('tripTime')
        name_in = request.form.get('name')
        desc_in = request.form.get('desc')
        tripType_in = request.form.get('tripType')
        date_time = datetime.strptime(date_in + " " + time_in,"%Y-%m-%d %H:%M")
        if len(name_in) < 1:
            flash('Trip name is too short!', category='error')
        else:
            new_trip = Trip(name = name_in, desc = desc_in, trip_type = tripType_in, date = date_time, user_id=current_user.id)
            db.session.add(new_trip)
            db.session.commit()
            flash('Trip added!', category='success')
    return render_template("events.html", user=current_user)

@views.route('/profile/', methods = ['GET', 'POST'])
@login_required
def profile():
    return render_template("profile.html", user=current_user)