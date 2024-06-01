import streamlit as st
import plotly.express as px
from streamlit_extras.app_logo import add_logo

from utils import render_ai_button, render_box_score_table
from sql_queries import get_team_event_dataframe
from static_prompts import player_report_prompt

st.set_page_config(
    page_title="CerebroEvent - Team Report",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded"
)
add_logo("assets/cerebro_logo.png", height = 300)

if "selected_event" not in st.session_state or not st.session_state.selected_event or "selected_year" not in st.session_state:
    st.session_state.selected_event = "Nike EYBL (17U)"
    st.session_state.selected_year = 2021

st.title(f"Team Report for {st.session_state.selected_event}")

team_averages_dataframe = get_team_event_dataframe(st.session_state.selected_event, st.session_state.selected_year)

st.dataframe(team_averages_dataframe)

