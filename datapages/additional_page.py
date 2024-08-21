import streamlit as st
import pandas as pd
from datetime import datetime

def show_data_input():
    st.title("Digital Product Passport Data Input")

    # Create tabs for different sections
    tabs = st.tabs(["Basic Info", "Files", "Manufacturing", "Repair", "Quality"])

    # Basic Info Tab
    with tabs[0]:
        st.header("Basic Information")
        col1, col2 = st.columns(2)
        with col1:
            part_number = st.text_input("Part Number")
            mass = st.text_input("Mass")
            hardness = st.text_input("Hardness")
        with col2:
            part_description = st.text_area("Part Description")
            material = st.text_input("Material")

    # Files Tab
    with tabs[1]:
        st.header("File Uploads")
        col1, col2 = st.columns(2)
        with col1:
            cad_file = st.file_uploader("CAD File", type=["stp", "step", "iges"])
            mbd_qif_file = st.file_uploader("MBD QIF File", type=["qif"])
            pdf_3d = st.file_uploader("3D PDF", type=["pdf"])
        with col2:
            cad_file_remake = st.file_uploader("CAD File (Remake)", type=["stp", "step", "iges"])
            mbd_qif_file_remake = st.file_uploader("MBD QIF File (Remake)", type=["qif"])
            pdf_3d_remake = st.file_uploader("3D PDF (Remake)", type=["pdf"])

    # Manufacturing Tab
    with tabs[2]:
        st.header("Manufacturing Information")
        col1, col2 = st.columns(2)
        with col1:
            mes_part_number = st.text_input("MES Part Number")
            machine_number = st.text_input("Machine Number")
        with col2:
            operation_time = st.text_input("Operation Time")
            excel_report = st.file_uploader("Excel Report", type=["xlsx", "xls"])

    # Repair Tab
    with tabs[3]:
        st.header("Repair Information")
        repair_guideline = st.file_uploader("Repair Guideline", type=["pdf", "docx"])
        repair_images = st.file_uploader("Repair Images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    # Quality Tab
    with tabs[4]:
        st.header("Quality Information")
        qif_results_file = st.file_uploader("QIF Results File", type=["qif"])
        audit_report = st.file_uploader("Audit Report", type=["pdf", "docx"])

    # Submit Button
    if st.button("Submit Data"):
        # Here you would typically process and save the data
        # For now, we'll just show a success message
        st.success("Data submitted successfully!")

    # Download existing data (placeholder for future functionality)
    st.header("Download Existing Data")
    if st.button("Download Data"):
        # Here you would typically retrieve and provide the data for download
        # For now, we'll just show an info message
        st.info("Data download functionality will be implemented in the future.")

def show_data_input_page():
    show_data_input()

if __name__ == "__main__":
    show_data_input_page()