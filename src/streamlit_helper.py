"""
Helper functions for the streamlit frontent
"""

import sys
from pathlib import Path

import folium
import pandas as pd

sys.path.append(str(Path(__file__).parent.parent))

from src import cli


def extra_args(gpt):
    """
    By default, the location is the only argument when cli.run()
    is ran. Extra args outputs and other arguments the user wants,
    like using the GPT function
    """
    # Arguments
    extra_args = ""

    if gpt:
        extra_args += ",gpt"

    return extra_args


def get_report(location, extra_args):
    """
    Executes cli.run(), retrns the report dictionary,
    gpt response, lat and long
    """
    gpt_response = None
    args = "location=" + location
    if extra_args:
        args += extra_args
    surf_report = cli.run(args=["placeholder", args])
    report_dict, gpt_response = surf_report[0], surf_report[1]
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
        forecast["height"] for forecast in report_dict["Forecast"]
    ]
    forecasted_periods = [
        forecast["period"] for forecast in report_dict["Forecast"]
    ]
    forecasted_directions = [
        forecast["direction"] for forecast in report_dict["Forecast"]
    ]
    # table
    if graph_type == "Height/Period :ocean:" or graph_type == None:
        df = pd.DataFrame({
            "date": forecasted_dates,
            "heights": forecasted_heights,
            "periods": forecasted_periods,
        })
    else:
        df = pd.DataFrame({
            "date": forecasted_dates,
            "directions": forecasted_directions
        })

    return df



