import streamlit as st
import pandas as pd
import openai
import plotly.express as px
from openai import OpenAI
import altair as alt
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode, ColumnsAutoSizeMode

def call_gpt_and_stream_response(dataframe: pd.DataFrame, prompt: str) -> str:
    # Convert the DataFrame to CSV string
    openai.api_key = st.secrets.CHAT_COMPLETION_KEY

    client = OpenAI(api_key=st.secrets.CHAT_COMPLETION_KEY)
    dataframe_csv = dataframe.to_csv(index=False)
    
    # Prepare the message for the ChatGPT API
    messages = [
        {"role": "system", "content": "You are an NBA data analyst."},
        {"role": "user", "content": f"{prompt}\n\nHere is the data:\n{dataframe_csv}"}
    ]

  
    
    with st.chat_message("assistant"):
      response = ""
      resp_container = st.empty()
      for delta in client.chat.completions.create(
          model="gpt-4o",  # Ensure you're using a model available in the new API
          messages=messages,
          stream=True
      ):
        if delta.choices and delta.choices[0].delta.content:
          response += delta.choices[0].delta.content
          resp_container.markdown(response)
    
    # Extract and return the description from the response
    return response

def plot_bar_chart(dataframe):
    colname = dataframe.columns[1]
    colname = str(colname)

    # Define the custom color scale
    colors = ['#000000', '#CD7F32', '#C0C0C0', '#FFD700']  # Grey to Bronze to Silver to Gold
    
    # Normalize the values in the column for the continuous color scale
    dataframe['Normalized'] = (dataframe[colname] - dataframe[colname].min()) / (dataframe[colname].max() - dataframe[colname].min())

    fig = px.bar(
        dataframe,
        x=colname,
        y="PLAYER",
        orientation='h',
        color='Normalized',
        color_continuous_scale=colors,
        template='plotly_white',
        hover_data={colname: True, 'PLAYER': True, 'Normalized': False}  # Include only desired columns in hover data
    )
    fig.update_layout(
        xaxis_title=colname,
        xaxis_title_font_size=18,
        yaxis_title='PLAYER',
        yaxis_title_font_size=18,
        yaxis={'categoryorder': 'total ascending'},
        margin=dict(l=20, r=20, t=30, b=20),  # Adjust margins
        autosize=True  # Make the chart auto-size
    )
    st.plotly_chart(fig)

def plot_pie_chart(event_dataframe):
  # Pie chart data
  colors = ['#FFD700', '#C0C0C0', '#CD7F32', '#808080']  # Adjusted colors for contrast

  gold_player_count = (event_dataframe['C_RAM'] > 10).sum()
  silver_player_count = ((event_dataframe['C_RAM'] > 8.5) & (event_dataframe['C_RAM'] <= 10)).sum()
  bronze_player_count = ((event_dataframe['C_RAM'] > 7) & (event_dataframe['C_RAM'] <= 8.5)).sum()
  not_rated_player_count = len(event_dataframe) - (gold_player_count + silver_player_count + bronze_player_count)

  categories = ['Gold', 'Silver', 'Bronze', 'Not Rated']
  values = [gold_player_count, silver_player_count, bronze_player_count, not_rated_player_count]
  pie_data = pd.DataFrame({
    'Category': categories,
    'Values': values
  })
  base = alt.Chart(pie_data).encode(
    theta=alt.Theta("Values:Q", stack=True),
    color=alt.Color("Category:N", scale=alt.Scale(domain=categories, range=colors))
  )

  arc = base.mark_arc(innerRadius=50, outerRadius=150, stroke="#fff")
  
  st.altair_chart(arc, use_container_width=True)

def color_cram_value(val):
    if val >= 10:
        color = 'gold'
    elif 8.5 <= val < 10:
        color = 'silver'
    elif 7 <= val < 8.5:
        color = 'brown'
    else:
        color = 'transparent'
    return f'background-color: {color}'


def render_table(event_dataframe):
  cell_style_jscode = JsCode("""
    function(params) {
        if (params.value >= 10) {
            return { 'backgroundColor': 'gold' };
        } else if (params.value >= 8.5 && params.value < 10) {
            return { 'backgroundColor': 'silver' };
        } else if (params.value >= 7 && params.value < 8.5) {
            return { 'backgroundColor': 'brown' };
        } else {
            return { 'backgroundColor': 'transparent' };
        }
    }
""")

  gb = GridOptionsBuilder.from_dataframe(event_dataframe)

  # Apply custom cell styles using JS function for the 'C_RAM' column
  gb.configure_column('C_RAM', cellStyle=cell_style_jscode)

  gridOptions = gb.build()

  # Calculate dynamic height
  num_rows = len(event_dataframe)
  row_height = 25
  dynamic_height = min(max(200, 56 + num_rows * row_height), 600)

  # Display using AgGrid with custom styling
  AgGrid(
      event_dataframe,
      gridOptions=gridOptions,
      height=dynamic_height,
      width='100%',
      allow_unsafe_jscode=True,
      columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS
  )


def render_ai_button(dataframe, prompt):
  # Custom CSS to center the button
  st.markdown("""
    <style>
    .stButton > button {
        display: block;
        margin: 0 auto;
        padding: 10px 20px;  /* Adjust padding */
        width: 200px;  /* Adjust width */
        height: 60px;
    }
    </style>
    """, unsafe_allow_html=True)

  # Center the button using the custom CSS
  if st.button("Get AI Analysis"):
    call_gpt_and_stream_response(dataframe, prompt)

def render_player_match_ai_button(event_dataframe, player1, player2, prompt):
  st.markdown("""
    <style>
    .stButton > button {
        display: block;
        margin: 0 auto;
        padding: 10px 20px;  /* Adjust padding */
        width: 200px;  /* Adjust width */
        height: 60px;
    }
    </style>
    """, unsafe_allow_html=True)

  if st.button('Confirm Selection'):
    st.write(f'You selected: {player1} and {player2}')
    selected_players_averages = event_dataframe[event_dataframe['PLAYER'].isin([player1, player2])]
    call_gpt_and_stream_response(selected_players_averages, prompt)