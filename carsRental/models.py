from enum import unique

from sqlalchemy.orm import backref
from carsRental import db, login_manager
from datetime import datetime
from flask_login import UserMixin
#from flask_admin.contrib.sqla import ModelView


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class Car(db.Model): # to improve the car db model
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(128), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    #image = db.Column(db.LargeBinary, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    location = db.Column(db.String(128), nullable=False)
    price = db.Column(db.Float, nullable=False)
    #rendered_data = db.Column(db.Text, nullable=False)#Data to render the pic in browser

    def __repr__(self):
        return f"Car('{self.model}', {self.date_posted})"

class Station(db.Model): # to improve the stations db model
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(128), unique=True, nullable=False)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default = False)
    #cars =  db.relationship('Car', backref='uploader', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', {self.email})"




db.create_all()