"""
QA tests for api.py
Make sure pytest is installed: pip install pytest
Run pytest: pytest
"""

import logging
from http import HTTPStatus
from unittest.mock import Mock, patch, MagicMock

import numpy as np
import pytest
from openmeteo_requests.Client import OpenMeteoRequestsError

from src import api

from src.api import (
    _forecast_cache,
    _ocean_history_cache,
    default_location,
    forecast,
    gather_data,
    get_coordinates,
    get_uv,
    get_uv_history,
    ocean_information,
    ocean_information_history,
    seperate_args_and_get_location,
    uv_history_cache,
)
from src.helper import arguments_dictionary


@pytest.mark.parametrize(
    ("status_code", "json_data", "expected_result"),
    [
        (
            HTTPStatus.OK,
            {"loc": "43.03,-72.001", "city": "New York"},
            ["43.03", "-72.001", "New York"],
        ),
        (HTTPStatus.BAD_REQUEST, {}, "No data"),
    ],
)
def test_default_location_mocked(
    mocker, status_code, json_data, expected_result
):
    # Arrange: Mock the response from the API
    mock_response = Mock()
    mock_response.status_code = status_code
    mock_response.json = Mock(return_value=json_data)

    # Mock the 'requests.get' method
    mock_requests = mocker.patch("requests.get", return_value=mock_response)

    # Act: Call the function
    result = default_location()

    # Assert: Verify function returns correct location data
    assert result == expected_result

    # Assert: Verify 'requests.get' is called with correct arguments
    mock_requests.assert_called_once_with("https://ipinfo.io/json", timeout=10)

"""
return [
                    location.latitude,
                    location.longitude,
                    location.raw["name"],
                ]
"""

@patch("src.api.Nominatim")
def test_get_coordinates(mock_nominatim):
    # setup the fake location objects geocode returns
    mock_location = MagicMock()
    mock_location.latitude = 32.41
    mock_location.longitude = -84.92
    mock_location.raw = {"name": "santa_cruz"}

    # Nominatim() returns an instance, .geocode() returns mock_location
    mock_nominatim.return_value.geocode.return_value = mock_location

    get_coordinates.cache_clear()
    result = get_coordinates(("loc=santa_cruz",))

    assert result == [32.41, -84.92, "santa_cruz"]
    assert isinstance(result[0], (int, float))
    assert isinstance(result[1], (int, float))
    assert isinstance(result[2], str)


@patch("src.api._create_openmeteo_client")
def test_get_uv(mock_create_client):
    mock_variable = MagicMock()
    mock_variable.Value.return_value = 5.0  # real number so round() works

    mock_current = MagicMock()
    mock_current.Variables.return_value = mock_variable  # .Variables(0) → mock_variable

    mock_response = MagicMock()
    mock_response.Current.return_value = mock_current

    mock_client = MagicMock()
    mock_client.weather_api.return_value = [mock_response]
    mock_create_client.return_value = mock_client

    result = get_uv(31.41, -84.92, 2, "imperial")

    assert result == 5.0
    assert isinstance(result, float)




@patch("src.api._create_openmeteo_client")
def test_ocean_information(mock_create_client):
    # fake each variable (height, direction, period)
    mock_var_0 = MagicMock()
    mock_var_0.Value.return_value = 3.5

    mock_var_1 = MagicMock()
    mock_var_1.Value.return_value = 180.0

    mock_var_2 = MagicMock()
    mock_var_2.Value.return_value = 12.0

    # Variables(0), Variables(1), Variables(2) return different mocks
    mock_current = MagicMock()
    mock_current.Variables.side_effect = [mock_var_0, mock_var_1, mock_var_2]

    mock_response = MagicMock()
    mock_response.Current.return_value = mock_current

    mock_client = MagicMock()
    mock_client.weather_api.return_value = [mock_response]
    mock_create_client.return_value = mock_client

    result = ocean_information(31.41, -84.92, 2, "imperial")

    assert result == [3.5, 180.0, 12.0]


@patch("src.api._create_openmeteo_client")
def test_forecast(mock_create_client):
    """
    Test forecast() at an arbitrary location(palm beach),
    ensures it returns 7 days of heights/directions/periods
    """
    fake_array = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0])

    mock_marine_var = MagicMock()
    mock_marine_var.ValuesAsNumpy.return_value = fake_array
    mock_marine_daily = MagicMock()
    mock_marine_daily.Variables.return_value = mock_marine_var
    mock_marine_daily.Time.return_value = 1700000000
    mock_marine_daily.TimeEnd.return_value = 1700604800
    mock_marine_daily.Interval.return_value = 86400
    mock_marine_response = MagicMock()
    mock_marine_response.Daily.return_value = mock_marine_daily

    mock_general_var = MagicMock()
    mock_general_var.ValuesAsNumpy.return_value = fake_array
    mock_general_daily = MagicMock()
    mock_general_daily.Variables.return_value = mock_general_var
    mock_general_response = MagicMock()
    mock_general_response.Daily.return_value = mock_general_daily

    mock_client = MagicMock()
    mock_client.weather_api.side_effect = [
        [mock_marine_response],
        [mock_general_response],
    ]
    mock_create_client.return_value = mock_client

    _forecast_cache.clear()
    fc = forecast(26.705, -80.036, 1, 7)

    assert len(fc["wave_height_max"]) == 7
    assert len(fc["wave_direction_dominant"]) == 7
    assert len(fc["wave_period_max"]) == 7


