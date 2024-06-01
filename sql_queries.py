import streamlit as st
import pandas as pd

def get_player_box_scores(player_name, event_keyword, selected_year):
    conn = st.connection("snowpark")
    player_scores = pd.DataFrame()

    if player_name and event_keyword and selected_year:
        sql = f"""
            SELECT *
            FROM NIKE_TEST.SCHEMA_NIKE_TEST.PLAYER_STATS_MAY_21
            WHERE 
                PLAYER = '{player_name}' AND
                EVENT ILIKE '{event_keyword}' AND
                YEAR = '{selected_year}'
        """
        
        player_scores = conn.query(sql)

        whole_number_columns = ["PSP", "DSI", "FGS", "THREE_PE", "ATR", "RAM"]
        percentage_columns = ["FG_PCT", "THREE_PT_PCT", "FT_PCT"]
        
        for col in whole_number_columns:
            if col in player_scores.columns:
                player_scores[col] = player_scores[col].round(0)

        for col in percentage_columns:
            if col in player_scores.columns:
                player_scores[col] = player_scores[col].fillna(0)  # Replace NaN with 0
                player_scores[col] = (player_scores[col] * 100).round(0)

        for col in player_scores.select_dtypes(include='number').columns:
            if col not in whole_number_columns and col not in percentage_columns:
                player_scores[col] = player_scores[col].round(1)

    return player_scores


def get_table_from_snowflake(selected_event, selected_year):
    conn = st.connection("snowpark")
    table_response = pd.DataFrame()

    if selected_event and selected_year:
        sql = get_sql_query_from_event(selected_event, selected_year)
        table_response = conn.query(sql)

        whole_number_columns = ["PSP", "DSI", "FGS", "THREE_PE", "ATR", "RAM"]
        percentage_columns = ["FG_PCT", "THREE_PT_PCT", "FT_PCT"]
        
        for col in whole_number_columns:
            if col in table_response.columns:
                table_response[col] = table_response[col].round(0)

        for col in percentage_columns:
            if col in table_response.columns:
                table_response[col] = table_response[col].fillna(0)  # Replace NaN with 0
                table_response[col] = (table_response[col] * 100).round(0)

        for col in table_response.select_dtypes(include='number').columns:
            if col not in whole_number_columns and col not in percentage_columns:
                table_response[col] = table_response[col].round(1)

    return table_response

def get_sql_query_from_event(event_name, selected_year):
    print(event_name)
    
    event_keyword = event_name

    sql_query = f"""
        SELECT 
            PLAYER,
            COUNT(*) AS GAMES_PLAYED,
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
        WHERE EVENT ILIKE '{event_keyword}' AND YEAR = {selected_year}
        GROUP BY PLAYER
        ORDER BY RAM DESC
    """

    return sql_query

