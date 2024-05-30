"""
QA tests for api.py
Make sure pytest is installed: pip install pytest
Run pytest: pytest
"""

from src.api import get_coordinates, get_uv, ocean_information


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
