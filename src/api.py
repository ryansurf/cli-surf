"""
Functions that make API calls stored here
"""

import logging
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from functools import lru_cache
from http import HTTPStatus
from threading import Lock

import numpy as np
import pandas as pd
import requests
from cachetools import TTLCache, cached
from geopy.distance import great_circle
from geopy.geocoders import Nominatim

from src import helper
from src.open_meteo import openmeteo_client

logger = logging.getLogger(__name__)

# data expires after 600 seconds (10 min)
_TTL = 600
# max size = 300 items
_MAXSIZE = 300
_ocean_cache = TTLCache(maxsize=_MAXSIZE, ttl=_TTL)
_uv_cache = TTLCache(maxsize=_MAXSIZE, ttl=_TTL)
uv_history_cache = TTLCache(maxsize=_MAXSIZE, ttl=_TTL)
ocean_history_cache = TTLCache(maxsize=_MAXSIZE, ttl=_TTL)
_wind_temp_cache = TTLCache(maxsize=_MAXSIZE, ttl=_TTL)
_rain_cache = TTLCache(maxsize=_MAXSIZE, ttl=_TTL)
forecast_cache = TTLCache(maxsize=_MAXSIZE, ttl=_TTL)
_hourlyforecast_cache = TTLCache(maxsize=_MAXSIZE, ttl=_TTL)
_tide_cache = TTLCache(maxsize=_MAXSIZE, ttl=_TTL)
_ocean_lock = Lock()


@lru_cache(maxsize=128)
def get_coordinates(args: tuple) -> list | str:
    """
    Takes a location (city or address) and returns the coordinates: [lat, long]
    If no location is specified or the location is invalid, default_location()
    finds the user's coordinates.
    """
    for arg in args:
        arg_str = str(arg)
        if arg_str.startswith("location=") or arg_str.startswith("loc="):
            address = arg.split("=")[1].replace("_", " ")
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


def default_location() -> list | str:
    """
    If no location specified in cli, find user's location
    Make a GET request to the API endpoint
    """
    try:
        response = requests.get("https://ipinfo.io/json", timeout=10)
    except requests.exceptions.Timeout:
        return "No data"
    except requests.exceptions.RequestException:
        return "No data"

    if response.status_code == HTTPStatus.OK:
        data = response.json()
        location = data["loc"].split(",")
        lat = location[0]
        long = location[1]
        city = data["city"]
        return [lat, long, city]
    return "No data"


@cached(_uv_cache, lock=_ocean_lock)
def get_uv(
    lat: float, long: float, decimal: int, unit: str = "imperial"
) -> float | str:
    """
    Get UV at coordinates (lat, long)
    Calling the API here: https://open-meteo.com/en/docs
    """
    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = {
        "latitude": lat,
        "longitude": long,
        "length_unit": unit,
        "current": "uv_index",
    }
    try:
        responses = openmeteo_client.weather_api(url, params=params)
    except ValueError:
        return "No data"

    response = responses[0]

    # Current values. The order of variables needs to be the same as requested.
    current = response.Current()
    current_uv_index = round(current.Variables(0).Value(), decimal)

    return current_uv_index


@cached(uv_history_cache, lock=_ocean_lock)
def get_uv_history(
    lat: float, long: float, decimal: int, unit: str = "imperial"
) -> str:
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

    # Attempt to fetch the UV index data from the API
    try:
        responses = openmeteo_client.weather_api(url, params=params)
    except ValueError:
        return "No data"

    # Process the first response (assuming a single location)
    response = responses[0]

    # Extract hourly UV index values
    hourly = response.Hourly()
    hourly_uv_index = hourly.Variables(0).ValuesAsNumpy()

    # Retrieve the UV index for the current hour from one year ago
    historical_uv_index = hourly_uv_index[current_hour]

    # Format the result to the specified decimal precision
    return f"{historical_uv_index:.{decimal}f}"


