import streamlit as st
from utils import plot_bar_chart, plot_pie_chart, render_ai_button
from sql_queries import get_table_from_snowflake
from streamlit_extras.app_logo import add_logo
from static_prompts import get_overview_prompt

st.set_page_config(
    page_title="CerebroEvent - Overview",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="collapsed"
)
add_logo("assets/cerebro_logo.png", height = 300)

if "selected_event" not in st.session_state or not st.session_state.selected_event or "selected_year" not in st.session_state:
    st.error(" ### Please return to Home and select an event ")
    st.stop()

# Title of the page
st.title(f"Overview of {st.session_state.selected_event}")

event_dataframe = get_table_from_snowflake(st.session_state.selected_event, st.session_state.selected_year)

total_players = event_dataframe["PLAYER"].nunique()
avg_ram = event_dataframe['RAM'].mean()
avg_cram = event_dataframe['C_RAM'].mean()

# Display total players and average RAM using columns
col1, col2, col3 = st.columns(3)
col1.metric("Total Players", total_players)
col2.metric("Average RAM", f"{avg_ram:.2f}")
col3.metric("Average C_RAM", f"{avg_cram:.2f}")

top_10_cram = event_dataframe.nlargest(10, 'C_RAM')[['PLAYER', 'C_RAM']]

# Layout for table and pie chart
left_column, right_column = st.columns([1, 1])
with left_column:
    st.markdown("### Top Players by C-RAM Score")
    plot_bar_chart(top_10_cram)
with right_column:
    st.markdown("### Event Breakdown by C-RAM")
    plot_pie_chart(event_dataframe)

render_ai_button(event_dataframe, get_overview_prompt(total_players, avg_ram, avg_cram))