"""
General helper functions
"""

import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src import api, art, gpt

# At the top of helper.py, add a constant dict for default args;

DEFAULT_ARGUMENTS = {
    "show_wave": 1,
    "show_large_wave": 0,
    "show_uv": 1,
    "show_past_uv": 0,
    "show_height": 1,
    "show_direction": 1,
    "show_period": 1,
    "show_height_history": 0,
    "show_direction_history": 0,
    "show_period_history": 0,
    "show_city": 1,
    "show_date": 1,
    "show_air_temp": 0,
    "show_wind_speed": 0,
    "show_wind_direction": 0,
    "json_output": 0,
    "show_rain_sum": 0,
    "show_precipitation_prob": 0,
    "unit": "imperial",
    "gpt": 0,
    "show_cloud_cover": 0,
    "show_visibility": 0,
}


def arguments_dictionary(lat, long, city, args):
    """
    Create argument dict with defaults, updated with location and CLI args.
    """
    # Start with location and default args
    arguments = {
        "lat": lat,
        "long": long,
        "city": city,
        **DEFAULT_ARGUMENTS,
    }

    # Extract dynamic values from args
    arguments["decimal"] = extract_decimal(args)
    arguments["forecast_days"] = get_forecast_days(args)
    arguments["color"] = get_color(args)

    # Override default flags with CLI args like "hide_wave", "json", etc.
    arguments = set_output_values(args, arguments)

    return arguments



def set_output_values(args, arguments_dictionary):  # noqa
    """
    Takes a list of command line arguments(args)
    and sets the appropritate values in the
    arguments_dictionary(show_wave = 1, etc).
    Returns the arguments_dictionary dict with the updated CLI args
    """
    # map of arguments to dictionary keys & values
    mappings = {
        "hide_wave": ("show_wave", 0),
        "hw": ("show_wave", 0),
        "show_large_wave": ("show_large_wave", 1),
        "slw": ("show_large_wave", 1),
        "hide_uv": ("show_uv", 0),
        "huv": ("show_uv", 0),
        "show_past_uv": ("show_past_uv", 1),
        "spuv": ("show_past_uv", 1),
        "hide_past_uv": ("show_past_uv", 0),
        "hide_height": ("show_height", 0),
        "hh": ("show_height", 0),
        "show_height_history": ("show_height_history", 1),
        "shh": ("show_height_history", 1),
        "hide_height_history": ("show_height_history", 0),
        "hide_direction": ("show_direction", 0),
        "hdir": ("show_direction", 0),
        "show_direction_history": ("show_direction_history", 1),
        "sdh": ("show_direction_history", 1),
        "hide_direction_history": ("show_direction_history", 0),
        "hide_period": ("show_period", 0),
        "hp": ("show_period", 0),
        "show_period_history": ("show_period_history", 1),
        "sph": ("show_period_history", 1),
        "hide_period_history": ("show_period_history", 0),
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
        "show_rain_sum": ("show_rain_sum", 1),
        "srs": ("show_rain_sum", 1),
        "show_precipitation_prob": ("show_precipitation_prob", 1),
        "spp": ("show_precipitation_prob", 1),
        "show_cloud_cover": ("show_cloud_cover", 1),
        "scc": ("show_cloud_cover", 1),
        "show_visibility": ("show_visibility", 1),
        "sv": ("show_visibility", 1),
    }

    # Update arguments_dictionary based on the cli arguments in args
    # Ex: If "hide_uv" in args,
    # "show_uv" will be set to 0 in arguments_dictionary
    for arg in args:
        if arg in mappings:
            key, value = mappings[arg]
            arguments_dictionary[key] = value

    return arguments_dictionary


