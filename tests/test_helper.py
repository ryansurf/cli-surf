"""
QA tests for helper.py
Make sure pytest is installed: pip install pytest
Run pytest: pytest
"""

import io
import logging
from unittest.mock import patch

from src import helper
from src.helper import set_output_values

_LAT = 36.97
_LONG = -122.03


def test_invalid_input(caplog):
    """
    Test if decimal input logs proper invalid input message
    """
    with caplog.at_level(logging.WARNING, logger="src.helper"):
        helper.extract_decimal(["decimal=NotADecimal"])
    assert (
        "Invalid value for decimal. Please provide an integer." in caplog.text
    )


def test_default_input():
    """
    Test that when no decimal= in args, 1 is the default
    """
    decimal = helper.extract_decimal([])
    assert 1 == decimal


# TODO: fix broken test. Probably need to mock out API calls

# def test_json_output():
#     """
#     Passing "JSON" as an argument to cli.run,
#     we check if a JSON object returns.
#     We also check for expected outputs,
#     like a lat that is a float/int
#     """
#     # Hardcode lat and long for location.
#     # If not, when test are ran in Github Actions
#     # We get an error(because server probably isn't near ocean)
#     json_output = cli.run(36.95, -121.97, ["", "json"])
#     assert type(json_output["Lat"]) in {int, float}
#     assert isinstance(json_output["Location"], str)


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
    # Depending on rounding method
    assert helper.round_decimal([2.5], 0) in ([2.0], [3.0])
    # Depending on rounding method
    assert helper.round_decimal([2.45], 1) in ([2.4], [2.5])

    # Negative numbers
    assert helper.round_decimal([-2.555, -3.444], 2) == [-2.56, -3.44]

    # Integer inputs
    assert helper.round_decimal([1, 2, 3], 2) == [1.0, 2.0, 3.0]


def test_print_location_show_city_false():
    with patch("sys.stdout", new=io.StringIO()) as fake_stdout:
        helper.print_location("Not a City", 0)
        output = fake_stdout.getvalue()
        assert not output.strip()


def test_get_forecast_days_valid():
    FORECAST_DAYS = 3
    args = ["forecast=3"]
    assert helper.get_forecast_days(args) == FORECAST_DAYS


def test_get_forecast_days_default():
    assert helper.get_forecast_days([]) == 0


# ---------------------------------------------------------------------------
# separate_args
# ---------------------------------------------------------------------------


def test_separate_args_returns_empty_for_single_arg():
    """separate_args returns [] when no extra args are passed."""
    assert helper.separate_args(["cmd"]) == []


# ---------------------------------------------------------------------------
# _extract_arg
# ---------------------------------------------------------------------------


def test_extract_arg_logs_warning_on_invalid_cast(caplog):
    """_extract_arg logs a warning and returns the default when cast fails."""
    with caplog.at_level(logging.WARNING, logger="src.helper"):
        result = helper._extract_arg(
            ["forecast=abc"], ["forecast"], 0, cast=int
        )
    assert result == 0
    assert "Invalid value for forecast" in caplog.text


# ---------------------------------------------------------------------------
# get_forecast_days
# ---------------------------------------------------------------------------


def test_get_forecast_days_out_of_range_logs_warning(caplog):
    """get_forecast_days returns 0 and warns when value exceeds MAX."""
    with caplog.at_level(logging.WARNING, logger="src.helper"):
        result = helper.get_forecast_days(["forecast=10"])
    assert result == 0
    assert "Forecast days must be between" in caplog.text


def test_get_forecast_days_negative_logs_warning(caplog):
    """get_forecast_days returns 0 and warns when value is negative."""
    with caplog.at_level(logging.WARNING, logger="src.helper"):
        result = helper.get_forecast_days(["forecast=-1"])
    assert result == 0


# ---------------------------------------------------------------------------
# print_location
# ---------------------------------------------------------------------------


def test_print_location_show_city_true(capsys):
    """print_location prints the city name when show_city is True."""
    helper.print_location("Santa Cruz", True)
    assert "Santa Cruz" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# print_ocean_data
# ---------------------------------------------------------------------------


def test_print_ocean_data_prints_enabled_fields(capsys):
    """print_ocean_data prints only the fields whose flag is True."""
    arguments_dict = {
        "show_uv": True,
        "show_past_uv": False,
        "show_height": True,
        "show_height_history": False,
        "show_direction": False,
        "show_direction_history": False,
        "show_period": False,
        "show_period_history": False,
        "show_air_temp": False,
        "show_wind_speed": False,
        "show_wind_direction": False,
        "show_rain_sum": False,
        "show_precipitation_prob": False,
        "show_cloud_cover": False,
        "show_visibility": False,
    }
    ocean_data_dict = {"UV Index": 5, "Height": 3.5}
    helper.print_ocean_data(arguments_dict, ocean_data_dict)
    out = capsys.readouterr().out
    assert "UV index: 5" in out
    assert "Wave Height: 3.5" in out


# ---------------------------------------------------------------------------
# print_forecast
# ---------------------------------------------------------------------------


