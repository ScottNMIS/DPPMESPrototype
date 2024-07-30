import streamlit as st
import pandas as pd
from datetime import datetime

def show_additional_page():
    st.title("Process Input Form")

    with st.form(key='additional_form'):
        st.subheader("Process Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            part_id = st.selectbox('Part ID', options=['Part 1', 'Part 2', 'Part 3'])
            process_name = st.selectbox('Process Name', options=['Process A', 'Process B', 'Process C'])
            operator = st.text_input('Operator')
        
        with col2:
            process_start_time = st.date_input('Process Start Date', value=datetime.today())
            process_start_time_hour = st.time_input('Process Start Time')
            process_end_time = st.date_input('Process End Date', value=datetime.today())
            process_end_time_hour = st.time_input('Process End Time')

        attachments = st.file_uploader('Attachments', accept_multiple_files=True)

        submit_button = st.form_submit_button(label='Submit')
        if submit_button:
            st.success(f"Form submitted successfully!\n"
                       f"Part ID: {part_id}\n"
                       f"Process Name: {process_name}\n"
                       f"Operator: {operator}\n"
                       f"Process Start: {process_start_time} {process_start_time_hour}\n"
                       f"Process End: {process_end_time} {process_end_time_hour}\n"
                       f"Attachments: {attachments}")

    st.write("Please note that attachments will not be saved until the full form is submitted using the button below.")

    if st.button('Back to Home Screen'):
        st.experimental_set_query_params(page="home")

# Function call for testing in standalone mode
if __name__ == "__main__":
    show_additional_page()
