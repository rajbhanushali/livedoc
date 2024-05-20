import streamlit as st
import pandas as pd
import plotly.express as px
from utils import get_dataframe_description

st.set_page_config(
    page_title="Cerebro Event Analyzer",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Sample data from the "Pure Scoring Prowess" table
# Streamlit app
df = pd.read_csv('EYBL.csv')
st.title("Top 10 Players Based on Selected Metric")

# Dropdown for selecting the column
selected_column = st.selectbox(
    "Select a metric to display the top 10 players",
    ("RAM", "C-RAM", "PSP", "3PE", "FGS", "BMS", "DSI")
)

# Get the top 10 players based on the selected column
top_10_df = df.nlargest(10, selected_column)[['PLAYER', 'TEAM', selected_column,'PTS/G','REB/G','AST/G','FG%']]

# Display the top 10 players
if st.button("Confirm"):
    st.write(f"Top 10 players based on {selected_column}:")
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(top_10_df)

    def plot_bar_chart(dataframe,selected_column):
        fig = px.bar(
            dataframe,
            x=selected_column,
            y="PLAYER",
            orientation='h',
            title="Top Players",
            color=selected_column,
            color_continuous_scale='viridis',
            labels={'C-RAM': 'C-RAM Score', 'Name': 'Player Name'},
            template='plotly_white'
        )
        fig.update_layout(
            title_font_size=24,
            xaxis_title_font_size=18,
            yaxis_title_font_size=18,
            yaxis={'categoryorder': 'total ascending'}
        )
        st.plotly_chart(fig)

    with col2:
        plot_bar_chart(top_10_df,selected_column)   





prompt = ("""
You are a youth basketball analyst. The data in this table represents the top performers from the EYBL tournament. The tournament has 323 players across 32 different teams with average performers scoring 6 points per game, average field goal percentage of 42.5 percent, average RAM (which is a proprietary metric showing individual game performance) of 405.3 and C_RAM (cumulative ram) of 5.1.

I want you to take the data passed and provide a description

Here is an example of a "good description": Cayden Boozer led the event in FGS, a metric showcasing Floor General Skills. He scored a 94 which was X% better than the average, and averaged 9 assists per game, 1.6 TOs per game, and 1.4 STL/G. He accounted for X% of his teams overall assists, and was the leader in overall assists for the event with Z assists. Trailing him in our FGS leaderboard is Christian Jeffrey from NH Lightining, with a FGS score of 85 and averages of 5.5 assists, 0.5 turnovers and half a steal per game. His key outlier stat is X (AI finds one outlier stat for him). Same overall thing for player #3.


In the response, can you bold the player names
""")
if st.button("AI Analysis"):
    description = get_dataframe_description(top_10_df, prompt)
    st.write(description)