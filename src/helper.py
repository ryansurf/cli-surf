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
    arguments = {
        "lat": lat,
        "long": long,
        "city": city,
        **DEFAULT_ARGUMENTS,
    }

    arguments["decimal"] = extract_decimal(args)
    arguments["forecast_days"] = get_forecast_days(args)
    arguments["color"] = get_color(args)

    arguments = set_output_values(args, arguments)

    return arguments


def set_output_values(args, arguments_dictionary):  # noqa
    """
    Takes a list of command line arguments (args)
    and sets the appropriate values in the
    arguments_dictionary (show_wave = 1, etc).
    Returns the arguments_dictionary dict with the updated CLI args.
    """
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

    for arg in args:
        if arg in mappings:
            key, value = mappings[arg]
            arguments_dictionary[key] = value

    return arguments_dictionary


def separate_args(args):
    """
    Args are separated by commas in input. Separate them and return list.
    """
    if len(args) > 1:
        return args[1].split(",")
    return []


# Keep old name as an alias for backwards compatibility
seperate_args = separate_args


def _extract_arg(args, keys, default, cast=str):
    """
    Scan args for the first token matching 'key=value' where key is in keys.
    Parses the value with cast and returns it, or returns default on failure.
    """
    for arg in args:
        arg_str = str(arg)
        if any(arg_str.startswith(f"{k}=") for k in keys):
            try:
                return cast(arg_str.split("=", 1)[1])
            except (ValueError, IndexError):
                print(f"Invalid value for {keys[0]}. Using default.")
    return default


def extract_decimal(args):
    """
    Extract decimal precision from CLI args. Defaults to 1.
    """
    value = _extract_arg(args, ["decimal", "dec"], default=None, cast=int)
    if value is None:
        return 1
    return value


def get_forecast_days(args):
    """
    Extract forecast day count from CLI args. Defaults to 0. Max is 7.
    """
    MAX_VALUE = 7
    value = _extract_arg(args, ["forecast", "fc"], default=0, cast=int)
    if value < 0 or value > MAX_VALUE:
        print("Must choose a non-negative number <= 7 in forecast!")
        return 0
    return value


def get_color(args):
    """
    Extract color from CLI args. Defaults to 'blue'.
    """
    return _extract_arg(args, ["color", "c"], default="blue")


def print_location(city, show_city):
    """
    Prints location.
    """
    if int(show_city) == 1:
        print("Location: ", city)
        print("\n")


def print_ocean_data(arguments_dict, ocean_data_dict):
    """
    Prints ocean data (height, wave direction, period, etc).
    """
    mappings = [
        ("show_uv", "UV Index", "UV index: "),
        ("show_past_uv", "UV Index one year ago", "UV Index one year ago: "),
        ("show_height", "Height", "Wave Height: "),
        ("show_height_history", "Height one year ago", "Wave Height one year ago: "),
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

    for arg_key, data_key, label in mappings:
        if int(arguments_dict[arg_key]) == 1:
            print(f"{label}{ocean_data_dict[data_key]}")


def print_forecast(ocean, forecast):
    """
    Prints forecast data for each forecasted day.
    forecast is a dict of lists, one entry per day.
    """
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

    for day in range(ocean["forecast_days"]):
        for arg_key, data_key, label in mappings:
            if int(ocean[arg_key]) == 1:
                try:
                    data = forecast[data_key][day]
                    formatted = round(float(data), ocean["decimal"])
                    print(f"{label}{formatted}")
                except TypeError:
                    print(f"{label}{forecast[data_key][day]}")
        print("\n")


def round_decimal(round_list, decimal):
    """
    Rounds each element of round_list to the given decimal precision.
    """
    return [round(num, decimal) for num in round_list]


def json_output(data_dict, print_output=True):
    """
    If JSON=TRUE in .args, we print and return the JSON data.
    Data dict includes current & forecast data.
    """
    json_out = json.dumps(data_dict, indent=4)
    if print_output:
        print(json_out)
    return data_dict


def print_outputs(ocean_data_dict, arguments, gpt_prompt, gpt_info):
    """
    Main printing function; calls all the other printing functions.
    """
    print("\n")
    if ocean_data_dict["Height"] == "No data":
        print(ocean_data_dict["Lat"], ocean_data_dict["Long"])
        print("No ocean data at this location.")
    else:
        print_location(arguments["city"], arguments["show_city"])
        art.print_wave(
            arguments["show_wave"],
            arguments["show_large_wave"],
            arguments["color"],
        )
        print_ocean_data(arguments, ocean_data_dict)
    print("\n")

    forecast = api.forecast(
        ocean_data_dict["Lat"],
        ocean_data_dict["Long"],
        arguments["decimal"],
        arguments["forecast_days"],
    )
    print_forecast(arguments, forecast)

    gpt_response = None
    if arguments["gpt"] == 1:
        gpt_response = print_gpt(ocean_data_dict, gpt_prompt, gpt_info)
        print(gpt_response)
    return gpt_response


def set_location(location):
    """
    Unpacks location dict into (city, lat, long).
    """
    return location["city"], location["lat"], location["long"]


def forecast_to_json(forecast_data, decimal):
    """
    Converts forecast_data from forecast() into a list of day dicts.
    """
    forecasts = []
    for i, date in enumerate(forecast_data["date"]):
        forecast = {
            "date": str(date.date()),
            "surf height": round(float(forecast_data["wave_height_max"][i]), decimal),
            "swell direction": round(
                float(forecast_data["wave_direction_dominant"][i]), decimal
            ),
            "swell period": round(float(forecast_data["wave_period_max"][i]), decimal),
            "uv index": round(float(forecast_data["uv_index_max"][i]), decimal),
            "temperature_2m_max": round(
                float(forecast_data["temperature_2m_max"][i]), decimal
            ),
            "temperature_2m_min": round(
                float(forecast_data["temperature_2m_min"][i]), decimal
            ),
            "rain_sum": round(float(forecast_data["rain_sum"][i]), decimal),
            "daily_precipitation_probability": round(
                float(forecast_data["precipitation_probability_max"][i]), decimal
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


def print_gpt(surf_data, gpt_prompt, gpt_info):
    """
    Builds a surf summary and returns the GPT response.
    """
    summary = (
        f"Today at {surf_data['Location']}, the surf height is "
        f"{surf_data['Height']} {surf_data['Unit']}, the direction of the "
        f"swell is {surf_data['Swell Direction']} degrees and the swell "
        f"period is {surf_data['Period']} seconds."
    )
    api_key, gpt_model = gpt_info
    MIN_KEY_LEN = 5
    if not api_key or len(api_key) < MIN_KEY_LEN:
        return gpt.simple_gpt(summary, gpt_prompt)
    return gpt.openai_gpt(summary, gpt_prompt, api_key, gpt_model)
