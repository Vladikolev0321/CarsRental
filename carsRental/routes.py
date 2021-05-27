from flask_login.utils import login_required, logout_user
from werkzeug.utils import redirect
from wtforms.validators import Email
from carsRental.models import *
from carsRental import app, bcrypt, db, folium
from flask import request, render_template, url_for, flash, redirect, abort
from carsRental.forms import CarPoolForm, LoginForm, RegistrationForm, RentForm, WaypointForm
from flask_login import login_user, current_user
from base64 import b64encode
import base64
import os
from io import BytesIO #Converts data from Database into bytes
from geopy.geocoders import Nominatim
from geopy import distance
from wtforms import TimeField
from datetime import datetime
import pytz
import geocoder
import math



nom = Nominatim(user_agent="CarsRental")
@app.route("/", methods=['GET', 'POST'])

def home():
    if request.method == 'GET':
        return render_template('home_js.html')
    else:
        latitude = request.form['latitude']
        longitude = request.form['longitude']

        if float(latitude) > 0 and float(longitude) > 0: #Check if Location is allowed
            user_location = (float(latitude), float(longitude))
            cars = Car.query.all()
            #func = lambda car: math.sqrt(((user_location[0] - car.latitude)**2)+((user_location[1] - car.longitude)**2))
            func = lambda car: distance.distance(user_location, (car.latitude, car.longitude)).km
            sorted_cars = sorted(cars,key=func, reverse=False)
            return render_template('home.html', title = "Home", cars = sorted_cars, path = "\\static\\carImages\\")

        else:
            cars = Car.query.all()
            return render_template('home.html', title = "Home", cars = cars, path = "\\static\\carImages\\")


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

        email = User.query.filter_by(email=form.email.data).first()
        if email:
            flash('That email is taken. Choose another one.', 'danger')
            return redirect(url_for('register'))

        # valid username and email
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pass, is_admin = False)
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
            return redirect(url_for('home'))
        
        flash('Login unsuccessful. Please check username and password', 'danger')

    return render_template('login.html', title = "Login", form=form)


#@app.route('/add_car', methods=['GET', 'POST'])
#    return render_template('add_car.html')



#def render_picture(data):

#    render_pic = base64.b64encode(data).decode('ascii') 
#    return render_pic

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def view_profile():
    if request.method == 'GET':
        rental_info = RentalInformation.query.filter_by(user_id=current_user.id).first()
        if rental_info:
            car = Car.query.filter_by(id=rental_info.car_id).first()
            start_coords = (42.69807953619626, 23.321380446073142)
            folium_map = folium.Map(location=start_coords, zoom_start=13)
            tooltip = "Click me!"

            cord1 = [float(item) for item in rental_info.start_location.split(", ")]
            rev1 = nom.reverse(rental_info.start_location)
            popup1 = rev1.address.split(", ")
            marker1 = folium.Marker(
                cord1, popup=popup1[0], tooltip=tooltip
            ).add_to(folium_map)
            
            cord2 = [float(item) for item in rental_info.end_location.split(", ")]
            rev2 = nom.reverse(rental_info.end_location)
            popup2 = rev2.address.split(", ")
            marker2 = folium.Marker(
                cord2, popup=popup2[0], tooltip=tooltip
            ).add_to(folium_map)
            
            coordinates = [cord1, cord2]

            folium.PolyLine(coordinates,
                color='red',
                weight=1,
                opacity=1).add_to(folium_map)  

            folium_map.save(app.root_path + '\\templates\\map.html')

            return render_template('profile.html', rental_info = rental_info, car = car)
        else:
            return render_template('profile.html')

    else:
        pass


