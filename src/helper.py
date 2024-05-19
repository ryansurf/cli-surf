from geopy.geocoders import Nominatim
import openmeteo_requests
import requests_cache
from retry_requests import retry    
import requests
from termcolor import colored
import pandas as pd

#Args are seperated by commas in input. Sereperat them and return list
def seperate_args(args):
    if len(args) > 1:
        new_args = args[1].split(",")
        return new_args
    else:
        return []

# Takes a location(city or address) and returns the coordinates: [lat, long]
#If no location is specified, default_location() finds the users coordinates
def get_coordinates(args):
    for arg in args:
        arg = str(arg)
        if arg.startswith("location=") or arg.startswith("loc=") :
            address = arg.split('=')[1]
            geolocator = Nominatim(user_agent="cli-surf")
            location = geolocator.geocode(address)
            if location != None:
                return [location.latitude, location.longitude, location]
            else:
                return "No data"
    return default_location()

#Checks to see if forecast in cli args. Defaults to 0
def get_forecast_days(args):
    for arg in args:
        arg = str(arg)
        if arg.startswith("forecast=") or arg.startswith("fc="):
            forecast = int(arg.split('=')[1])
            if forecast < 0 or forecast > 7:
                print("Must choose a non-negative number >= 7 in forecast!")
                break
            return forecast
    return 0

#If no location specified in cli, find users location
def default_location():
    # Make a GET request to the API endpoint
    response = requests.get("https://ipinfo.io/json")

    if response.status_code == 200:
        data = response.json()
        location = data['loc'].split(',')
        lat = location[0]
        long = location[1]
        city = data['city']
        return [lat, long, city]
    else:
        return "No data"

#Get UV at coordinates
def get_uv(lat, long, decimal, unit="imperial"):
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = {
        "latitude": lat,
        "longitude": long,
        "length_unit": unit,
        "current": "uv_index"
    }
    try:
        responses = openmeteo.weather_api(url, params=params)
    except:
        return "No data"

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    # print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    # print(f"Elevation {response.Elevation()} m asl")
    # print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    # print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    # Current values. The order of variables needs to be the same as requested.
    current = response.Current()
    current_uv_index = round(current.Variables(0).Value(), decimal)

    return current_uv_index

#Get Ocean Data at coordinates
def ocean_information(lat, long, decimal, unit="imperial"):
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
        "length_unit": unit,
        "timezone": "auto",
        "forecast_days": 3
    }
    try:
        responses = openmeteo.weather_api(url, params=params)
    except:
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

def print_location(city, show_city):
    if int(show_city) == 1:
        print("Location: ", city)
        print("\n")

#Prints output
def print_output(uv_index, ocean_data, show_uv, show_height, show_direction, show_period):
    if int(show_uv) == 1:
        print("UV index: ", uv_index)
    if int(show_height) == 1:
        print("Wave Height: ", ocean_data[0])
    if int(show_direction) == 1:
        print("Wave Direction: ", ocean_data[1])
    if int(show_period) == 1:
        print("Wave Period: ", ocean_data[2])

#Takes in list of forecast data and prints
def print_forecast(forecast_list, uv_index, ocean_data, show_uv, show_height, show_direction, show_period, show_date):
    transposed = list(zip(*forecast_list))
    for day in transposed:
        if show_date == 1:
            print("Date: ", day[3])
        # if int(show_uv) == 1:
        #     print("UV index: ", uv_index)
        if int(show_height) == 1:
            print("Wave Height: ", day[0])
        if int(show_direction) == 1:
            print("Wave Direction: ", day[1])
        if int(show_period) == 1:
            print("Wave Period: ", day[2])
        print("\n")

# Function to extract decimal value from command-line arguments
#Default is 1
def extract_decimal(args):
    for arg in args:
        if arg.startswith("decimal=") or arg.startswith("dec="):
            try:
                decimal_value = int(arg.split('=')[1])
                return decimal_value
            except (ValueError, IndexError):
                print("Invalid value for decimal. Please provide an integer.")
    return 1

#Prints Wave
def print_wave(show_wave, show_large_wave):
    if int(show_wave) == 1:


        print(colored("""
      .-``'.
    .`   .`
_.-'     '._ 
        """, "light_blue"))
    
    if int(show_large_wave) == 1:
        print(colored(""" 
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⣶⠾⠿⠿⠯⣷⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⣾⠛⠁⠀⠀⠀⠀⠀⠀⠈⢻⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⠿⠁⠀⠀⠀⢀⣤⣾⣟⣛⣛⣶⣬⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⠟⠃⠀⠀⠀⠀⠀⣾⣿⠟⠉⠉⠉⠉⠛⠿⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⡟⠋⠀⠀⠀⠀⠀⠀⠀⣿⡏⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣠⡿⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣷⡍⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣤⣤⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣠⣼⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠷⣤⣤⣠⣤⣤⡤⡶⣶⢿⠟⠹⠿⠄⣿⣿⠏⠀⣀⣤⡦⠀⠀⠀⠀⣀⡄
⢀⣄⣠⣶⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠓⠚⠋⠉⠀⠀⠀⠀⠀⠀⠈⠛⡛⡻⠿⠿⠙⠓⢒⣺⡿⠋⠁
⠉⠉⠉⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠁⠀
""", "light_blue"))

#Takes a list as input and rounds each of the elements to the decimal
def round_decimal(round_list, decimal):
    rounded_list = list()
    for num in round_list:
        rounded_list.append(round(num, decimal))
    return rounded_list

#Number of forecast days. Max is 7
def forecast(lat, long, decimal, days=0):
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
        "daily": ["wave_height_max", "wave_direction_dominant", "wave_period_max"],
        "length_unit": "imperial",
        "timezone": "auto",
        "forecast_days": days
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]

    # Process daily data. The order of variables needs to be the same as requested.
    daily = response.Daily()
    daily_wave_height_max = round_decimal(daily.Variables(0).ValuesAsNumpy(), decimal)
    daily_wave_direction_dominant = round_decimal(daily.Variables(1).ValuesAsNumpy(), decimal)
    daily_wave_period_max = round_decimal(daily.Variables(2).ValuesAsNumpy(), decimal)

    daily_data = {"date": pd.date_range(
        start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
        end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = daily.Interval()),
        inclusive = "left"
    )}
    time_data = daily_data['date']

    return [daily_wave_height_max, daily_wave_direction_dominant, daily_wave_period_max, time_data]


    