@cached(_ocean_cache, lock=_ocean_lock)
def ocean_information(
    lat: float, long: float, decimal: int, unit: str = "imperial"
) -> list | str:
    """
    Get Ocean Data at coordinates
    API: https://open-meteo.com/en/docs/marine-weather-api
    """
    url = "https://marine-api.open-meteo.com/v1/marine"
    params = {
        "latitude": lat,
        "longitude": long,
        "current": [
            "wave_height",
            "wave_direction",
            "wave_period",
            "sea_surface_temperature",
        ],
        "length_unit": unit,
        "timezone": "auto",
        "forecast_days": 3,
    }
    try:
        responses = openmeteo_client.weather_api(url, params=params)
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
    current_sea_surface_temperature = current.Variables(3).Value()

    return [
        current_wave_height,
        current_wave_direction,
        current_wave_period,
        current_sea_surface_temperature,
    ]


@cached(ocean_history_cache, lock=_ocean_lock)
def ocean_information_history(
    lat: float, long: float, decimal: int, unit: str = "imperial"
) -> list | str:
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

    # Attempt to fetch the UV index data from the API
    try:
        responses = openmeteo_client.weather_api(url, params=params)

    except ValueError:
        return "No data"

    # Process the first response (assuming a single location)
    response = responses[0]

    # Extract hourly values for the specified metrics
    hourly = response.Hourly()
    hourly_wave_height = hourly.Variables(0).ValuesAsNumpy()
    hourly_wave_direction = hourly.Variables(1).ValuesAsNumpy()
    hourly_wave_period = hourly.Variables(2).ValuesAsNumpy()

    # Retrieve data for the current hour from one year ago
    return [
        f"{hourly_wave_height[current_hour]:.{decimal}f}",
        f"{hourly_wave_direction[current_hour]:.{decimal}f}",
        f"{hourly_wave_period[current_hour]:.{decimal}f}",
    ]


@cached(_wind_temp_cache, lock=_ocean_lock)
def current_wind_temp(
    lat: float, long: float, decimal: int, temp_unit: str = "fahrenheit"
) -> list:
    """
    Gathers the wind and temperature data
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": long,
        "current": ["temperature_2m", "wind_speed_10m", "wind_direction_10m"],
        "temperature_unit": temp_unit,
        "wind_speed_unit": "mph",
    }
    responses = openmeteo_client.weather_api(url, params=params)

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


@cached(_rain_cache, lock=_ocean_lock)
def get_rain(lat: float, long: float) -> tuple[float, float]:
    """
    Get rain data at coordinates (lat, long)
    Calling the API here: https://open-meteo.com/en/docs
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": long,
        "daily": ["rain_sum", "precipitation_probability_max"],
    }
    responses = openmeteo_client.weather_api(url, params=params)

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


@cached(forecast_cache, lock=_ocean_lock)
def forecast(lat: float, long: float, decimal: int, days: int = 0) -> dict:
    """
    Number of forecast days. Max is 7
    API: https://open-meteo.com/en/docs/marine-weather-api
    """
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

    responses_marine = openmeteo_client.weather_api(
        urls[0], params=params_marine
    )
    responses_general = openmeteo_client.weather_api(
        urls[1], params=params_general
    )

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


@cached(_hourlyforecast_cache, lock=_ocean_lock)
def get_hourly_forecast(
    lat: float, long: float, days: int = 1, unit: str = "fahrenheit"
) -> dict:
    """
    Gets hourly weather data
    """
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

    responses = openmeteo_client.weather_api(url, params=params)
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


@cached(_tide_cache, lock=_ocean_lock)
def get_tide_data(lat: float, long: float):
    """
    Fetches tide data for the given cords
    """
    station_id, _ = nearest_station(lat, long)
    begin = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y%m%d")

    url = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter"
    params = {
        "station": station_id,
        "product": "predictions",
        "datum": "MLLW",
        "interval": "hilo",  # high/low only; omit for 6-min intervals
        "units": "english",
        "time_zone": "gmt",
        "format": "json",
        "begin_date": begin,
        "range": 72,  # hours
    }
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    return r.json()