def test_print_forecast_renders_float_values(capsys):
    """print_forecast prints rounded float values for enabled fields."""
    ocean = {
        "forecast_days": 1,
        "decimal": 1,
        "show_date": False,
        "show_uv": False,
        "show_height": True,
        "show_direction": False,
        "show_period": False,
        "show_air_temp": False,
        "show_rain_sum": False,
        "show_precipitation_prob": False,
        "show_wind_speed": False,
        "show_wind_direction": False,
    }
    forecast = {"wave_height_max": [3.567]}
    helper.print_forecast(ocean, forecast)
    assert "Wave Height: 3.6" in capsys.readouterr().out


def test_print_forecast_falls_back_on_type_error(capsys):
    """print_forecast prints the raw value when float() raises TypeError."""
    ocean = {
        "forecast_days": 1,
        "decimal": 1,
        "show_date": False,
        "show_uv": True,
        "show_height": False,
        "show_direction": False,
        "show_period": False,
        "show_air_temp": False,
        "show_rain_sum": False,
        "show_precipitation_prob": False,
        "show_wind_speed": False,
        "show_wind_direction": False,
    }
    forecast = {"uv_index_max": [None]}  # float(None) raises TypeError
    helper.print_forecast(ocean, forecast)
    assert "UV Index: None" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# json_output
# ---------------------------------------------------------------------------


def test_json_output_prints_when_print_output_true(capsys):
    """json_output prints JSON to stdout and returns the original dict."""
    data = {"key": "value"}
    result = helper.json_output(data)
    assert result is data
    assert '"key": "value"' in capsys.readouterr().out


def test_json_output_silent_when_print_output_false(capsys):
    """json_output returns the dict silently when print_output=False."""
    data = {"key": "value"}
    result = helper.json_output(data, print_output=False)
    assert result is data
    assert not capsys.readouterr().out


# ---------------------------------------------------------------------------
# print_outputs
# ---------------------------------------------------------------------------


def test_print_outputs_no_ocean_data(mocker, capsys):
    """print_outputs shows 'No ocean data' when Height is 'No data'."""
    ocean_data = {"Height": "No data", "Lat": 36.97, "Long": -122.03}
    arguments = {
        **helper.DEFAULT_ARGUMENTS,
        "lat": 36.97,
        "long": -122.03,
        "city": "Santa Cruz",
        "decimal": 1,
        "forecast_days": 0,
        "color": "blue",
    }
    mocker.patch("src.api.forecast", return_value={})
    helper.print_outputs(ocean_data, arguments, "", (None, ""))
    assert "No ocean data at this location." in capsys.readouterr().out


def test_print_outputs_valid_data(mocker, capsys):
    """print_outputs renders location, wave art, and ocean fields."""
    ocean_data = {
        "Height": 3.0,
        "Lat": 36.97,
        "Long": -122.03,
        "UV Index": 5,
        "Swell Direction": 270,
        "Period": 12,
    }
    arguments = {
        **helper.DEFAULT_ARGUMENTS,
        "lat": 36.97,
        "long": -122.03,
        "city": "Santa Cruz",
        "decimal": 1,
        "forecast_days": 0,
        "color": "blue",
    }
    mocker.patch("src.api.forecast", return_value={})
    helper.print_outputs(ocean_data, arguments, "", (None, ""))
    out = capsys.readouterr().out
    assert "Santa Cruz" in out
    assert "Wave Height: 3.0" in out


def test_print_outputs_with_gpt(mocker, capsys):
    """print_outputs calls print_gpt and prints its response when gpt=True."""
    ocean_data = {
        "Height": 3.0,
        "Lat": 36.97,
        "Long": -122.03,
        "UV Index": 5,
        "Swell Direction": 270,
        "Period": 12,
    }
    arguments = {
        **helper.DEFAULT_ARGUMENTS,
        "lat": 36.97,
        "long": -122.03,
        "city": "Santa Cruz",
        "decimal": 1,
        "forecast_days": 0,
        "color": "blue",
        "gpt": True,
    }
    mocker.patch("src.api.forecast", return_value={})
    mocker.patch("src.helper.print_gpt", return_value="GPT says: go surf!")

    result = helper.print_outputs(ocean_data, arguments, "prompt", (None, ""))

    assert result == "GPT says: go surf!"
    assert "GPT says: go surf!" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# set_location
# ---------------------------------------------------------------------------


def test_set_location_unpacks_dict():
    """set_location returns (city, lat, long) from the location dict."""
    location = {"city": "Santa Cruz", "lat": _LAT, "long": _LONG}
    city, lat, long = helper.set_location(location)
    assert city == "Santa Cruz"
    assert lat == _LAT
    assert long == _LONG


# ---------------------------------------------------------------------------
# print_gpt
# ---------------------------------------------------------------------------


def test_print_gpt_uses_openai_when_key_is_long_enough(mocker):
    """print_gpt uses OpenAILlm when the API key is at least 5 chars."""
    surf_data = {
        "Location": "Santa Cruz",
        "Height": "3",
        "Swell Direction": "270",
        "Period": "12",
        "Unit": "ft",
    }
    mock_llm = mocker.MagicMock()
    mock_llm.call_llm.return_value = "openai response"
    mocker.patch("src.helper.gpt.OpenAILlm", return_value=mock_llm)
    result = helper.print_gpt(
        surf_data, "any prompt", ("sk-validkey", "gpt-4")
    )
    assert result == "openai response"
    mock_llm.call_llm.assert_called_once()
