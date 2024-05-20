import streamlit as st
import pandas as pd

# Data for all three sections, filled with example data
# For your application, fill in the actual data instead of these placeholders
data = {
    'SECTION': ['FIRST TEAM']*5 + ['SECOND TEAM']*5 + ['THIRD TEAM']*5,
    'PLAYER': ['Cameron Boozer', 'Cooper Flagg', 'Cayden Boozer', 'Jaylen Harrell', 'William Riley'] + ['Shareef Jackson', 'Gregory Lawson', 'Adlan Elamin', 'Mike Jones', 'Kedrick Simmons'] + ['Christian Jeffrey', 'Preston Fowler', 'Bryce Heard', 'Jayden Myers', 'Jaylen Cross'],
    'TEAM': ['Nightrydas Elite (16U)']*5 + ['NJ Scholars (16U)', 'Indy Heat (16U)', 'Team Takeover (16U)', 'Mac Irvin Fire (16U)', 'Team Thad (16U)'] + ['NH Lightning (16U)']*2 + ['Florida Rebels (16U)', 'NJ Scholars (16U)', 'Team CP3 (16U)'],
    'RAM': [1477, 1152, 939, 916, 872] + [843, 837, 836, 831, 814] + [795, 783, 747, 730, 728],
    'C-RAM': [17.3, 13.6, 11.2, 10.9, 10.4] + [10.1, 10.0, 10.0, 9.9, 9.8] + [9.5, 9.4, 9.0, 8.8, 8.8],
    # Add other columns like FG%, PTS/G, etc.
}

# Create the DataFrame
df = pd.DataFrame(data)

# Define color based on the section
def background_color(row):
    if row['SECTION'] == 'FIRST TEAM':
        return ['background-color: #FFCCCC'] * len(row)
    elif row['SECTION'] == 'SECOND TEAM':
        return ['background-color: #CCCCFF'] * len(row)
    elif row['SECTION'] == 'THIRD TEAM':
        return ['background-color: #CCFFCC'] * len(row)
    return [''] * len(row)

# Define color based on C-RAM value
def color_cram_value(val):
    if val >= 10:
        return 'background-color: gold'
    elif 8.5 <= val < 10:
        return 'background-color: silver'
    elif 7 <= val < 8.5:
        return 'background-color: bronze'
    return ''

# Apply the color styles to the DataFrame
styled_df = df.style.apply(
    background_color, axis=1
).applymap(
    color_cram_value, subset=['C-RAM']
).hide_index()

# Streamlit page setup
st.title("CEREBRO ALL-TOURNEY TEAMS")

# Display the styled DataFrame
st.dataframe(styled_df)

# Description at the bottom
st.write("""
The table showcases the 'CEREBRO ALL-TOURNEY TEAMS' highlighting the top players. 
The players are grouped into First, Second, and Third teams based on their performance metrics such as RAM and C-RAM.
Color coding is applied to indicate the tier (gold, silver, bronze) of each player's C-RAM score.
""")

# Please make sure to update the data accordingly to match the full dataset from your image.
