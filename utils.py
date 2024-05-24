import streamlit as st
import pandas as pd
import openai
import plotly.express as px
from openai import OpenAI
import altair as alt

def get_dataframe_description(dataframe: pd.DataFrame, prompt: str) -> str:
    # Convert the DataFrame to CSV string
    openai.api_key = st.secrets.CHAT_COMPLETION_KEY

    client = OpenAI(api_key=st.secrets.CHAT_COMPLETION_KEY)
    dataframe_csv = dataframe.to_csv(index=False)
    
    # Prepare the message for the ChatGPT API
    messages = [
        {"role": "system", "content": "You are an NBA data analyst."},
        {"role": "user", "content": f"{prompt}\n\nHere is the data:\n{dataframe_csv}"}
    ]
    
    
    response = ""
    resp_container = st.empty()
    for delta in client.chat.completions.create(
        model="gpt-4o",  # Ensure you're using a model available in the new API
        messages=messages,
        stream=True
    ):
      if delta.choices:
        response += delta.choices[0].delta.content
        resp_container.markdown(response)
    
    # Extract and return the description from the response
    return response


url_data = (r'https://raw.githubusercontent.com/cerebrosportsdev/livedoc/main/EYBL.csv')

eybl=pd.read_csv(url_data)
# conn = st.experimental_connection("snowpark")
# sql = ""
# eybl=conn.query(sql)
ppg=eybl['PTS/G'].mean()
ppg = round(ppg,2)

eybl['FG%'] = eybl['FG%'].str.rstrip('%').astype(float)
fg_pct=eybl['FG%'].mean()
fg_pct= round(fg_pct,2)

ram = eybl['RAM'].mean()
ram = round(ram,2)

c_ram=eybl['C-RAM'].mean()
c_ram=round(c_ram,2)

gold = (eybl['C-RAM'] > 10).sum()
silver = ((eybl['C-RAM'] > 8.5) & (eybl['C-RAM'] < 10)).sum()
bronze = ((eybl['C-RAM'] > 7) & (eybl['C-RAM'] < 8.5)).sum()


# Custom HTML for the table
table_html = """
<table style='width:100%'>
  <tr style='background-color: black; color: white;'>
    <th>Tiers</th>
    <th>C-RAM</th>
    <th>#</th>
    <th>Avg RAM</th>
  </tr>
  <tr style='background-color: #FFD700;'>
    <td>Gold:</td>
    <td>10+</td>
    <td>6</td>
    <td>1033</td>
  </tr>
  <tr style='background-color: #C0C0C0;'>  <!-- Adjusted Silver color to a lighter shade -->
    <td>Silver:</td>
    <td>8.5-10</td>
    <td>13</td>
    <td>747</td>
  </tr>
  <tr style='background-color: #CD7F32;'>
    <td>Bronze:</td>
    <td>7-8.5</td>
    <td>45</td>
    <td>635</td>
  </tr>
</table>
"""

def plot_bar_chart(dataframe):
    fig = px.bar(
        dataframe,
        x="C_RAM",
        y="PLAYER",
        orientation='h',
        title="Top Players by C-RAM Score",
        color='C_RAM',
        color_continuous_scale='viridis',
        labels={'C-RAM': 'C-RAM Score', 'Name': 'Player Name'},
        template='plotly_white'
    )
    fig.update_layout(
        title_font_size=24,
        xaxis_title_font_size=18,
        yaxis_title_font_size=18,
        yaxis={'categoryorder': 'total ascending'}
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
