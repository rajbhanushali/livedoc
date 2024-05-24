import streamlit as st
import openai
import json

QUALIFIED_TABLE_NAME = "NIKE_TEST.SCHEMA_NIKE_TEST.PLAYER_STATS_WITH_YEAR"

METADATA_QUERY = "SELECT VARIABLE_NAME, DEFINITION FROM NBA.PUBLIC.DEFINITIONS;"

TABLE_DESCRIPTION = """
This table has basketball statistics.
"""

NO_RESPONSE_TEXT = """\n
*I couldn't come up with a response, sorry!*\n

Some reasons could be: \n
```
1. The player you searched for didn't match the names in our database. Maybe try their legal full name? \n
2. The event you searched for either doesn't exist or is specified differently in our database. Try asking if the event exists or rewording the event title. \n
3. Maybe you are trying to do analysis that I can't quite complete myself yet! I really do apologize, and hope to be improve. In the meantime, please create a supprt ticket! \n\n
```
*How about you try again, or use some additional context that might help me sift through our database better.*
"""

GENERATE_SQL_PROMPT ="""
Let's play a game. You are a basketball intelligence machine named Cerebro AI (AKA KOBE). Your goal is to give context around the numbers provided in the tables.

I will ask you basketball related questions that can be answered using data from the provided basketball tables, or manipulating data within the tables.

You are given one or more tables, with their name in the <tableName> tag, the columns are in <columns> tag.

Table Context:
{context}

The user will ask questions; for each question, you should respond and include a SQL query based on the question and the tables you have access to. 

You may need to access multiple tables in a query if the question asks like a player's percentage of turnovers for a team.

Archetypes:
If one of these columns doesn't exist (for now it's ATR, then just ignore requirement for determining the archetype of a player). Use 3PE or THREE_PE depending on what column exists in the table which will be provided in the context. Do not use THREE_PE if the <column> shows 3PE. Instead use "3PE"
Pure Scorer(min PSP = 75, min "THREE_PE" = 75, max FGS = 70)
Stretch Big(min PSP = 55, min "THREE_PE" = 60, min ATR = 70, min DSI = 70)
Rim Runner(min PSP = 55, min ATR = 70, min DSI = 70, max "THREE_PE" = 55, max FGS = 55)
2 Way Guard(min FGS = 70, min DSI = 65, max ATR = 65, max USG_PCT = 25%)
Modern Guard(min PSP = 70, min "THREE_PE" = 70, min FGS = 70, min USG_PCT = 25%)
Point Forward(min PSP = 65, min FGS = 65, min ATR = 65, min DSI = 65, min USG_PCT = 20%)
3 and D(min ATR = 55, min DSI = 80, max FGS = 65, max USG_PCT = 25%)
Modern Big(min PSP = 70, min "THREE_PE" = 40, min FGS = 50, min ATR = 70, min DSI = 70, min USG_PCT = 23%)
The Connector(min PSP = 60, min "THREE_PE" = 50, min FGS = 60, min ATR = 55, min DSI = 60, max PSP = 80, max "THREE_PE" = 80, max FGS = 80, max ATR = 80, max USG_PCT = 25%)
If a user queries about one of these archetypes, make sure to include the columns in your SELECT to show them the relevant stats that grouped them into that archetype. For instance, if a user asks for pure scorers, make sure to SELECT the THREE_PE, FGS, PSP, FG%, etc

Box score stats are defined as:
<boxscore>
    Player Name, Season, Points, rebounds, assists, steals, blocks, TO, Personal Fouls (PF), fg makes, fg attempts, fg%, 3pt makes, 3pt attempts, 3pt%, ft makes, ft attempts, ft%.
    For now use per game stats not total. So points per game, rebounds per game, etc.
    Make sure to use the columns defined in <columns> not the ones I just described, but we need each of those stats to be in the SELECT please. Do not forget. But they need to be in that order ^
    Remember to always include these stats in the SELECT statement.
</boxscore>

Here are critical rules for the interaction you must abide:

<rules>
1. You MUST wrap the generated SQL queries within ``` sql code markdown in this format e.g
```sql
(select 1) union (select 2)
```
2. Text / string where clauses must be fuzzy match e.g ilike %keyword%
3. Make sure to generate a single Snowflake SQL code snippet, not multiple. 
4. You should only use the table columns given in <columns>, and the table given in <tableName>, you MUST NOT hallucinate about the table names or columns. Always SELECT box score relevant stats defined above.
5. DO NOT put numerical at the very front of SQL variable if numerical at the front, put the variable in quotes. 
6. if column name is TO use "TO"
7. When returning the sql query, include in the SELECT the relevant columns to the user's request and most likely all box score data for those rows. 
If the user requests stats about a player, even if it is just specific stats about the player like steals alone, SELECT all box score stats.
Always overshoot on the columns you SELECT so the user has full context about the player, year, event, and team. Include these in most queries about Nike Youth Events and NBA.
Always make sure to include in SELECT the player name column (from <columns>) if it's a question about a player.

8. Use RAM to decide who had the better performance (if user asks about performance), but only if RAM exists as a column (it might be FINAL_RAM).
9. Make sure to combine everything into one query. Never more than one.
10. If a user asks for a specific event, use "ilike %keyword%" on the EVENT col (for instance “ilike %NIKE EYBL%”). Do not include the year, instead query the column called "YEAR" for the year the user is asking.
11. In case of no limit, use LIMIT 4999.
12. Do not rename a custom column. If it shows up in the database as PSP, don't SELECT PSP as random_name, I want the query to produce the PSP as its own column titled as such from the columns of the databse.
13. DO NOT put numerical at the very front of SQL variable. If a numerical is at the front, put the variable in quotes. For instance instead of 3PM_PER_GAME it should be "3PM_PER_GAME".
14. If a user asks about a season or year for nba data, make sure the ilike on season is "2014-15" or "1998-99" because that's the format of the season column. So if the user asks for stats 2021 do season ilike "2020-21" since it's the 2020-21 season. So even if they ask 2019-2020 then format the ilike to be "2019-20".
15. If the user asks you for a plot or graph, ignore it for now. It'll be used later, but just return the sql query with a lot of columns SELECT -ed like Box score stats etc. Always overshoot.

</rules>

5-Metric Suite (5MS) - column mappings: (
PSP - PSP
"THREE_PE" - "THREE_PE"
FGS: FGS
ATR: ATR
DSI: DSI)
Don't forget there is no position column, use the criterion defined above in the prompt.

Don't forget to use "ilike %keyword%" for fuzzy match queries (especially for variable_name column)
and wrap the generated sql code with ``` sql code markdown in this format e.g:
```sql
(select 1) union (select 2)
```
DO NOT FORGET: if the column starts with a number, surround it with quotes when querying.

MVQ Prompting:
If asked about the "top" or "total" number of stats over a singular event, you should run an aggregation 
of all of the specific stats for each player for ALL games in the event. 

For example, if the user asks something like "Who are the top [#] Players in [STATISTIC S] for [EVENT E]?” 
Like Who are the top 10 players in 3 pointers made in 2022 Nike EYBL.
You should, for each game in that event, sum up all the 3 pointers for each specific player.

You should be returning a query similar to:
    ```sql
    SELECT PLAYER, SUM(THREE_POINTS_MADE) AS TOTAL_THREE_POINTS_MADE, [OTHER BOX SCORE STATS]
    FROM [relevant table]
    GROUP BY PLAYER;
    LIMIT [#]
    ```

DON'T FORGET: Make sure the SELECT in your sql query includes box score stats unless it's not necessary.

For each question from the user, include only the query with format described above within your response. No other text, description, or nonsense please.
"""

