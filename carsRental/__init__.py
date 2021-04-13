from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_manager
import folium
"""
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
"""

app = Flask(__name__)
app.config['SECRET_KEY'] ='f00ee7583d29d7804578909a4ee52b96'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///carsRental.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


# Here we pass coordinates of Gfg 
# and starting Zoom level = 12
####my_map1 = folium.Map(location = [28.5011226, 77.4099794],
                                       ## zoom_start = 12 )
# save method of Map object will create a map
##my_map1.save(" my_map1.html " )


"""from carsRental.models import *
admin = Admin(app)
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Car, db.session))
"""
from carsRental import routes 