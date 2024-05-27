"""
General helper functions
"""
import subprocess
import json
import api
import art
import pandas as pd

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
        "json_output" : 0,
        "unit": "imperial",
        "decimal": extract_decimal(args),
        "forecast_days": get_forecast_days(args),
        "color": get_color(args)
    }
    return arguments

def query_to_args_list(query):
    """
    Convert query string to a list of arguments.
    """
    args = [query] if query else []
    return args

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
    for arg in args:
        arg = str(arg)
        if arg.startswith("forecast=") or arg.startswith("fc="):
            forecast = int(arg.split("=")[1])
            if forecast < 0 or forecast > 7:
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


# def print_output(uv_index, ocean_data, show_uv, show_height, show_direction, show_period):
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
        arg = str(arg)
        if arg.startswith("color=") or arg.startswith("c="):
            color_name = arg.split("=")[1]
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
    Takes a list of command line arguments(args) and sets the appropritate values
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
    return ocean

def start_website(website):
    """
    If the WEBSITE .env variable is true, the webserver is started
    """
    if website == True:
        subprocess.Popen(["python", "-m", "http.server", "9000"], cwd="../frontend")

def json_output(data_dict):
    """
    If JSON=TRUE in .args, we print and return the JSON data
    """ 
    json_output = json.dumps(data_dict, indent=4)
    print(json_output)
    return json_output

def print_outputs(lat, long, coordinates, ocean_data, arguments):
    """
    Basically the main printing function, calls all the other printing functions
    """
    print("\n")
    if coordinates == "No data":
        print("No location found")
    if ocean_data == "No data":
        print(coordinates)
        print("No ocean data at this location.")
    else:
        print_location(arguments["city"], arguments["show_city"])
        art.print_wave(arguments["show_wave"], arguments["show_large_wave"], arguments["color"])
        print_output(arguments)
    print("\n")
    forecast = api.forecast(lat, long, arguments["decimal"], arguments["forecast_days"])
    print_forecast(arguments, forecast)

def set_location(location):
    """
    Sets locations variables
    """
    coordinates, city = location["coordinates"], location["city"]
    lat, long = location["lat"], location["long"]
    return coordinates, city, lat, long

def forecast_to_json(data):
    """
    Takes forecast() as input and returns it in JSON format
    """
    surf_height, swell_direction, swell_period, dates = data
    
    # Formatting into JSON
    forecasts = []
    for i in range(len(dates)):
        forecast = {
            "date": str(dates[i].date()),
            "surf height": surf_height[i],
            "swell direction": swell_direction[i],
            "swell period": swell_period[i]
        }
        forecasts.append(forecast)

    output = {"forecasts": forecasts}
    # Converting to JSON string
    output_json = json.dumps(str(output), indent=4)
    return output_json