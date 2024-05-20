import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
from utils import get_dataframe_description
from utils import *
# Create the DataFrame
st.set_page_config(
    page_title="Cerebro Event Analyzer",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Title of the page
st.title("Overview of EYBL")

# Display total players and average RAM using columns
col1, col2 = st.columns(2)
col1.metric("Total Players", "323")
col2.metric("Average RAM", "405")
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

df = pd.DataFrame(data)
fulldf= df.merge(eybl, on='PLAYER', how='inner')
#st.write(fulldf)



# Pie chart data
total_performers = 323
categories = ['Gold', 'Silver', 'Bronze', 'Not Rated']
not_rated = total_performers - (gold + silver + bronze)
values = [gold, silver, bronze, not_rated]
colors = ['#FFD700', '#C0C0C0', '#CD7F32', '#808080']  # Adjusted colors for contrast

def plot_bar_chart(dataframe):
    fig = px.bar(
        dataframe,
        x="C-RAM",
        y="PLAYER",
        orientation='h',
        title="Top Players by C-RAM Score",
        color='C-RAM',
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
df2 = pd.read_csv("EYBL.csv")
df2 = df2.nlargest(20, 'C-RAM')[['PLAYER', 'C-RAM']]
#plot_bar_chart(df2)    




# Layout for table and pie chart
left_column, right_column = st.columns([1, .6])
with left_column:
    plot_bar_chart(df2)
with right_column:
    # Plot the pie chart
    st.subheader("C-RAM Breakdown")
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(values, labels=categories, colors=colors, startangle=90,
                                      autopct='%1.1f%%', pctdistance=1.2)
    # Draw a circle at the center of pie to make it look like a donut
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig.gca().add_artist(centre_circle)
    
    # Change autotexts properties
    for autotext in autotexts:
        autotext.set_color('black')
    
    plt.setp(texts, weight="bold")
    ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
    st.pyplot(fig)




prompt = (f"""
You are a youth basketball analyst. The data in this table represents the top performers from the EYBL tournament. The tournament has 323 players across 32 different teams with average performers scoring {ppg} points per game, average field goal percentage of {fg_pct} percent, average RAM (which is a proprietary metric showing individual game performance) of {ram} and C_RAM (cumulative ram) of {c_ram}. Can you take this table and describe the top players performances relative to the averages

Here is an example of a "good description": This event contained 323 players across X teams, with players averaging X ppg, X FG%, and X RAM. The most notable performance in the event came from Player X (this will be calculated based on highest game RAM, played at least 24 min) who had statistics of X, Y, and Z (show the best stats of the player here, traditional not cerebro metrics). Team Y had the most wins in the event, with their leading player X averaging A, B and C. 

In the response, can you bold the player names
""")
if st.button("AI Analysis"):
    description = get_dataframe_description(fulldf, prompt)
    st.write(description)