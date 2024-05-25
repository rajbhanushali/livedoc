import json
from chatbot.data_visuals import plot_dataviz
import streamlit as st
import pandas as pd
import re

from openai import OpenAI
from chatbot.utils.helper import update_session_state_cost

client = OpenAI(api_key=st.secrets.CHATBOT_KEY)

def create_thread():  
    thread = client.beta.threads.create()
    return thread.id

def create_message_in_thread(thread_id, user_query):
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_query
    )
    return message.id

def retrieve_all_message_in_thread(thread_id):
    thread_messages = client.beta.threads.messages.list(thread_id)
    list_messages = thread_messages.data
    thread_messages = []
    for message in list_messages:
        obj = {}
        obj['content'] = message.content[0].text.value
        obj['role'] = message.role
        thread_messages.append(obj)
    return thread_messages[::-1]

def create_run(thread_id, assistant_id):
    run_obj = client.beta.threads.runs.create_and_poll(
        thread_id=thread_id,
        assistant_id=assistant_id
    )

    if run_obj.status == "completed":
        update_session_state_cost(run_obj.usage.total_tokens)

    return run_obj

def generate_table_response_from_run(conn, thread_id):

    all_messages = retrieve_all_message_in_thread(thread_id)
    assistant_sql_response = all_messages[-1]["content"]

    return run_conn_query_sql(conn, assistant_sql_response)


def run_conn_query_sql(conn, sql_query):
    sql_match = re.search(r"```sql\n(.*)\n```", sql_query, re.DOTALL)
    table_response = pd.DataFrame()

    if sql_match:
        sql = sql_match.group(1)
        try:
            st.markdown(f"```sql\n{sql}\n```")
            table_response = conn.query(sql)
        except Exception as e:
            st.error(f'Could not reach snowflake database due to error: {e}')
            table_response = pd.DataFrame()

    else:
        try:
            st.markdown(sql_query)
            table_response = conn.query(sql_query)
        except Exception as e:
            st.error(f'Could not reach snowflake database due to error: {e}')
            table_response = pd.DataFrame()

    if 'YEAR' in table_response.columns:
        table_response['YEAR'] = table_response['YEAR'].astype(str)

    return table_response

def data_viz_assistant_response(user_query, table_response, thread_id, assistant_id):

    table_columns = table_response.columns.tolist()

    input_text = f"User Query: {user_query}. \n Table Data: \n{table_response.to_json(orient='records', lines=True)} \n Columns: {table_columns}"
    
    message_id = create_message_in_thread(thread_id, input_text)

    dataviz_run_obj = create_run(thread_id, assistant_id)
    
    all_messages = retrieve_all_message_in_thread(thread_id)

    most_recent_message = all_messages[-1]["content"]
    data_viz_response = json.loads(most_recent_message)

    if data_viz_response:
        return plot_dataviz(data_viz_response, table_response)
    else:
        print("No JSON found in response.")
        return {"requires_visual" : False}
    
# How to use custom functions
# run_obj = client.beta.threads.runs.retrieve(
#     thread_id=thread_id,
#     run_id=run_id
# )

# output_table = pd.DataFrame()
# tool_outputs = []

# if run_obj.status == "requires_action":
#     required_actions = run_obj.required_action.submit_tool_outputs.tool_calls

#     for action in required_actions:
#         function_name = action.function.name
#         function_args = json.loads(action.function.arguments)
        
#         if "run_conn_query_sql" in function_name:
#             sql_query_parameter = function_args["query"]
#             output_table = run_conn_query_sql(conn, sql_query_parameter)

#             tool_outputs.append({
#                 "tool_call_id": action.id,
#                 "output": output_table.to_json()
#             })

#     client.beta.threads.runs.submit_tool_outputs_and_poll(
#         thread_id=thread_id,
#         run_id=run_obj.id,
#         tool_outputs=tool_outputs
#     )

#return output_table
