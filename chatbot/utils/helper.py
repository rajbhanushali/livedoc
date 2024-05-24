import streamlit as st
from chatbot.data_visuals import create_and_display_chart
from chatbot.assets.floating_box import get_thread_cost_string

def show_existing_chat_messages(messages):
    # rerender the new old messages when user submits a query
    for message in messages:
        if message["role"] == "system":
            continue

        if message["role"] == "assistant" and "key" in message:
            
            if "results" in message:
                with st.chat_message(message["role"]):    
                    st.dataframe(message["results"])
                    if message["key"] == "sql_response":
                        create_and_display_chart(message)
            
            if message["key"] == 'welcome_message':
                with st.chat_message(message["role"]):
                    st.write(message["content"])

        if message["role"] == "user":
            with st.chat_message(message["role"]):    
                st.write(message["content"])
    
    #Show total cost so far
    total_cost = f'${st.session_state.thread_cost:.4f}'

    st.markdown(get_thread_cost_string(total_cost), unsafe_allow_html=True)



def update_session_state_cost(token_usage):
    st.session_state.thread_tokens = st.session_state.thread_tokens + token_usage
    
    current_cost = st.session_state.thread_cost

    # using .7 cents per 1k tokens. Actual cost is actually little bit less right now with gpt 4o
    cost_per_1k_tokens = .007
    cost_of_run = (token_usage / 1000) * cost_per_1k_tokens

    st.session_state.thread_cost = current_cost + cost_of_run