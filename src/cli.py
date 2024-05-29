"""
Main module
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src import api, helper


def run(lat=0, long=0):
    """
    Main function
    """
    # Seperates the cli args into a list
    args = helper.seperate_args(sys.argv)

    #  return coordinates, lat, long, city
    location = api.seperate_args_and_get_location(args)

    set_location = helper.set_location(location)
    coordinates, city = set_location[0], set_location[1]

    # Check if lat and long are set to defaults(no argumentes passed in main())
    if lat == 0 and long == 0:
        lat, long = set_location[2], set_location[3]

    # Sets ocean = dictionary with
    arguments = helper.arguments_dictionary(lat, long, city, args)
    # Updates the ocean dict with the valeus from the arguments
    arguments = helper.set_output_values(args, arguments)

    lat = float(lat)
    long = float(long)
    # Makes calls to the apis(ocean, UV) and returns the values
    data = api.gather_data(lat, long, arguments)
    ocean_data = data[0]
    # uv_index = data[1]
    data_dict = data[2]

    # Non-JSON output
    if arguments["json_output"] == 0:
        helper.print_outputs(lat, long, coordinates, ocean_data, arguments)
        return data_dict
    # JSON Output
    else:
        json_output = helper.json_output(data_dict)
        return json_output


if __name__ == "__main__":
    run()
