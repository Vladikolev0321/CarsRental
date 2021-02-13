from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] ='f00ee7583d29d7804578909a4ee52b96'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///carsRental.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from carsRental import routes 