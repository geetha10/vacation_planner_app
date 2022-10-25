from hashlib import new
import uuid
from vacation_planner_app import app
from flask import redirect,render_template, session, request, url_for,flash
from vacation_planner_app.models.place import Place
from vacation_planner_app.models.trip import Trip
from vacation_planner_app.service.places_api import Places_api
from collections import defaultdict
from pprint import pprint
import random
import pickle

@app.route('/plan_new_trip')
def save_trip():
    return render_template("new_trip_form.html")

@app.route('/plan_trip',methods=['post'])
def plan_trip():
    if not Trip.validate_trip(request.form):
        return redirect('/plan_new_trip')

    session['uuid']=uuid.uuid4()
    places_api=Places_api()

    data={
        'trip_id':session['uuid'],
        "name":request.form['state']+' Trip',
        'city' : request.form['city'],
        'image_url': places_api.get_city_photo(request.form['city']),
        'start_date':request.form['start_date'],
        'end_date':request.form['end_date'],
        'user_id':session['user_id']
    }
    
    Trip.save_trip(data)
    address =request.form['city']+","+request.form['state']

    intrests=[request.form['places_of_interest1'], request.form['places_of_interest2']]
    places = defaultdict(list)
    for idx, interest in enumerate(intrests):
        list_of_places = places_api.get_places(address, interest, 20)
        
        for item in list_of_places:
            data={
                'place_name':item['name'],
                'place_id':item['place_id'],
                'image_url': '',
                'rating':item['rating'],
                'start_time':'09:00:00',
                'end_time':'11:00:00',
                'trip_id':session['uuid']
            }

            places[idx].append(Place(data))

    shortlisted = []
    shortlisted.extend(random.sample(places[0], 5))
    shortlisted.extend(random.sample(places[1], 4))
    random.shuffle(shortlisted)

    plans = defaultdict(list)
    times = [('09:00:00', '11:00:00'), ('13:00:00', '16:00:00'), ('19:00:00', '20:00:00')]

    for i in range(3):
        planned_places = shortlisted[3*i:3*i+3]
        for time, place in zip(times, planned_places):
            place.start_time = time[0]
            place.end_time = time[1]
            place.image_url = places_api.get_place_photo(place.place_id)
        
        plans[i].extend(planned_places)


    session['plans']=pickle.dumps(plans)
    return render_template("render_generated_plan.html",plans=list(plans.values()))

@app.route('/save_plan/<int:num>')
def save_plan(num):
    places_api=Places_api()
    plans = pickle.loads(session['plans'])
    
    selected_plan=plans[num]
    for place in selected_plan:
        
        data={
            'place_name':place.place_name,
            'image_url': place.image_url,
            'place_id':place.place_id,
            'rating':place.rating,
            'start_time':place.start_time,
            'end_time':place.end_time,
            'trip_id':session['uuid']
        }
        Place.save_place(data)
    return redirect('/dashboard')

@app.route("/view_plan/<trip_id>")
def view_plan(trip_id):
    print(f"Trip_id is {trip_id}")
    data={
        'trip_id':trip_id
    }
    places=Place.get_places(data)
    print(places)
    return render_template('show_plan.html',places=places)