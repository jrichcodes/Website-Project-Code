from . import db
from flask_login import UserMixin
from hashlib import md5
from sqlalchemy.sql import func


class Trip(db.Model):
    id = db.Column(db.String(40), primary_key=True)
    name = db.Column(db.String(50))
    desc = db.Column(db.String(10000))
    trip_type = db.Column(db.Integer)
    date = db.Column(db.DateTime())
    num_people = db.Column(db.Integer)
    #how to associate different imformation with different users
    #do this in the form of a foregin key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

class Friends(db.Model):
    __tablename__ = 'friends'
    id = db.Column(db.Integer, primary_key=True)
    #1 for waiting on friend1, 2 for waiting on friend2, 0 for active
    status = db.Column(db.Integer)
    # holds the id of the partners friend id
    partner_link = db.Column(db.Integer)
    friend1_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    friend2_id = db.Column(db.Integer)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150), unique=True)
    last_name = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    trip = db.relationship('Trip')
    menu = db.relationship('Menu')
    friended = db.relationship('Friends')
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

class tripTypes(db.Model): 
    __tablename__ = 'trip_types'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(150))

class gearItems(db.Model):
    __tablename__ = 'gear_items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'))
    quantity = db.Column(db.Integer)

class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    m_desc = db.Column(db.String(10000))
    menu_type = db.Column(db.String(50))
    num_servings = db.Column(db.Integer)
    #how to associate different imformation with different users
    #do this in the form of a foregin key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class menuTypes(db.Model):
    __tablename__ = 'menu_types'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(150))

class menuItems(db.Model):
    __tablename__ = 'menu_items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'))
    quantity = db.Column(db.Integer)
