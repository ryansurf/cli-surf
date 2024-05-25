"""
QA tests
Make sure pytest is installed: pip install pytest
Run pytest: pytest
"""

import sys

sys.path.append("../backend")

import unittest
from unittest.mock import patch
import io
import threading
import requests
import time
import subprocess
import os
from main import main
from helper import extract_decimal
from api import get_coordinates, get_uv, ocean_information


def test_invalid_input():
        with patch("sys.stdout", new=io.StringIO()) as fake_stdout:
            extract_decimal(["decimal=NotADecimal"])
            printed_output = fake_stdout.getvalue().strip()
            assert(
                printed_output == "Invalid value for decimal. Please provide an integer."
            )

def test_default_input():
        decimal = extract_decimal([])
        assert 1 == decimal

def test_get_coordinates():
    coordinates = get_coordinates(["loc=santa_cruz"])
    lat = coordinates[0]
    long = coordinates[1]
    assert(isinstance(lat, (int, float)))
    assert(isinstance(long, (int, float)))

def test_get_uv():
    uv = get_uv(37, 122, 2)
    assert(isinstance(uv, (int, float)))

def test_ocean_information():
    ocean = ocean_information(37, 122, 2)
    assert(isinstance(ocean[0], (int, float)))
    assert(isinstance(ocean[1], (int, float)))
    assert(isinstance(ocean[2], (int, float)))

def test_main():
    """
    Main() returns a dictionary of: location, height, period, etc.
    This functions checks if the dictionary is returned and is populated
    """
    data_dict = main()
    time.sleep(5)
    assert(len(data_dict) >= 5)