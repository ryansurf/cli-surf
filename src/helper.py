"""
General helper functions
"""

import json
import logging

from src import api, art, gpt

logger = logging.getLogger(__name__)

MAX_FORECAST_DAYS = 7

DEFAULT_ARGUMENTS = {
    "show_wave": True,
    "show_large_wave": False,
    "show_uv": True,
    "show_past_uv": False,
    "show_height": True,
    "show_direction": True,
    "show_period": True,
    "show_height_history": False,
    "show_direction_history": False,
    "show_period_history": False,
    "show_city": True,
    "show_date": True,
    "show_air_temp": False,
    "show_wind_speed": False,
    "show_wind_direction": False,
    "json_output": False,
    "show_rain_sum": False,
    "show_precipitation_prob": False,
    "unit": "imperial",
    "gpt": False,
    "show_cloud_cover": False,
    "show_visibility": False,
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


def set_output_values(args, args_dict):  # noqa
    """
    Takes a list of command line arguments (args) and sets the appropriate
    values in args_dict (show_wave = True, etc).
    Returns args_dict with the updated CLI args.
    """
    mappings = {
        "hide_wave": ("show_wave", False),
        "hw": ("show_wave", False),
        "show_large_wave": ("show_large_wave", True),
        "slw": ("show_large_wave", True),
        "hide_uv": ("show_uv", False),
        "huv": ("show_uv", False),
        "show_past_uv": ("show_past_uv", True),
        "spuv": ("show_past_uv", True),
        "hide_past_uv": ("show_past_uv", False),
        "hide_height": ("show_height", False),
        "hh": ("show_height", False),
        "show_height_history": ("show_height_history", True),
        "shh": ("show_height_history", True),
        "hide_height_history": ("show_height_history", False),
        "hide_direction": ("show_direction", False),
        "hdir": ("show_direction", False),
        "show_direction_history": ("show_direction_history", True),
        "sdh": ("show_direction_history", True),
        "hide_direction_history": ("show_direction_history", False),
        "hide_period": ("show_period", False),
        "hp": ("show_period", False),
        "show_period_history": ("show_period_history", True),
        "sph": ("show_period_history", True),
        "hide_period_history": ("show_period_history", False),
        "hide_location": ("show_city", False),
        "hl": ("show_city", False),
        "hide_date": ("show_date", False),
        "hdate": ("show_date", False),
        "metric": ("unit", "metric"),
        "m": ("unit", "metric"),
        "json": ("json_output", True),
        "j": ("json_output", True),
        "gpt": ("gpt", True),
        "g": ("gpt", True),
        "show_air_temp": ("show_air_temp", True),
        "sat": ("show_air_temp", True),
        "show_wind_speed": ("show_wind_speed", True),
        "sws": ("show_wind_speed", True),
        "show_wind_direction": ("show_wind_direction", True),
        "swd": ("show_wind_direction", True),
        "show_rain_sum": ("show_rain_sum", True),
        "srs": ("show_rain_sum", True),
        "show_precipitation_prob": ("show_precipitation_prob", True),
        "spp": ("show_precipitation_prob", True),
        "show_cloud_cover": ("show_cloud_cover", True),
        "scc": ("show_cloud_cover", True),
        "show_visibility": ("show_visibility", True),
        "sv": ("show_visibility", True),
    }

    for arg in args:
        if arg in mappings:
            key, value = mappings[arg]
            args_dict[key] = value

    return args_dict


def separate_args(args):
    """
    Args are separated by commas in input. Separate them and return list.
    """
    if len(args) > 1:
        return args.split(",")
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
                logger.warning("Invalid value for %s. Using default.", keys[0])
    return default


def extract_decimal(args):
    """
    Extract decimal precision from CLI args. Defaults to 1.
    """
    for arg in args:
        if arg.startswith("decimal=") or arg.startswith("dec="):
            try:
                return int(arg.split("=")[1])
            except (ValueError, IndexError):
                logger.warning(
                    "Invalid value for decimal. Please provide an integer."
                )
    return 1


def get_forecast_days(args):
    """
    Extract forecast day count from CLI args. Defaults to 0. Max is 7.
    """
    value = _extract_arg(args, ["forecast", "fc"], default=0, cast=int)
    if value < 0 or value > MAX_FORECAST_DAYS:
        logger.warning(
            "Forecast days must be between 0 and %d. Using default.",
            MAX_FORECAST_DAYS,
        )
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
    if show_city:
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

    for arg_key, data_key, label in mappings:
        if arguments_dict[arg_key]:
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
            if ocean[arg_key]:
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
    Serializes data_dict to JSON. Prints to stdout if print_output is True.
    Returns the original dict for programmatic use.
    """
    if print_output:
        print(json.dumps(data_dict, indent=4))
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
    if arguments["gpt"]:
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
