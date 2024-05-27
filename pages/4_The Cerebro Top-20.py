import streamlit as st
from utils import plot_bar_chart, plot_pie_chart, render_ai_button
from sql_queries import get_table_from_snowflake
from streamlit_extras.app_logo import add_logo
from static_prompts import get_overview_prompt, get_skill_leader_prompt
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode


st.set_page_config(
    page_title="CerebroEvent - Overview",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="collapsed"
)
add_logo("assets/cerebro_logo.png", height = 300)

st.title(f"CEREBRO top 20 for {st.session_state.selected_event}")

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
grid_response = AgGrid(df, gridOptions=gridOptions, allow_unsafe_jscode=True, update_mode='selection_changed', ColumnsAutoSizeMode.FIT_CONTENTS)
selected_rows_df = pd.DataFrame(grid_response['selected_rows'])

# Get selected rows
selected_rows = grid_response['selected_rows']

# Display the selected player's name
if not selected_rows_df.empty:
    st.write("Selected player:"  )
    st.write(selected_rows)
else:
    st.write("No player selected")
