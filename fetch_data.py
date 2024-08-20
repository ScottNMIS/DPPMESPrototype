import requests
import streamlit as st

def fetch_data_from_basyx(endpoint):
    try:
        st.write(f"Fetching data from: {endpoint}")
        response = requests.get(endpoint, timeout=10)  # Added timeout
        response.raise_for_status()  # Check if the request was successful
        st.write(f"Response status code: {response.status_code}")
        
        # Log the headers and content for debugging
        st.write(f"Response headers: {response.headers}")
        st.write(f"Response content: {response.content}")
        
        return response.json()
    except requests.Timeout:
        st.error("Request timed out. The server may be unreachable or the request took too long to complete.")
        return None
    except requests.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return None
    except ValueError as e:
        st.error(f"Error decoding JSON: {e}")
        return None