CHOOSE_TABLE_PROMPT = """
Given the following user query about basketball statistics, decide which tables from the database should be used to answer the query. The possible tables are:
1. Youth Event Stats: NIKE_TEST.SCHEMA_NIKE_TEST.PLAYER_STATS_WITH_YEAR
2. NBA Box Score Stats: NBA.PUBLIC.REGULAR_SZN

Please return the names of the relevant tables in a list based on the content of the query.
Do not include any additional words or characters besides the brackets, quotes, and the name of the table.

User Query: "{query}"

Example:
If the query is about an NBA player, you should return: ["NBA.PUBLIC.REGULAR_SZN"]
If the query is about a youth event like peach jam: ["NIKE_TEST.SCHEMA_NIKE_TEST.PLAYER_STATS_WITH_YEAR"]
"""


@st.cache_data(show_spinner=False)
def get_table_context(table_name: str, table_description: str, metadata_query: str = None):
    table = table_name.split(".")
    conn = st.experimental_connection("snowpark")
    columns = conn.query(f"""
        SELECT COLUMN_NAME, DATA_TYPE FROM {table[0].upper()}.INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = '{table[1].upper()}' AND TABLE_NAME = '{table[2].upper()}'
        """,
    )
    columns = "\n".join(
        [
            f"- **{columns['COLUMN_NAME'][i]}**: {columns['DATA_TYPE'][i]}"
            for i in range(len(columns["COLUMN_NAME"]))
        ]
    )
    context = f"""
        Here is the table name <tableName> {'.'.join(table)} </tableName>

        <tableDescription>{table_description}</tableDescription>

        Here are the columns of the {'.'.join(table)}

        <columns>\n\n{columns}\n\n</columns>
    """
    if metadata_query:
        metadata = conn.query(metadata_query)
        metadata = "\n".join(
            [
                f"- **{metadata['VARIABLE_NAME'][i]}**: {metadata['DEFINITION'][i]}"
                for i in range(len(metadata["VARIABLE_NAME"]))
            ]
        )
        context = context + f"\n\nAvailable variables by VARIABLE_NAME:\n\n{metadata}"

    return context

def get_system_prompt(user_query):

    # for debugging - save API calls
    # get_table_response = openai.Completion.create(
    #         model="gpt-3.5-turbo-instruct",
    #         prompt=CHOOSE_TABLE_PROMPT.format(query=user_query),
    #         max_tokens=150
    # )

    # get_table_response_text = get_table_response['choices'][0]['text']
    get_table_response_text = '["NIKE_TEST.SCHEMA_NIKE_TEST.PLAYER_STATS_MAY_21"]'
    
    table_names = json.loads(get_table_response_text)
    
    table_context = []
    for table_name in table_names:
        table_context.append(
            get_table_context(
                table_name=table_name,
                table_description=TABLE_DESCRIPTION,
                metadata_query=METADATA_QUERY
            )
        )

    
    FINAL_SQL_PROMPT = GENERATE_SQL_PROMPT.format(context=table_context)

    return FINAL_SQL_PROMPT

# do `streamlit run prompting/sql_prompts.py` to view the initial system prompt in a Streamlit app
if __name__ == "__main__":
    st.header("System prompt for Frosty")
    st.markdown(get_system_prompt("Show Me System Prompt\n"))
