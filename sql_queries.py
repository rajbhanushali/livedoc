import streamlit as st
import pandas as pd

def get_table_from_snowflake(selected_event):
  conn = st.experimental_connection("snowpark")
  table_response = pd.DataFrame()

  if selected_event:
    sql = get_sql_query_from_event(selected_event)
    table_response = conn.query(sql)
    
  return table_response

def get_sql_query_from_event(event_name):
    if event_name == "Nike EYBL 17U - 2023":
        year = 2023
        event_keyword = '%Nike EYBL (17U)%'
    if event_name == "Nike Hoop Summit - 2022":
        year = 2022
        event_keyword = '%Nike Hoop Summit (Mens)%'
    if event_name == "Nike EYBL 17U - 2021":
        year = 2021
        event_keyword = '%Nike EYBL (17U)%'
    if event_name == "Nike EYBL 17U - 2019":
        year = 2019
        event_keyword = '%Nike EYBL (17U)%'
    if event_name == "Augusta Peach Jam - 2022":
        year = 2022
        event_keyword = '%Peach Jam%'

    if year and event_keyword:
        sql_query = f"""
            SELECT 
                PLAYER,
                AVG(RAM) AS RAM,
                AVG(C_RAM) AS C_RAM,
                AVG(PSP) AS PSP,
                AVG(DSI) AS DSI,
                AVG(FGS) AS FGS,
                AVG(THREE_PE) AS THREE_PE,
                AVG(ATR) AS ATR,
                AVG(PTS) AS PPG,
                AVG(REB) AS RPG,
                AVG(AST) AS APG,
                AVG(STL) AS SPG,
                AVG(BLK) AS BPG,
                SUM(FGM) / NULLIF(SUM(FGA), 0) AS FG_PCT,
                SUM(THREE_POINTS_MADE) / NULLIF(SUM(THREE_POINTS_ATTEMPTED), 0) AS THREE_PT_PCT,
                SUM(FREE_THROWS_MADE) / NULLIF(SUM(FTA), 0) AS FT_PCT
            FROM NIKE_TEST.SCHEMA_NIKE_TEST.PLAYER_STATS_MAY_21
            WHERE EVENT ILIKE '{event_keyword}' AND YEAR = {year}
            GROUP BY PLAYER
            ORDER BY RAM DESC
    """

    return sql_query
