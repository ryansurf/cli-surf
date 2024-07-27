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
        "show_air_temp": 0,
        "show_wind_speed": 0,
        "show_wind_direction": 0,
        "json_output": 0,
        "unit": "imperial",
        "decimal": extract_decimal(args),
        "forecast_days": get_forecast_days(args),
        "color": get_color(args),
        "gpt": 0,
    }
    # Updates the arguments dict with the values from the CLI args
    arguments = set_output_values(args, arguments)
    return arguments


def set_output_values(args, arguments):
    """
    Takes a list of command line arguments (args)
    and sets the appropriate values
    in the arguments dictionary (show_wave = 1, etc).
    Returns the arguments dict with the updated CLI args.
    """
    actions = {
        "hide_wave": ("show_wave", 0),
        "hw": ("show_wave", 0),
        "show_large_wave": ("show_large_wave", 1),
        "slw": ("show_large_wave", 1),
        "hide_uv": ("show_uv", 0),
        "huv": ("show_uv", 0),
        "hide_height": ("show_height", 0),
        "hh": ("show_height", 0),
        "hide_direction": ("show_direction", 0),
        "hdir": ("show_direction", 0),
        "hide_period": ("show_period", 0),
        "hp": ("show_period", 0),
        "hide_location": ("show_city", 0),
        "hl": ("show_city", 0),
        "hide_date": ("show_date", 0),
        "hdate": ("show_date", 0),
        "metric": ("unit", "metric"),
        "m": ("unit", "metric"),
        "json": ("json_output", 1),
        "j": ("json_output", 1),
        "gpt": ("gpt", 1),
        "g": ("gpt", 1),
        "show_air_temp": ("show_air_temp", 1),
        "sat": ("show_air_temp", 1),
        "show_wind_speed": ("show_wind_speed", 1),
        "sws": ("show_wind_speed", 1),
        "show_wind_direction": ("show_wind_direction", 1),
        "swd": ("show_wind_direction", 1),
    }

    for arg in args:
        if arg in actions:
            key, value = actions[arg]
            arguments[key] = value

    return arguments


def separate_args(args):
    """
    Args are separated by commas in input. Separate them and return list
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


def print_ocean_data(arguments_dict, ocean_data):
    """
    Prints ocean data (height, wave direction, period, etc.)
    """
    display_mapping = {
        "show_uv": ("UV Index", "UV index: "),
        "show_height": ("Height", "Wave Height: "),
        "show_direction": ("Swell Direction", "Wave Direction: "),
        "show_period": ("Period", "Wave Period: "),
        "show_air_temp": ("Air Temperature", "Air Temp: "),
        "show_wind_speed": ("Wind Speed", "Wind Speed: "),
        "show_wind_direction": ("Wind Direction", "Wind Direction: ")
    }

    for key, (data_key, label) in display_mapping.items():
        if int(arguments_dict.get(key, 0)) == 1:
            value = ocean_data.get(data_key)
            if value is not None:
                print(f"{label} {value}")
            else:
                print(f"{label} None")


def print_forecast(ocean, forecast):
    """
    Takes in list of forecast data and prints
    """
    transposed = list(zip(*forecast))

    for day in transposed:
        actions = {
            "show_date": (3, "Date: "),
            "show_height": (0, "Wave Height: "),
            "show_direction": (1, "Wave Direction: "),
            "show_period": (2, "Wave Period: ")
        }

        for key, (index, forecast_data) in actions.items():
            if int(ocean.get(key, 0)) == 1:
                print(forecast_data, day[index])
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


def json_output(data_dict):
    """
    If JSON=TRUE in .args, we print and return the JSON data
    """
    json_out = json.dumps(data_dict, indent=4)
    print(json_out)
    return data_dict


def print_outputs(city, data_dict, arguments, gpt_prompt, gpt_info):
    """
    Basically the main printing function,
    calls all the other printing functions
    """
    print("\n")
    if city == "No data":
        print("No location found")
    if data_dict["Height"] == "No data":
        print(data_dict["Lat"], data_dict["Long"])
        print("No ocean data at this location.")
    else:
        # Location is found, print details
        print_location(arguments["city"], arguments["show_city"])
        art.print_wave(
            arguments["show_wave"],
            arguments["show_large_wave"],
            arguments["color"],
        )
        # Prints(Height: <>, Period: <>, etc.)
        print_ocean_data(arguments, data_dict)
    print("\n")
    forecast = api.forecast(
        data_dict["Lat"],
        data_dict["Long"],
        arguments["decimal"],
        arguments["forecast_days"],
    )
    # Prints the forecast(if activated in CLI args)
    print_forecast(arguments, forecast)
    # Checks if GPT in args, prints GPT response if True
    if arguments["gpt"] == 1:
        gpt_response = print_gpt(data_dict, gpt_prompt, gpt_info)
        print(gpt_response)


def set_location(location):
    """
    Sets locations variables
    """
    city = location["city"]
    lat, long = location["lat"], location["long"]
    return city, lat, long


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
    Useed by the GPT as input
    """
    location = surf_data["Location"]
    height = surf_data["Height"]
    direction = surf_data["Direction"]
    period = surf_data["Period"]
    unit = surf_data["Unit"]
    report = f"""
    Today at {location}, the surf height is {height} {unit}, the direction
    of the swell is {direction} degrees and the swell period is {period}
    seconds.
    """
    return report


def print_gpt(surf_data, gpt_prompt, gpt_info):
    """
    Returns the GPT response
    """
    summary = surf_summary(surf_data)
    api_key = gpt_info[0]
    gpt_model = gpt_info[1]
    minumum_key_length = 5
    if api_key is None or not api_key or len(api_key) < minumum_key_length:
        gpt_response = gpt.simple_gpt(summary, gpt_prompt)
    else:
        gpt_response = gpt.openai_gpt(summary, gpt_prompt, api_key, gpt_model)
    return gpt_response
