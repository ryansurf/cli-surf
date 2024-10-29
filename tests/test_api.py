"""
QA tests for api.py
Make sure pytest is installed: pip install pytest
Run pytest: pytest
"""
import unittest
from openmeteo_requests.Client import OpenMeteoRequestsError
from unittest.mock import patch

from src.api import (
    forecast,
    gather_data,
    get_coordinates,
    get_uv,
    get_uv_history,
    ocean_information_history,
    ocean_information,
    seperate_args_and_get_location,
)
from src.helper import arguments_dictionary


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


def test_forecast():
    """
    Test forecast() at an arbitrary location(palm beach),
    ensures it returns 7 days of heights/directions/periods
    """
    len_of_forecast_list = 7
    fc = forecast(26.705, -80.036, 1, 7)
    heights = fc["wave_height_max"]
    directions = fc["wave_direction_dominant"]
    periods = fc["wave_period_max"]
    assert len(heights) == len_of_forecast_list
    assert len(directions) == len_of_forecast_list
    assert len(periods) == len_of_forecast_list


def test_gather_data():
    """
    Gather data needs the arguments dictionary as input,
    so we will get this by calling arguments_dictionary()
    from helper.py with arbitrary arguments
    """
    lat = 33.37
    long = -117.57
    arguments = arguments_dictionary(lat, long, "San Clemente", [])
    ocean_data_dict = gather_data(lat, long, arguments)
    assert ocean_data_dict["Location"] == "San Clemente"
    assert ocean_data_dict["Lat"] == lat
    assert ocean_data_dict["Long"] == long


def test_seperate_args_and_get_location():
    """
    Test with an abritrary location
    """
    location = ["location=pleasure_point_california"]
    location_data = seperate_args_and_get_location(location)
    lat = location_data["lat"]
    long = location_data["long"]
    city = location_data["city"]
    assert isinstance(lat, (int, float))
    assert isinstance(long, (int, float))
    assert "Pleasure Point" in str(city)


class TestGetUVHistory(unittest.TestCase):

    def test_basic_functionality(self):
        # Test 1: Basic Functionality for Perth
        uv = get_uv_history(31.9505, 115.8605, 2)  # Perth coordinates
        self.assertIsInstance(uv, str)

    def test_invalid_coordinates(self):
        # Test 2: Invalid Coordinates using assertRaises
        with self.assertRaises(OpenMeteoRequestsError):
            get_uv_history(1000, -2000, 2)

    @patch('src.api.testing', new=0)  # Set testing variable to 0
    def test_get_uv_history(self):
        result = get_uv_history(31.9505, 115.8605, 1)
        expected_result = '0.6'
        self.assertEqual(result, expected_result)

class TestGetWaveHistory(unittest.TestCase):

    def test_basic_functionality(self):
        # Test 1: Basic Functionality for Perth
        waves = ocean_information_history(31.9505, 115.8605, 2)  # Perth coordinates
        self.assertIsNotNone(waves[0])
        self.assertIsNotNone(waves[1])
        self.assertIsNotNone(waves[2])

    def test_invalid_coordinates(self):
        # Test 2: Invalid Coordinates using assertRaises
        with self.assertRaises(OpenMeteoRequestsError):
            get_uv_history(1000, -2000, 2)

    def test_response_format(self):
        # Test 4: Response Format
        waves = ocean_information_history(31.9505, 115.8605, 2)  # Perth coordinates
        self.assertIsInstance(waves, list)
        self.assertGreater(len(waves), 0)
        self.assertEqual(len(waves),3)

    @patch('src.api.testing', new=0)  # Set testing variable to 0
    def test_ocean_information_history(self):
        result = ocean_information_history(31.9505, 115.8605, 1)
        expected_result = ['0.6', '0.6', '0.6']
        self.assertEqual(result, expected_result)