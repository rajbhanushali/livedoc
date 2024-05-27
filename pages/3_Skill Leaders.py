import streamlit as st
from utils import plot_bar_chart, plot_pie_chart, render_ai_button
from sql_queries import get_table_from_snowflake
from streamlit_extras.app_logo import add_logo
from static_prompts import get_overview_prompt, get_skill_leader_prompt
import pandas as pd

st.set_page_config(
    page_title="CerebroEvent - Overview",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

add_logo("assets/cerebro_logo.png", height = 300)

st.title(f"Skill Leaders of {st.session_state.selected_event}")

event_dataframe = get_table_from_snowflake(st.session_state.selected_event, st.session_state.selected_year)

event_dataframe_trimmed = event_dataframe[["RAM","C_RAM","PSP","DSI","FGS","THREE_PE","ATR"]]

columns = event_dataframe_trimmed.columns

# Dropdown menu for selecting a column
column_to_plot = st.selectbox("Select a skill to analyze", columns)


col1, col2 , col3= st.columns([2,.75,1]) 


with col1:
    st.write(f"Top {column_to_plot} for {st.session_state.selected_event}")
    top_10 = event_dataframe.nlargest(10, column_to_plot)[['PLAYER', column_to_plot]]
    top_player = top_10.iloc[0,0]
    plot_bar_chart(top_10)

avg_fgs_delta = round(event_dataframe.loc[event_dataframe['PLAYER'] == top_player,"FGS"].values[0] - event_dataframe['FGS'].mean(),2)
avg_dsi_delta = round(event_dataframe.loc[event_dataframe['PLAYER'] == top_player,"DSI"].values[0] - event_dataframe['DSI'].mean(),2)
avg_3pe_delta = round(event_dataframe.loc[event_dataframe['PLAYER'] == top_player,"THREE_PE"].values[0] - event_dataframe['THREE_PE'].mean(),2)
avg_atr_delta = round(event_dataframe.loc[event_dataframe['PLAYER'] == top_player,"ATR"].values[0] - event_dataframe['ATR'].mean(),2)
avg_psp_delta = round(event_dataframe.loc[event_dataframe['PLAYER'] == top_player,"PSP"].values[0] - event_dataframe['PSP'].mean(),2)
avg_ram_delta = round(event_dataframe.loc[event_dataframe['PLAYER'] == top_player,"RAM"].values[0] - event_dataframe['RAM'].mean(),2)


with col2:
    st.write(f"5MS Highlights for {top_player}")
    st.metric(f"RAM for {top_player}", event_dataframe.loc[event_dataframe['PLAYER'] == top_player,"RAM"].values[0],avg_ram_delta)
    st.metric(f"FGS for {top_player}", event_dataframe.loc[event_dataframe['PLAYER'] == top_player,"FGS"].values[0],avg_fgs_delta)
    st.metric(f"DSI for {top_player}",event_dataframe.loc[event_dataframe['PLAYER'] == top_player,"DSI"].values[0],avg_dsi_delta)

with col3:
    st.write("*")
    st.metric(f"3PE for {top_player}",event_dataframe.loc[event_dataframe['PLAYER'] == top_player,"THREE_PE"].values[0],avg_3pe_delta)
    st.metric(f"ATR for {top_player}",event_dataframe.loc[event_dataframe['PLAYER'] == top_player,"ATR"].values[0],avg_atr_delta)
    st.metric(f"PSP for {top_player}",event_dataframe.loc[event_dataframe['PLAYER'] == top_player,"PSP"].values[0],avg_psp_delta)
    
render_ai_button(event_dataframe, get_skill_leader_prompt(column_to_plot,st.session_state.selected_event,))
