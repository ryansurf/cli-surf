"""
Main module
"""

import sys
import helper
import api
import art
import os
import subprocess
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
website = bool(os.getenv("WEBSITE"))

if website == True:
    print("RUNNING WEBSITE")
    subprocess.Popen(["python", "-m", "http.server", "9000"], cwd="../frontend")

args = helper.seperate_args(sys.argv)
# sys cli inputs
# Defaults. 1 == Show, anything else == hide
coordinates = api.get_coordinates(args)
lat = coordinates[0]
long = coordinates[1]
city = coordinates[2]

# Dictionary to keep ocean vars
ocean = {
    "lat": lat,
    "long": long,
    "city": city,
    "show_wave": 1,
    "show_large_wave": 0,
    "show_uv": 1,
    "show_height": 1,
    "show_direction": 1,
    "show_period": 1,
    "show_city": 1,
    "show_date": 1,
    "unit": "imperial",
    "decimal": helper.extract_decimal(args),
    "forecast_days": helper.get_forecast_days(args),
    "color": helper.get_color(args),
}

# Check if specific options are present in args and update ocean dictionary accordingly
if "hide_wave" in args or "hw" in args:
    ocean["show_wave"] = 0
if "show_large_wave" in args or "slw" in args:
    ocean["show_large_wave"] = 1
if "hide_uv" in args or "huv" in args:
    ocean["show_uv"] = 0
if "hide_height" in args or "hh" in args:
    ocean["show_height"] = 0
if "hide_direction" in args or "hdir" in args:
    ocean["show_direction"] = 0
if "hide_period" in args or "hp" in args:
    ocean["show_period"] = 0
if "hide_location" in args or "hl" in args:
    ocean["show_city"] = 0
if "hide_date" in args or "hdate" in args:
    ocean["show_date"] = 0
if "metric" in args or "m" in args:
    ocean["unit"] = "metric"

# Calls APIs though python files
ocean_data = api.ocean_information(lat, long, ocean["decimal"], ocean["unit"])
uv_index = api.get_uv(lat, long, ocean["decimal"], ocean["unit"])

ocean["ocean_data"] = ocean_data
ocean["uv_index"] = uv_index


def main():
    """
    Main function
    """
    print("\n")
    if coordinates == "No data":
        print("No location found")
    if ocean_data == "No data":
        print(coordinates)
        print("No ocean data at this location.")
    else:
        helper.print_location(ocean["city"], ocean["show_city"])
        art.print_wave(ocean["show_wave"], ocean["show_large_wave"], ocean["color"])
        helper.print_output(ocean)
    print("\n")
    forecast = api.forecast(lat, long, ocean["decimal"], ocean["forecast_days"])
    helper.print_forecast(ocean, forecast)


main()
