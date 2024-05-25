"""
General helper functions
"""

import matplotlib.pyplot as plt, mpld3


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