@app.route('/add/car', methods=['GET', 'POST'])
@login_required
def add_car():
    if request.method == 'GET':
        if current_user.is_admin == True:
            return render_template('add_car.html', stations = Station.query.all())
        else:
            abort(403)
    else:
        app.config["IMAGE_UPLOADS"] = app.root_path + "\\static\\carImages"
        #flash('path: {app.config["IMAGE_UPLOADS"]}')
        file = request.files['inputFile']
        #image = file.read()
        #render_file = render_picture(image)
        model = request.form['model']
        location = request.form['location']

        station = Station.query.filter_by(id=location).first()
        station.count_cars += 1
        db.session.commit()
        #return str(station is None)
        price = request.form['price']

        newCar = Car(model = model, filename = file.filename, location = station.name,
                                    latitude=station.latitude, longitude=station.longitude, price = price)
        db.session.add(newCar)
        db.session.commit() 
        #flash(f'Pic {newCar.model} uploaded Text: {newCar.rendered_data}')

        file.save(os.path.join(app.config["IMAGE_UPLOADS"], file.filename))

        return redirect(url_for('home'))

@app.route('/show/car/<int:car_id>', methods=['GET', 'POST'])
@login_required
def show_car(car_id):
    if request.method == 'GET':
        car = Car.query.get(car_id)
        rent = RentalInformation.query.filter_by(car_id=car_id).first()
        start_coords = (car.latitude, car.longitude)
        folium_map = folium.Map(location=start_coords, zoom_start=15)
        tooltip = "Click me!"   
        folium.Marker([car.latitude, car.longitude], popup=car.model, tooltip=tooltip).add_to(folium_map)
        folium_map.save(app.root_path + '\\templates\\map.html')
        return render_template('show_car.html', car=car, path = "\\static\\carImages\\", rent=rent)

@app.route('/show/car/<int:car_id>/remove', methods=['GET', 'POST'])
@login_required
def remove_car(car_id):
    if request.method == 'GET':
        if current_user.is_admin == True:
            car = Car.query.get_or_404(car_id)
            station = Station.query.filter_by(name=car.location).first()
            station.count_cars -= 1
            db.session.commit()
            app.config["IMAGE_UPLOADS"] = app.root_path + "\\static\\carImages"
            os.remove(os.path.join(app.config['IMAGE_UPLOADS'], car.filename))
            db.session.delete(car)
            db.session.commit()
            flash('This car has been deleted!', 'success')
            return redirect(url_for('home'))
        else:
            abort(403)

@app.route('/carpool', methods=['GET', 'POST'])
@login_required
def carpool():
    form = CarPoolForm()
    if request.method == 'GET':
            return render_template('carpool.html', form=form)
    else:
        startlocation = form.startlocation.data
        geo_start = nom.geocode(startlocation)

        endloctation =  form.endloctation.data
        geo_end = nom.geocode(endloctation)

        starttime = str(form.starttime.data)
        endtime = str(form.endtime.data)

        isdriver =  True if form.isdriver.data == 'yes' else False
            
        # if form.isdriver.data == 'yes':
        #     isdriver = True
        #return str(isdriver)
        #return starttime

        path = Paths(start_location_x = str(geo_start.latitude), start_location_y = str(geo_start.longitude),
        end_location_x = str(geo_end.latitude), end_location_y = str(geo_end.longitude), start_time = starttime, end_time = endtime, user_id=current_user.id
        , is_driver=isdriver)

        db.session.add(path)
        db.session.commit()



        return redirect(url_for('home'))

        #location = form.endloctation.data
        #geo = nom.geocode(location)
        #end_location = (str(geo.latitude) + ", " + str(geo.longitude))
        #rental_info = RentalInformation(start_location=start_location, end_location=end_location, end_time=end_time, start_time = start_time, user_id=current_user.id, car_id=car_id, nearest_station_id=station.id)
        #db.session.add(rental_info)
        #db.session.commit()
        




    

@app.route('/show/car/<int:car_id>/update', methods=['GET', 'POST'])
@login_required
def update(car_id):
    car = Car.query.get_or_404(car_id)
    
    if request.method == 'GET':
        if current_user.is_admin == True:
            return render_template('update_car.html', car=car, stations = Station.query.all())
        else:
            abort(403)
    else:
        #### not sure
        # app.config["IMAGE_UPLOADS"] = app.root_path + "\\static\\carImages"
        #flash('path: {app.config["IMAGE_UPLOADS"]}')
        app.config["IMAGE_UPLOADS"] = app.root_path + "\\static\\carImages"
        #os.remove(os.path.join(app.config['IMAGE_UPLOADS'], car.filename))
        
        file = request.files['inputFile']
        if file.filename != "":
            os.remove(os.path.join(app.config['IMAGE_UPLOADS'], car.filename))  
            car.filename = file.filename
            file.save(os.path.join(app.config["IMAGE_UPLOADS"], file.filename))
        #image = file.read()
        #render_file = render_picture(image)
        car.model = request.form['model']
        location = request.form['location']

        station = Station.query.filter_by(id=location).first()#maybe some check
        car.location = station.name
        car.latitude = station.latitude
        car.longitude = station.longitude

        #return str(station is None)
        car.price = request.form['price']
        #return "Updated"
        db.session.commit()
        flash('This car has been updated', 'success')
        return redirect(url_for('show_car', car_id=car_id))

        #newCar = Car(model = model, filename = file.filename, location = station.name,
         #                           latitude=station.latitude, longitude=station.longitude, price = price)
         ##not sure

