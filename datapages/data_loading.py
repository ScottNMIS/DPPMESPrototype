import streamlit as st
import json
import base64
import time
import pandas as pd

# Function to convert session state to a JSON-serializable dictionary
def serialize_session_state():
    session_data = {}
    for key, value in st.session_state.items():
        # Check if the value is a DataFrame, if so, convert it to a dictionary
        if isinstance(value, pd.DataFrame):
            session_data[key] = value.to_dict()  # Convert DataFrame to a dictionary
        else:
            session_data[key] = value
    return session_data

# Function to create a downloadable link for the session state JSON file
def download_session_state():
    session_data = serialize_session_state()
    session_json = json.dumps(session_data)
    b64 = base64.b64encode(session_json.encode()).decode()  # Encode to base64 for download
    href = f'<a href="data:file/json;base64,{b64}" download="session_state.json">Download Session State</a>'
    st.markdown(href, unsafe_allow_html=True)

# Auto-save and download mechanism
def auto_download_session_state(interval=30):
    if "last_saved" not in st.session_state:
        st.session_state.last_saved = time.time()

    current_time = time.time()
    if current_time - st.session_state.last_saved >= interval:
        download_session_state()  # Trigger the download
        st.session_state.last_saved = current_time
        st.rerun()  # Refresh the page to keep auto-saving every interval