@patch("src.api.ocean_information", return_value=[3.5, 180.0, 12.0])
@patch("src.api.get_uv", return_value=5.0)
@patch("src.api.get_hourly_forecast", return_value={"cloud_cover": 50.0, "visibility": 10.0})
@patch("src.api.current_wind_temp", return_value=[70.0, 10.0, 180.0])
@patch("src.api.get_rain", return_value=(0.1, 30.0))
@patch("src.api.forecast", return_value={})
@patch("src.api.ocean_information_history", return_value=["3.5", "180.0", "12.0"])
@patch("src.api.get_uv_history", return_value="5.0")
@patch("src.helper.forecast_to_json", return_value={})
def test_gather_data(
    mock_ftj, mock_uv_hist, mock_ocean_hist, mock_fc,
    mock_rain, mock_wind, mock_hourly, mock_uv, mock_ocean,
):
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


@patch("src.api.Nominatim")
def test_seperate_args_and_get_location(mock_nominatim):
    """
    Test with an arbitrary location
    """
    mock_location = MagicMock()
    mock_location.latitude = 36.97
    mock_location.longitude = -121.98
    mock_location.raw = {"name": "Pleasure Point"}
    mock_nominatim.return_value.geocode.return_value = mock_location

    get_coordinates.cache_clear()
    location = ["location=pleasure_point_california"]
    location_data = seperate_args_and_get_location(location)
    lat = location_data["lat"]
    long = location_data["long"]
    city = location_data["city"]
    assert isinstance(lat, (int, float))
    assert isinstance(long, (int, float))
    assert "Pleasure Point" in str(city)


@patch("src.api._create_openmeteo_client")
def test_get_uv_history_basic_functionality(mock_create_client):
    """
    Test the basic functionality of the get_uv_history function.

    This test verifies that the function returns a string
    when provided with valid latitude and longitude coordinates.
    """
    fake_uv = np.array([3.5] * 24)
    mock_hourly = MagicMock()
    mock_hourly.Variables.return_value.ValuesAsNumpy.return_value = fake_uv
    mock_response = MagicMock()
    mock_response.Hourly.return_value = mock_hourly
    mock_client = MagicMock()
    mock_client.weather_api.return_value = [mock_response]
    mock_create_client.return_value = mock_client

    uv_history_cache.clear()
    uv = get_uv_history(31.9505, 115.8605, 2)
    assert isinstance(uv, str)


@patch("src.api._create_openmeteo_client")
def test_get_uv_history_invalid_coordinates(mock_create_client):
    """
    Test get_uv_history with invalid coordinates.

    This test checks that the function raises an OpenMeteoRequestsError
    when provided with latitude and longitude values that are out of range.
    """
    mock_client = MagicMock()
    mock_client.weather_api.side_effect = OpenMeteoRequestsError("out of range")
    mock_create_client.return_value = mock_client

    uv_history_cache.clear()
    with pytest.raises(OpenMeteoRequestsError):
        get_uv_history(1000, -2000, 2)


@patch("src.api._create_openmeteo_client")
@patch("src.api.testing", new=0)  # Set testing variable to 0
def test_get_uv_history_api_response(mock_create_client):
    """
    Test how get_uv_history handles API response.

    This test verifies that the function returns the expected values
    when called with valid coordinates while patching the API call request.
    """
    mock_create_client.return_value = MagicMock()

    uv_history_cache.clear()
    result = get_uv_history(31.9505, 115.8605, 1)
    expected_result = "0.6"
    assert result == expected_result


@patch("src.api._create_openmeteo_client")
def test_ocean_information_history_basic_functionality(mock_create_client):
    """
    Test the basic functionality of the ocean_information_history function.

    This test checks that the function returns actual values for
    the wave data points when provided with valid coordinates.
    """
    fake_array = np.array([1.5] * 24)
    mock_hourly = MagicMock()
    mock_hourly.Variables.return_value.ValuesAsNumpy.return_value = fake_array
    mock_response = MagicMock()
    mock_response.Hourly.return_value = mock_hourly
    mock_client = MagicMock()
    mock_client.weather_api.return_value = [mock_response]
    mock_create_client.return_value = mock_client

    _ocean_history_cache.clear()
    waves = ocean_information_history(31.9505, 115.8605, 2)
    assert waves[0] is not None
    assert waves[1] is not None
    assert waves[2] is not None


