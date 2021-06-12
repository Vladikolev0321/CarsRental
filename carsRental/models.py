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
    is_rent = db.Column(db.Boolean, nullable=False, default = False)
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
    nearest_station_id = db.Column(db.Integer, db.ForeignKey('station.id'), nullable=False)

    def __repr__(self):
        return f"RentalInfo('{self.user_name}', {self.car_id})"

class Paths(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_location_x = db.Column(db.String(100), nullable=False)
    start_location_y = db.Column(db.String(100), nullable=False)
    end_location_x = db.Column(db.String(100), nullable=False)
    end_location_y = db.Column(db.String(100), nullable=False)
    start_time = db.Column(db.String(20), nullable=True)
    end_time = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_driver = db.Column(db.Boolean, nullable=False, default = False)

class Waypoints(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location_x = db.Column(db.String(100), nullable=False)
    location_y = db.Column(db.String(100), nullable=False)
    path_id = db.Column(db.Integer, db.ForeignKey('paths.id'), nullable=False)

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    driver_name = db.Column(db.String(100), nullable=False)
    driver_phone_number = db.Column(db.String(100), nullable=False)

class Member_Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(100), nullable=False)
    # phone_number = db.Column(db.String(100), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    member_id =  db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey(User.id))
    # receiver_id = db.Column(db.Integer, db.ForeignKey(User.id))
    group_id = db.Column(db.Integer, db.ForeignKey(Group.id))
    content = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


db.create_all()