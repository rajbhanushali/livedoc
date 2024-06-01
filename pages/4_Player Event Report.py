import streamlit as st
import plotly.express as px
from streamlit_extras.app_logo import add_logo

from utils import render_ai_button, render_box_score_table
from sql_queries import get_table_from_snowflake, get_player_box_scores
from static_prompts import player_report_prompt

st.set_page_config(
    page_title="CerebroEvent - Player Report",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded"
)
add_logo("assets/cerebro_logo.png", height = 300)

if "selected_event" not in st.session_state or not st.session_state.selected_event or "selected_year" not in st.session_state:
    st.session_state.selected_event = "Nike EYBL (17U)"
    st.session_state.selected_year = 2021

st.title(f"Player Event Report for {st.session_state.selected_event}")


event_averages_dataframe = get_table_from_snowflake(st.session_state.selected_event, st.session_state.selected_year)

st.markdown("### Select a player. Get Some Insights")
selected_player = st.selectbox(
    "Select Players for Radar Plot",
    options=event_averages_dataframe["PLAYER"].unique(),
)

player_box_score_dataframe = get_player_box_scores(selected_player, st.session_state.selected_event, st.session_state.selected_year)

col_data, col_radar = st.columns(2)

# Display the DataFrame in the first column with color coding
with col_data:
    st.markdown("### Player Visuals")
    render_box_score_table(player_box_score_dataframe)

# Create the bar chart and display it in the second column
with col_radar:
    st.markdown("### Player 5MS")
    selected_player_row = event_averages_dataframe[event_averages_dataframe["PLAYER"] == selected_player]

    categories = ['PSP', 'ATR', 'DSI', 'FGS', 'THREE_PE']
    radar_data = selected_player_row.melt(id_vars=['PLAYER'], value_vars=categories, var_name='categories', value_name='values')

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

    fig.update_layout(legend_font_color="black")    
    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.1,
            xanchor="center",
            x=0.5
        ),
        legend_font_color="white"    
    )

    st.plotly_chart(fig, theme="streamlit", use_container_width = False)

# Description at the bottom of the page

render_ai_button(player_box_score_dataframe, player_report_prompt)