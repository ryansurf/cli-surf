"""
QA tests for helper.py
Make sure pytest is installed: pip install pytest
Run pytest: pytest
"""

import io
from unittest.mock import patch

from src import cli, helper
from src.helper import set_output_values


def test_invalid_input():
    """
    Test if decimal input prints proper invalid input message
    """
    with patch("sys.stdout", new=io.StringIO()) as fake_stdout:
        helper.extract_decimal(["decimal=NotADecimal"])
        printed_output = fake_stdout.getvalue().strip()
        expected = "Invalid value for decimal. Please provide an integer."
        assert printed_output == expected


def test_default_input():
    """
    Test that when no decimal= in args, 1 is the default
    """
    decimal = helper.extract_decimal([])
    assert 1 == decimal


def test_json_output():
    """
    Passing "JSON" as an argument to cli.run,
    we check if a JSON object returns.
    We also check for expected outputs,
    like a lat that is a float/int
    """
    # Hardcode lat and long for location.
    # If not, when test are ran in Github Actions
    # We get an error(because server probably isn't near ocean)
    json_output = cli.run(36.95, -121.97, ["", "json"])
    assert type(json_output["Lat"]) in {int, float}
    assert isinstance(json_output["Location"], str)


def test_print_gpt():
    """
    Tests the simple_gpt()
    """
    surf_data = {
        "Location": "test",
        "Height": "test",
        "Swell Direction": "test",
        "Period": "test",
        "Unit": "test",
    }
    gpt_prompt = "Please output 'gpt works'"
    gpt_info = [None, ""]
    gpt_response = helper.print_gpt(surf_data, gpt_prompt, gpt_info)
    assert "gpt works" in gpt_response


def test_set_output_values_show_past_uv():
    args = ["show_past_uv"]
    arguments_dictionary = {}
    expected = {"show_past_uv": 1}
    result = set_output_values(args, arguments_dictionary)
    assert result == expected


def test_set_output_values_hide_past_uv():
    args = ["hide_past_uv"]
    arguments_dictionary = {}
    expected = {"show_past_uv": 0}
    result = set_output_values(args, arguments_dictionary)
    assert result == expected


def test_set_output_values_show_height_history():
    args = ["show_height_history"]
    arguments_dictionary = {}
    expected = {"show_height_history": 1}
    result = set_output_values(args, arguments_dictionary)
    assert result == expected


def test_set_output_values_hide_height_history():
    args = ["hide_height_history"]
    arguments_dictionary = {}
    expected = {"show_height_history": 0}
    result = set_output_values(args, arguments_dictionary)
    assert result == expected


def test_set_output_values_show_direction_history():
    args = ["show_direction_history"]
    arguments_dictionary = {}
    expected = {"show_direction_history": 1}
    result = set_output_values(args, arguments_dictionary)
    assert result == expected


def test_set_output_values_hide_direction_history():
    args = ["hide_direction_history"]
    arguments_dictionary = {}
    expected = {"show_direction_history": 0}
    result = set_output_values(args, arguments_dictionary)
    assert result == expected


def test_set_output_values_show_period_history():
    args = ["show_period_history"]
    arguments_dictionary = {}
    expected = {"show_period_history": 1}
    result = set_output_values(args, arguments_dictionary)
    assert result == expected


def test_set_output_values_hide_period_history():
    args = ["hide_period_history"]
    arguments_dictionary = {}
    expected = {"show_period_history": 0}
    result = set_output_values(args, arguments_dictionary)
    assert result == expected

def test_set_output_values_combined_arguments():
    args = [
        "show_past_uv",
        "show_height_history",
        "show_direction_history",
        "show_period_history",
    ]
    arguments_dictionary = {}
    expected = {
        "show_past_uv": 1,
        "show_height_history": 1,
        "show_direction_history": 1,
        "show_period_history": 1,
    }
    result = set_output_values(args, arguments_dictionary)
    assert result == expected

def test_round_decimal():
    # Standard rounding
    rounded = helper.round_decimal([2.4345, 30.2789], 2)
    assert rounded == [2.43, 30.28]

    # Empty input
    assert helper.round_decimal([], 2) == []

    # Rounding to zero decimals
    assert helper.round_decimal([2.5, 3.7, -1.2], 0) == [2.0, 4.0, -1.0]

    # Midpoint values
    assert helper.round_decimal([2.5], 0) == [2.0] or helper.round_decimal([2.5], 0) == [3.0]  # Depending on rounding method
    assert helper.round_decimal([2.45], 1) == [2.4] or helper.round_decimal([2.45], 1) == [2.5]  # Depending on rounding method

    # Negative numbers
    assert helper.round_decimal([-2.555, -3.444], 2) == [-2.56, -3.44]

    # Integer inputs
    assert helper.round_decimal([1, 2, 3], 2) == [1.0, 2.0, 3.0]

def test_print_location_show_city_false():
    with patch("sys.stdout", new=io.StringIO()) as fake_stdout:
        helper.print_location("Not a City", 0)
        output = fake_stdout.getvalue()
        assert output.strip() == ""

def test_get_forecast_days_valid():
    args = ["forecast=3"]
    assert helper.get_forecast_days(args) == 3

def test_get_forecast_days_default():
    assert helper.get_forecast_days([]) == 0
