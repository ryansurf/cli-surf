"""
Functions that make API calls stored here
"""

from http import HTTPStatus

import openmeteo_requests
import pandas as pd
import requests
import requests_cache
from geopy.geocoders import Nominatim
from retry_requests import retry

from src import helper


def get_coordinates(args):
    """
    Takes a location(city or address) and returns the coordinates: [lat, long]
    If no location is specified, default_location() finds the users coordinates
    """
    for arg in args:
        arg_str = str(arg)
        if arg_str.startswith("location=") or arg_str.startswith("loc="):
            address = arg.split("=")[1]
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

    if response.status_code == HTTPStatus.OK:
        data = response.json()
        location = data["loc"].split(",")
        lat = location[0]
        long = location[1]
        city = data["city"]
        return [lat, long, city]
    return "No data"


def get_uv(lat, long, decimal, unit="imperial"):
    """
    Get UV at coordinates (lat, long)
    Calling the API here: https://open-meteo.com/en/docs
    """
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = {
        "latitude": lat,
        "longitude": long,
        "length_unit": unit,
        "current": "uv_index",
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
    API: https://open-meteo.com/en/docs/marine-weather-api
    """
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://marine-api.open-meteo.com/v1/marine"
    params = {
        "latitude": lat,
        "longitude": long,
        "current": ["wave_height", "wave_direction", "wave_period"],
        "length_unit": unit,
        "timezone": "auto",
        "forecast_days": 3,
    }
    try:
        responses = openmeteo.weather_api(url, params=params)
    except ValueError:
        return "No data"

    # Process first location.
    # Add a for-loop for multiple locations or weather models
    response = responses[0]

    # Current values. The order of variables needs to be the same as requested.
    current = response.Current()
    current_wave_height = round(current.Variables(0).Value(), decimal)
    current_wave_direction = round(current.Variables(1).Value(), decimal)
    current_wave_period = round(current.Variables(2).Value(), decimal)

    # print(f"Current time {current.Time(``)}")

    return [current_wave_height, current_wave_direction, current_wave_period]

def current_wind_temp(lat, long, decimal, temp_unit="fahrenheit"):
    """
    Gathers the wind and temperature data
    """
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": long,
        "current": ["temperature_2m", "wind_speed_10m", "wind_direction_10m"],
        "temperature_unit": temp_unit,
        "wind_speed_unit": "mph",
        "precipitation_unit": "inch"
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]

    # Current values. The order of variables needs to be the same as requested.
    current = response.Current()
    current_temperature = round(
        current.Variables(0).Value(), decimal)
    current_wind_speed = round(
        current.Variables(1).Value(), decimal)
    current_wind_direction = round(
        current.Variables(2).Value(), decimal)

    return current_temperature, current_wind_speed, current_wind_direction


def forecast(lat, long, decimal, days=0):
    """
    Number of forecast days. Max is 7
    API: https://open-meteo.com/en/docs/marine-weather-api
    """
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://marine-api.open-meteo.com/v1/marine"
    params = {
        "latitude": lat,
        "longitude": long,
        "daily": [
            "wave_height_max",
            "wave_direction_dominant",
            "wave_period_max",
        ],
        "length_unit": "imperial",
        "timezone": "auto",
        "forecast_days": days,
    }
    responses = openmeteo.weather_api(url, params=params)

    response = responses[0]

    daily_height_max = helper.round_decimal(
        response.Daily().Variables(0).ValuesAsNumpy(), decimal
    )
    daily_direction_dominant = helper.round_decimal(
        response.Daily().Variables(1).ValuesAsNumpy(), decimal
    )
    daily_period_max = helper.round_decimal(
        response.Daily().Variables(2).ValuesAsNumpy(), decimal
    )

    daily_data = {
        "date": pd.date_range(
            start=pd.to_datetime(response.Daily().Time(), unit="s", utc=True),
            end=pd.to_datetime(response.Daily().TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=response.Daily().Interval()),
            inclusive="left",
        )
    }

    return [
        daily_height_max,
        daily_direction_dominant,
        daily_period_max,
        daily_data["date"],
    ]


def gather_data(lat, long, arguments):
    """
    Calls APIs though python files,
    returns all the ocean data(height, period...)
    in a dictionary (ocean_data_dict)
    """
    lat, long = float(lat), float(long)
    ocean_data = ocean_information(
        lat, long, arguments["decimal"], arguments["unit"]
    )
    uv_index = get_uv(lat, long, arguments["decimal"], arguments["unit"])

    wind_temp = current_wind_temp(lat, long, arguments["decimal"])
    air_temp, wind_speed, wind_dir = wind_temp[0], wind_temp[1], wind_temp[2]

    arguments["ocean_data"] = ocean_data
    arguments["uv_index"] = uv_index
    spot_forecast = forecast(lat, long, arguments["decimal"], 7)
    json_forecast = helper.forecast_to_json(
        spot_forecast, arguments["decimal"]
    )

    ocean_data_dict = {
        "Lat": lat,
        "Long": long,
        "Location": arguments["city"],
        "Height": ocean_data[0],
        "Swell Direction": ocean_data[1],
        "Period": ocean_data[2],
        "UV Index": uv_index,
        "Air Temperature": air_temp,
        "Wind Speed": wind_speed,
        "Wind Direction": wind_dir,
        "Forecast": json_forecast,
        "Unit": arguments["unit"],
    }
    return ocean_data_dict


def seperate_args_and_get_location(args):
    """
    Gets user's coordinates from either
    the argument(location=) or, if none,
    the default coordinates(default_location())
    """
    coordinates = get_coordinates(args)
    location_data = {
        "coordinates": coordinates,
        "lat": coordinates[0],
        "long": coordinates[1],
        "city": coordinates[2],
    }
    return location_data
