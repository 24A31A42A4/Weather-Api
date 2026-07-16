from geopy.geocoders import Nominatim

def get_location(city_name):
    geolocator = Nominatim(user_agent="my_coordinate_finder_application")
    location = geolocator.geocode(city_name)
    return location
