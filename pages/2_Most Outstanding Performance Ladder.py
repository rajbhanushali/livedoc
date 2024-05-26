import streamlit as st
import plotly.express as px
from streamlit_extras.app_logo import add_logo

from utils import render_table, render_ai_button
from sql_queries import get_table_from_snowflake

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

mop_ladder_prompt = f"""
You are a youth basketball analyst. The data in this table represents the top performers from an event. Analyze the top players' performances relative to these averages and the 5 metric suite (PSP, 3PE, FGS, ATR, DSI).

Provide a summary highlighting:
- Notable performances from players with the highest RAM and C_RAM scores.
- Comparison of these players' stats to the average RAM and C_RAM.
- Insights on their scoring, shooting, playmaking, around-the-rim skills, and defensive impact using the 5 metric suite.
- Bold the player names in your response.

For example:
"The most notable performance came from **Player X** with a C_RAM score of 9.8, significantly above the average. **Player Y** also stood out with a PSP score of 85, indicating a strong scoring ability." Make it very detailed and include insights on each metric and each player. Focus on box score stats also like average points per game, rebounds, shooting percentage, etc.

Here are descriptions of the key metrics:
- **RAM**: Overall Evaluation Score, ranging from 0 to 1000+, balancing efficiency, volume, and per-minute impact.
- **C-RAM**: Context Metric, comparing performance to the average, with scores from 0 to 10+, and medals for different performance levels.
- **PSP**: Pure Scoring Prowess, blending scoring volume and efficiency.
- **3PE**: 3-Point Efficiency, considering shooting volume and efficiency.
- **FGS**: Floor General Skills, exploring passing efficiency and volume.
- **ATR**: Around the Rim, indicators for big man play, including rebounds, blocks, and 2-point efficiency.
- **DSI**: Defensive Statistical Impact, combining events creation and defensive efficiency.

Use this information to generate a detailed analysis of the top players' performances. Focus on comparisons between the players and highlighting strengths in one where a different player has a weakness, etc.
"""

render_ai_button(top_10_cram, mop_ladder_prompt)