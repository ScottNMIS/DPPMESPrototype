import streamlit as st
import uuid
from datapages.api_calls import create_dpp_api
from datetime import datetime

def generate_unique_code():
    return str(uuid.uuid4())

def show_create_dpp_page():
    st.title("Create Digital Product Passport")

    # Initialize session state variables if not present
    if 'dpp_data' not in st.session_state or not isinstance(st.session_state.dpp_data, dict):
        st.session_state.dpp_data = {}

    # Create tabs for different sections
    tabs = st.tabs(["Basic Info", "Manufacturing", "Quality", "Files"])

    # Basic Info Tab
    with tabs[0]:
        st.header("Basic Information")
        col1, col2 = st.columns(2)
        with col1:
            product_name = st.text_input("Product Name", st.session_state.dpp_data.get('title', ''))
            manufacturer = st.text_input("Manufacturer", st.session_state.dpp_data.get('manufacturer', ''))
        with col2:
            production_date = st.date_input("Production Date", value=datetime.now())
            description = st.text_area("Product Description", st.session_state.dpp_data.get('description', ''))

    # Manufacturing Tab
    with tabs[1]:
        st.header("Manufacturing Information")
        col1, col2 = st.columns(2)
        with col1:
            material = st.text_input("Material", st.session_state.dpp_data.get('material', ''))
            machine_number = st.text_input("Machine Number", st.session_state.dpp_data.get('machine_number', ''))
        with col2:
            mass = st.number_input("Mass (kg)", min_value=0.0, format="%.2f", value=float(st.session_state.dpp_data.get('mass', 0)))
            operation_time = st.time_input("Operation Time")

    # Quality Tab
    with tabs[2]:
        st.header("Quality Information")
        col1, col2 = st.columns(2)
        with col1:
            hardness = st.number_input("Hardness", min_value=0, value=int(st.session_state.dpp_data.get('hardness', 0)))
            quality_check = st.selectbox("Quality Check", ["Passed", "Failed", "Pending"], index=["Passed", "Failed", "Pending"].index(st.session_state.dpp_data.get('quality_check', 'Pending')))
        with col2:
            inspector = st.text_input("Inspector Name", st.session_state.dpp_data.get('inspector', ''))
            inspection_date = st.date_input("Inspection Date")

    # Files Tab
    with tabs[3]:
        st.header("File Uploads")
        col1, col2 = st.columns(2)
        with col1:
            cad_file = st.file_uploader("CAD File", type=["stp", "step", "iges"])
            qif_file = st.file_uploader("QIF File", type=["qif"])
        with col2:
            pdf_3d = st.file_uploader("3D PDF", type=["pdf"])
            other_files = st.file_uploader("Other Files", type=["pdf", "docx", "xlsx"], accept_multiple_files=True)

    # Create DPP Button
    if st.button("Create DPP"):
        if product_name and manufacturer:
            unique_code = generate_unique_code()
            dpp_data = {
                "title": product_name,
                "qrcode": unique_code,
                "manufacturer": manufacturer,
                "production_date": str(production_date),
                "description": description,
                "material": material,
                "machine_number": machine_number,
                "mass": mass,
                "operation_time": str(operation_time),
                "hardness": hardness,
                "quality_check": quality_check,
                "inspector": inspector,
                "inspection_date": str(inspection_date)
            }
            
            # Call the API to create the DPP
            response = create_dpp_api(dpp_data)
            
            if response.status_code == 201:
                st.session_state.dpp_data = dpp_data
                st.success(f"DPP created successfully! Unique Code: {unique_code}")
                st.info("You can now use this code to access the DPP via the 'Scan QR Code' page.")
            else:
                st.error(f"Failed to create DPP. Error: {response.text}")
        else:
            st.error("Please fill in at least the Product Name and Manufacturer fields.")

    # Display current DPP data if available
    if st.session_state.dpp_data:
        st.header("Current DPP Data")
        st.json(st.session_state.dpp_data)

if __name__ == "__main__":
    show_create_dpp_page()