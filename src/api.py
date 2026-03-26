"""
Functions that make API calls stored here
"""

import logging
from datetime import datetime, timedelta
from http import HTTPStatus

from functools import lru_cache

import numpy as np
import openmeteo_requests
import pandas as pd
import requests
import requests_cache
from geopy.geocoders import Nominatim
from retry_requests import retry

from src import helper

logger = logging.getLogger(__name__)

testing = 1


def _create_openmeteo_client():
    """Creates a cached, retry-enabled Open-Meteo API client."""
    cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    return openmeteo_requests.Client(session=retry_session)

@lru_cache(maxsize=128)
def get_coordinates(args):
    """
    Takes a location (city or address) and returns the coordinates: [lat, long]
    If no location is specified or the location is invalid, default_location()
    finds the user's coordinates.
    """
    for arg in args:
        arg_str = str(arg)
        if arg_str.startswith("location=") or arg_str.startswith("loc="):
            address = arg.split("=")[1]
            geolocator = Nominatim(user_agent="cli-surf")
            location = geolocator.geocode(address)
            if location is not None:
                return [
                    location.latitude,
                    location.longitude,
                    location.raw["name"],
                ]
            else:
                logger.warning(
                    "Invalid location '%s' provided. Using default location.",
                    address,
                )
                return default_location()
    return default_location()


