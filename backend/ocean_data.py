# Makes an API call and returns the ocean data 
# Template from: https://open-meteo.com/en/docs/marine-weather-api#current=wave_height,wave_direction,wave_period&hourly=&daily=&location_mode=csv_coordinates&length_unit=imperial&timezone=America%2FLos_Angeles&forecast_days=1

import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry

def ocean_information(lat, long, decimal):
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://marine-api.open-meteo.com/v1/marine"
    params = {
        "latitude": lat,
        "longitude": long,
        "current": ["wave_height", "wave_direction", "wave_period"],
        "length_unit": "imperial",
        "timezone": "America/Los_Angeles",
        "forecast_days": 1
    }
    try:
        responses = openmeteo.weather_api(url, params=params)
    except:
        return ["No data. Please be more exact or enter a nearby location", 0, 0]

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    # print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    # print(f"Elevation {response.Elevation()} m asl")
    # print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    # print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    # Current values. The order of variables needs to be the same as requested.
    current = response.Current()
    current_wave_height = round(current.Variables(0).Value(), decimal)
    current_wave_direction = round(current.Variables(1).Value(), decimal)
    current_wave_period = round(current.Variables(2).Value(), decimal)

    # print(f"Current time {current.Time(``)}")

    return [current_wave_height, current_wave_direction, current_wave_period]

