from vacation_planner_app import gmaps_client, API_KEY
import pprint
import json

from vacation_planner_app.models.place import Place

class Places_api:

    def miles_to_meters(self,miles):
        try:
            return miles * 1_609.344
        except:
            return 0

    def get_geocode(self,address):
        geocode=gmaps_client.geocode(address=address)
        (lat, lng) = map(geocode[0]['geometry']['location'].get,('lat', 'lng'))
        return (lat,lng)

    def get_places(self,address,keyword,distance):
        places=[]
        radius=self.miles_to_meters(distance)
        (lat,lng)= self.get_geocode(address)
        response=gmaps_client.places_nearby(location=(lat, lng),keyword=keyword,radius=radius)
        
        for place in response['results']:
            data={
                    'name':place['name'],
                    'place_id':place['place_id'],
                    'price_level': place.get('price_level','N/A'),
                    'rating': place.get('rating','N/A')
                }
        
            places.append(data)
        
        return places

    def get_place_photo(self, place_id):
        final_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Google_Maps_pin.svg/274px-Google_Maps_pin.svg.png"

        place_details = gmaps_client.place(place_id=place_id)
        place_photos = place_details['result'].get('photos')
        if place_photos:
            photo_reference = place_photos[0]['photo_reference']
            final_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={API_KEY}"
        else:
            print(f"Place photos not fond for {place_details}")
        return final_url

    def get_city_photo(self, city_name):
        city_placeid = self._get_city_placeid(city_name)
        return self.get_place_photo(city_placeid)
        
    def _get_city_placeid(self, place_name):
        autocomplete_results = gmaps_client.places_autocomplete(input_text=place_name)
        return autocomplete_results[0]['place_id']
