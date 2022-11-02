from geopy.geocoders import Nominatim

def ret_location(location):
    geolocator = Nominatim(user_agent="geoapiExercises")
    address=geolocator.geocode(location)
    ret = []
    ret.append(address.latitude)
    ret.append(address.longitude)
    return ret
