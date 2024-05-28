import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
from sql_queries import get_event_data_df

from utils import *

st.set_page_config(
    page_title="CerebroEvent - Home",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded"
)

add_logo("assets/cerebro_logo.png", height = 290)

if "selected_event" not in st.session_state:
    st.session_state.selected_event = ""
if 'selected_year' not in st.session_state:
    st.session_state.selected_year = ""

st.markdown(
    """
    ## Welcome to the Cerebro Event Analyzer 🏀
    Use this portal to quickly identify top performers in youth basketball events.
    
    To begin, select an event from below, \n
    👈 and start your analysis on the side menu
    
    """
)

event_dataframe = get_event_data_df()

# Event selection
event_options = event_dataframe['Event'].unique().tolist()
selected_event = st.selectbox("Select an Event", event_options, index=event_options.index("Nike EYBL (17U)"))

# Get the available years for the selected event
year_options = event_dataframe[event_dataframe['Event'] == selected_event]['Year'].unique().tolist()

# Set the default year for the default event
if selected_event == "Nike EYBL (17U)":
    default_year = 2021 if 2021 in year_options else year_options[0]
else:
    default_year = year_options[0]

# Year selection based on selected event
selected_year = st.selectbox("Select a Year", year_options, index=year_options.index(default_year))

# Store selected values in session state
st.session_state.selected_event = selected_event
st.session_state.selected_year = selected_year

st.success(f"You have selected: {st.session_state.selected_event} - {st.session_state.selected_year}")