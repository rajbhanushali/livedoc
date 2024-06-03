import streamlit as st
import plotly.express as px
import pandas as pd

from streamlit_extras.app_logo import add_logo
from utils import render_event_table, render_ai_button
from sql_queries import get_player_averages_dataframe
from static_prompts import get_comparative_prompt

st.set_page_config(
    page_title="CerebroEvent - MOP Ladder",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded"
)
add_logo("assets/cerebro_logo.png", height = 300)

if "selected_event" not in st.session_state or not st.session_state.selected_event or "selected_year" not in st.session_state:
    st.session_state.selected_event = "Nike EYBL (17U)"
    st.session_state.selected_year = 2021

st.title(f"Most Outstanding Performance Ladder for {st.session_state.selected_event}")

event_dataframe = get_player_averages_dataframe(st.session_state.selected_event, st.session_state.selected_year)

top_20_cram = event_dataframe.nlargest(20, 'C_RAM')

col_data, col_radar = st.columns(2)

# Display the DataFrame in the first column with color coding
with col_data:
    st.markdown("### Player Rankings")

    grid_object = render_event_table(top_20_cram)
    selected_rows_df = pd.DataFrame(grid_object['selected_rows'])

# Create the bar chart and display it in the second column
with col_radar:
    st.markdown("### Player Comparison using 5MS")

    if selected_rows_df.empty:
        selected_players = event_dataframe.iloc[:1]  # Default to the first player
    else:
        selected_players = event_dataframe[event_dataframe["PLAYER"].isin(selected_rows_df["PLAYER"])]

    categories = ['PSP', 'ATR', 'DSI', 'FGS', 'THREE_PE']
    radar_data = selected_players.melt(id_vars=['PLAYER'], value_vars=categories, var_name='categories', value_name='values')

    fig = px.line_polar(radar_data, r="values",
                    theta="categories",
                    color="PLAYER",
                    line_close=True,
                    #color_discrete_sequence=["#00eb93", "#4ed2ff"],
                    template="plotly_dark"
                    )                   

    fig.update_polars(angularaxis_showgrid=False,
                  radialaxis_gridwidth=0,
                  gridshape='linear',
                  bgcolor="#494b5a",
                  radialaxis_showticklabels=False
                  #legend_title_font_color="green"
                  )

    fig.update_layout(legend_font_color="black",title = "Player Comparison")    
    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        legend_font_color="white"    
    )

    st.plotly_chart(fig, theme="streamlit", use_container_width = False)

# Display the selected player's name
if not selected_rows_df.empty:
    selected_rows_df = selected_rows_df.drop('_selectedRowNodeInfo', axis=1)
    selected_players = selected_rows_df["PLAYER"].tolist()  # Assuming the column name is 'Player'
    st.markdown("#### **Selected players:**")
    for player in selected_players:
        st.write(player)
    render_ai_button(event_dataframe, get_comparative_prompt(selected_players, st.session_state.selected_event))
else:
    st.write(f"Here we see the top 20 most outstanding players in the event. Click a players name to generate a statistical analysis on their performance. ")

# Description at the bottom of the page