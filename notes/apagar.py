import streamlit as st
import pandas as pd

data = [
    ["Arizona", "Phoenix"],
    ["Arizona", "Tucson"],
    ["Arizona", "Glendale"],
    ["Montana", "Billings"],
    ["Montana", "Butte"],
    ["Wyoming", "Cheyenne"],
    ["Wyoming", "Casper"],
    ["Wyoming", "Gillette"],
]

df = pd.DataFrame(data, columns=["State", "City"])
st.dataframe(df)

mystates = st.multiselect("States ?", df["State"].unique())
if len(mystates) > 0:
    mycities = df.get(["City"]).where(df.get("State").isin(mystates)).dropna()
    mycities = st.multiselect("Cities ?", mycities)