@app.route('/show/car/<int:car_id>/rent', methods=['GET', 'POST'])
@login_required
def rent(car_id):
    car = Car.query.get_or_404(car_id)
    form = RentForm()
    if car.status is True:
        abort(403)
    if request.method == 'GET':
        return render_template('rent.html', car=car, form=form)
    else:
        current_user.is_rent = True
        db.session.commit()
        start_location = (str(car.latitude) + ", " + str(car.longitude))
        location = form.endloctation.data
        geo = nom.geocode(location)
        end_location = (str(geo.latitude) + ", " + str(geo.longitude))
        end_time = str(form.endtime.data)
        stations = Station.query.all()
        list_end_location = (float(item) for item in end_location.split(", "))
        func = lambda station: distance.distance(end_location, (station.latitude, station.longitude)).km
        sorted_stations = sorted(stations,key=func, reverse=False)
        station = sorted_stations[0]
        #return str(end_time)
        #return str(type(end_time))
        tz_Sofia = pytz.timezone('Europe/Sofia')
        start_time =  datetime.now(tz_Sofia).strftime("%H:%M:%S")
        rental_info = RentalInformation(start_location=start_location, end_location=end_location,
            end_time=end_time, start_time = start_time, user_id=current_user.id, car_id=car_id, nearest_station_id=station.id)
        db.session.add(rental_info)
        db.session.commit()

        car.status = True
        db.session.commit()
        return redirect(url_for('rentinfo'))

@app.route('/rentinfo', methods=['GET', 'POST'])
@login_required
def rentinfo():
    if request.method == 'GET':
        rentinfo = RentalInformation.query.filter_by(user_id = current_user.id).first()
        if rentinfo is None:
            abort(403)
        car = Car.query.filter_by(id = rentinfo.car_id).first()
        station = Station.query.filter_by(id = rentinfo.nearest_station_id).first()

        #Map
        start_coords = [float(item) for item in rentinfo.start_location.split(", ")]
        folium_map = folium.Map(location=start_coords, zoom_start=15)
        tooltip = "Click me!"
        #marksers
        cord1 = [float(item) for item in rentinfo.start_location.split(", ")]
        rev1 = nom.reverse(rentinfo.start_location)
        popup1 = rev1.address.split(", ")
        marker1 = folium.Marker(
            cord1, popup=popup1[0], tooltip=tooltip, icon=folium.Icon(color='green', icon = "map-marker", prefix='fa')
        ).add_to(folium_map)
            
        cord2 = [float(item) for item in rentinfo.end_location.split(", ")]
        rev2 = nom.reverse(rentinfo.end_location)
        popup2 = rev2.address.split(", ")
        marker2 = folium.Marker(
            cord2, popup=popup2[0], tooltip=tooltip, icon=folium.Icon(color='blue', icon = "location-arrow", prefix='fa')
        ).add_to(folium_map)
        
        cord3 = [station.latitude, station.longitude]
        listToStr = ' '.join([str(elem) for elem in cord3])
        rev3 = nom.reverse(listToStr)
        popup3 = rev3.address.split(", ")
        marker3 = folium.Marker(
            cord3, popup=popup3[0], tooltip=tooltip, icon=folium.Icon(color='black', icon = "flag-checkered", prefix='fa')
        ).add_to(folium_map)

        coordinates1 = [cord1, cord2]
        coordinates2 = [cord2, cord3]

        folium.PolyLine(coordinates1,
            color='red',
            weight=1,
            opacity=1).add_to(folium_map)

        folium.PolyLine(coordinates2,
            color='red',
            weight=1,
            opacity=1).add_to(folium_map)  

        folium_map.save(app.root_path + '\\templates\\map.html')

        return render_template('rent_car.html', rentinfo=rentinfo, car=car, path = "\\static\\carImages\\", station = station )

