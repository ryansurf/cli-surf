"""
General helper functions
"""

import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src import api, art, gpt


def arguments_dictionary(lat, long, city, args):
    """
    Dictionary to keep cli argument values
    """
    arguments = {
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
        "json_output": 0,
        "unit": "imperial",
        "decimal": extract_decimal(args),
        "forecast_days": get_forecast_days(args),
        "color": get_color(args),
        "gpt": 1
    }
    return arguments


def seperate_args(args):
    """
    Args are seperated by commas in input. Sereperat them and return list
    """
    if len(args) > 1:
        new_args = args[1].split(",")
        return new_args
    return []


def get_forecast_days(args):
    """
    Checks to see if forecast in cli args. Defaults to 0
    """
    MAX_VALUE = 7
    for arg in args:
        arg_str = str(arg)
        if arg_str.startswith("forecast=") or arg_str.startswith("fc="):
            forecast = int(arg_str.split("=")[1])
            if forecast < 0 or forecast > MAX_VALUE:
                print("Must choose a non-negative number >= 7 in forecast!")
                break
            return forecast
    return 0


def print_location(city, show_city):
    """
    Prints location
    """
    if int(show_city) == 1:
        print("Location: ", city)
        print("\n")


def print_output(ocean_data_dict):
    """
    Prints output
    """
    if int(ocean_data_dict["show_uv"]) == 1:
        print("UV index: ", ocean_data_dict["uv_index"])
    if int(ocean_data_dict["show_height"]) == 1:
        print("Wave Height: ", ocean_data_dict["ocean_data"][0])
    if int(ocean_data_dict["show_direction"]) == 1:
        print("Wave Direction: ", ocean_data_dict["ocean_data"][1])
    if int(ocean_data_dict["show_period"]) == 1:
        print("Wave Period: ", ocean_data_dict["ocean_data"][2])


def print_forecast(ocean, forecast):
    """
    Takes in list of forecast data and prints
    """
    transposed = list(zip(*forecast))
    for day in transposed:
        if ocean["show_date"] == 1:
            print("Date: ", day[3])
        if int(ocean["show_height"]) == 1:
            print("Wave Height: ", day[0])
        if int(ocean["show_direction"]) == 1:
            print("Wave Direction: ", day[1])
        if int(ocean["show_period"]) == 1:
            print("Wave Period: ", day[2])
        print("\n")


def extract_decimal(args):
    """
    Function to extract decimal value from command-line arguments
    Default is 1
    """
    for arg in args:
        if arg.startswith("decimal=") or arg.startswith("dec="):
            try:
                decimal_value = int(arg.split("=")[1])
                return decimal_value
            except (ValueError, IndexError):
                print("Invalid value for decimal. Please provide an integer.")
    return 1


def get_color(args):
    """
    Gets the color in the cli args
    """
    for arg in args:
        arg_str = str(arg)
        if arg_str.startswith("color=") or arg_str.startswith("c="):
            color_name = arg_str.split("=")[1]
            return color_name
    return "blue"


def round_decimal(round_list, decimal):
    """
    Takes a list as input and rounds each of the elements to the decimal
    """
    rounded_list = []
    for num in round_list:
        rounded_list.append(round(num, decimal))
    return rounded_list


def set_output_values(args, ocean):
    """
    Takes a list of command line arguments(args)
    and sets the appropritate values
    in the ocean dictionary(show_wave = 1, etc)
    """
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
    if "json" in args or "j" in args:
        ocean["json_output"] = 1
    if "hide_gpt" in args or "hgpt" in args:
        ocean["gpt"] = 0
    return ocean


def json_output(data_dict):
    """
    If JSON=TRUE in .args, we print and return the JSON data
    """
    json_out = json.dumps(data_dict, indent=4)
    print(json_out)
    return data_dict


def print_outputs(lat, long, coordinates, ocean_data, arguments, data_dict, gpt_prompt):
    """
    Basically the main printing function,
    calls all the other printing functions
    """
    print("\n")
    if coordinates == "No data":
        print("No location found")
    if ocean_data == "No data":
        print(coordinates)
        print("No ocean data at this location.")
    else:
        print_location(arguments["city"], arguments["show_city"])
        art.print_wave(
            arguments["show_wave"],
            arguments["show_large_wave"],
            arguments["color"],
        )
        print_output(arguments)
    print("\n")
    forecast = api.forecast(
        lat, long, arguments["decimal"], arguments["forecast_days"]
    )
    print_forecast(arguments, forecast)
    if arguments["gpt"] == 1:
        gpt_response = print_gpt(data_dict, gpt_prompt)
        print(gpt_response)


def set_location(location):
    """
    Sets locations variables
    """
    coordinates, city = location["coordinates"], location["city"]
    lat, long = location["lat"], location["long"]
    return coordinates, city, lat, long


def forecast_to_json(data, decimal):
    """
    Takes forecast() as input and returns it in JSON format
    """
    surf_height, swell_direction, swell_period, dates = data

    # Formatting into JSON
    forecasts = []
    for i in range(len(dates)):
        forecast = {
            "date": str(dates[i].date()),
            "surf height": round(float(surf_height[i]), decimal),
            "swell direction": round(float(swell_direction[i]), decimal),
            "swell period": round(float(swell_period[i]), decimal),
        }
        forecasts.append(forecast)

    return forecasts

def surf_summary(surf_data):
    """
    Outputs a simple summary of the surf data.
    Useful for the GPT
    """
    location = surf_data['Location']
    height = surf_data['Height']
    direction = surf_data['Direction']
    period = surf_data['Period']
    report = f"""
    Today at {location}, the surf height is {height}, the direction of the 
    swell is {direction} degrees and the swell period is {period} seconds.
    """
    return report


def print_gpt(surf_data, gpt_prompt):
    """
    Returns the GPT response
    """
    summary = surf_summary(surf_data)
    gpt_response = gpt.simple_gpt(summary, gpt_prompt)
    return gpt_response
