import pandas as pd
import email
import streamlit as st
import io
import numpy as np

st.title("FULL LEADERBOARD")

df = pd.read_csv('EYBL.csv')
def color_cram_value(val):
    if val >= 10:
        color = 'gold'
    elif 8.5 <= val < 10:
        color = 'silver'
    elif 7 <= val < 8.5:
        color = 'brown'
    else:
        color = 'white'
    return f'background-color: {color}'

st.dataframe(df.style.applymap(color_cram_value, subset=['C-RAM']),width=10000, height=768)

#st.dataframe(data = df, width=10000, height=768)

