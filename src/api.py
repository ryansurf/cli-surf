"""
Functions that make API calls stored here
"""

from geopy.geocoders import Nominatim
import openmeteo_requests
import requests_cache
from retry_requests import retry
import requests
import pandas as pd
from helper import round_decimal


def get_coordinates(args):
    """
    Takes a location(city or address) and returns the coordinates: [lat, long]
    If no location is specified, default_location() finds the users coordinates
    """
    for arg in args:
        arg = str(arg)
        if arg.startswith("location=") or arg.startswith("loc=") :
            address = arg.split('=')[1]
            geolocator = Nominatim(user_agent="cli-surf")
            location = geolocator.geocode(address)
            if location is not None:
                return [location.latitude, location.longitude, location]
            return "No data"
    return default_location()

def default_location():
    """
    If no location specified in cli, find users location
    Make a GET request to the API endpoint
    """
    response = requests.get("https://ipinfo.io/json", timeout=10)

    if response.status_code == 200:
        data = response.json()
        location = data['loc'].split(',')
        lat = location[0]
        long = location[1]
        city = data['city']
        return [lat, long, city]
    return "No data"

def get_uv(lat, long, decimal, unit="imperial"):
    """
    Get UV at coordinates
    """
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = {
        "latitude": lat,
        "longitude": long,
        "length_unit": unit,
        "current": "uv_index"
    }
    try:
        responses = openmeteo.weather_api(url, params=params)
    except ValueError:
        return "No data"

    response = responses[0]

    # Current values. The order of variables needs to be the same as requested.
    current = response.Current()
    current_uv_index = round(current.Variables(0).Value(), decimal)

    return current_uv_index

def ocean_information(lat, long, decimal, unit="imperial"):
    """
    Get Ocean Data at coordinates
    """
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    url = "https://marine-api.open-meteo.com/v1/marine"
    params = {
        "latitude": lat,
        "longitude": long,
        "current": ["wave_height", "wave_direction", "wave_period"],
        "length_unit": unit,
        "timezone": "auto",
        "forecast_days": 3
    }
    try:
        responses = openmeteo.weather_api(url, params=params)
    except ValueError:
        return "No data"

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]

    # Current values. The order of variables needs to be the same as requested.
    current = response.Current()
    current_wave_height = round(current.Variables(0).Value(), decimal)
    current_wave_direction = round(current.Variables(1).Value(), decimal)
    current_wave_period = round(current.Variables(2).Value(), decimal)

    # print(f"Current time {current.Time(``)}")

    return [current_wave_height, current_wave_direction, current_wave_period]


def forecast(lat, long, decimal, days=0):
    """
    Number of forecast days. Max is 7
    """
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    url = "https://marine-api.open-meteo.com/v1/marine"
    params = {
        "latitude": lat,
        "longitude": long,
        "daily": ["wave_height_max", "wave_direction_dominant", "wave_period_max"],
        "length_unit": "imperial",
        "timezone": "auto",
        "forecast_days": days
    }
    responses = openmeteo.weather_api(url, params=params)

    response = responses[0]

    daily_height_max = round_decimal(response.Daily().Variables(0).ValuesAsNumpy(), decimal)
    daily_direction_dominant = round_decimal(response.Daily().Variables(1).ValuesAsNumpy(), decimal)
    daily_period_max = round_decimal(response.Daily().Variables(2).ValuesAsNumpy(), decimal)

    daily_data = {"date": pd.date_range(
        start = pd.to_datetime(response.Daily().Time(), unit = "s", utc = True),
        end = pd.to_datetime(response.Daily().TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = response.Daily().Interval()),
        inclusive = "left"
    )}

    return [daily_height_max, daily_direction_dominant, daily_period_max, daily_data['date']]
