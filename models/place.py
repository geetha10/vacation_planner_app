import imp

from flask import appcontext_popped, redirect
from vacation_planner_app.config import mysqlconnection
from vacation_planner_app import DATA_BASE

class Place:

    def __init__(self,data) :
        # self.id = data['id']
        self.place_name = data['place_name']
        self.place_id = data['place_id']
        self.rating = data['rating']
        self.image_url = data['image_url']
        self.start_time= data['start_time']
        self.end_time=data['end_time']
        # self.created_at=data['created_at']
        # self.updated_at=data['updated_at']
        self.trip_id=data['trip_id']    

    @classmethod
    def save_place(cls,data):
        query = "INSERT INTO places_visited (place_name,place_id,rating,image_url,start_time,end_time,trip_id) VALUES(%(place_name)s,%(place_id)s,%(rating)s,%(image_url)s,%(start_time)s,%(end_time)s,%(trip_id)s);"
        return mysqlconnection.connectToMySQL(DATA_BASE).query_db(query,data)

    @classmethod
    def get_places(cls,data):
        query = "SELECT * FROM places_visited where trip_id=%(trip_id)s;"
        return mysqlconnection.connectToMySQL(DATA_BASE).query_db(query,data)

    def __repr__(self) -> str:
        return f"Image url for {self.place_name} is {self.image_url}"


