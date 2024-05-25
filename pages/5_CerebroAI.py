import streamlit as st
from chatbot.assets.loading_popup import loading_popup_str
from chatbot.prompting.sql_prompts import NO_RESPONSE_TEXT
from chatbot.prompting.welcome_message import WELCOME_MESSAGE_PROMPT
from chatbot.utils.helper import show_existing_chat_messages
from chatbot.utils.session_state import initialize_thread_session, initialize_login_session

from chatbot.utils.assistants import create_message_in_thread, create_run, generate_table_response_from_run, data_viz_assistant_response

st.set_page_config(
    page_title="CerebroAI",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

LOGIN_SECRET = st.secrets.LOGIN_PASSWORD
sql_assistant_id = st.secrets.ASSISTANT_ID
dataviz_assistant_id = st.secrets.DATAVIZ_ID

password_placeholder = "Please Enter The Password"

conn = st.experimental_connection("snowpark")

# Initialize session state for login
st.session_state = initialize_login_session(st.session_state)


st.title("🔍 CerebroAI")
st.caption("Sift our extensive database of basketball stats.")

# Commented out password field - Login is temporarily open

# login_attempt_input = st.text_input("Enter Password", type = 'password', placeholder=password_placeholder)
# if login_attempt_input and st.session_state.login != LOGIN_SECRET:
#     if login_attempt_input == LOGIN_SECRET:
#         st.session_state.login = login_attempt_input
#         st.experimental_rerun()
#     else:
#         st.error("Incorrect Password. Please Try Again")
#         st.caption("*Hint: You get no hints*")

if st.button('Get Started'):
    st.session_state.begin = True

if st.session_state.begin:
    # Initialize session state for OpenAI Assistants Thread(s)
    st.session_state = initialize_thread_session(st.session_state)

    # Refresh Button
    if st.button("Refresh"):
        conn.reset()
        st.session_state.messages.clear()
        st.session_state.clear()
        st.experimental_rerun()

    # Initialize the chat messages history
    conn.reset()
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": WELCOME_MESSAGE_PROMPT, "key": "welcome_message"}]

    # On USER SUBMIT QUERY:
    if user_query := st.chat_input():

        st.session_state.messages.append({"role": "user", "content": user_query})
        st.session_state.user_query = user_query

        message_id = create_message_in_thread(st.session_state.sql_thread_id, user_query)

        st.session_state.submitted = True
        st.session_state.loading = True
        st.experimental_rerun()

    loading_popup = st.empty()
    if st.session_state.loading:
        loading_popup = st.markdown(loading_popup_str, unsafe_allow_html=True)

    # rerender the new old messages when user submits a query, from helper file
    show_existing_chat_messages(st.session_state.messages)   

    if st.session_state.loading:
        st.session_state.loading = False
        loading_popup.empty()

    # If last message is from the user, we need to generate a new sql response
    user_submitted_query = st.session_state.submitted and st.session_state.messages[-1]["role"] == "user"
    if user_submitted_query:
        with st.chat_message("assistant"):
            
            # # Fun placeholders for sql loading ...
            text_placeholder = st.empty()
            text_placeholder.caption("I'm looking through our database now to find your answer...")
            gif_placeholder = st.empty()
            gif_placeholder.image("chatbot/assets/bot_loading.gif", width=250)

            # Run the thread to generate the table
            sql_run_id = create_run(st.session_state.sql_thread_id, sql_assistant_id).id
            table_response = generate_table_response_from_run(conn, st.session_state.sql_thread_id)

            # all_messages = retrieve_all_message_in_thread(st.session_state.sql_thread_id)

            # Clear sql loading placeholders
            text_placeholder.empty()  # Clears the text
            gif_placeholder.empty()  # Clears the GIF
            
            st.session_state.submitted = False
            
            message = {"role": "assistant", "content": table_response}
            message["results"] = table_response
            message["key"] = "sql_response"

            if not table_response.empty:
                st.caption("Here's whats I think you were looking for:")
                st.dataframe(table_response)

                message["chart_data"] = data_viz_assistant_response(st.session_state.user_query, table_response, st.session_state.dataviz_thread_id, dataviz_assistant_id)
                
                # if message["chart_data"] and "description" in message["chart_data"]:
                #     st.markdown(message["chart_data"]["description"])
                    
            else:
                st.markdown(NO_RESPONSE_TEXT)

            st.session_state.messages.append(message)
        
        conn.reset()
        session = st.experimental_connection("snowpark").session
