from flask_login.utils import login_required, logout_user
from werkzeug.utils import redirect
from wtforms.validators import Email
from carsRental.models import *
from carsRental import app, bcrypt, db
from flask import request, render_template, url_for, flash, redirect
from carsRental.forms import LoginForm, RegistrationForm
from carsRental.models import Admin 
from flask_login import login_user, current_user
from base64 import b64encode
import base64
from io import BytesIO #Converts data from Database into bytes



@app.route("/")
def home():
    return render_template('home.html', title = "Home")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    if(current_user.is_authenticated):
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        username = User.query.filter_by(username=form.username.data).first()
        if username:
            flash('That username is taken. Choose another one.', 'danger')
            return redirect(url_for('register'))

        admin_username = Admin.query.filter_by(username=form.username.data).first()
        if admin_username:
            flash('That username is taken. Choose another one.', 'danger')
            return redirect(url_for('register'))


        email = User.query.filter_by(email=form.email.data).first()
        if email:
            flash('That email is taken. Choose another one.', 'danger')
            return redirect(url_for('register'))

        admin_email = Admin.query.filter_by(email=form.email.data).first()
        if admin_email:
            flash('That email is taken. Choose another one.', 'danger')
            return redirect(url_for('register'))
        # valid username and email
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pass)
        db.session.add(user)
        db.session.commit()
        flash(f'Created account for {form.username.data}. You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title = "Register", form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if(current_user.is_authenticated):
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if(user and bcrypt.check_password_hash(user.password, form.password.data)):
            login_user(user, remember=form.remember.data)
            flash('You have been logged in!', 'success')
            return render_template('home.html', title = "Home")

        admin = Admin.query.filter_by(username=form.username.data).first()
        if(admin and bcrypt.check_password_hash(admin.password, form.password.data)):
            login_user(admin, remember=form.remember.data)
            flash('You have been logged in!', 'success')
            return render_template('home.html', title = "Home")
        
        flash('Login unsuccessful. Please check username and password', 'danger')

    return render_template('login.html', title = "Login", form=form)


#@app.route('/add_car', methods=['GET', 'POST'])
#    return render_template('add_car.html')

def render_picture(data):

    render_pic = base64.b64encode(data).decode('ascii') 
    return render_pic

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'GET':
        return render_template('add_car.html')
    else:
        file = request.files['inputFile']
        image = file.read()
        render_file = render_picture(image)
        model = request.form['model']
        location = request.form['location']
        price = request.form['price']

        newCar = Car(model = model, image=image, location = location, price = price, rendered_data=render_file)
        db.session.add(newCar)
        db.session.commit() 
        #flash(f'Pic {newCar.model} uploaded Text: {newCar.rendered_data}')

        return redirect(url_for('home'))



