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
        "show_rain_sum": 0,
        "show_precipitation_prob": 0,
        "unit": "imperial",
        "decimal": extract_decimal(args),
        "forecast_days": get_forecast_days(args),
        "color": get_color(args),
        "gpt": 0,
    }
    # Updates the arguments dict with the values from the CLI args
    arguments = set_output_values(args, arguments)
    return arguments


def set_output_values(args, arguments):  # noqa
    """
    Takes a list of command line arguments(args)
    and sets the appropritate values
    in the arguments dictionary(show_wave = 1, etc).
    Returns the arguments dict with the updated CLI args
    """
    if "hide_wave" in args or "hw" in args:
        arguments["show_wave"] = 0
    if "show_large_wave" in args or "slw" in args:
        arguments["show_large_wave"] = 1
    if "hide_uv" in args or "huv" in args:
        arguments["show_uv"] = 0
    if "hide_height" in args or "hh" in args:
        arguments["show_height"] = 0
    if "hide_direction" in args or "hdir" in args:
        arguments["show_direction"] = 0
    if "hide_period" in args or "hp" in args:
        arguments["show_period"] = 0
    if "hide_location" in args or "hl" in args:
        arguments["show_city"] = 0
    if "hide_date" in args or "hdate" in args:
        arguments["show_date"] = 0
    if "metric" in args or "m" in args:
        arguments["unit"] = "metric"
    if "json" in args or "j" in args:
        arguments["json_output"] = 1
    if "gpt" in args or "g" in args:
        arguments["gpt"] = 1
    if "show_air_temp" in args or "sat" in args:
        arguments["show_air_temp"] = 1
    if "show_wind_speed" in args or "sws" in args:
        arguments["show_wind_speed"] = 1
    if "show_wind_direction" in args or "swd" in args:
        arguments["show_wind_direction"] = 1
    if "show_rain_sum" in args or "srs" in args:
        arguments["show_rain_sum"] = 1
    if "show_precipitation_prob" in args or "spp" in args:
        arguments["show_precipitation_prob"] = 1

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


def print_ocean_data(arguments_dict, ocean_data_dict):
    """
    Prints ocean data(height, wave direction, period, etc)
    """
    if int(arguments_dict["show_uv"]) == 1:
        print("UV index: ", ocean_data_dict["UV Index"])
    if int(arguments_dict["show_height"]) == 1:
        print("Wave Height: ", ocean_data_dict["Height"])
    if int(arguments_dict["show_direction"]) == 1:
        print("Wave Direction: ", ocean_data_dict["Swell Direction"])
    if int(arguments_dict["show_period"]) == 1:
        print("Wave Period: ", ocean_data_dict["Period"])
    if int(arguments_dict["show_air_temp"]) == 1:
        print("Air Temp: ", ocean_data_dict["Air Temperature"])
    if int(arguments_dict["show_wind_speed"]) == 1:
        print("Wind Speed: ", ocean_data_dict["Wind Speed"])
    if int(arguments_dict["show_wind_direction"]) == 1:
        print("Wind Direction: ", ocean_data_dict["Wind Direction"])


def print_forecast(ocean, forecast):
    """
    Takes in list of forecast data and prints
    """
    transposed = list(zip(*forecast))
    for day in transposed:
        if ocean["show_date"] == 1:
            print("Date: ", day[3])
        if int(ocean["show_uv"]) == 1:
            print("UV Index: ", day[4])
        if int(ocean["show_height"]) == 1:
            print("Wave Height: ", day[0])
        if int(ocean["show_direction"]) == 1:
            print("Wave Direction: ", day[1])
        if int(ocean["show_period"]) == 1:
            print("Wave Period: ", day[2])
        if int(ocean["show_air_temp"]) == 1:
            print("Air Temp Max: ", day[5])
        if int(ocean["show_air_temp"]) == 1:
            print("Air Temp Min: ", day[6])
        if int(ocean["show_rain_sum"]) == 1:
            print("Rain Sum: ", day[7])
        if int(ocean["show_precipitation_prob"]) == 1:
            print("Precipitation Probability: ", day[8], "%")
        if int(ocean["show_wind_speed"]) == 1:
            print("Max Wind Speed: ", day[9])
        if int(ocean["show_wind_direction"]) == 1:
            print("Wind Direction ", day[10])
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
    (
        surf_height,
        swell_direction,
        swell_period,
        dates,
        uv_index,
        temp_max,
        temp_min,
        rain_sum,
        precipitation_probability,
        wind_speed,
        wind_direction_dominant,
    ) = data
    # Formatting into JSON
    forecasts = []
    for i in range(len(dates)):
        forecast = {
            "date": str(dates[i].date()),
            "surf height": round(float(surf_height[i]), decimal),
            "swell direction": round(float(swell_direction[i]), decimal),
            "swell period": round(float(swell_period[i]), decimal),
            "uv index": round(float(uv_index[i]), decimal),
            "temperature_2m_max": round(float(temp_max[i]), decimal),
            "temperature_2m_min": round(float(temp_min[i]), decimal),
            "rain_sum": round(float(rain_sum[i]), decimal),
            "daily_precipitation_probability": round(
                float(precipitation_probability[i]), decimal
            ),
            "wind_speed_max": round(float(wind_speed[i]), decimal),
            "wind_direction_10m_dominant": round(
                float(wind_direction_dominant[i]), decimal
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