@app.route('/paths', methods=['GET', 'POST'])
@login_required
def paths():
    path = Paths.query.filter_by(user_id=current_user.id).first()
    #return str(path.id)
    if path is None:
        abort(403)

    # #Map
    # start_coords = [float(item) for item in path.start_location.split(", ")]
    start_coords = [float(path.start_location_x), float(path.start_location_y)]
    folium_map = folium.Map(location=start_coords, zoom_start=15)
    tooltip = "Click me!"

    #Other paths
    other_paths = Paths.query.all()
    for other_path in other_paths:
        if other_path.id != path.id:
            user = User.query.filter_by(id=other_path.user_id).first()
            #marksers
            #cord1 = [float(item) for item in rentinfo.start_location.split(", ")]
            cord1 = [float(other_path.start_location_x), float(other_path.start_location_y)]

            rev1 = nom.reverse(other_path.start_location_x + ', ' + other_path.start_location_y)
            
            popup1 = rev1.address.split(", ")
            marker1 = folium.Marker(
                cord1, popup=popup1[0], tooltip=user.username, icon=folium.Icon(color='blue', icon = "map-marker", prefix='fa')
            ).add_to(folium_map)
                
            # cord2 = [float(item) for item in rentinfo.end_location.split(", ")]
            cord2 = [float(other_path.end_location_x), float(other_path.end_location_y)]
            rev2 = nom.reverse(other_path.end_location_x + ', ' + other_path.end_location_y)
            popup2 = rev2.address.split(", ")
            marker2 = folium.Marker(
                cord2, popup=popup2[0], tooltip=user.username, icon=folium.Icon(color='blue', icon = "location-arrow", prefix='fa')
            ).add_to(folium_map)
            

            coordinates = [cord1, cord2]

            folium.PolyLine(coordinates,
                color='blue',
                weight=10,
                opacity=1).add_to(folium_map)
            

    #Waypoints
    waypoints = Waypoints.query.filter_by(path_id=path.id).all()
    waypoints_count = Waypoints.query.filter_by(path_id=path.id).count
    for waypoint in waypoints:
        cord = [float(waypoint.location_x), float(waypoint.location_y)]
        rev = nom.reverse(waypoint.location_x + ', ' + waypoint.location_y)
        popup = rev.address.split(", ")
        marker = folium.Marker(
        cord, popup=popup[0], tooltip=tooltip, icon=folium.Icon(color='green', icon = "road", prefix='fa')
        ).add_to(folium_map)
    #marksers
    #cord1 = [float(item) for item in rentinfo.start_location.split(", ")]
    cord1 = [float(path.start_location_x), float(path.start_location_y)]

    rev1 = nom.reverse(path.start_location_x + ', ' + path.start_location_y)
    
    popup1 = rev1.address.split(", ")
    marker1 = folium.Marker(
        cord1, popup=popup1[0], tooltip=tooltip, icon=folium.Icon(color='green', icon = "map-marker", prefix='fa')
    ).add_to(folium_map)
        
    # cord2 = [float(item) for item in rentinfo.end_location.split(", ")]
    cord2 = [float(path.end_location_x), float(path.end_location_y)]
    rev2 = nom.reverse(path.end_location_x + ', ' + path.end_location_y)
    popup2 = rev2.address.split(", ")
    marker2 = folium.Marker(
        cord2, popup=popup2[0], tooltip=tooltip, icon=folium.Icon(color='green', icon = "location-arrow", prefix='fa')
    ).add_to(folium_map)
    
    #cord3 = [station.latitude, station.longitude]
    #listToStr = ' '.join([str(elem) for elem in cord3])
    #rev3 = nom.reverse(listToStr)
    # popup3 = rev3.address.split(", ")
    # marker3 = folium.Marker(
    #     cord3, popup=popup3[0], tooltip=tooltip, icon=folium.Icon(color='black', icon = "flag-checkered", prefix='fa')
    # ).add_to(folium_map)

    coordinates1 = [cord1, cord2]
    #coordinates2 = [cord2, cord3]

    folium.PolyLine(coordinates1,
        color='green',
        weight=10,
        opacity=1).add_to(folium_map)

    # folium.PolyLine(coordinates2,
    #     color='red',
    #     weight=1,
    #     opacity=1).add_to(folium_map)  

    folium_map.save(app.root_path + '\\templates\\map.html')

    our_path_start_time =  datetime.strptime(path.start_time, '%Y-%m-%d %H:%M:%S')
    our_path_end_time =  datetime.strptime(path.end_time, '%Y-%m-%d %H:%M:%S')
    
    for curr_path in other_paths:
        curr_path_start_time = datetime.strptime(curr_path.start_time, '%Y-%m-%d %H:%M:%S')
        return str(our_path_start_time)


    return render_template('paths.html', path=path)

