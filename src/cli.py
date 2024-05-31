"""
Main module
"""

import sys

from src import api, helper, settings

# Load environment variables from .env file
env = settings.GPTSettings()
gpt_prompt = env.GPT_PROMPT
api_key = env.API_KEY
model = env.GPT_MODEL

gpt_info = [api_key, model]


def run(lat=0, long=0):
    """
    Main function
    """
    # Seperates the cli args into a list
    args = helper.seperate_args(sys.argv)

    #  return coordinates, lat, long, city
    location = api.seperate_args_and_get_location(args)

    # Set location returns: city, lat, long
    set_location = helper.set_location(location)
    city = set_location[0]

    # Check if lat and long are set to defaults(no argumentes passed in main())
    if lat == 0 and long == 0:
        lat, long = set_location[1], set_location[2]

    # Sets arguments = dictionary with all the CLI args(show_wave, city, ect.)
    arguments = helper.arguments_dictionary(lat, long, city, args)

    # Makes calls to the apis(ocean, UV) and returns the values in a dictionary
    ocean_data_dict = api.gather_data(lat, long, arguments)

    # Non-JSON output
    if arguments["json_output"] == 0:
        helper.print_outputs(
            city, ocean_data_dict, arguments, gpt_prompt, gpt_info
        )
        return ocean_data_dict
    else:
        # print the output in json format!
        json_output = helper.json_output(ocean_data_dict)
        return json_output


if __name__ == "__main__":
    run()
