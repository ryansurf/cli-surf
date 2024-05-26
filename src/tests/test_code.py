"""
QA tests
Make sure pytest is installed: pip install pytest
Run pytest: pytest
"""

import sys
import json

sys.path.append("../backend")

from unittest.mock import patch
import io
import time
from main import main
from helper import extract_decimal, query_to_args_list
from api import get_coordinates, get_uv, ocean_information


def test_query_to_args_list_with_non_empty_params():
    """
    Test if query_to_args_list function correctly converts non-empty query parameters to a list.
    """
    args = query_to_args_list("location=new_york,hide_height,show_large_wave")
    assert args == ["location=new_york,hide_height,show_large_wave"]


def test_query_to_args_list_with_empty_params():
    """
    Test if query_to_args_list function correctly handles empty query parameters and returns an empty list.
    """
    args = query_to_args_list("")
    assert args == []


def test_invalid_input():
    """
    Test if decimal input prints proper invalid input message
    """
    with patch("sys.stdout", new=io.StringIO()) as fake_stdout:
        extract_decimal(["decimal=NotADecimal"])
        printed_output = fake_stdout.getvalue().strip()
        assert printed_output == "Invalid value for decimal. Please provide an integer."


def test_default_input():
    decimal = extract_decimal([])
    assert 1 == decimal


def test_get_coordinates():
    coordinates = get_coordinates(["loc=santa_cruz"])
    lat = coordinates[0]
    long = coordinates[1]
    assert isinstance(lat, (int, float))
    assert isinstance(long, (int, float))


def test_get_uv():
    uv = get_uv(37, 122, 2)
    assert isinstance(uv, (int, float))


def test_ocean_information():
    ocean = ocean_information(37, 122, 2)
    assert isinstance(ocean[0], (int, float))
    assert isinstance(ocean[1], (int, float))
    assert isinstance(ocean[2], (int, float))


def test_main_output():
    """
    Main() returns a dictionary of: location, height, period, etc.
    This functions checks if the dictionary is returned and is populated
    """
    data_dict = main(36.95, -122.02)
    time.sleep(5)
    assert len(data_dict) >= 5
