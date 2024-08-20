import streamlit as st
import pandas as pd

def show_data_visualisation():
    st.title("Data Visualisation")

    if 'df' not in st.session_state:
        st.session_state.df = pd.DataFrame()

    if st.session_state.df.empty:
        st.warning("No data available. Please add data through the Data Input page.")
    else:
        st.subheader('Machine Output Over Time')
        output_chart = st.session_state.df.pivot_table(index='Start Time', columns='Machine', values='Output')
        st.line_chart(output_chart)

        st.subheader('Energy Consumption by Machine')
        energy_chart = st.session_state.df.pivot_table(index='Machine', values='Energy Consumption', aggfunc='sum')
        st.bar_chart(energy_chart)

        st.subheader('Carbon Footprint by Machine')
        carbon_chart = st.session_state.df.pivot_table(index='Machine', values='Carbon Footprint', aggfunc='sum')
        st.bar_chart(carbon_chart)

        total_output = st.session_state.df['Output'].sum()
        total_energy = st.session_state.df['Energy Consumption'].sum()
        total_carbon = st.session_state.df['Carbon Footprint'].sum()
        avg_energy_per_output = total_energy / total_output if total_output else 0
        avg_carbon_per_output = total_carbon / total_output if total_output else 0

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Output", total_output)
        col2.metric("Total Energy Consumption (kWh)", total_energy)
        col3.metric("Total Carbon Footprint (kg CO2)", total_carbon)
        col4.metric("Average Energy per Output (kWh/unit)", f"{avg_energy_per_output:.2f}")
        col4.metric("Average Carbon per Output (kg CO2/unit)", f"{avg_carbon_per_output:.2f}")
