import streamlit as st
import pandas as pd

# Sample data from the "Pure Scoring Prowess" table
data_pure_scoring = {
    'PLAYER': ['Cameron Boozer', 'Cooper Flagg'],
    'TEAM': ['Nightrydas Elite (16U)', 'Maine United (16U)'],
    'Pure Scoring Prowess': [121, 109],
    'C-RAM': [17.3, 13.6],
    # Add other columns like PTS/G, FG%, etc.
}

# Sample data from the "Floor General Skills" table
data_floor_general = {
    'PLAYER': ['Cayden Boozer', 'Christian Jeffrey'],
    'TEAM': ['Nightrydas Elite (16U)', 'NH Lightning (16U)'],
    'Floor General Skills': [94, 85],
    'C-RAM': [11.2, 9.5],
    # Add other columns like AST/G, TOV/G, etc.
}

# Sample data from the "3-Point Efficiency" table
data_three_point = {
    'PLAYER': ['Aleksandar Alston', 'Derek Dixon'],
    'TEAM': ['Mac Irvin Fire (16U)', 'Team Takeover (16U)'],
    '3-Point Efficiency': [108, 103],
    'C-RAM': [8.5, 8.1],
    # Add other columns like 3PM/G, 3PT%, etc.
}

# Sample data from the "Big Man Strengths" table
data_big_man = {
    'PLAYER': ['Cameron Boozer', 'Christian Guradak'],
    'TEAM': ['Nightrydas Elite (16U)', 'Team Takeover (16U)'],
    'Big Man Strengths': [103, 85],
    'C-RAM': [17.3, 8.2],
    # Add other columns like REB/G, ORB/G, etc.
}

# Convert dictionaries to DataFrames
df_pure_scoring = pd.DataFrame(data_pure_scoring)
df_floor_general = pd.DataFrame(data_floor_general)
df_three_point = pd.DataFrame(data_three_point)
df_big_man = pd.DataFrame(data_big_man)

# Function to color C-RAM cells
def color_cram_value(val):
    if val >= 10:
        return 'background-color: gold'
    elif 8.5 <= val < 10:
        return 'background-color: silver'
    elif val < 8.5:
        return 'background-color: #cd7f32'  # Bronze
    return ''

# Streamlit page setup
st.title("CEREBRO SKILL LADDER")

# Display styled DataFrames
st.write("Pure Scoring Prowess")
st.dataframe(df_pure_scoring.style.applymap(color_cram_value, subset=['C-RAM']))

st.write("Floor General Skills")
st.dataframe(df_floor_general.style.applymap(color_cram_value, subset=['C-RAM']))

st.write("3-Point Efficiency")
st.dataframe(df_three_point.style.applymap(color_cram_value, subset=['C-RAM']))

st.write("Big Man Strengths")
st.dataframe(df_big_man.style.applymap(color_cram_value, subset=['C-RAM']))

# Description at the bottom
st.write("""
The tables above showcase selected categories from the All-Tourney Teams, each highlighting different skill sets.
Players are evaluated on various metrics such as Pure Scoring Prowess, Floor General Skills, 3-Point Efficiency, and Big Man Strengths.
The C-RAM column is color-coded to indicate the player's score tier.
""")

# Note: This code only handles the color coding for the C-RAM column.
# To precisely match the color schemes from your image, you'll need to apply similar styling for other columns.

# Reminder to the user to complete the tables with all the data.
