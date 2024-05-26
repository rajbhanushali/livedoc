import streamlit as st
from utils import render_player_match_ai_button, render_table
from sql_queries import get_table_from_snowflake
from streamlit_extras.app_logo import add_logo
from static_prompts import get_player_match_prompt

st.set_page_config(
    page_title="CerebroEvent - Player Match",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded"
)
add_logo("assets/cerebro_logo.png", height = 300)

if "selected_event" not in st.session_state or not st.session_state.selected_event or "selected_year" not in st.session_state:
    st.error(" ### Please return to Home and select an event ")
    st.stop()

st.title(f"Player Match for {st.session_state.selected_event}")

event_dataframe = get_table_from_snowflake(st.session_state.selected_event, st.session_state.selected_year)

# Sort the DataFrame by the specified column in descending order and take the top 100 records
event_dataframe = event_dataframe.sort_values(by="C_RAM", ascending=False)

# Display the DataFrame in the first column with color coding

st.write("Player Rankings")
render_table(event_dataframe)

# Create the bar chart and display it in the second column
col1, col2 = st.columns(2)

with col1:
    player1 = st.selectbox('Select Player 1', event_dataframe['PLAYER'], index=0)

with col2:
    player2 = st.selectbox('Select Player 2', event_dataframe['PLAYER'], index=1)

# Use the selected players' averages for the analysis
selected_players_averages = event_dataframe[event_dataframe['PLAYER'].isin([player1, player2])]

player_match_prompt = get_player_match_prompt(player1, player2)
# Render the AI button with the updated prompt
render_player_match_ai_button(selected_players_averages, player1, player2, player_match_prompt)