def get_event_data_df():
    event_list = [
        ("Nike Hoop Summit (Mens)", 1995),
        ("Nike Hoop Summit (Mens)", 1996),
        ("Nike Hoop Summit (Mens)", 1997),
        ("Nike Hoop Summit (Mens)", 1998),
        ("Nike Hoop Summit (Mens)", 1999),
        ("Nike Hoop Summit (Mens)", 2000),
        ("Nike Hoop Summit (Mens)", 2004),
        ("Nike Hoop Summit (Mens)", 2005),
        ("Nike Hoop Summit (Mens)", 2006),
        ("Nike Global Challenge", 2007),
        ("Nike Hoop Summit (Mens)", 2007),
        ("Nike Global Challenge", 2008),
        ("Nike Hoop Summit (Mens)", 2008),
        ("Nike Global Challenge", 2009),
        ("Nike Hoop Summit (Mens)", 2009),
        ("Nike Global Challenge", 2010),
        ("Nike Hoop Summit (Mens)", 2010),
        ("Nike Global Challenge", 2011),
        ("Nike Hoop Summit (Mens)", 2011),
        ("Nike Global Challenge", 2012),
        ("Nike Hoop Summit (Mens)", 2012),
        ("Nike Global Challenge", 2013),
        ("Nike Hoop Summit (Mens)", 2013),
        ("Nike EYBL (17U)", 2014),
        ("Nike Global Challenge", 2014),
        ("Nike Hoop Summit (Mens)", 2014),
        ("Nike Global Challenge", 2015),
        ("Nike Hoop Summit (Mens)", 2015),
        ("Nike Hoop Summit (Mens)", 2016),
        ("Nike Hoop Summit (Mens)", 2017),
        ("Nike Hoop Summit (Mens)", 2018),
        ("Nike EYBL (17U)", 2019),
        ("Nike Extravaganza (Boys)", 2019),
        ("Nike Extravaganza (Girls)", 2019),
        ("Nike Hoop Summit (Mens)", 2019),
        ("Nike EYBL (15U)", 2021),
        ("Nike EYBL (16U)", 2021),
        ("Nike EYBL (17U - Girls) - Nationals", 2021),
        ("Nike EYBL (17U)", 2021),
        ("Nike Extravaganza (Boys)", 2021),
        ("Nike EYBL (15U) - Session III (Kentucky)", 2022),
        ("Nike EYBL (15U) - Session IV (Kansas City)", 2022),
        ("Nike EYBL (16U) - Peach Jam (Augusta)", 2022),
        ("Nike EYBL (16U) - Session I (Orlando)", 2022),
        ("Nike EYBL (16U) - Session II (Indy)", 2022),
        ("Nike EYBL (16U) - Session III (Kentucky)", 2022),
        ("Nike EYBL (16U) - Session IV (Kansas City)", 2022),
        ("Nike EYBL (17U - Girls) - Nationals (Chicago)", 2022),
        ("Nike EYBL (17U - Girls) - Session I (Hampton)", 2022),
        ("Nike EYBL (17U - Girls) - Session II (Iowa)", 2022),
        ("Nike EYBL (17U - Girls) - Session II (Louisville)", 2022),
        ("Nike EYBL (17U) - Peach Jam (Augusta)", 2022),
        ("Nike EYBL (17U) - Session I (Orlando)", 2022),
        ("Nike EYBL (17U) - Session II (Indy)", 2022),
        ("Nike EYBL (17U) - Session III (Kentucky)", 2022),
        ("Nike EYBL (17U) - Session IV (Kansas City)", 2022),
        ("Nike EYBL (17U) - Session V (Augusta)", 2022),
        ("Nike Extravaganza (Boys)", 2022),
        ("Nike Extravaganza (Girls)", 2022),
        ("Nike Hoop Summit (Mens)", 2022),
        ("Nike EYBL (15U) - Peach Jam (Augusta)", 2023),
        ("Nike EYBL (15U) - Session I (Atlanta)", 2023),
        ("Nike EYBL (15U) - Session II (Phoenix)", 2023),
        ("Nike EYBL (15U) - Session III (Dallas)", 2023),
        ("Nike EYBL (15U) - Session IV (Memphis)", 2023),
        ("Nike EYBL (16U) - Peach Jam (Augusta)", 2023),
        ("Nike EYBL (16U) - Session I (Atlanta)", 2023),
        ("Nike EYBL (16U) - Session II (Phoenix)", 2023),
        ("Nike EYBL (16U) - Session III (Dallas)", 2023),
        ("Nike EYBL (16U) - Session IV (Memphis)", 2023),
        ("Nike EYBL (17U - Girls) - Nationals", 2023),
        ("Nike EYBL (17U - Girls) - Session I (Hampton)", 2023),
        ("Nike EYBL (17U - Girls) - Session II (Ames)", 2023),
        ("Nike EYBL (17U - Girls) - Session II (Birmingham)", 2023),
        ("Nike EYBL (17U - Girls) - Session II (Dallas)", 2023),
        ("Nike EYBL (17U - Girls) - Session II (Phoenix)", 2023),
        ("Nike EYBL (17U) - Peach Invitational Tournament (Augusta)", 2023),
        ("Nike EYBL (17U) - Peach Jam (Augusta)", 2023),
        ("Nike EYBL (17U) - Session I (Atlanta)", 2023),
        ("Nike EYBL (17U) - Session II (Phoenix)", 2023),
        ("Nike EYBL (17U) - Session III (Dallas)", 2023),
        ("Nike EYBL (17U) - Session IV (Memphis)", 2023),
        ("Nike EYBL (EYCL) - Session I (Atlanta)", 2023),
        ("Nike EYBL (EYCL) - Session II (Phoenix)", 2023),
        ("Nike EYBL (EYCL) - Session III (Memphis)", 2023),
        ("Nike Elite 100 Camp", 2023),
        ("Nike Extravaganza (Boys)", 2023),
        ("Nike Extravaganza (Girls)", 2023),
        ("Nike Hoop Summit (Mens)", 2023),
        ("Nike Hoop Summit (Womens)", 2023),
        ("Nike/USAB Hoop Summit - World Team Scrimmage (Mens)", 2023),
        ("Nike EYBL Scholastic Final", 2024)
    ]
    return pd.DataFrame(event_list, columns=['Event', 'Year'])

