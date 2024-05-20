import pandas as pd
import email
import streamlit as st
import io
import numpy as np
from streamlit_extras.app_logo import add_logo
from utils import *


st.set_page_config(
    page_title="Cerebro Event Analyzer",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded",
    
)
st.write("# Welcome to the Cerebro Event Analyzer 🏀")
st.markdown(
    """
    Use this portal to quickly identify top performers in youth basketball events:

    👈 To begin, select an event from the sidebar. 
    of how this app operates
    ### The pages are as follows:
    - Overview
    - Most Outstanding Performance Ladder
    - All-Tourney Teams
    - Skill Leaders
    - Full Leaderboard
   
"""
)

df = pd.DataFrame({
    'Options': ["Select Option","EYBL", "Metro North", "NorCal Tip-Off Classic", "Forum Tip-off Classic"]
})

# Step 2 & 3: Use Streamlit for the web app with a sidebar dropdown pulling from the DataFrame.
# Adding a title for clarity

# Sidebar dropdown
selected_option = st.sidebar.selectbox(
    "Select an Option",
    df['Options']
)

#add_logo("https://d1muf25xaso8hp.cloudfront.net/https%3A%2F%2F5091af9f881c9c1d14eb408cf6b9162f.cdn.bubble.io%2Ff1623868126182x114384330409815780%2FCerebro%2520Logo%2520Black.png?w=&h=&auto=compress&dpr=1&fit=max")
add_logo("logo2.png", height = 200)
# Step 4: Add a button for confirmation
if st.sidebar.button('Confirm Selection'):
    # Step 5: Store the dropdown response in the session state upon button click.
    st.session_state.selected_option = selected_option
    st.sidebar.success(f"You have selected: {selected_option}")

# Displaying the selected option outside of the sidebar, if any selection is made


