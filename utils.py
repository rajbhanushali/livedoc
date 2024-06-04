import streamlit as st
import pandas as pd
import openai
import plotly.express as px
import altair as alt

from fpdf import FPDF
from openai import OpenAI
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

def plot_c_ram_bar_chart(dataframe):
    colname = "C_RAM"

    # Define the custom color scale
    colors = {
        'Gold': '#FFD700',
        'Silver': '#C0C0C0',
        'Bronze': '#CD7F32',
        'Not Rated': '#000000'
    }

    # Assign categories based on the value ranges
    def assign_category(value):
        if value > 10:
            return 'Gold'
        elif value > 8.5:
            return 'Silver'
        elif value > 7:
            return 'Bronze'
        else:
            return 'Not Rated'

    dataframe['Category'] = dataframe[colname].apply(assign_category)

    # Ensure all categories are present in the dataframe to avoid KeyError
    for category in colors.keys():
        if category not in dataframe['Category'].values:
            dataframe = dataframe.append({'PLAYER': '', colname: 0, 'Category': category}, ignore_index=True)

    fig = px.bar(
        dataframe,
        x=colname,
        y="PLAYER",
        orientation='h',
        color='Category',
        color_discrete_map=colors,
        template='plotly_white',
        hover_data={colname: True, 'PLAYER': True, 'Category': False}  # Include only desired columns in hover data
    )

    fig.update_layout(
        xaxis_title=colname,
        xaxis_title_font_size=18,
        yaxis_title='PLAYER',
        yaxis_title_font_size=18,
        yaxis={'categoryorder': 'total ascending'},
        margin=dict(l=20, r=20, t=30, b=20),  # Adjust margins
        autosize=True,  # Make the chart auto-size
        legend_title_text="Medal"  # Change the legend title
    )

    st.plotly_chart(fig)

def plot_player_chart(dataframe):
   plot_bar_chart(dataframe, dataframe.columns[1], 'PLAYER')

