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
from helper import arguments_dictionary

#Seperates the cli args into a list
args = helper.seperate_args(sys.argv)

#  return coordinates, lat, long, city
location = api.seperate_args_and_get_location(args)
coordinates, city = location["coordinates"], location["city"]
lat, long = location["lat"], location["long"]

#Sets ocean = dictionary with
arguments = helper.arguments_dictionary(lat, long, city, args)
#Updates the ocean dict with the valeus from the arguments
arguements = helper.set_output_values(args, arguments)


def main(lat, long):
    """
    Main function
    """
    lat = float(lat)
    long = float(long)
    # Makes calls to the apis(ocean, UV) and returns the values
    data = api.gather_data(lat, long, arguments)
    ocean_data = data[0]
    uv_index = data[1]
    data_dict = data[2]

    #Non-JSON output
    if arguments["json_output"] == 0:
        helper.print_outputs(lat, long, coordinates, ocean_data, arguments)
        return data_dict
    #JSON Output
    else:
        json_output = helper.json_output(data_dict)
        return json_output

main(lat, long)

