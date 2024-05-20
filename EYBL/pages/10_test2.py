import streamlit as st
import pandas as pd
import plotly.express as px
from utils import get_dataframe_description



data = {
    'PLAYER': ["Cameron Boozer", "Cooper Flagg", "Cayden Boozer", "Jaylen Harrell", "William Riley", "Shareef Jackson", "Gregory Lawson", "Adlan Elamin", "Mike Jones", "Kedrick Simmons", "Christian Jeffrey", "Preston Fowler", "Bryce Heard", "Jaylen Myers", "Jaylen Cross"],
    'TEAM': ["Nightyrdas Elite (16U)", "Maine United (16U)", "Nightyrdas Elite (16U)", "Expressions (16U)", "UPlay (16U)", "NJ Scholars (16U)", "Indy Heat (16U)", "Team Takeover (16U)", "Mac Irvin Fire (16U)", "Team Thad (16U)", "NH Lightning (16U)", "NH Lightning (16U)", "Florida Rebels (16U)", "NJ Scholars (16U)", "Team CP3 (16U)"],
    'RAM': [1477.3, 1151.8, 939.2, 916.2, 872.4, 843.1, 836.8, 835.7, 830.6, 814.3, 795.4, 783.1, 746.9, 729.8, 728.0],
    'C-RAM': [17.3, 13.6, 11.2, 10.9, 10.4, 10.1, 10.0, 10.0, 9.9, 9.9, 9.9, 8.8, 8.4, 8.8, 8.8],
    'PSP': [121.1, 85.7, 76.1, 99.9, 104.1, 88.7, 91.7, 86.3, 90.7, 77.0, 84.0, 63.8, 66.3, 70.1, 82.4],
    '3PE': [68.2, 73.5, 32.2, 41.9, 76.4, 79.2, 67.9, 63.1, 53.1, 53.6, 52.6, 66.7, 59.7, 64.5, 68.6],
    'FGS': [68.0, 68.2, 94.4, 96.1, 64.2, 62.4, 63.3, 75.3, 68.0, 64.4, 58.6, 55.2, 46.6, 59.5, 47.0],
    'BMS': [88.0, 85.3, 70.8, 88.9, 53.7, 68.3, 72.0, 73.0, 61.1, 78.0, 68.0, 53.6, 57.0, 53.4, 80.4],
    'DSI': [106.6, 99.8, 78.6, 90.3, 64.7, 68.3, 66.0, 91.4, 80.1, 83.7, 76.3, 68.0, 53.0, 52.5, 80.4]
}

df = pd.DataFrame(data)
df = pd.read_csv('EYBL.csv')
# Function to classify players into tiers
def classify_tier(c_ram):
    if c_ram >= 10:
        return "Gold"
    elif 8.5 <= c_ram < 10:
        return "Silver"
    elif 7 <= c_ram < 8.5:
        return "Bronze"
    else:
        return "Not Rated"

df['Tier'] = df['C-RAM'].apply(classify_tier)

# Streamlit app


# Plotly bar chart for C-RAM
fig_bar = px.bar(
    df.nlargest(10, 'C-RAM'), 
    x='C-RAM', 
    y='PLAYER', 
    color='C-RAM', 
    color_continuous_scale='viridis', 
    labels={'C-RAM': 'C-RAM Score', 'PLAYER': 'Player Name'},
    template='plotly_white',
    orientation='h'
)

st.plotly_chart(fig_bar)

# Plotly pie chart for Tiers
tier_counts = df['Tier'].value_counts().reset_index()
tier_counts.columns = ['Tier', 'Count']

fig_pie = px.pie(
    tier_counts, 
    values='Count', 
    names='Tier', 
    title='Player Distribution by Tier', 
    color='Tier',
    color_discrete_map={'Gold': '#FFD700', 'Silver': '#C0C0C0', 'Bronze': '#CD7F32', 'Not Rated': 'grey'},
    template='plotly_white'
)

st.plotly_chart(fig_pie)