def plot_bar_chart(dataframe, x_col, y_col):

    # Define the custom color scale
    colors = ['#000000', '#CD7F32', '#C0C0C0', '#FFD700']  # Grey to Bronze to Silver to Gold
    
    # Normalize the values in the column for the continuous color scale
    dataframe['Normalized'] = (dataframe[x_col] - dataframe[x_col].min()) / (dataframe[x_col].max() - dataframe[x_col].min())

    fig = px.bar(
        dataframe,
        x=x_col,
        y=y_col,
        orientation='h',
        color='Normalized',
        color_continuous_scale=colors,
        template='plotly_white',
        hover_data={x_col: True, y_col: True, 'Normalized': False}  # Include only desired columns in hover data
    )
    fig.update_layout(
        xaxis_title=x_col,
        xaxis_title_font_size=18,
        yaxis_title=y_col,
        yaxis_title_font_size=18,
        yaxis={'categoryorder': 'total ascending'},
        margin=dict(l=20, r=20, t=30, b=20),  # Adjust margins
        autosize=True,
        coloraxis_showscale=False
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
    color=alt.Color("Category:N", scale=alt.Scale(domain=categories, range=colors), title="Medal")
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


def render_box_score_table(box_score_dataframe):
    # Filter and order columns
    columns_to_show = [
        "PLAYER", "TEAM", "MINUTES", "OPP", "WIN", "TEAM_SCORE", "OPP_SCORE", 
        "RAM", "C_RAM", "PSP", "FGS", "DSI", "THREE_PE", "ATR",
        "PTS", "REB",
        "AST", "STL", "BLK", "FGM", "FGA", "FG_PCT", "THREE_POINTS_MADE",
        "THREE_POINTS_ATTEMPTED", "THREE_PT_PCT", "FREE_THROWS_MADE", 
        "FTA", "FT_PCT"
    ]

    # Select and reorder the columns
    box_score_dataframe = box_score_dataframe[columns_to_show]

    # Define the JS code for cell styles based on value ranges for C_RAM
    cram_color_js = JsCode(
        """
        function(params) {
            if (params.value >= 10) {
                return { 'backgroundColor': 'gold' };
            } else if (params.value >= 8.5 && params.value < 10) {
                return { 'backgroundColor': 'silver' };
            } else if (params.value >= 7 && params.value < 8.5) {
                return { 'backgroundColor': '#CD7F32' };
            } else {
                return { 'backgroundColor': 'transparent' };
            }
        }
        """
    )

    gb = GridOptionsBuilder.from_dataframe(box_score_dataframe)

    # Apply percentage formatting to specific columns
    percentage_columns = ["FG_PCT", "THREE_PT_PCT", "FT_PCT"]
    for col in percentage_columns:
        gb.configure_column(col, type=["numericColumn"], valueFormatter="x.toFixed(0) + '%'")

    # Apply custom cell styles using JS function for the 'C_RAM' column
    gb.configure_column('C_RAM', cellStyle=cram_color_js)

    gridOptions = gb.build()

    # Calculate dynamic height
    num_rows = len(box_score_dataframe)
    row_height = 25
    dynamic_height = min(max(200, 56 + num_rows * row_height), 600)

    # Display using AgGrid with custom styling
    grid_response = AgGrid(
        box_score_dataframe,
        gridOptions=gridOptions,
        height=dynamic_height,
        width='100%',
        allow_unsafe_jscode=True,
        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS
    )
    
    selected_rows_df = pd.DataFrame(grid_response['selected_rows'])
    
    return selected_rows_df



def render_event_table(event_dataframe):
    cram_color_js = JsCode(
        """
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
        """
    )

    max_values = event_dataframe.iloc[:, 1:].max()
    highlight_max = JsCode(
        """
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
        """ % max_values.to_dict()
    )

    # Add a checkbox column at the first position
    event_dataframe.insert(0, "", False)

    gb = GridOptionsBuilder.from_dataframe(event_dataframe)

    # Apply percentage formatting to specific columns
    percentage_columns = ["FG_PCT", "THREE_PT_PCT", "FT_PCT"]
    for col in percentage_columns:
        gb.configure_column(col, type=["numericColumn"], valueFormatter="x.toFixed(0) + '%'")

    # Apply custom cell styles using JS function for the 'C_RAM' column
    gb.configure_column('C_RAM', cellStyle=cram_color_js)

    # Apply highlight for max values
    for col in event_dataframe.columns[1:]:  # Exclude the checkbox column from styling
        if col != 'C_RAM':
            gb.configure_column(col, cellStyle=highlight_max)

    gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren=True)
    gridOptions = gb.build()

    # Calculate dynamic height
    num_rows = len(event_dataframe)
    row_height = 25
    dynamic_height = min(max(200, 56 + num_rows * row_height), 400)

    # Display using AgGrid with custom styling
    return AgGrid(
        event_dataframe,
        gridOptions=gridOptions,
        height=dynamic_height,
        width='100%',
        allow_unsafe_jscode=True,
        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS
    )


