import streamlit as st
import cv2
from pyzbar.pyzbar import decode
import numpy as np
import time
import pandas as pd  # Import pandas
from st_aggrid import AgGrid, GridOptionsBuilder

def show_howden_remake():
    session_vars = [
        'howden_remake_screen', 'qr_code', 'part_number', 'part_description', 'approval_status', 
        'logged_file', 'supplier_input', 'cad_files', 'operation_routing', 'materials_alloy',
        'repair_images', 'authorised_file', 'mes_part_number', 'machine_number', 'operation_time',
        'excel_report', 'qif_results_file', 'submitted', 'audit_report', 'automatic_check'
    ]
    for var in session_vars:
        if var not in st.session_state:
            st.session_state[var] = ""

    if 'howden_remake_screen' not in st.session_state or st.session_state.howden_remake_screen == "":
        st.session_state.howden_remake_screen = 0

    if 'submitted' not in st.session_state:
        st.session_state.submitted = False

    try:
        st.session_state.howden_remake_screen = int(st.session_state.howden_remake_screen)
    except ValueError:
        st.session_state.howden_remake_screen = 0

    def next_screen():
        if st.session_state.howden_remake_screen < 10:
            st.session_state.howden_remake_screen += 1

    def prev_screen():
        if st.session_state.howden_remake_screen > 0:
            st.session_state.howden_remake_screen -= 1

    if st.session_state.howden_remake_screen == 0:
        st.title("Login")
        st.markdown("### Please sign in to access the dataset")
        with st.form(key='login_form'):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            login_submitted = st.form_submit_button("Sign In")

        if login_submitted:
            st.success("Sign in successful")
            st.markdown("You are authorised to access this dataset.")
            st.button("Continue", on_click=next_screen, key="continue_0")

    elif st.session_state.howden_remake_screen == 1:
        st.title("QR Code Scanning")
        st.text("QR code scanner placeholder.")
        st.button("Continue", on_click=next_screen, key="continue_1")
        
        if st.session_state.qr_code:
            st.write(f"Scanned URL: {st.session_state.qr_code}")
            st.button("Continue", on_click=next_screen, key="continue_2")

    elif st.session_state.howden_remake_screen == 2:
        st.title("Confirm Remake Suitability")
        st.markdown("### Determine if the part is suitable for remanufacturing or recycling")
        images = ["images/part1.png", "images/part2.png", "images/part3.png", "images/part4.png"]
        for img in images:
            st.image(img, caption="Part Image", use_column_width=True)
        
        if st.button("Allow Remanufacture"):
            st.session_state.approval_status = "Remanufacture Allowed"
            next_screen()
        
        if st.button("Confirm Recycling"):
            st.session_state.approval_status = "Recycling Confirmed"
            next_screen()

    elif st.session_state.howden_remake_screen == 3:
        st.title("Upload Verification Images")
        st.markdown("### Upload images for verification of the part's suitability")
        uploaded_files = st.file_uploader("Upload images", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

        if st.button("Submit for Manual Verification"):
            st.write("Sending images to Howden for manual verification...")
            time.sleep(2)
            st.success("Images sent for manual verification. Please wait for confirmation.")
            next_screen()

        if st.button("Automatic Verification"):
            with st.spinner("Processing images with computer vision..."):
                time.sleep(5)
                st.success("Images verified automatically. Part is suitable for remanufacture.")
                next_screen()

    elif st.session_state.howden_remake_screen == 4:
        st.title("ReMake - Logged File")
        st.markdown("### Displaying data or providing download links")
        st.write(f"**Part Number:** {st.session_state.part_number}")
        st.write(f"**Part Description:** {st.session_state.part_description}")

        st.write("#### CAD files")
        st.download_button(label="Download CAD File", data="CAD file content here", file_name="cad_file.step")
        st.write("#### Operation Routing")
        st.download_button(label="Download Operation Routing", data="Operation routing content here", file_name="operation_routing.txt")
        st.write("#### Materials and Alloy Information")
        st.download_button(label="Download Materials and Alloy Info", data="Materials and Alloy content here", file_name="materials_alloy.txt")
        st.write("#### Repair Guidelines")
        st.download_button(label="Download Repair Images", data="Repair images content here", file_name="repair_images.zip")
        st.write("#### Authorised 3D File")
        st.download_button(label="Download 3D Authorised File", data="3D authorised file content here", file_name="authorised_file.step")
        st.button("Continue", on_click=next_screen, key="continue_3")

    elif st.session_state.howden_remake_screen == 5:
        st.title("ReMake - Repair Input")
        st.markdown("### Input and Output Data for Repair")
        with st.form(key='remake_repair_form'):
            st.text_input("MES Part Number", key="mes_part_number")
            st.text_input("Machine Number", key="machine_number")
            st.text_input("Operation Time", key="operation_time")
            st.file_uploader("Upload Repair Images", key="repair_images_upload", accept_multiple_files=True)
            submitted = st.form_submit_button("Submit")

        if submitted:
            st.success("Repair data submitted successfully!")
            st.button("Continue", on_click=next_screen, key="continue_4")

    elif st.session_state.howden_remake_screen == 6:
        st.title("Final Inputs and Outputs")
        st.write(f"### Part Number: {st.session_state.part_number}")
        st.file_uploader("Upload Excel Report", key="excel_report")
        st.file_uploader("Upload QIF Results File", key="qif_results_file")
        if st.button("Submit"):
            st.session_state.submitted = True
            next_screen()

    elif st.session_state.howden_remake_screen == 7:
        st.title("Submitting Data...")
        st.write("Please wait while your data is being submitted.")
        st.progress(100)
        time.sleep(5)
        next_screen()

    elif st.session_state.howden_remake_screen == 8:
        st.title("Submission Complete")
        st.write("Your data has been submitted successfully.")
        st.write("Please wait for authorisation which could take up to 72 hours.")
        st.button("Continue", on_click=next_screen, key="continue_8")

    elif st.session_state.howden_remake_screen == 9:
        st.title("Authentic Data - Kanban Board")
        st.markdown("### View Approval Status")
        kanban_data = {
            "To Do": ["Task 1", "Task 2"],
            "In Progress": ["Task 3"],
            "Done": ["Task 4"]
        }
        df_kanban = pd.DataFrame([
            {"Status": key, "Task": value}
            for key, values in kanban_data.items()
            for value in values
        ])
        gb = GridOptionsBuilder.from_dataframe(df_kanban)
        gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)
        gb.configure_grid_options(domLayout='normal')
        gridOptions = gb.build()
        AgGrid(
            df_kanban,
            gridOptions=gridOptions,
            enable_enterprise_modules=True,
            theme='streamlit',
            update_mode='SELECTION_CHANGED',
            allow_unsafe_jscode=True
        )
        st.file_uploader("Upload Audit Report", key="audit_report")
        st.button("Continue", on_click=next_screen, key="continue_9")

    elif st.session_state.howden_remake_screen == 10:
        st.title("Authentic Data - Automatic Check")
        st.markdown("### Run Automatic Verification")
        kanban_data = {
            "To Do": ["Task 1", "Task 2"],
            "In Progress": ["Task 3"],
            "Done": ["Task 4"]
        }
        df_kanban = pd.DataFrame([
            {"Status": key, "Task": value}
            for key, values in kanban_data.items()
            for value in values
        ])
        gb = GridOptionsBuilder.from_dataframe(df_kanban)
        gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)
        gb.configure_grid_options(domLayout='normal')
        gridOptions = gb.build()
        AgGrid(
            df_kanban,
            gridOptions=gridOptions,
            enable_enterprise_modules=True,
            theme='streamlit',
            update_mode='SELECTION_CHANGED',
            allow_unsafe_jscode=True
        )
        if st.button("Run Automatic Check"):
            with st.spinner("Running automatic verification..."):
                time.sleep(5)
                st.success("Automatic verification completed successfully.")
                st.session_state.howden_remake_screen += 1

    elif st.session_state.howden_remake_screen == 11:
        st.title("Verification Complete")
        st.write("Your data has been verified successfully.")
        st.write("Please wait for further instructions.")
        st.button("Finish", on_click=lambda: st.session_state.update(howden_remake_screen=0))

# Function call for testing in standalone mode
if __name__ == "__main__":
    show_howden_remake()
