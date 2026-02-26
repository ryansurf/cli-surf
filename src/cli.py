"""
Main module
"""

import sys

from src import api, helper, settings
from src.db import operations

# Load environment variables from .env file
env = settings.GPTSettings()
gpt_prompt = env.GPT_PROMPT
api_key = env.API_KEY
model = env.GPT_MODEL

# Check for DB
env_db = settings.DatabaseSettings()
db_uri = env_db.DB_URI
if db_uri:
    db_handler = operations.SurfReportDatabaseOps()

gpt_info = [api_key, model]


def run(lat=0, long=0, args=None):
    """
    Main function
    """
    if args is None:
        args = helper.separate_args(sys.argv)
    else:
        args = helper.separate_args(args)

    location = api.seperate_args_and_get_location(args)

    city, loc_lat, loc_long = helper.set_location(location)
    if lat == 0 and long == 0:
        lat, long = loc_lat, loc_long

    # Sets arguments = dictionary with all the CLI args (show_wave, city, etc.)
    arguments = helper.arguments_dictionary(lat, long, city, args)

    # Makes API calls (ocean, UV) and returns the values in a dictionary
    ocean_data_dict = api.gather_data(lat, long, arguments)

    # Build JSON output once — used by both branches and optional DB insert
    json_out = helper.json_output(ocean_data_dict, print_output=False)

    if arguments["json_output"] == 0:
        response = helper.print_outputs(
            ocean_data_dict, arguments, gpt_prompt, gpt_info
        )
        if db_uri:
            db_handler.insert_report(json_out)
        return ocean_data_dict, response
    else:
        if db_uri:
            db_handler.insert_report(json_out)
        return json_out


if __name__ == "__main__":
    run()