def render_team_table(event_dataframe):
    max_values = event_dataframe.iloc[:, 1:].max()
    highlight_max = JsCode(
        """
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
        """ % max_values.to_dict()
    )

    # Add a checkbox column at the first position
    event_dataframe.insert(0, "", False)

    gb = GridOptionsBuilder.from_dataframe(event_dataframe)

    # Apply highlight for max values
    for col in event_dataframe.columns[1:]:  # Exclude the checkbox column from styling
        if col != 'C_RAM':
            gb.configure_column(col, cellStyle=highlight_max)
    
    # Apply percentage formatting to specific columns
    percentage_columns = ["FG%", "3FG%", "FT%"]
    for col in percentage_columns:
        gb.configure_column(col, type=["numericColumn"], valueFormatter="x.toFixed(0) + '%'")

    gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren=True)
    gridOptions = gb.build()
    
    #gb.configure_grid_options(autoSizeColumnsOnLoad=True)

    # Calculate dynamic height
    num_rows = len(event_dataframe)
    row_height = 25
    dynamic_height = min(max(200, 56 + num_rows * row_height), 400)

    # Display using AgGrid with custom styling
    return AgGrid(
        event_dataframe,
        gridOptions=gridOptions,
        height=dynamic_height,
        width='100%',
        allow_unsafe_jscode=True,
        columns_auto_size_mode=None
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
  if st.button("Generate AI Analysis"):
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

def export_to_pdf_button(selected_player, player_box_score_dataframe, selected_player_row):

    def header(pdf):
    # Add the header
        pdf.set_font("Arial", 'B', 20)
        pdf.cell(0, 10, "Player Event Breakdown", ln=True, align='R')

    def add_title_section(pdf, player_name, team_name, event_name, games_played, minutes_per_game):
        # Add the player's name and team on the left, and the event name on the right
        pdf.set_font("Arial", 'B', 16)
        left_cell_width = pdf.get_string_width(f"{player_name} - {team_name}") + 2
        right_cell_width = pdf.get_string_width(event_name) + 2
        
        pdf.cell(left_cell_width, 10, f"{player_name} - {team_name}", ln=False, align='L')
        pdf.set_x(pdf.w - right_cell_width - pdf.r_margin)  # Position the right-aligned cell
        pdf.cell(right_cell_width, 10, event_name, ln=True, align='R')
        
        # Add games played and minutes per game on the left
        pdf.set_font("Arial", '', 12)
        details_width = pdf.get_string_width(f"{games_played} GAMES PLAYED | {minutes_per_game} MINUTES PER GAME") + 2
        pdf.cell(details_width, 10, f"{games_played} GAMES PLAYED | {minutes_per_game} MINUTES PER GAME", ln=True, align='L')
        pdf.ln(10)

    def add_metrics_section(pdf, ram, cram):
        # Add metrics section
        pdf.set_font("Arial", 'B', 20)
        pdf.cell(42, 20, f"{ram} RAM", ln=False, align='C', border=1)
        pdf.cell(42, 20, f"{cram} C-RAM", ln=False, align='C', border=1)

    def add_breakdowns(pdf, stat_breakdown_df, skill_breakdown_df):
        # Add stat breakdown table
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "STAT BREAKDOWN", ln=True, align='L')
        pdf.set_font("Arial", '', 10)
        
        # Calculate column widths based on content
        col_widths = []
        for col in stat_breakdown_df.columns:
            max_width = pdf.get_string_width(col) + 4  # Column header width
            for value in stat_breakdown_df[col]:
                max_width = max(max_width, pdf.get_string_width(str(value)) + 4)
            col_widths.append(max_width)
        
        row_height = pdf.font_size * 1.5
        
        # Header
        for i, column in enumerate(stat_breakdown_df.columns):
            pdf.cell(col_widths[i], row_height, column, border=1, align='C')
        pdf.ln()
        
        # Rows
        for index, row in stat_breakdown_df.iterrows():
            for i, item in enumerate(row):
                pdf.cell(col_widths[i], row_height, str(item), border=1, align='C')
            pdf.ln()
        
        pdf.ln(4)
        
        # Add skill breakdown table transposed
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "SKILL BREAKDOWN", ln=True, align='L')
        pdf.set_font("Arial", '', 10)
        
        transposed_skill_df = skill_breakdown_df.T
        transposed_skill_df.columns = transposed_skill_df.iloc[0]
        transposed_skill_df = transposed_skill_df[1:]
        
        # Calculate column widths based on content
        col_widths = []
        for col in transposed_skill_df.columns:
            max_width = pdf.get_string_width(col) + 4  # Column header width
            for value in transposed_skill_df[col]:
                max_width = max(max_width, pdf.get_string_width(str(value)) + 4)
            col_widths.append(max_width)
        
        # Header
        for i, column in enumerate(transposed_skill_df.columns):
            pdf.cell(col_widths[i], row_height, column, border=1, align='C')
        pdf.ln(row_height)
        
        # Rows
        for index, row in transposed_skill_df.iterrows():
            for i, item in enumerate(row):
                pdf.cell(col_widths[i], row_height, str(item), border=1, align='C')
            pdf.ln(row_height)
        
        pdf.ln(5)

    def add_game_log(pdf, game_log_df):
        # Add game log table
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "GAME LOG", ln=True, align='L')
        pdf.set_font("Arial", '', 10)
        
        # Calculate column widths based on content
        col_widths = []
        for col in game_log_df.columns:
            max_width = pdf.get_string_width(col) + 4  # Column header width
            for value in game_log_df[col]:
                max_width = max(max_width, pdf.get_string_width(str(value)) + 4)
            col_widths.append(max_width)
        
        # Header
        for i, column in enumerate(game_log_df.columns):
            pdf.cell(col_widths[i], 10, column, border=1, align='C')
        pdf.ln()
        
        # Rows
        for index, row in game_log_df.iterrows():
            for i, item in enumerate(row):
                pdf.cell(col_widths[i], 10, str(item), border=1, align='C')
            pdf.ln()

    # Function to create PDF using fpdf
    def create_pdf(player_name, box_score_df, selected_player_row):

        #Grab necessary fields for data population
        YEAR = str(st.session_state.selected_year)
        EVENT = str(st.session_state.selected_event)
        GAMES_PLAYED = selected_player_row['GAMES_PLAYED'].iloc[0]
        MINUTES = selected_player_row['MIN'].iloc[0]
        TEAM = str(box_score_df['TEAM'].iloc[0])
        RAM = selected_player_row['RAM'].iloc[0]
        C_RAM = selected_player_row['C_RAM'].iloc[0]

        per_game_stat_breakdown = selected_player_row[['PPG', 'RPG', 'APG', 'SPG', 'BPG', 'FG_PCT', 'THREE_PT_PCT', 'FT_PCT']]
        per_40_stat_breakdown = pd.DataFrame(columns=['PPG', 'RPG', 'APG', 'SPG', 'BPG', 'FG_PCT', 'THREE_PT_PCT', 'FT_PCT'])
        per_40_stat_breakdown[['PPG', 'RPG', 'APG', 'SPG', 'BPG']] = round((per_game_stat_breakdown[['PPG', 'RPG', 'APG', 'SPG', 'BPG']]/MINUTES)*40, 1)
        per_40_stat_breakdown[['FG_PCT', 'THREE_PT_PCT', 'FT_PCT']] = per_game_stat_breakdown[['FG_PCT', 'THREE_PT_PCT', 'FT_PCT']]
        per_game_stat_breakdown['Category'] = 'PER GAME'
        per_40_stat_breakdown['Category'] = 'PER 40 MINS'

        col = per_game_stat_breakdown.pop('Category')
        per_game_stat_breakdown.insert(0, 'Category', col)

        col = per_40_stat_breakdown.pop('Category')
        per_40_stat_breakdown.insert(0, 'Category', col)

        stat_breakdown_df = pd.concat([per_game_stat_breakdown, per_40_stat_breakdown], axis=0)

        skill_breakdown_df = pd.DataFrame({
            '5 Metric Suite': ['Pure Scoring Prowess', '3-Point Efficiency', 'Floor General Skills', 'Big Man Strengths', 'Defensive Statistical Impact'],
            'Score': list(selected_player_row[['PSP', 'THREE_PE', 'FGS', 'ATR', 'DSI']].iloc[0].astype(int))
        })

        game_log_df = pd.DataFrame(columns=['TEAMS', 'MP', 'FG', '3PT', 'FT', 'PTS', 'AST', 'REB', 'STL', 'BLK'])
        game_log_df['FG'] = box_score_df['FGM'].astype(str) + '-' + box_score_df['FGA'].astype(str)
        game_log_df['3PT'] = box_score_df['THREE_POINTS_MADE'].astype(str) + '-' + box_score_df['THREE_POINTS_ATTEMPTED'].astype(str)
        game_log_df['FT'] = box_score_df['FREE_THROWS_MADE'].astype(str) + '-' + box_score_df['FTA'].astype(str)
        game_log_df[['TEAMS', 'MP', 'PTS', 'AST', 'REB', 'STL', 'BLK']] = box_score_df[['OPP', 'MINUTES', 'PTS', 'AST', 'REB', 'STL', 'BLK']]

        pdf = FPDF(orientation='L', unit='mm', format='A4')
        pdf.add_page()
        
        # Add header
        header(pdf)
        
        # Add the title section
        add_title_section(pdf, selected_player, TEAM, YEAR + " - " + EVENT, GAMES_PLAYED, MINUTES)
        
        pdf.line(10, pdf.get_y()-8, 287, pdf.get_y()-8)

        # Add metrics section
        add_metrics_section(pdf, RAM, C_RAM)
        pdf.ln(25)
        
        # Add stat breakdown
        add_breakdowns(pdf, stat_breakdown_df, skill_breakdown_df)

        # Add game log
        add_game_log(pdf, game_log_df)
        
        pdf_output_path = '/tmp/player_report.pdf'
        pdf.output(pdf_output_path)
        return pdf_output_path
        
    # Button to generate and download the PDF report
    if st.button("Export Report as PDF"):
        pdf_path = create_pdf(selected_player, player_box_score_dataframe, selected_player_row)
        with open(pdf_path, 'rb') as f:
            pdf_data = f.read()
        st.download_button(label="Download Player Report", data=pdf_data, file_name="player_report.pdf", mime='application/pdf')
