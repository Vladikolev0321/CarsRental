from enum import unique

from sqlalchemy.orm import backref
from carsRental import db
from datetime import datetime

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    cars =  db.relationship('Car', backref='uploader', lazy=True)

    def __repr__(self):
        return f"Admin('{self.username}', {self.email})"

class Car(db.Model): # to improve the car db model
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(20), unique=True, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)

    def __repr__(self):
        return f"Car('{self.model}', {self.date_posted})"