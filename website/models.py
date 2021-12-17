from os import name
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150),unique=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    dni = db.Column(db.Integer, unique = True)
    date= db.Column(db.DateTime(timezone=True),default=func.now())
class Client(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150),unique=True)
    name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    dni = db.Column(db.Integer, unique = True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))