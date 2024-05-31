import streamlit as st
import plotly.express as px
from streamlit_extras.app_logo import add_logo

from utils import render_table, render_ai_button
from sql_queries import get_table_from_snowflake
from static_prompts import mop_ladder_prompt

st.set_page_config(
    page_title="CerebroEvent - MOP Ladder",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded"
)
add_logo("assets/cerebro_logo.png", height = 300)

if "selected_event" not in st.session_state or not st.session_state.selected_event or "selected_year" not in st.session_state:
    st.error(" ### Please return to Home and select an event ")
    st.stop()

st.title(f"Most Outstanding Performance Ladder for {st.session_state.selected_event}")

event_dataframe = get_table_from_snowflake(st.session_state.selected_event, st.session_state.selected_year)

top_10_cram = event_dataframe.nlargest(10, 'C_RAM')

col_data, col_radar = st.columns(2)

# Display the DataFrame in the first column with color coding
with col_data:
    st.markdown("### Player Rankings")

    selected_players = st.multiselect(
        "Select Players for Radar Plot",
        options=top_10_cram["PLAYER"].unique(),
        default=top_10_cram["PLAYER"].iloc[:2]
    )

    render_table(top_10_cram)

# Create the bar chart and display it in the second column
with col_radar:
    st.markdown("### Player Comparison using 5MS")
    selected_players = top_10_cram[top_10_cram["PLAYER"].isin(selected_players)]

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
            y=-0.1,
            xanchor="center",
            x=0.5
        ),
        legend_font_color="white"    
    )

    st.plotly_chart(fig, theme="streamlit", use_container_width = False)

# Description at the bottom of the page

render_ai_button(top_10_cram, mop_ladder_prompt)