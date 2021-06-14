from flask.globals import request, session
from flask.helpers import url_for
from flask.templating import render_template
#from carsRental.models import Message
from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_manager
from flask_socketio import SocketIO, send
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
socketio = SocketIO(app, cors_allowed_origins='*')


# @socketio.on('message')
# def handleMessage(data):
#     print(f"Message: {data}")
#     send(data, broadcast=True)

#     message = Message(username=data['username'], msg=data['msg'])
#     db.session.add(message)
#     db.session.commit()

# @app.route('/chat2')
# def chat():
#     print(session)
#     username = None
#     if session.get('username'):
#         username = session.get('username')
#     return render_template('chat2.html', username=username)

# @app.route('/login2', methods=["POST"])
# def login2():
#     if request.method == "POST":
#         username = request.form.get('username')
#         session['username'] = username
#     return redirect(url_for('chat'))



# @app.route('/logout2')
# def logout():
#     session.pop('username', None)
#     return redirect(url_for('/'))



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