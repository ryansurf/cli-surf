# Takes a location(city or address) and returns the coordinates: [lat, long]

from geopy.geocoders import Nominatim

def get_cordinates(address):
    geolocator = Nominatim(user_agent="ryansurf")
    location = geolocator.geocode(address)
    return[location.latitude, location.longitude]
