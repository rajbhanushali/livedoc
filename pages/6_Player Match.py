import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import get_dataframe_description

# Create the DataFrame
st.set_page_config(
    page_title="Cerebro Event Analyzer",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded",
)
prompt = ("""
You are a youth basketball analyst. The data in this table represents the top performers from the EYBL tournament. The tournament has 323 players across 32 different teams with average performers scoring 6 points per game, average field goal percentage of 42.5 percent, average RAM (which is a proprietary metric showing individual game performance) of 405.3 and C_RAM (cumulative ram) of 5.1. Can you take this table and describe the top players performances relative to the averages

Can you compare the two players in the passed dataframe both against each other and against the rest of the field

In the response, can you bold the player names
""")

# Title of the page
st.title("Player Match")
data = {
    'RANK': range(1, 11),
    'PLAYER': [
        'Cameron Boozer', 'Cayden Boozer', 'Jaylen Harrell', 'William Riley', 
        'Adlan Elamin', 'Kedrick Simmons', 'Jaylen Cross', 'Cooper Flagg', 
        'Isaiah Henry', 'Alexander Lloyd'
    ],
    'TEAM': [
        'Nightrydas Elite (16U)', 'Nightrydas Elite (16U)', 'Expressions (16U)', 'UPlay (16U)', 
        'Team Takeover (16U)', 'Team Thad (16U)', 'Team CP3 (16U)', 'Maine United (16U)', 
        'Team CP3 (16U)', 'Nightrydas Elite (16U)'
    ],
    'W%': [1.000, 1.000, 0.800, 0.750, 0.800, 0.750, 0.800, 0.250, 0.800, 1.000],
    'C-RAM': [17.3, 11.2, 10.9, 10.4, 10.0, 9.8, 8.8, 13.6, 8.7, 7.9],
    'MOP SCORE': [229, 130, 113, 103, 101, 94, 85, 84, 83, 82]
}
df = pd.read_csv('EYBL.csv')

sort_column = 'C-RAM'

# Sort the DataFrame by the specified column in descending order and take the top 10 records
df = df.sort_values(by=sort_column, ascending=False).head(100)

# Function to color the C-RAM values
def color_cram_value(val):
    if val >= 10:
        color = 'gold'
    elif 8.5 <= val < 10:
        color = 'silver'
    elif 7 <= val < 8.5:
        color = 'beige'
    else:
        color = 'white'
    return f'background-color: {color}'

# Display the DataFrame in the first column with color coding

st.write("Player Rankings")
st.dataframe(df.style.applymap(color_cram_value, subset=['C-RAM']))

# Create the bar chart and display it in the second column
col1, col2 = st.columns(2)

with col1:
    player1 = st.selectbox('Select Player 1', df['PLAYER'])

with col2:
    player2 = st.selectbox('Select Player 2', df['PLAYER'])

# Button to confirm selection
if st.button('Confirm Selection'):
    st.write(f'You selected: {player1} and {player2}')
    selected_players_df = df[df['PLAYER'].isin([player1, player2])]
    description = get_dataframe_description(selected_players_df, prompt)
    st.write(description)

# Display the dataframe (optional)

    