import json
from geopy.geocoders import Nominatim

def get_json():
    json_file = open('website/static/json_files/suggestions.json')

    data = json.load(json_file)

    # for continent in data:
    #     for trip in data[continent]:
    #         print(trip + ": " + data[continent][trip])
    return data

def ret_location(location):
    geolocator = Nominatim(user_agent="geoapiExercises")
    address=geolocator.geocode(location)
    ret = []
    ret.append(address.latitude)
    ret.append(address.longitude)
    return ret