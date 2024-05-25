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

add_logo("assets/cerebro_logo.png", height = 290)

user_already_selected = False
if "selected_event" not in st.session_state:
    st.session_state.selected_event = ""
else:
    user_already_selected = True

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

selected_option = st.selectbox(
    "**Select an Event**",
    df['Options']
)

selection_box = st.empty()
if user_already_selected:
    selection_box.success(f"You have selected: {st.session_state.selected_event}")

# Step 4: Add a button for confirmation
if st.button('Confirm Selection') and selected_option != "Select Option":
    # Step 5: Store the dropdown response in the session state upon button click.
    st.session_state.selected_event = selected_option
    selection_box.success(f"You have selected: {selected_option}")