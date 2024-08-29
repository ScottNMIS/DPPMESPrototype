import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from datapages.api_calls import get_machine_data, get_dpp_data

def auto_populate_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def set_start_time():
    st.session_state.start_time = auto_populate_time()

def set_end_time():
    st.session_state.end_time = auto_populate_time()

def calculate_operation_time():
    if st.session_state.start_time and st.session_state.end_time:
        start = datetime.strptime(st.session_state.start_time, "%Y-%m-%d %H:%M:%S")
        end = datetime.strptime(st.session_state.end_time, "%Y-%m-%d %H:%M:%S")
        st.session_state.operation_time = str(end - start)

def initialize_session_state():
    if 'initialized' not in st.session_state:
        mock_data = get_dpp_data()
        for key, value in mock_data.items():
            if key not in st.session_state:
                st.session_state[key] = value
        st.session_state.initialized = True

def show_data_input():
    initialize_session_state()

    st.markdown("""
    <style>
    .big-font {
        font-size:30px !important;
        font-weight: bold;
    }
    .stButton>button {
        width: 100%;
        background-color: #3498db;
        color: white;
        height: 3em;
    }
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        height: 3em;
    }
    .stDownloadButton>button {
        width: 100%;
        background-color: #2ecc71;
        color: white;
    }
    .styled-table {
        width: 100%;
        border-collapse: collapse;
        margin: 25px 0;
        font-size: 0.9em;
        font-family: sans-serif;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
    }
    .styled-table thead tr {
        background-color: #3498db;
        color: #ffffff;
        text-align: left;
    }
    .styled-table th,
    .styled-table td {
        padding: 12px 15px;
    }
    .styled-table tbody tr {
        border-bottom: 1px solid #dddddd;
    }
    .styled-table tbody tr:nth-of-type(even) {
        background-color: #f3f3f3;
    }
    .styled-table tbody tr:last-of-type {
        border-bottom: 2px solid #3498db;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<p class="big-font">Digital Product Passport Data</p>', unsafe_allow_html=True)

    # Create tabs for different sections
    tabs = st.tabs(["Basic Info", "Files", "Manufacturing", "Repair", "Quality"])

    # Basic Info Tab
    with tabs[0]:
        st.header("Basic Information")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.session_state.part_number = st.text_input("Part Number", value=st.session_state.part_number)
            st.session_state.mass = st.number_input("Mass (kg)", value=float(st.session_state.mass))
            st.session_state.hardness = st.number_input("Hardness", value=int(st.session_state.hardness))
        with col2:
            st.session_state.part_description = st.text_area("Part Description", value=st.session_state.part_description, height=150)
            st.session_state.material = st.text_input("Material", value=st.session_state.material)
        with col3:
            st.session_state.start_time = st.text_input("Start Time", value=st.session_state.start_time)
            st.button("Set Current Time as Start", on_click=set_start_time)
            st.session_state.end_time = st.text_input("End Time", value=st.session_state.end_time)
            st.button("Set Current Time as End", on_click=set_end_time)

    # Files Tab
    with tabs[1]:
        st.header("File Management")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Original Files")
            st.session_state.cad_file = st.file_uploader("CAD File", type=["stp", "step", "iges"])
            if st.session_state.cad_file is not None:
                st.download_button("Download CAD File", data=st.session_state.cad_file, file_name="cad_file.stp", mime="application/octet-stream")
            
            st.session_state.mbd_qif_file = st.file_uploader("MBD QIF File", type=["qif"])
            if st.session_state.mbd_qif_file is not None:
                st.download_button("Download MBD QIF File", data=st.session_state.mbd_qif_file, file_name="mbd_qif_file.qif", mime="application/octet-stream")
            
            st.session_state.pdf_3d = st.file_uploader("3D PDF", type=["pdf"])
            if st.session_state.pdf_3d is not None:
                st.download_button("Download 3D PDF", data=st.session_state.pdf_3d, file_name="3d_model.pdf", mime="application/pdf")
        
        with col2:
            st.subheader("Remake Files")
            st.session_state.cad_file_remake = st.file_uploader("CAD File (Remake)", type=["stp", "step", "iges"])
            if st.session_state.cad_file_remake is not None:
                st.download_button("Download CAD File (Remake)", data=st.session_state.cad_file_remake, file_name="cad_file_remake.stp", mime="application/octet-stream")
            
            st.session_state.mbd_qif_file_remake = st.file_uploader("MBD QIF File (Remake)", type=["qif"])
            if st.session_state.mbd_qif_file_remake is not None:
                st.download_button("Download MBD QIF File (Remake)", data=st.session_state.mbd_qif_file_remake, file_name="mbd_qif_file_remake.qif", mime="application/octet-stream")
            
            st.session_state.pdf_3d_remake = st.file_uploader("3D PDF (Remake)", type=["pdf"])
            if st.session_state.pdf_3d_remake is not None:
                st.download_button("Download 3D PDF (Remake)", data=st.session_state.pdf_3d_remake, file_name="3d_model_remake.pdf", mime="application/pdf")


    # Manufacturing Tab
    with tabs[2]:
        st.header("Manufacturing Information")
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.mes_part_number = st.text_input("MES Part Number", value=st.session_state.mes_part_number)
            st.session_state.operation_name = st.text_input("Operation Name", value=st.session_state.operation_name)
            
            # Get machine data from API
            machine_data = get_machine_data()
            st.session_state.machines_used = st.multiselect("Select Machines Used", 
                                               options=machine_data.keys(), 
                                               default=st.session_state.get('machines_used', []))
            
            if st.session_state.machines_used:
                st.markdown("<h4>Selected Machine Data:</h4>", unsafe_allow_html=True)
                machine_table_data = []
                for machine in st.session_state.machines_used:
                    machine_info = machine_data[machine]
                    machine_table_data.append([
                        machine_info['name'],
                        machine_info['status'],
                        machine_info['last_maintenance']
                    ])
                
                machine_table_html = "<table class='styled-table'>"
                machine_table_html += "<thead><tr><th>Machine Name</th><th>Status</th><th>Last Maintenance</th></tr></thead>"
                machine_table_html += "<tbody>"
                for row in machine_table_data:
                    machine_table_html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td></tr>"
                machine_table_html += "</tbody></table>"
                
                st.markdown(machine_table_html, unsafe_allow_html=True)
        
        with col2:
            st.session_state.operation_time = st.text_input("Operation Time", value=st.session_state.operation_time)
            st.button("Calculate Operation Time", on_click=calculate_operation_time)
            st.session_state.excel_report = st.file_uploader("Excel Report", type=["xlsx", "xls"])
            if st.session_state.get('excel_report'):
                st.download_button("Download Excel Report", data=st.session_state.excel_report, file_name="manufacturing_report.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    # Repair Tab
    with tabs[3]:
        st.header("Repair Information")
        st.session_state.repair_guideline = st.file_uploader("Repair Guideline", type=["pdf", "docx"])
        if st.session_state.repair_guideline is not None:
            st.download_button("Download Repair Guideline", data=st.session_state.repair_guideline, file_name="repair_guideline.pdf", mime="application/pdf")
        
        st.session_state.repair_images = st.file_uploader("Repair Images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
        if st.session_state.repair_images:
            for i, image in enumerate(st.session_state.repair_images):
                st.download_button(f"Download Repair Image {i+1}", data=image, file_name=f"repair_image_{i+1}.jpg", mime="image/jpeg")

    # Quality Tab
    with tabs[4]:
        st.header("Quality Information")
        st.session_state.qif_results_file = st.file_uploader("QIF Results File", type=["qif"])
        if st.session_state.qif_results_file is not None:
            st.download_button("Download QIF Results", data=st.session_state.qif_results_file, file_name="qif_results.qif", mime="application/octet-stream")
        
        st.session_state.audit_report = st.file_uploader("Audit Report", type=["pdf", "docx"])
        if st.session_state.audit_report is not None:
            st.download_button("Download Audit Report", data=st.session_state.audit_report, file_name="audit_report.pdf", mime="application/pdf")


    # Submit button
    if st.button("Submit Data"):
        st.success("Data submitted successfully!")

def show_data_input_page():
    show_data_input()

if __name__ == "__main__":
    show_data_input_page()