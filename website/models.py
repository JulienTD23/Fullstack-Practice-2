# stores database models: users & notes.
# set up the database
from . import db
# custom class we can inherit that will give the user object some specific things for flask login.
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    # func automatically gets the datetime for us
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    # associating the id of the user that created a note - foreign key, user has a one to many relationship
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')