@patch("src.api._create_openmeteo_client")
def test_ocean_information_history_invalid_coordinates(mock_create_client):
    """
    Test ocean_information_history with invalid coordinates.

    This test ensures that the function raises an OpenMeteoRequestsError
    when provided with latitude and longitude values that are out of range.
    """
    mock_client = MagicMock()
    mock_client.weather_api.side_effect = OpenMeteoRequestsError("out of range")
    mock_create_client.return_value = mock_client

    _ocean_history_cache.clear()
    with pytest.raises(OpenMeteoRequestsError):
        ocean_information_history(1000, -2000, 2)


@patch("src.api._create_openmeteo_client")
def test_ocean_information_history_response_format(mock_create_client):
    """
    Test the response format of ocean_information_history.

    This test verifies that the function returns a list with a
    specific number of elements when called with valid coordinates.
    """
    fake_array = np.array([2.0] * 24)
    mock_hourly = MagicMock()
    mock_hourly.Variables.return_value.ValuesAsNumpy.return_value = fake_array
    mock_response = MagicMock()
    mock_response.Hourly.return_value = mock_hourly
    mock_client = MagicMock()
    mock_client.weather_api.return_value = [mock_response]
    mock_create_client.return_value = mock_client

    _ocean_history_cache.clear()
    waves = ocean_information_history(31.9505, 115.8605, 2)
    expected_wave_count = 3
    assert isinstance(waves, list)
    assert len(waves) > 0
    assert len(waves) == expected_wave_count


@patch("src.api._create_openmeteo_client")
@patch("src.api.testing", new=0)  # Set testing variable to 0
def test_ocean_information_history(mock_create_client):
    """
    Test how ocean_information_history handles API response.

    This test verifies that the function returns the expected values
    when called with valid coordinates while patching the API call request.
    """
    mock_create_client.return_value = MagicMock()

    _ocean_history_cache.clear()
    result = ocean_information_history(31.9505, 115.8605, 1)
    expected_result = ["0.6", "0.6", "0.6"]
    assert result == expected_result


# ---------------------------------------------------------------------------
# Error / fallback paths
# ---------------------------------------------------------------------------


def test_get_coordinates_no_args_falls_back_to_default(mocker):
    """get_coordinates falls back to default when no location= arg is given."""
    mocker.patch(
        "src.api.default_location", return_value=[0.0, 0.0, "Default City"]
    )
    get_coordinates.cache_clear()
    result = get_coordinates(())
    assert result == [0.0, 0.0, "Default City"]


def test_get_coordinates_invalid_location_falls_back_to_default(
    mocker, caplog
):
    """get_coordinates logs a warning and falls back when geocoding fails."""
    mock_geo = mocker.patch("src.api.Nominatim")
    mock_geo.return_value.geocode.return_value = None
    mocker.patch(
        "src.api.default_location", return_value=[0.0, 0.0, "Default City"]
    )

    get_coordinates.cache_clear()
    with caplog.at_level(logging.WARNING, logger="src.api"):
        result = get_coordinates(tuple(["location=nowhere_xyz_invalid"]))

    assert result == [0.0, 0.0, "Default City"]
    assert "Invalid location" in caplog.text


def test_get_uv_returns_no_data_on_value_error(mocker):
    """get_uv returns 'No data' when Open-Meteo client raises ValueError."""
    mock_client = mocker.patch("src.api._create_openmeteo_client")
    mock_client.return_value.weather_api.side_effect = ValueError("bad coords")
    assert get_uv(1000, -2000, 2) == "No data"


def test_get_uv_history_returns_no_data_on_value_error(mocker):
    """get_uv_history returns 'No data' when the API raises ValueError."""
    uv_history_cache.clear()
    mock_client = mocker.patch("src.api._create_openmeteo_client")
    mock_client.return_value.weather_api.side_effect = ValueError("bad coords")
    assert get_uv_history(31.9505, 115.8605, 2) == "No data"


def test_ocean_information_returns_no_data_on_value_error(mocker):
    """ocean_information returns 'No data' when the API raises ValueError."""
    mock_client = mocker.patch("src.api._create_openmeteo_client")
    mock_client.return_value.weather_api.side_effect = ValueError("bad coords")
    assert ocean_information(1000, -2000, 2) == "No data"


def test_ocean_information_history_returns_no_data_on_value_error(mocker):
    """ocean_information_history returns 'No data' on ValueError."""
    mock_client = mocker.patch("src.api._create_openmeteo_client")
    mock_client.return_value.weather_api.side_effect = ValueError("bad coords")
    assert ocean_information_history(1000, -2000, 2) == "No data"