def default_location():
    """
    If no location specified in cli, find user's location
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
    openmeteo = _create_openmeteo_client()

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


def get_uv_history(lat, long, decimal, unit="imperial"):
    """
    Retrieve the UV index from one year ago for specified coordinates.

    This function accesses the Open-Meteo API to fetch the hourly UV index
    for the given latitude and longitude. It formats the result based on the
    specified decimal precision.

    Args:
        lat (float): Latitude of the location.
        long (float): Longitude of the location.
        decimal (int): Number of decimal places to round the output.
        unit (str): Unit of measurement ('imperial' or 'metric').
        Defaults to 'imperial'.

    Returns:
        str: The historical UV index rounded to the specified decimal places,
              or an error message if no data is found.

    API Documentation:
    https://open-meteo.com/en/docs/air-quality-api
    """
    openmeteo = _create_openmeteo_client()

    # Calculate the date one year ago and the current hour
    one_year_ago = datetime.now() - timedelta(days=365)
    formatted_date_one_year_ago = one_year_ago.strftime("%Y-%m-%d")
    current_hour = one_year_ago.hour

    # Define the API request parameters
    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = {
        "latitude": lat,
        "longitude": long,
        "length_unit": unit,
        "hourly": ["uv_index"],
        "start_date": formatted_date_one_year_ago,
        "end_date": formatted_date_one_year_ago,
        "timezone": "auto",
    }

    # For testing purposes if testing equals 1 it will continue
    if testing == 1:
        # Attempt to fetch the UV index data from the API
        try:
            responses = openmeteo.weather_api(url, params=params)

        except ValueError:
            return "No data"

        # Process the first response (assuming a single location)
        response = responses[0]

        # Extract hourly UV index values
        hourly = response.Hourly()
        hourly_uv_index = hourly.Variables(0).ValuesAsNumpy()

    else:
        hourly_uv_index = [0.5678] * 24

    # Retrieve the UV index for the current hour from one year ago
    historical_uv_index = hourly_uv_index[current_hour]

    # Format the result to the specified decimal precision
    return f"{historical_uv_index:.{decimal}f}"


def ocean_information(lat, long, decimal, unit="imperial"):
    """
    Get Ocean Data at coordinates
    API: https://open-meteo.com/en/docs/marine-weather-api
    """
    openmeteo = _create_openmeteo_client()

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

    return [current_wave_height, current_wave_direction, current_wave_period]


def ocean_information_history(lat, long, decimal, unit="imperial"):
    """
    Retrieve ocean data from one year ago for specified coordinates.

    This function accesses the Open-Meteo API to fetch
    hourly ocean data including wave height,
    direction, and period for the specified latitude
    and longitude. It formats the results based on the
    specified decimal precision.

    Args:
        lat (float): Latitude of the location.
        long (float): Longitude of the location.
        decimal (int): Number of decimal places to round the output.
        unit (str): Unit of measurement ('imperial' or 'metric').
                Defaults to 'imperial'.

    Returns:
        list: A list containing the wave height, direction, and period rounded
              to the specified decimal places,
              or an error message if no data is found.

    API Documentation:
    https://open-meteo.com/en/docs/marine-weather-api
    """
    openmeteo = _create_openmeteo_client()

    # Calculate the date and current hour one year ago
    one_year_ago = datetime.now() - timedelta(days=365)
    formatted_date_one_year_ago = one_year_ago.strftime("%Y-%m-%d")
    current_hour = one_year_ago.hour

    # Define the API request parameters
    url = "https://marine-api.open-meteo.com/v1/marine"
    params = {
        "latitude": lat,
        "longitude": long,
        "hourly": ["wave_height", "wave_direction", "wave_period"],
        "length_unit": unit,
        "timezone": "auto",
        "start_date": formatted_date_one_year_ago,
        "end_date": formatted_date_one_year_ago,
    }

    # For testing purposes if testing equals 1 it will continue
    if testing == 1:
        # Attempt to fetch the UV index data from the API
        try:
            responses = openmeteo.weather_api(url, params=params)

        except ValueError:
            return "No data"

        # Process the first response (assuming a single location)
        response = responses[0]

        # Extract hourly values for the specified metrics
        hourly = response.Hourly()
        hourly_wave_height = hourly.Variables(0).ValuesAsNumpy()
        hourly_wave_direction = hourly.Variables(1).ValuesAsNumpy()
        hourly_wave_period = hourly.Variables(2).ValuesAsNumpy()

    else:
        hourly_wave_height = [0.5678] * 24
        hourly_wave_direction = [0.5678] * 24
        hourly_wave_period = [0.5678] * 24

    # Retrieve data for the current hour from one year ago
    return [
        f"{hourly_wave_height[current_hour]:.{decimal}f}",
        f"{hourly_wave_direction[current_hour]:.{decimal}f}",
        f"{hourly_wave_period[current_hour]:.{decimal}f}",
    ]


def current_wind_temp(lat, long, decimal, temp_unit="fahrenheit"):
    """
    Gathers the wind and temperature data
    """
    openmeteo = _create_openmeteo_client()

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": long,
        "current": ["temperature_2m", "wind_speed_10m", "wind_direction_10m"],
        "temperature_unit": temp_unit,
        "wind_speed_unit": "mph",
    }
    responses = openmeteo.weather_api(url, params=params)

    response = responses[0]

    # Current values. The order of variables needs to be the same as requested.
    current = response.Current()
    current_temperature = round(current.Variables(0).Value(), decimal)
    current_wind_speed = round(current.Variables(1).Value(), decimal)
    current_wind_direction = round(current.Variables(2).Value(), decimal)

    return [
        current_temperature,
        current_wind_speed,
        current_wind_direction,
    ]


def get_rain(lat, long):
    """
    Get rain data at coordinates (lat, long)
    Calling the API here: https://open-meteo.com/en/docs
    """
    openmeteo = _create_openmeteo_client()

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": long,
        "daily": ["rain_sum", "precipitation_probability_max"],
    }
    responses = openmeteo.weather_api(url, params=params)

    response = responses[0]
    # Process daily data. The order of variables needs to be the
    # same as requested.
    daily = response.Daily()
    daily_rain_sum = daily.Variables(0).ValuesAsNumpy()
    daily_precipitation_probability_max = daily.Variables(1).ValuesAsNumpy()

    return (
        float(daily_rain_sum[0]),
        float(daily_precipitation_probability_max[0]),
    )


def forecast(lat, long, decimal, days=0):
    """
    Number of forecast days. Max is 7
    API: https://open-meteo.com/en/docs/marine-weather-api
    """
    openmeteo = _create_openmeteo_client()

    # First URL is the marine API. Second is for general weather/UV index
    urls = (
        "https://marine-api.open-meteo.com/v1/marine",
        "https://api.open-meteo.com/v1/forecast",
    )
    params_marine = {
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

    params_general = {
        "latitude": lat,
        "longitude": long,
        "daily": [
            "uv_index_max",
            "temperature_2m_max",
            "temperature_2m_min",
            "rain_sum",
            "precipitation_probability_max",
            "wind_speed_10m_max",
            "wind_direction_10m_dominant",
        ],
        "temperature_unit": "fahrenheit",
        "wind_speed_unit": "mph",
        "precipitation_unit": "inch",
        "timezone": "auto",
        "forecast_days": days,
    }

    responses_marine = openmeteo.weather_api(urls[0], params=params_marine)
    responses_general = openmeteo.weather_api(urls[1], params=params_general)

    response_marine = responses_marine[0]
    response_general = responses_general[0]

    # Extract marine data using a loop
    marine_data = [
        helper.round_decimal(
            response_marine.Daily().Variables(i).ValuesAsNumpy(), decimal
        )
        for i in range(3)
    ]

    # Extract general weather data using a loop to reduce number of local
    # variables
    general_data = [
        helper.round_decimal(
            response_general.Daily().Variables(i).ValuesAsNumpy(), decimal
        )
        for i in range(7)
    ]

    daily_data = {
        "date": pd.date_range(
            start=pd.to_datetime(
                response_marine.Daily().Time(), unit="s", utc=True
            ),
            end=pd.to_datetime(
                response_marine.Daily().TimeEnd(), unit="s", utc=True
            ),
            freq=pd.Timedelta(seconds=response_marine.Daily().Interval()),
            inclusive="left",
        )
    }

    forecast_data = {
        "date": daily_data["date"],
        "wave_height_max": marine_data[0],
        "wave_direction_dominant": marine_data[1],
        "wave_period_max": marine_data[2],
        "uv_index_max": general_data[0],
        "temperature_2m_max": general_data[1],
        "temperature_2m_min": general_data[2],
        "rain_sum": general_data[3],
        "precipitation_probability_max": general_data[4],
        "wind_speed_10m_max": general_data[5],
        "wind_direction_10m_dominant": general_data[6],
        "daily_data": daily_data["date"],
    }

    return forecast_data


def get_hourly_forecast(lat, long, days=1, unit="fahrenheit"):
    """
    Gets hourly weather data
    """
    openmeteo = _create_openmeteo_client()

    # The order of variables in hourly or daily is important
    # to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": long,
        "hourly": ["cloud_cover", "visibility"],
        "temperature_unit": unit,
        "wind_speed_unit": "mph",
        "precipitation_unit": "inch",
        "forecast_days": days,
    }

    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]

    hourly = response.Hourly()
    hourly_cloud_cover = hourly.Variables(0).ValuesAsNumpy()
    hourly_visibility = hourly.Variables(1).ValuesAsNumpy()

    hourly_data = pd.DataFrame({
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left",
        ),
        "cloud_cover": hourly_cloud_cover,
        "visibility": hourly_visibility,
    })

    current_time = pd.Timestamp.now(tz="UTC")
    curr_hour = np.argmin(np.abs(hourly_data["date"] - current_time))

    curr_hour_data = {}
    for i in ["cloud_cover", "visibility"]:
        curr_hour_data[i] = round(float(hourly_data[i].iloc[curr_hour]), 1)

    return curr_hour_data


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

    hourly_dict = get_hourly_forecast(lat, long)

    air_temp, wind_speed, wind_dir = current_wind_temp(
        lat, long, arguments["decimal"]
    )
    rain_sum, precipitation_probability_max = get_rain(lat, long)

    arguments["ocean_data"] = ocean_data
    arguments["uv_index"] = uv_index
    spot_forecast = forecast(lat, long, arguments["decimal"], 7)
    json_forecast = helper.forecast_to_json(
        spot_forecast, arguments["decimal"]
    )

    ocean_history = ocean_information_history(
        lat, long, arguments["decimal"], arguments["unit"]
    )
    ocean_data_dict = {
        "Lat": lat,
        "Long": long,
        "Location": arguments["city"],
        "Height": ocean_data[0],
        "Height one year ago": ocean_history[0],
        "Swell Direction": ocean_data[1],
        "Swell Direction one year ago": ocean_history[1],
        "Period": ocean_data[2],
        "Period one year ago": ocean_history[2],
        "UV Index": uv_index,
        "UV Index one year ago": (
            get_uv_history(lat, long, arguments["decimal"], arguments["unit"])
        ),
        "Air Temperature": air_temp,
        "Wind Speed": wind_speed,
        "Wind Direction": wind_dir,
        "Forecast": json_forecast,
        "Unit": arguments["unit"],
        "Rain Sum": rain_sum,
        "Precipitation Probability Max": precipitation_probability_max,
        "Cloud Cover": hourly_dict["cloud_cover"],
        "Visibility": hourly_dict["visibility"],
    }
    return ocean_data_dict


def separate_args_and_get_location(args):
    """
    Gets user's coordinates from either
    the argument(location=) or, if none,
    the default coordinates(default_location())
    """
    coordinates = get_coordinates(tuple(args))
    location_data = {
        "coordinates": coordinates,
        "lat": coordinates[0],
        "long": coordinates[1],
        "city": coordinates[2],
    }
    return location_data


# Backward-compatible alias for the misspelled name
seperate_args_and_get_location = separate_args_and_get_location
