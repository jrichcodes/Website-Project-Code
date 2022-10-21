from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    desc = db.Column(db.String(10000))
    trip_type = db.Column(db.String(50))
    date = db.Column(db.DateTime())
    num_people = db.Column(db.Integer)
    #how to associate different imformation with different users
    #do this in the form of a foregin key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    trip = db.relationship('Trip')

class tripTypes(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(150))

class gearItems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    trip_type_id = db.Column(db.Integer, db.ForeignKey('tripTypes.id'))

