from carsRental import app
from flask import render_template, url_for
from carsRental.forms import LoginForm, RegistrationForm

@app.route("/")
def home():
    return render_template('home.html', title = "Home")

@app.route("/register")
def register():
    form = RegistrationForm()
    return render_template('register.html', title = "Register", form=form)

@app.route("/login")
def login():
    form = LoginForm()
    return render_template('register.html', title = "Register", form=form)