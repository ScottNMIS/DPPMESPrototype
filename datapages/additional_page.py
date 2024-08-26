import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def auto_populate_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def set_start_time():
    st.session_state.start_time = auto_populate_time()

def set_end_time():
    st.session_state.end_time = auto_populate_time()

def set_machine_number():
    st.session_state.machine_number = "M001"

def calculate_operation_time():
    if st.session_state.start_time and st.session_state.end_time:
        start = datetime.strptime(st.session_state.start_time, "%Y-%m-%d %H:%M:%S")
        end = datetime.strptime(st.session_state.end_time, "%Y-%m-%d %H:%M:%S")
        st.session_state.operation_time = str(end - start)

def show_data_input():
    st.title("Digital Product Passport Data Input")

    # Initialize session state variables if not present
    if 'part_number' not in st.session_state:
        st.session_state.part_number = ""
    if 'mass' not in st.session_state:
        st.session_state.mass = ""
    if 'hardness' not in st.session_state:
        st.session_state.hardness = ""
    if 'start_time' not in st.session_state:
        st.session_state.start_time = ""
    if 'end_time' not in st.session_state:
        st.session_state.end_time = ""
    if 'part_description' not in st.session_state:
        st.session_state.part_description = ""
    if 'material' not in st.session_state:
        st.session_state.material = ""
    if 'mes_part_number' not in st.session_state:
        st.session_state.mes_part_number = ""
    if 'machine_number' not in st.session_state:
        st.session_state.machine_number = ""
    if 'operation_time' not in st.session_state:
        st.session_state.operation_time = ""

    # Create tabs for different sections
    tabs = st.tabs(["Basic Info", "Files", "Manufacturing", "Repair", "Quality"])

    # Basic Info Tab
    with tabs[0]:
        st.header("Basic Information")
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.part_number = st.text_input("Part Number", st.session_state.part_number)
            st.session_state.mass = st.text_input("Mass", st.session_state.mass)
            st.session_state.hardness = st.text_input("Hardness", st.session_state.hardness)
            st.text_input("Start Time", st.session_state.start_time)
            st.button("Set Current Time as Start", on_click=set_start_time)
        with col2:
            st.session_state.part_description = st.text_area("Part Description", st.session_state.part_description)
            st.session_state.material = st.text_input("Material", st.session_state.material)
            st.text_input("End Time", st.session_state.end_time)
            st.button("Set Current Time as End", on_click=set_end_time)

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
            st.session_state.mes_part_number = st.text_input("MES Part Number", st.session_state.mes_part_number)
            st.session_state.machine_number = st.text_input("Machine Number", st.session_state.machine_number)
            st.button("Set Machine Number to M001", on_click=set_machine_number)
        with col2:
            st.session_state.operation_time = st.text_input("Operation Time", st.session_state.operation_time)
            excel_report = st.file_uploader("Excel Report", type=["xlsx", "xls"])
            st.button("Calculate Operation Time", on_click=calculate_operation_time)

    with tabs[3]:
        st.header("Repair Information")
        repair_guideline = st.file_uploader("Repair Guideline", type=["pdf", "docx"])
        repair_images = st.file_uploader("Repair Images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)


    with tabs[4]:
        st.header("Quality Information")
        qif_results_file = st.file_uploader("QIF Results File", type=["qif"])
        audit_report = st.file_uploader("Audit Report", type=["pdf", "docx"])


    if st.button("Submit Data"):
        st.success("Data submitted successfully!")


    st.header("Download Existing Data")
    if st.button("Download Data"):
        st.info("Data download functionality will be implemented in the future.")

def show_data_input_page():
    show_data_input()

if __name__ == "__main__":
    show_data_input_page()
