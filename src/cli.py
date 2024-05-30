"""
Main module
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src import api, helper, settings

# Load environment variables from .env file
env = settings.GPTSettings()
gpt_prompt = env.GPT_PROMPT


def run(lat=0, long=0):
    """
    Main function
    """
    # Seperates the cli args into a list
    args = helper.seperate_args(sys.argv)

    #  return coordinates, lat, long, city
    location = api.seperate_args_and_get_location(args)

    set_location = helper.set_location(location)
    city = set_location[0]

    # Check if lat and long are set to defaults(no argumentes passed in main())
    if lat == 0 and long == 0:
        lat, long = set_location[1], set_location[2]

    # Sets ocean = dictionary with
    arguments = helper.arguments_dictionary(lat, long, city, args)
    # Updates the ocean dict with the valeus from the arguments
    arguments = helper.set_output_values(args, arguments)

    lat = float(lat)
    long = float(long)
    # Makes calls to the apis(ocean, UV) and returns the values
    data_dict = api.gather_data(lat, long, arguments)

    # Non-JSON output
    if arguments["json_output"] == 0:
        helper.print_outputs(city, data_dict, arguments, gpt_prompt)
        return data_dict
    # JSON Output
    else:
        json_output = helper.json_output(data_dict)
        return json_output


if __name__ == "__main__":
    run()
