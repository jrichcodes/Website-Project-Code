import json
from geopy.geocoders import Nominatim

def get_json():
    json_file = open('website/static/json_files/suggestions.json')

    data = json.load(json_file)

    # for continent in data:
    #     for trip in data[continent]:
    #         print(trip + ": " + data[continent][trip])
    return data

import requests, json


def ret_location(location):
    name_list = location.split()

    formatted_name = "%20".join(name_list)


    path = 'https://api.opencagedata.com/geocode/v1/json?q=' + formatted_name + '&key=03c48dae07364cabb7f121d8c1519492'

    req = requests.get(path,headers={"User-Agent":"Mozilla/5.0"})

    response_info = json.loads(req.text)

    #print(response_info['geometry']['lat'])

    lat = response_info['results'][0]['geometry']['lat']
    long = response_info['results'][0]['geometry']['lng']

    ret = []
    ret.append(lat)
    ret.append(long)

    return ret

def get_recipes():
    json_file = open('website/static/json_files/recipes.json')
    data = json.load(json_file)
    return data
