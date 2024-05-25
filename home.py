import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
from sql_queries import get_event_data_df

from utils import *

st.set_page_config(
    page_title="CerebroEvent - Home",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="collapsed"
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

# df = pd.DataFrame({
#     'Options': ["Select Option","Nike EYBL 17U - 2023", "Nike EYBL 17U - 2021", "Nike EYBL 17U - 2019", "Nike Hoop Summit - 2022", "Augusta Peach Jam - 2022"]
# })

event_data_df = get_event_data_df()

# Event selection
event_options = event_data_df['Event'].unique().tolist()
selected_event = st.selectbox("Select an Event", ["Select Option"] + event_options)

# Step 4: Add a button for confirmation
if selected_event != "Select Option":
    st.session_state.selected_event = selected_event

    # Year selection based on selected event
    year_options = event_data_df[event_data_df['Event'] == st.session_state.selected_event]['Year'].tolist()
    selected_year = st.selectbox("Select a Year", ["Select Option"] + year_options)

    if selected_year != "Select Option":
        st.session_state.selected_year = selected_year
        st.success(f"You have selected: {st.session_state.selected_event} - {st.session_state.selected_year}")
    else:
        st.session_state.selected_year = None
else:
    st.session_state.selected_event = None
