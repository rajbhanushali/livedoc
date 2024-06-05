import streamlit as st
import plotly.express as px
import plotly.io as pio

from streamlit_extras.app_logo import add_logo
from utils import render_ai_button, render_box_score_table, export_to_pdf_button
from sql_queries import get_player_averages_dataframe, get_player_box_scores, get_event_top_5ms
from static_prompts import player_report_prompt
import copy

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


event_averages_dataframe = get_player_averages_dataframe(st.session_state.selected_event, st.session_state.selected_year)

st.markdown("### Select a player. Get Some Insights")
selected_player = st.selectbox(
    "Select Players for Radar Plot",
    options=event_averages_dataframe["PLAYER"].unique(),
)

player_box_score_dataframe = get_player_box_scores(selected_player, st.session_state.selected_event, st.session_state.selected_year)
selected_player_row = event_averages_dataframe[event_averages_dataframe["PLAYER"] == selected_player]
selected_player_row.rename(columns={'THREE_PE': '3PE'}, inplace=True)
st.dataframe(selected_player_row)

event_top_5ms = get_event_top_5ms(st.session_state.selected_event, st.session_state.selected_year)
print(event_top_5ms)
col_data, col_radar = st.columns(2)

# Display the DataFrame in the first column with color coding
with col_data:
    st.markdown("#### Player Box Score")
    render_box_score_table(player_box_score_dataframe)

# Create the bar chart and display it in the second column
with col_radar:
    st.markdown("#### Player 5MS")

    categories = ['PSP', 'ATR', 'DSI', 'FGS', '3PE']
    radar_data = selected_player_row.melt(id_vars=['PLAYER'], value_vars=categories, var_name='categories', value_name='values')

    scale_const = 0.7

    # Custom scales for each axis
    custom_scales = {
        'PSP': [0, scale_const * int(event_top_5ms['TOP_PSP'].iloc[0])],
        'ATR': [0, scale_const * int(event_top_5ms['TOP_ATR'].iloc[0])],
        'DSI': [0, scale_const * int(event_top_5ms['TOP_DSI'].iloc[0])],
        'FGS': [0, scale_const * int(event_top_5ms['TOP_FGS'].iloc[0])],
        '3PE': [0, scale_const * int(event_top_5ms['TOP_THREE_PE'].iloc[0])]
    }
    
    fig = px.line_polar(radar_data, r="values",
                    theta="categories",
                    color="PLAYER",
                    line_close=True,
                    #color_discrete_sequence=["#00eb93", "#4ed2ff"],
                    template="plotly_dark"
                    )                   

    # Update the radar plot with custom scales
    fig.update_polars(
        angularaxis_showgrid=False,
        radialaxis_gridwidth=0,
        gridshape='linear',
        bgcolor="#494b5a",
        radialaxis_showticklabels=False,
        radialaxis=dict(
            range=[min(custom_scales[cat][0] for cat in categories),
                max(custom_scales[cat][1] for cat in categories)]
        )
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

    pdf_fig = copy.deepcopy(fig)
    pdf_fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
        plot_bgcolor='rgba(0,0,0,0)',   # Transparent background
        font=dict(color='black'),       # Black text
        legend_font_color="black",
        legend_font_size=16,
        polar=dict(
            radialaxis=dict(
                tickfont=dict(size=16),  # Adjust radial axis tick font size
                title=dict(font=dict(size=16))  # Adjust radial axis title font size
            ),
            angularaxis=dict(
                tickfont=dict(size=22)  # Adjust the font size for the category labels
            )
        )
    )

    pdf_fig.update_polars(
        angularaxis_showgrid=False,
        radialaxis_gridwidth=0,
        gridshape='linear',
        radialaxis_showticklabels=False
    )
    pio.write_image(pdf_fig, '/tmp/player_radar_chart.png')

# Description at the bottom of the page

render_ai_button(player_box_score_dataframe, player_report_prompt)

export_to_pdf_button(selected_player, player_box_score_dataframe, selected_player_row)