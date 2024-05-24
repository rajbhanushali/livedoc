from chatbot.utils.assistants import create_thread

def initialize_login_session(session_state):
    # Initialize session state for login
    if "login" not in session_state:
        session_state.login = ""
    if "submitted" not in session_state:
        session_state.submitted = False
    if "loading" not in session_state:
        session_state.loading = False
    if "thread_cost" not in session_state:
        session_state.thread_cost = 0
    
    return session_state


def initialize_thread_session(session_state):
    if "sql_thread_id" not in session_state:
        session_state.sql_thread_id = create_thread()
    if "dataviz_thread_id" not in session_state:
        session_state.dataviz_thread_id = create_thread()
    if "thread_tokens" not in session_state:
        session_state.thread_tokens = 0
    
    return session_state