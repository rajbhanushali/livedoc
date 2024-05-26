import streamlit as st
from utils import plot_bar_chart, plot_pie_chart, render_ai_button
from sql_queries import get_table_from_snowflake
from streamlit_extras.app_logo import add_logo

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

overview_prompt = f"""
You are a youth basketball analyst. The data in this table represents the top performers from the EYBL tournament. The tournament has {total_players} total players, with an average RAM score of {avg_ram:.2f} and an average C_RAM score of {avg_cram:.2f}. Analyze the top players' performances relative to these averages and the 5 metric suite (PSP, 3PE, FGS, ATR, DSI).

Provide a summary highlighting:
- Notable performances from players with the highest RAM and C_RAM scores.
- Comparison of these players' stats to the average RAM and C_RAM.
- Insights on their scoring, shooting, playmaking, around-the-rim skills, and defensive impact using the 5 metric suite.
- Bold the player names in your response.

For example:
"This event contained {total_players} players with an average RAM score of {avg_ram:.2f} and an average C_RAM score of {avg_cram:.2f}. The most notable performance came from **Player X** with a C_RAM score of 9.8, significantly above the average. **Player Y** also stood out with a PSP score of 85, indicating a strong scoring ability."

Here are descriptions of the key metrics:
- **RAM**: Overall Evaluation Score, ranging from 0 to 1000+, balancing efficiency, volume, and per-minute impact.
- **C-RAM**: Context Metric, comparing performance to the average, with scores from 0 to 10+, and medals for different performance levels.
- **PSP**: Pure Scoring Prowess, blending scoring volume and efficiency.
- **3PE**: 3-Point Efficiency, considering shooting volume and efficiency.
- **FGS**: Floor General Skills, exploring passing efficiency and volume.
- **ATR**: Around the Rim, indicators for big man play, including rebounds, blocks, and 2-point efficiency.
- **DSI**: Defensive Statistical Impact, combining events creation and defensive efficiency.

Use this information to generate a detailed analysis of the top players' performances, and easter-egg insights into interesting statistics from the event.
"""

render_ai_button(event_dataframe, overview_prompt)