"""
QA tests for helper.py
Make sure pytest is installed: pip install pytest
Run pytest: pytest
"""

import io
import sys
from io import StringIO
from unittest.mock import patch

from src.helper import (
    extract_decimal,
    print_location,
    print_ocean_data,
    set_output_values,
)


def test_invalid_input():
    """
    Test if decimal input prints proper invalid input message
    """
    with patch("sys.stdout", new=io.StringIO()) as fake_stdout:
        extract_decimal(["decimal=NotADecimal"])
        printed_output = fake_stdout.getvalue().strip()
        expected = "Invalid value for decimal. Please provide an integer."
        assert printed_output == expected


def test_default_input():
    """
    Test that when no decimal= in args, 1 is the default
    """
    decimal = extract_decimal([])
    assert 1 == decimal


def test_print_location():
    """
    Test the print_location function to check if the city name is printed
    when the show_city parameter is 1
    """

    city = "Perth"
    show_city = 1
    captured_output = io.StringIO()
    sys.stdout = captured_output
    print_location(city, show_city)
    sys.stdout = sys.__stdout__
    expected_output = "Location: Perth"
    assert captured_output.getvalue().strip() == expected_output.strip()

def test_print_location_show_city_0():
    """
    Test the print_location function to check if the city name prints
    location not available when the show_city parameter is 0
    """
    city = "Perth"
    show_city = 0
    captured_output = io.StringIO()
    sys.stdout = captured_output
    print_location(city, show_city)
    sys.stdout = sys.__stdout__
    expected_output = "Not Available"
    assert captured_output.getvalue().strip() == expected_output.strip()


def test_set_output_values():
    """
    Tests the set_output_values function to verify that it correctly
    sets values in the output dictionary based on the provided list of
    input arguments (args)
    """
    args = ["hw", "show_large_wave", "huv"]
    arguments = {}
    expected = {"show_wave": 0, "show_large_wave": 1, "show_uv": 0}
    assert set_output_values(args, arguments) == expected


def test_print_ocean_data():
    """
    Test that checks if the print_ocean_data function prints all
    the ocean data
    """
    arguments_dict = {
        "show_uv": "1",
        "show_height": "1",
        "show_direction": "1",
        "show_period": "0",
        "show_air_temp": "1",
        "show_wind_speed": "1",
        "show_wind_direction": "0",
    }

    ocean_data = {
        "UV Index": 5,
        "Height": 2.5,
        "Swell Direction": "NE",
        "Air Temperature": 25,
        "Wind Speed": 15,
    }

    expected_output = (
        "UV index: 5\n"
        "Wave Height: 2.5\n"
        "Wave Direction: NE\n"
        "Air Temp: 25\n"
        "Wind Speed: 15\n"
    )

    captured_output = StringIO()
    sys.stdout = captured_output
    print_ocean_data(arguments_dict, ocean_data)
    sys.stdout = sys.__stdout__
    assert captured_output.getvalue() == expected_output
