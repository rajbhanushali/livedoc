import streamlit as st
from utils import render_ai_button
from sql_queries import get_table_from_snowflake
from streamlit_extras.app_logo import add_logo
from static_prompts import get_top20_prompt
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode , ColumnsAutoSizeMode

st.set_page_config(
    page_title="CerebroEvent - Overview",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded"
)
add_logo("assets/cerebro_logo.png", height = 300)

st.title(f"CEREBRO top 20 for {st.session_state.selected_event}")
st.header("Select a player to learn more")

event_dataframe = get_table_from_snowflake(st.session_state.selected_event, st.session_state.selected_year)
df = event_dataframe.nlargest(20, "RAM")


# Find the maximum values for each column
max_values = df.iloc[:, 1:].max()
# Define the JS code to highlight the max value in green
highlight_max = JsCode("""
function(params) {
    var maxValues = %s;
    if (params.value == maxValues[params.colDef.field]) {
        return {
            'color': 'white',
            'backgroundColor': 'green'
        }
    }
    return {
        'color': 'white',
        'backgroundColor': 'transparent'
    }
}
""" % max_values.to_dict())

# Add a checkbox column at the first position
df.insert(0,"", False)


# Create the AgGrid configuration
gb = GridOptionsBuilder.from_dataframe(df)
for col in df.columns[1:]:  # Exclude the 'SELECT' column from styling
    gb.configure_column(col, cellStyle=highlight_max)
gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren=True)
gridOptions = gb.build()


# Display the AgGrid table with highlighting
grid_response = AgGrid(df, gridOptions=gridOptions, allow_unsafe_jscode=True, update_mode='selection_changed', columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS)
selected_rows_df = pd.DataFrame(grid_response['selected_rows'])


top_player = df.iloc[0,1]

# Get selected rows
selected_rows = grid_response['selected_rows']

# Display the selected player's name
if not selected_rows_df.empty:
    selected_rows_df = selected_rows_df.drop('_selectedRowNodeInfo', axis=1)
    selected_player= selected_rows_df.iloc[0,1]
    selected_player
    st.write("Selected player:"  )
    st.write(selected_rows_df)
    render_ai_button(event_dataframe,get_top20_prompt(selected_player, st.session_state.selected_event))
else:
    st.write(f"Here we see the top 20 players in the event with {top_player} leading the way. Click a players name to generate a statistical analysis on their performance. ")


