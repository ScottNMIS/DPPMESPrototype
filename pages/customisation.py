import streamlit as st
from openai_api import get_openai_response
from sample_data import get_large_sample_data
import json

def show_customisation():
    st.title("Customisation with AI")

    st.write("Ask a question about the data, and AI will generate the required components.")
    
    api_key = st.text_input("Enter your OpenAI API key", type="password")
    question = st.text_area("Ask a question about the data:")
    
    if st.button("Generate Components"):
        if api_key and question:
            with st.spinner("Generating components..."):
                try:
                    # Get response from OpenAI
                    response = get_openai_response(question, api_key)
                    st.write("AI Response:", response)
                    
                    # Execute the generated code
                    exec(response)
                except Exception as e:
                    st.error(f"Error generating components: {e}")
        else:
            st.error("Please provide both the API key and a question.")

# Generate the data once
data = get_large_sample_data()

def plot_bar_chart():
    st.bar_chart(data[['Company', 'Value X']].set_index('Company'))

def plot_timeline():
    st.line_chart(data[['Date', 'Value Y']].set_index('Date'))

def show_values():
    st.write(data[['Value X', 'Value Y']])

def show_map():
    st.map(data[['Latitude', 'Longitude']])

# Example usage of the functions
if __name__ == "__main__":
    show_customisation()