def seperate_args(args):
    """
    Args are seperated by commas in input. Seperate them and return list
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


def print_ocean_data(arguments_dict, ocean_data_dict):
    """
    Prints ocean data(height, wave direction, period, etc)
    """

    # List of tuples mapping argument keys to ocean data keys and labels
    mappings = [
        ("show_uv", "UV Index", "UV index: "),
        ("show_past_uv", "UV Index one year ago", "UV Index one year ago: "),
        ("show_height", "Height", "Wave Height: "),
        (
            "show_height_history",
            "Height one year ago",
            "Wave Height one year ago: ",
        ),
        ("show_direction", "Swell Direction", "Wave Direction: "),
        (
            "show_direction_history",
            "Swell Direction one year ago",
            "Wave Direction one year ago: ",
        ),
        ("show_period", "Period", "Wave Period: "),
        (
            "show_period_history",
            "Period one year ago",
            "Wave Period one year ago:",
        ),
        ("show_air_temp", "Air Temperature", "Air Temp: "),
        ("show_wind_speed", "Wind Speed", "Wind Speed: "),
        ("show_wind_direction", "Wind Direction", "Wind Direction: "),
        ("show_rain_sum", "Rain Sum", "Rain Sum: "),
        (
            "show_precipitation_prob",
            "Precipitation Probability Max",
            "Precipitation Probability Max: ",
        ),
        ("show_cloud_cover", "Cloud Cover", "Cloud Cover: "),
        ("show_visibility", "Visibility", "Visibility: "),
    ]

    # arg_key example: "show_height : 1" from arguments_dict
    # data_key example: "Height : 2.4" from ocean_data_dict
    # Label example: "Wave Period: "
    for arg_key, data_key, label in mappings:
        if int(arguments_dict[arg_key]) == 1:
            print(f"{label}{ocean_data_dict[data_key]}")


def print_forecast(ocean, forecast):
    """
    Takes in dict of forecast data and prints.
    forecast = list of lists detailed forecast data (should be a dict?)
    Each "day" is a tuple of data for that forecasted day
    """
    # List of tuples mapping argument keys to ocean data keys and labels

    mappings = [
        ("show_date", "date", "Date: "),
        ("show_uv", "uv_index_max", "UV Index: "),
        ("show_height", "wave_height_max", "Wave Height: "),
        ("show_direction", "wave_direction_dominant", "Wave Direction: "),
        ("show_period", "wave_period_max", "Wave Period: "),
        ("show_air_temp", "temperature_2m_max", "Air Temp Max: "),
        ("show_air_temp", "temperature_2m_min", "Air Temp Min: "),
        ("show_rain_sum", "rain_sum", "Rain Sum: "),
        (
            "show_precipitation_prob",
            "precipitation_probability_max",
            "Precipitation Probability: ",
        ),
        ("show_wind_speed", "wind_speed_10m_max", "Max Wind Speed: "),
        (
            "show_wind_direction",
            "wind_direction_10m_dominant",
            "Wind Direction: ",
        ),
    ]

    forecast_days = ocean["forecast_days"]

    for day in range(forecast_days):
        for arg_key, data_key, label in mappings:
            if int(ocean[arg_key]) == 1:
                try:
                    data = forecast[data_key][day]
                    formatted = round(float(data), ocean["decimal"])
                    print(f"{label}{formatted}")
                except TypeError:
                    print(f"{label}{forecast[data_key][day]}")
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
    Data dict includes current & forecast data
    """
    json_out = json.dumps(data_dict, indent=4)
    print(json_out)
    return data_dict


def print_outputs(ocean_data_dict, arguments, gpt_prompt, gpt_info):
    """
    Basically the main printing function,
    calls all the other printing functions
    """
    print("\n")
    if ocean_data_dict["Height"] == "No data":
        print(ocean_data_dict["Lat"], ocean_data_dict["Long"])
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
        print_ocean_data(arguments, ocean_data_dict)
    print("\n")
    forecast = api.forecast(
        ocean_data_dict["Lat"],
        ocean_data_dict["Long"],
        arguments["decimal"],
        arguments["forecast_days"],
    )
    # Prints the forecast(if activated in CLI args)
    print_forecast(arguments, forecast)

    # Checks if GPT in args, prints GPT response if True
    gpt_response = None
    if arguments["gpt"] == 1:
        gpt_response = print_gpt(ocean_data_dict, gpt_prompt, gpt_info)
        print(gpt_response)
    return gpt_response


def set_location(location):
    """
    Sets locations variables
    """
    city = location["city"]
    lat, long = location["lat"], location["long"]
    return city, lat, long


def forecast_to_json(forecast_data, decimal):
    """
    Takes forecast_data from forecast() as input
    and returns it in JSON format
    """
    # Formatting into JSON
    forecasts = []
    for i in range(len(forecast_data["date"])):
        forecast = {
            "date": str(forecast_data["date"][i].date()),
            "surf height": round(
                float(forecast_data["wave_height_max"][i]), decimal
            ),
            "swell direction": round(
                float(forecast_data["wave_direction_dominant"][i]), decimal
            ),
            "swell period": round(
                float(forecast_data["wave_period_max"][i]), decimal
            ),
            "uv index": round(
                float(forecast_data["uv_index_max"][i]), decimal
            ),
            "temperature_2m_max": round(
                float(forecast_data["temperature_2m_max"][i]), decimal
            ),
            "temperature_2m_min": round(
                float(forecast_data["temperature_2m_min"][i]), decimal
            ),
            "rain_sum": round(float(forecast_data["rain_sum"][i]), decimal),
            "daily_precipitation_probability": round(
                float(forecast_data["precipitation_probability_max"][i]),
                decimal,
            ),
            "wind_speed_max": round(
                float(forecast_data["wind_speed_10m_max"][i]), decimal
            ),
            "wind_direction_10m_dominant": round(
                float(forecast_data["wind_direction_10m_dominant"][i]), decimal
            ),
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
    direction = surf_data["Swell Direction"]
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
