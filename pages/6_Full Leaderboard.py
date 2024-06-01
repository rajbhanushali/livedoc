import streamlit as st
from utils import render_event_table
from sql_queries import get_table_from_snowflake
from streamlit_extras.app_logo import add_logo

st.set_page_config(
    page_title="CerebroEvent - Leaderboard",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded"
)
add_logo("assets/cerebro_logo.png", height = 300)

if "selected_event" not in st.session_state or not st.session_state.selected_event or "selected_year" not in st.session_state:
    st.session_state.selected_event = "Nike EYBL (17U)"
    st.session_state.selected_year = 2021

st.title(f"Full Leaderboard for {st.session_state.selected_event}")

event_dataframe = get_table_from_snowflake(st.session_state.selected_event, st.session_state.selected_year)

render_event_table(event_dataframe)