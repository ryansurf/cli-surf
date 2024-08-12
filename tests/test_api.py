"""
QA tests for api.py
Make sure pytest is installed: pip install pytest
Run pytest: pytest
"""

from src.api import (
    forecast,
    gather_data,
    get_coordinates,
    get_uv,
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