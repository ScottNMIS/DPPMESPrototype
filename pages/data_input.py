import streamlit as st
import pandas as pd
from data_manager import create_dummy_data, add_new_entry

def show_data_input():
    st.title("Data Input Form")

    if 'df' not in st.session_state:
        st.session_state.df = create_dummy_data()

    with st.form(key='input_form'):
        machine = st.selectbox('Select Machine', options=st.session_state.df['Machine'].unique())
        start_time = st.text_input('Start Time', value='2024-07-23 11:00')
        stop_time = st.text_input('Stop Time', value='2024-07-23 11:30')
        status = st.selectbox('Select Status', options=['Scheduled', 'In progress', 'Completed'])
        output = st.number_input('Output Quantity', min_value=0)
        energy = st.number_input('Energy Consumption (kWh)', min_value=0.0, format="%.2f")
        carbon = st.number_input('Carbon Footprint (kg CO2)', min_value=0.0, format="%.2f")
        submit_button = st.form_submit_button(label='Submit')

        if submit_button:
            st.session_state.df = add_new_entry(st.session_state.df, machine, start_time, stop_time, status, output, energy, carbon)
            st.success("Data Submitted Successfully!")
            st.write(st.session_state.df)

    st.subheader("Existing Entries")
    st.table(st.session_state.df)
