from vacation_planner_app import app
from vacation_planner_app.controllers import trips
from flask import redirect,render_template, session, request, url_for,flash
from flask_bcrypt import Bcrypt
import uuid
from vacation_planner_app.models.trip import Trip
from vacation_planner_app.models.user import User
bcrypt = Bcrypt(app)

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/login_validation', methods=['POST'])
def login_validation():
    user = User.get_by_email(request.form)
    if not user:
        flash("Invalid Email","login")
        return redirect('/welcome')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/welcome')
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/register_user')
def register_user():
    return render_template('registration.html')

@app.route('/register', methods=['post'])
def register():
    if not User.validate_form(request.form):
        return redirect('/register_user')
    print("Validated Registration form")
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id'] = id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    print("")
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'user_id': session['user_id']
    }
    past_trips=Trip.get_past_trips(data);
    upcoming_trips=Trip.get_upcoming_trips(data);
    return render_template("dashboard.html",user=User.get_by_id(data),past_trips=past_trips,upcoming_trips=upcoming_trips)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/welcome')

