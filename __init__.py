from flask import Flask
import googlemaps

app = Flask(__name__)
app.secret_key = "shhhhhh"
API_KEY = 'AIzaSyA5w1VryGlvj1fcg-rZkI2PEM7oLEQW_OM'
gmaps_client = googlemaps.Client(key = API_KEY)
DATA_BASE = "vacations_db"