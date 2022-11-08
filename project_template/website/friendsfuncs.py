from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from .models import User, Friends

def getfriend(friend2_id):
    friend2 = User.query.get(friend2_id)
    return friend2

def acceptfriend(friends_id):
    friends = Friends.query.filter_by(id = friends_id).first()
    friends2 = Friends.query.filter_by(id = friends.partner_link).first()
    friends.status = 0
    friends2.status = 0
    db.session.commit()

def rejectfriend(friends_id):
    friends = Friends.query.filter_by(id = friends_id).first()
    friends2 = Friends.query.filter_by(id = friends.partner_link).first()
    db.session.delete(friends)
    db.session.delete(friends2)
    db.session.commit()