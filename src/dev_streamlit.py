import time

import numpy as np
import pandas as pd
import streamlit as st

# NOTE: This file is for testing purposes. Do not use it in production.

# Page Configuration ###
title = "Sample Dashboard"
st.set_page_config(
    page_title=title,
    page_icon="🌈",
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
st.write("Starting a long computation...")

latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
    latest_iteration.text(f"Iteration {i + 1}")
    bar.progress(i + 1)
    time.sleep(0.01)

st.write("...and now we're done!")

# Map
st.title("My first app")

map_data = pd.DataFrame(
    np.random.randn(500, 2) / [50, 50] + [35.7, 139.67], columns=["lat", "lon"]
)
st.map(map_data)


# test by markdown
st.write("# title")

# note
st.caption("note")

# images
st.image("https://ul.h3z.jp/tbfgZLSX.webp")

# table
df = pd.DataFrame({
    "first column": [1, 2, 3, 4],
    "second column": [10, 20, 30, 40],
})
st.write(df)

# chart
st.line_chart(df)

# input text
name = st.text_input("name")

# integer input
age = st.number_input("age", step=1)

st.write(f"name: {name}")
st.write(f"age: {age}")

# button
if st.button("Push"):
    st.write("Pushed")

# pulldown
select = st.selectbox("Fruits", options=["apple", "banana", "strawberry"])
st.write(select)

# pulldown multiple
multi_select = st.multiselect("Color", options=["red", "blue", "yellow"])
st.write(multi_select)

# checkbox
if st.checkbox("Show dataframe"):
    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
    st.line_chart(chart_data)

# radio button
radio = st.radio("Select", ["cat", "dog"])
st.write(f"radio: {radio}")

# file upload
uploaded_file = st.file_uploader("Upload", type=["csv"])
if uploaded_file:
    dataframe = pd.read_csv(uploaded_file)
    st.write(dataframe)