@app.route('/paths/<int:path_id>/add_waypoint', methods=['GET', 'POST'])
@login_required
def add_waypoint(path_id):

    form = WaypointForm()
    if request.method == 'GET': 
        return render_template('adding_waypoint.html', form=form)

    location = form.location.data
    geo_start = nom.geocode(location)

    waypoint = Waypoints(location_x = str(geo_start.latitude), location_y = str(geo_start.longitude),
     path_id= path_id)

    db.session.add(waypoint)
    db.session.commit()
    return redirect(url_for('paths'))
    



@app.route('/show/car/<int:car_id>/abandon', methods=['GET', 'POST'])
@login_required
def abandon(car_id):
    rental_info = RentalInformation.query.filter_by(car_id=car_id).first()
    if rental_info.user_id == current_user.id:
        car = Car.query.get_or_404(car_id)
        end_station = Station.query.filter_by(id = rental_info.nearest_station_id).first()
        start_station = Station.query.filter_by(name = car.location).first()
        start_station.count_cars -= 1
        end_station.count_cars +=1
        db.session.commit()
        car.location = end_station.name
        car.latitude = end_station.latitude
        car.longitude = end_station.longitude
        db.session.commit()
        current_user.is_rent = False
        db.session.commit()
        db.session.delete(rental_info)
        db.session.commit()
        car.status = False
        db.session.commit()
        return redirect(url_for('home'))
    else:
        abort(403) 
    
    
@app.route('/add/station', methods=['GET', 'POST'])
@login_required
def add_station():
    if request.method == 'GET':
        if current_user.is_admin == True:
            return render_template('add_station.html')
        else:
            abort(403)
    else:

        location = request.form['location']
        #nom = Nominatim(user_agent="CarsRental")
        geo = nom.geocode(location)
        name = request.form['name']

        if geo is None:
            flash("Couldn't find location with this name", 'danger')
            return redirect('/add/station')
        
        newStation = Station(location = location, name = name, latitude = geo.latitude, longitude = geo.longitude)
        db.session.add(newStation)
        db.session.commit()

        return redirect(url_for('show_map'))

@app.route('/stations/<int:station_id>/remove', methods=['GET', 'POST'])
@login_required
def remove_station(station_id):
    if current_user.is_admin == True:
        station = Station.query.get_or_404(station_id)
        db.session.delete(station)
        db.session.commit()
        return redirect(url_for('show_map'))
    else:
        abort(403)

# Testing maps
@app.route('/stations')
def show_map():
    start_coords = (42.69807953619626, 23.321380446073142)
    folium_map = folium.Map(location=start_coords, zoom_start=13)
    tooltip = "Click me!"   

    stations = Station.query.all()
    for station in stations:
        folium.Marker(
            [station.latitude, station.longitude], popup=station.name, tooltip=tooltip, icon=folium.Icon(color='red', icon = "circle", prefix='fa')
        ).add_to(folium_map)
    folium_map.save(app.root_path + '\\templates\\map.html')
    return render_template('stations.html', stations=stations, car=Car.query)
    #folium_map._repr_html_()


@app.route('/map')
def map():
    return render_template('map.html')

