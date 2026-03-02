"""
Helper functions for the streamlit frontend
"""

import folium
import pandas as pd

from src import cli


def extra_args(gpt):
    """
    By default, the location is the only argument when cli.run()
    is run. Extra args outputs and other arguments the user wants,
    like using the GPT function.
    """
    args = ""

    if gpt:
        args += ",gpt"

    return args


def get_report(location, extra_args):
    """
    Executes cli.run(), returns the report dictionary,
    gpt response, lat and long.
    """
    args = "location=" + location
    if extra_args:
        args += extra_args
    report_dict, gpt_response = cli.run(args=["placeholder", args])
    lat, long = report_dict["Lat"], report_dict["Long"]

    return report_dict, gpt_response, lat, long


def map_data(lat, long):
    """
    Gathers data for the map
    Docs: https://folium.streamlit.app/
    """
    m = folium.Map(location=[lat, long], zoom_start=16)
    folium.Marker(
        [lat, long], popup="Surf Spot!", tooltip="Get out there!"
    ).add_to(m)

    return m


def graph_data(report_dict, graph_type="Height/Period :ocean:"):
    """
    Gathers the forecasted dates, heights, period and stores them in a pandas
    dataframe. Will be used to display the line chart
    """
    forecasted_dates = [
        forecast["date"] for forecast in report_dict["Forecast"]
    ]
    forecasted_heights = [
        forecast["surf height"] for forecast in report_dict["Forecast"]
    ]
    forecasted_periods = [
        forecast["swell period"] for forecast in report_dict["Forecast"]
    ]
    forecasted_directions = [
        forecast["swell direction"] for forecast in report_dict["Forecast"]
    ]
    # table
    if graph_type == "Height/Period :ocean:" or graph_type is None:
        df = pd.DataFrame({
            "date": forecasted_dates,
            "heights": forecasted_heights,
            "periods": forecasted_periods,
        })
    else:
        df = pd.DataFrame({
            "date": forecasted_dates,
            "directions": forecasted_directions,
        })

    return df
