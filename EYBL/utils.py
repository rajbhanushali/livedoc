import streamlit as st
import pandas as pd
import openai
import json
from openai import OpenAI

def get_dataframe_description(dataframe: pd.DataFrame, prompt: str) -> str:
    # Convert the DataFrame to CSV string
    openai.api_key = st.secrets.OPENAI_API_KEY

    client = OpenAI(api_key=st.secrets.OPENAI_API_KEY)
    dataframe_csv = dataframe.to_csv(index=False)
    
    # Prepare the message for the ChatGPT API
    messages = [
        {"role": "system", "content": "You are an NBA data analyst."},
        {"role": "user", "content": f"{prompt}\n\nHere is the data:\n{dataframe_csv}"}
    ]
    
    # Send the request to the ChatGPT API
    response = client.chat.completions.create(
        model="gpt-4o",  # Ensure you're using a model available in the new API
        messages=messages
    )
    
    # Extract and return the description from the response
    description = response.choices[0].message.content
    return description

eybl=pd.read_csv("EYBL.CSV")
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