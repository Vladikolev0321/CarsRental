from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] ='f00ee7583d29d7804578909a4ee52b96'

from carsRental import routes 