@lru_cache(maxsize=1)
def _get_stations():
    url = (
        "https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations.json"
    )
    r = requests.get(url, params={"type": "tidepredictions"}, timeout=10)
    r.raise_for_status()
    return r.json()["stations"]


def nearest_station(lat: float, long: float) -> tuple[str, float]:
    """
    returns the id of the nearest NOAA station in respect to the given cords
    """
    min_station_distance = float("inf")
    nearest_id = None
    surf_spot_cords = (float(lat), float(long))

    stations = _get_stations()

    for station in stations:
        station_cords = (float(station["lat"]), float(station["lng"]))
        station_id = station["id"]
        distance = great_circle(surf_spot_cords, station_cords).mi
        if distance < min_station_distance:
            min_station_distance = distance
            nearest_id = station_id

    if nearest_id is None:
        raise RuntimeError("No stations returned")

    return nearest_id, min_station_distance


def _safe_current_tide(lat: float, long: float):
    try:
        return helper.current_tide(lat, long)
    except Exception:
        return None


def gather_data(lat: float | str, long: float | str, arguments: dict) -> dict:
    """
    Calls APIs though python files,
    returns all the ocean data(height, period...)
    in a dictionary (ocean_data_dict)
    """
    lat, long = float(lat), float(long)
    dec, unit = arguments["decimal"], arguments["unit"]

    with ThreadPoolExecutor(max_workers=9) as executor:
        futures = {
            "ocean": executor.submit(ocean_information, lat, long, dec, unit),
            "uv": executor.submit(get_uv, lat, long, dec, unit),
            "hourly": executor.submit(get_hourly_forecast, lat, long),
            "wind_temp": executor.submit(current_wind_temp, lat, long, dec),
            "rain": executor.submit(get_rain, lat, long),
            "forecast": executor.submit(forecast, lat, long, dec, 7),
            "ocean_hist": executor.submit(
                ocean_information_history, lat, long, dec, unit
            ),
            "uv_hist": executor.submit(get_uv_history, lat, long, dec, unit),
            "tide": executor.submit(_safe_current_tide, lat, long),
        }
        results = {k: f.result() for k, f in futures.items()}

    arguments["ocean_data"] = results["ocean"]
    arguments["uv_index"] = results["uv"]

    air_temp, wind_speed, wind_dir = results["wind_temp"]
    rain_sum, precipitation_probability_max = results["rain"]
    json_forecast = helper.forecast_to_json(results["forecast"], dec)

    sea_temp_c = results["ocean"][3]
    if unit == "imperial":
        sea_temp = round(sea_temp_c * 9 / 5 + 32, dec)
    else:
        sea_temp = round(sea_temp_c, dec)

    return {
        "Lat": lat,
        "Long": long,
        "Location": arguments["city"],
        "Height": results["ocean"][0],
        "Height one year ago": results["ocean_hist"][0],
        "Swell Direction": results["ocean"][1],
        "Swell Direction one year ago": results["ocean_hist"][1],
        "Period": results["ocean"][2],
        "Period one year ago": results["ocean_hist"][2],
        "UV Index": results["uv"],
        "UV Index one year ago": results["uv_hist"],
        "Air Temperature": air_temp,
        "Wind Speed": wind_speed,
        "Wind Direction": wind_dir,
        "Forecast": json_forecast,
        "Unit": arguments["unit"],
        "Rain Sum": rain_sum,
        "Precipitation Probability Max": precipitation_probability_max,
        "Cloud Cover": results["hourly"]["cloud_cover"],
        "Visibility": results["hourly"]["visibility"],
        "Tide": results["tide"],
        "Sea Surface Temperature": sea_temp,
    }


def separate_args_and_get_location(args: list) -> dict:
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


if __name__ == "__main__":
    print(get_tide_data(40.741895, -73.989308))
