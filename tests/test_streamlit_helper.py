"""
Tests for streamlit_helper.py
"""

import folium
import pandas as pd

from src import streamlit_helper

_LAT = 36.97
_LONG = -122.03
_EXPECTED_ROWS = 2


def test_extra_args_without_gpt():
    """extra_args returns an empty string when GPT is disabled."""
    assert not streamlit_helper.extra_args(gpt=False)


def test_extra_args_with_gpt():
    """extra_args appends ',gpt' when GPT is enabled."""
    assert streamlit_helper.extra_args(gpt=True) == ",gpt"


def test_get_report_returns_report_dict_and_coords(mocker):
    """get_report calls cli.run and unpacks the result correctly."""
    ocean_data = {"Lat": _LAT, "Long": _LONG, "Height": 3.0}
    mocker.patch("src.cli.SurfReport")
    mocker.patch(
        "src.streamlit_helper.cli.run",
        return_value=(ocean_data, "gpt response"),
    )

    report_dict, gpt_response, lat, long = streamlit_helper.get_report(
        "santa_cruz", ""
    )

    assert report_dict is ocean_data
    assert gpt_response == "gpt response"
    assert lat == _LAT
    assert long == _LONG


def test_get_report_appends_extra_args(mocker):
    """get_report forwards extra_args to cli.run correctly."""
    ocean_data = {"Lat": 1.0, "Long": 2.0}
    mock_run = mocker.patch(
        "src.streamlit_helper.cli.run",
        return_value=(ocean_data, None),
    )

    streamlit_helper.get_report("santa_cruz", ",gpt")

    call_kwargs = mock_run.call_args[1]
    assert "location=santa_cruz,gpt" in call_kwargs["args"][1]


def test_map_data_returns_folium_map():
    """map_data returns a folium Map centred on the given coordinates."""
    result = streamlit_helper.map_data(_LAT, _LONG)
    assert isinstance(result, folium.Map)


def test_graph_data_height_period_returns_dataframe():
    """graph_data returns a DataFrame with date/heights/periods columns."""
    report_dict = {
        "Forecast": [
            {
                "date": "2024-01-01",
                "surf height": 3.0,
                "swell period": 12.0,
                "swell direction": 270.0,
            },
            {
                "date": "2024-01-02",
                "surf height": 4.0,
                "swell period": 10.0,
                "swell direction": 260.0,
            },
        ]
    }

    df = streamlit_helper.graph_data(
        report_dict, graph_type="Height/Period :ocean:"
    )
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["date", "heights", "periods"]
    assert len(df) == _EXPECTED_ROWS


def test_graph_data_direction_returns_dataframe():
    """graph_data returns a DataFrame with date/directions columns."""
    report_dict = {
        "Forecast": [
            {
                "date": "2024-01-01",
                "surf height": 3.0,
                "swell period": 12.0,
                "swell direction": 270.0,
            },
        ]
    }

    df = streamlit_helper.graph_data(report_dict, graph_type="Direction")
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["date", "directions"]


def test_graph_data_none_graph_type_defaults_to_height_period():
    """graph_data with graph_type=None defaults to Height/Period layout."""
    report_dict = {
        "Forecast": [
            {
                "date": "2024-01-01",
                "surf height": 3.0,
                "swell period": 12.0,
                "swell direction": 270.0,
            },
        ]
    }

    df = streamlit_helper.graph_data(report_dict, graph_type=None)
    assert "heights" in df.columns
    assert "periods" in df.columns
