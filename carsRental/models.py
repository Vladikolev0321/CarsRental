from enum import unique

from sqlalchemy.orm import backref
from carsRental import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from dateutil.tz import gettz
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
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.Boolean, nullable=False, default=False)
    #rendered_data = db.Column(db.Text, nullable=False)#Data to render the pic in browser

    def __repr__(self):
        return f"Car('{self.model}', {self.date_posted})"

class Station(db.Model): # to improve the stations db model
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(50), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    name = db.Column(db.String(128), unique=True, nullable=False)
    count_cars = db.Column(db.Integer, nullable=False, default=0)



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default = False)
    money = db.Column(db.Float, nullable=False, default = 0.0)
    #cars =  db.relationship('Car', backref='uploader', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', {self.email})"

class RentalInformation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #user_name = db.Column(db.String(20), unique=True, nullable=False)
    start_location = db.Column(db.String(1000), nullable=False)
    end_location = db.Column(db.String(1000), nullable=False)
    start_time = db.Column(db.String(10), nullable=True)
    end_time = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)

    def __repr__(self):
        return f"RentalInfo('{self.user_name}', {self.car_id})"



db.create_all()