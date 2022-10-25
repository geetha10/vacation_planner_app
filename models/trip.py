from vacation_planner_app.config import mysqlconnection
from vacation_planner_app import DATA_BASE
from flask import flash
import datetime



class Trip:
    def __init__(self,data): 
        self.name = data['name']
        self.trip_id = data['trip_id']
        self.city = data['city']
        self.image_url = data['image_url']
        self.start_date = data['start_date']
        self.end_date= data['end_date']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.user_id=data['user_id']

    @classmethod
    def save_trip(cls,data):
        print(data)
        query = """INSERT INTO trips_info (name,trip_id,city,image_url,start_date,end_date,user_id) 
        VALUES(%(name)s,%(trip_id)s,%(city)s,%(image_url)s,%(start_date)s,%(end_date)s,%(user_id)s);"""
        return mysqlconnection.connectToMySQL(DATA_BASE).query_db(query,data)

    @classmethod
    def get_past_trips(cls,data):
        print(f"data: {data}")
        query = "SELECT * FROM trips_info WHERE user_id=%(user_id)s AND end_date < now();"
        results = mysqlconnection.connectToMySQL(DATA_BASE).query_db(query,data)
        trips = []
        for trip in results:
            trips.append( cls(trip))
        return trips

    @classmethod
    def get_upcoming_trips(cls,data):
        query = "SELECT * FROM trips_info WHERE user_id = %(user_id)s AND start_date > now();"
        results = mysqlconnection.connectToMySQL(DATA_BASE).query_db(query,data)
        trips = []
        for trip in results:
            trips.append( cls(trip))
        return trips

    @staticmethod
    def validate_trip(data):
        is_valid = True
        if len(data['city']) < 3:
            flash("City name must be at least 3 characters","new_trip")
            is_valid= False
        if len(data['state']) < 2:
            flash("State name must be at least 2 characters","new_trip")
            is_valid= False
        start_date =""
        end_date =""
        if data['end_date'] == '' or data['start_date'] == '':
            flash("Start or End Date cannot be empty","new_trip")
            is_valid= False
        else:
            format = '%Y-%m-%d'
            start_date =datetime.datetime.strptime(data['start_date'],format)
            print("start Date", start_date)
            end_date =datetime.datetime.strptime(data['end_date'],format)
            print("End Date", end_date)
        if start_date > end_date:
            flash("End date should be greater than start date","new_trip")
            is_valid= False
        return is_valid