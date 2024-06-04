import sys
import time
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).parent.parent))

from src import streamlit_helper as sl_help

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

latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
    latest_iteration.text(f"Iteration {i + 1}")
    bar.progress(i + 1)
    time.sleep(0.01)

st.caption("Enter a surf spot to see the map and forecast!")


# Toggles in a horizontal line
col1, col2 = st.columns(2)

with col1:
    gpt = st.toggle("Activate GPT")
with col2:
    map = st.toggle("Show Map", value=True)

extra_args = sl_help.extra_args(gpt)

# User input location
location = st.text_input("Surf Spot", placeholder="Enter surf spot!")

# Checks if location has been entered.
# If True, gathers surf report and displays map
if location:
    get_report = sl_help.get_report(location, extra_args)
    report_dict, gpt_response, lat, long = get_report

    # Displays the map
    if map:
        map_data = sl_help.map_data(lat, long)
        st.map(map_data, color="#FFFFFF")

    # Writes the GPT response
    if gpt_response is not None:
        st.write(gpt_response)

    # Displays the line graph
    st.write("# Surf Conditions")
    df = sl_help.graph_data(report_dict)
    st.line_chart(df.rename(columns={"date": "index"}).set_index("index"))
