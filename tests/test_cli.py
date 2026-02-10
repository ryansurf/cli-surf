"""
QA tests for cli.py
Make sure pytest is installed: pip install pytest
Run pytest: pytest
"""

import time

from src import cli


# TODO: fix broken test

# def test_cli_output():
#     """
#     Main() returns a dictionary of: location, height, period, etc.
#     This functions checks if the dictionary is returned and is populated
#     """
#     expected = 5
#     # Hardcode lat and long for location.
#     # If not, when test are ran in Github Actions
#     # We get an error(because server probably isn't near ocean)
#     data_dict = cli.run(36.95, -121.97)[0]
#     time.sleep(5)
#     assert len(data_dict) >= expected
