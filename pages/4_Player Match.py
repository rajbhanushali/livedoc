import streamlit as st
from utils import render_player_match_ai_button, render_table
from sql_queries import get_table_from_snowflake
from streamlit_extras.app_logo import add_logo

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


player_match_prompt = f"""
You are a youth basketball analyst. The data in this table represents the top performers from the EYBL tournament. The tournament has 323 players across 32 different teams with average performers scoring X points per game, average field goal percentage of Y percent, average RAM (which is a proprietary metric showing individual game performance) of R and C_RAM (cumulative RAM) of C.

Compare the performances of **{player1}** and **{player2}** both against each other and against the average performance metrics. Highlight their strengths and weaknesses using the 5 metric suite (PSP, 3PE, FGS, ATR, DSI), box score statistics, and other relevant metrics.

Here are the key points to cover in your comparison:
- Which player has better overall performance based on RAM and C_RAM?
- Detailed comparison of their 5MS metrics (PSP, 3PE, FGS, ATR, DSI).
- Insights into their scoring, shooting, playmaking, around-the-rim skills, and defensive impact.
- Highlight any specific areas where one player excels over the other.
- Suggest the type of team or playing style each player would fit better in.
- Highlight their box score stats and where one outperformed the other.

Descriptions of the key metrics:
- **RAM**: Overall Evaluation Score, ranging from 0 to 1000+, balancing efficiency, volume, and per-minute impact.
- **C-RAM**: Context Metric, comparing performance to the average, with scores from 0 to 10+, and medals for different performance levels.
- **PSP**: Pure Scoring Prowess, blending scoring volume and efficiency.
- **3PE**: 3-Point Efficiency, considering shooting volume and efficiency.
- **FGS**: Floor General Skills, exploring passing efficiency and volume.
- **ATR**: Around the Rim, indicators for big man play, including rebounds, blocks, and 2-point efficiency.
- **DSI**: Defensive Statistical Impact, combining events creation and defensive efficiency.

Please bold the player names in your response.
"""

# Use the selected players' averages for the analysis
selected_players_averages = event_dataframe[event_dataframe['PLAYER'].isin([player1, player2])]

# Render the AI button with the updated prompt
render_player_match_ai_button(selected_players_averages, player1, player2, player_match_prompt)
