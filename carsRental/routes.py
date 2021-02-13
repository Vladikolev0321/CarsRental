from werkzeug.utils import redirect
from wtforms.validators import Email
from carsRental.models import Admin
from carsRental import app
from flask import render_template, url_for, flash, redirect
from carsRental.forms import LoginForm, RegistrationForm
from carsRental.models import Admin
from carsRental import bcrypt
from carsRental import db

@app.route("/")
def home():
    return render_template('home.html', title = "Home")

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        admin_username = Admin.query.filter_by(username=form.username.data).first()
        if admin_username:
            flash('That username is taken. Choose another one.', 'danger')
            return redirect(url_for('register'))
        admin_email = Admin.query.filter_by(email=form.email.data).first()
        if admin_email:
            flash('That email is taken. Choose another one.', 'danger')
            return redirect(url_for('register'))
        # valid username and email
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        admin = Admin(username=form.username.data, email=form.email.data, password=hashed_pass)
        db.session.add(admin)
        db.session.commit()
        flash(f'Created account for {form.username.data}. You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title = "Register", form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', title = "Login", form=form)