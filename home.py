import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo

from utils import *

st.set_page_config(
    page_title="CerebroEvent - Home",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded",
    
)

if "selected_event" not in st.session_state:
    st.session_state.selected_event = ""


st.markdown(
    """
    ## Welcome to the Cerebro Event Analyzer 🏀
    Use this portal to quickly identify top performers in youth basketball events:
    
    *👈 To begin, select an event from the sidebar.*
    
    """
)

st.caption(
    """
    The pages are as follows:
    - Overview
    - Most Outstanding Performance Ladder
    - All-Tourney Teams
    - Full Leaderboard
    - Player Match
    - CerebroAI
    """
)

df = pd.DataFrame({
    'Options': ["Select Option","Nike EYBL 17U - 2023", "Nike EYBL 17U - 2021", "Nike EYBL 17U - 2019", "Nike Hoop Summit - 2022", "Augusta Peach Jam - 2022"]
})

# Sidebar dropdown
selected_option = st.sidebar.selectbox(
    "Select an Option",
    df['Options']
)

add_logo("assets/cerebro_logo.png", height = 210)

# Step 4: Add a button for confirmation
if st.sidebar.button('Confirm Selection') and selected_option != "Select Option":
    # Step 5: Store the dropdown response in the session state upon button click.
    st.session_state.selected_event = selected_option
    st.sidebar.success(f"You have selected: {selected_option}")

# Displaying the selected option outside of the sidebar, if any selection is made