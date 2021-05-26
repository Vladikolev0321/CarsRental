from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TimeField, RadioField
from wtforms.fields.core import RadioField, SelectField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms.widgets.core import CheckboxInput

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    
    submit = SubmitField('Log in')

class RentForm(FlaskForm):
    endloctation = StringField('End Location')
    endtime = TimeField('End of rental time')
    submit = SubmitField('Rent')

class CarPoolForm(FlaskForm):
    startlocation = StringField('Start location')
    endloctation = StringField('End Location')
    starttime = DateTimeLocalField('Start of rental time', format = '%Y-%m-%dT%H:%M')
    endtime = DateTimeLocalField('End of rental time', format = '%Y-%m-%dT%H:%M')
    isdriver = SelectField('Are you a driver?', choices=[('yes'), ('no')])
    submit = SubmitField('Find car')

class WaypointForm(FlaskForm):
    location = StringField('Location')
    submit = SubmitField('Add waypoint')

