import time

import numpy as np
import pandas as pd
import sys
from pathlib import Path
import streamlit as st
import pydeck as pdk

sys.path.append(str(Path(__file__).parent.parent))

from src import api, cli

# NOTE: This file is for testing purposes. Do not use it in production.

# Page Configuration ###
title = "cli-surf"
st.set_page_config(
    page_title=title,
    page_icon="🌊",
    layout="wide",
)
st.title(title)

# Page Content ###

# sidebar
st.sidebar.markdown(
    """
# MENU
- [weather](#weather)
- [csv upload](#csv-upload)
- [graph](#graph)
- [data sheet](#data-sheet)
""",
    unsafe_allow_html=True,
)

# progress bar
# st.write("Loading...")

latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
    latest_iteration.text(f"Iteration {i + 1}")
    bar.progress(i + 1)
    time.sleep(0.01)

# st.write("...and now we're done!")

# Map
# st.title("Surf Spot")

st.caption("Enter a surf spot to see the map and forecast!")

# User input location
location = st.text_input("Surf Spot", placeholder="Enter surf spot!")

# Checks if location has been entered. 
# If True, gathers surf report and displays map
if location:
    location = "location=" + location
    surf_report = cli.run(args=["placeholder",f"{location}"])
    lat, long = surf_report["Lat"], surf_report["Long"]
    map_data = pd.DataFrame(
        np.random.randn(500, 2) / [50, 50] + [lat, long], columns=["lat", "lon"]
    )
    st.map(map_data)
    forecasted_dates = [forecast['date'] for forecast in surf_report['Forecast']]
    forecasted_heights = [forecast['height'] for forecast in surf_report['Forecast']]
    forecasted_periods = [forecast['period'] for forecast in surf_report['Forecast']]
    



st.write("# Surf Conditions")

# Checks if location has been inputted. Loads map if True 
if location: 
    # table
    df = pd.DataFrame({

    'date': forecasted_dates,
    'heights': forecasted_heights,
    'periods': forecasted_periods
    })

    df

    st.line_chart(df.rename(columns={'date':'index'}).set_index('index'))




# DEFAULTS
# # input text
# name = st.text_input("name")

# # integer input
# age = st.number_input("age", step=1)

# st.write(f"name: {name}")
# st.write(f"age: {age}")

# # button
# if st.button("Push"):
#     st.write("Pushed")

# # pulldown
# select = st.selectbox("Fruits", options=["apple", "banana", "strawberry"])
# st.write(select)

# # pulldown multiple
# multi_select = st.multiselect("Color", options=["red", "blue", "yellow"])
# st.write(multi_select)

# # checkbox
# if st.checkbox("Show dataframe"):
#     chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
#     st.line_chart(chart_data)

# # radio button
# radio = st.radio("Select", ["cat", "dog"])
# st.write(f"radio: {radio}")

# # file upload
# uploaded_file = st.file_uploader("Upload", type=["csv"])
# if uploaded_file:
#     dataframe = pd.read_csv(uploaded_file)
#     st.write(dataframe)
