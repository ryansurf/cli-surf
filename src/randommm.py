import openmeteo_requests
import requests_cache
from retry_requests import retry
from datetime import datetime, timedelta


def get_uv_history(lat, long, decimal, unit="imperial"):
    """
    Get UV one year ago at coordinates (lat, long)
    Calling the API here: https://open-meteo.com/en/docs
    """
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    # Get current date
    current_date = datetime.now()

    # Calculate one year ago
    one_year_ago = current_date - timedelta(days=365)

    # Format to be suitable for API
    formatted_date_one_year_ago = one_year_ago.strftime("%Y-%m-%d")

    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = {
        "latitude": lat,
        "longitude": long,
        "length_unit": unit,
        "current": "uv_index",
        "start_date": formatted_date_one_year_ago,
        "end_date": formatted_date_one_year_ago
    }

    try:
        responses = openmeteo.weather_api(url, params=params)
    except ValueError:
        return "No data"

    response = responses[0]

    # Current values. The order of variables needs to be the same as requested.
    past_uv = response.Current()
    historical_uv_index = round(past_uv.Variables(0).Value(), decimal)

    print(params)
    return historical_uv_index


# Test the function with specific coordinates
lat = -31.9522  # Example: Perth, Australia
long = 115.8614  # Example: Perth, Australia

uv_index = get_uv_history(lat, long, decimal=2, unit="imperial")
print(f"UV Index one year ago: {uv_index}")
