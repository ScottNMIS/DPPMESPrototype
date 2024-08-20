import streamlit as st
from io import BytesIO
import time
from datetime import datetime
from streamlit_drawable_canvas import st_canvas

def show_howden_demo_initial():
    # Initialize session state variables
    session_vars = [
        'howden_demo_screen', 'part_number', 'part_description',
        'mass', 'material', 'hardness', 'excel_report_template', 'excel_report', 'qif_results_file', 'submitted'
    ]
    for var in session_vars:
        if var not in st.session_state:
            st.session_state[var] = ""

    if 'howden_demo_screen' not in st.session_state or st.session_state.howden_demo_screen == "":
        st.session_state.howden_demo_screen = 0

    if 'submitted' not in st.session_state:
        st.session_state.submitted = False

    # Ensure howden_demo_screen is an integer
    try:
        st.session_state.howden_demo_screen = int(st.session_state.howden_demo_screen)
    except ValueError:
        st.session_state.howden_demo_screen = 0

    # Function to move to the next screen
    def next_screen():
        if st.session_state.howden_demo_screen < 6:
            st.session_state.howden_demo_screen += 1

    # Function to move to the previous screen
    def prev_screen():
        if st.session_state.howden_demo_screen > 0:
            st.session_state.howden_demo_screen -= 1

    # Screen 0: Login Screen
    if st.session_state.howden_demo_screen == 0:
        st.title("Login")
        st.markdown("### Please sign in to access the dataset")
        with st.form(key='login_form'):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            login_submitted = st.form_submit_button("Sign In")

        if login_submitted:
            st.success("Sign in successful")
            st.markdown("You are authorised to access this dataset.")
            st.button("Continue", on_click=next_screen)

    # Screen 1: Part Information and File Uploads
    elif st.session_state.howden_demo_screen == 1:
        st.title("Screen 1: Part Information and File Uploads")
        st.markdown("### Enter Part Details and Upload Files")

        with st.form(key='part_info_form'):
            part_number = st.text_input("Part Number", value=st.session_state.part_number)
            part_description = st.text_input("Part Description", value=st.session_state.part_description)
            st.text_input("Mass", key="mass")
            st.text_input("Material (Solidworks)", key="material")
            st.text_input("Hardness", key="hardness")
            st.file_uploader("Upload CAD file (STEP) Finish", key="cad_file")
            st.file_uploader("MBD QIF file (Capvidia)", key="mbd_qif_file")
            st.file_uploader("3D Pdf", key="pdf_3d")
            st.file_uploader("Upload CAD file (STEP) ReMake", key="cad_file_remake")
            st.file_uploader("MBD QIF file (Capvidia) - Remake", key="mbd_qif_file_remake")
            st.file_uploader("3D Pdf - Remake", key="pdf_3d_remake")
            st.file_uploader("Repair guideline", key="repair_guideline")
            submitted = st.form_submit_button("Submit")

        if submitted:
            # Save the local variables to session state
            st.session_state.part_number = part_number
            st.session_state.part_description = part_description
            st.success("Part information submitted successfully!")
            st.button("Continue", on_click=next_screen)

    # Screen 2: Part Number and Excel Report Template
    elif st.session_state.howden_demo_screen == 2:
        st.title("Screen 2: Excel Report Template")
        st.write(f"### Part Number: {st.session_state.part_number}")
        st.file_uploader("Excel report template", key="excel_report_template")
        col1, col2 = st.columns([1, 1])
        with col1:
            st.button("Back", on_click=prev_screen)
        with col2:
            st.button("Continue", on_click=next_screen)

    # Screen 3: Part Number, Excel Report, and QIF Results File
    elif st.session_state.howden_demo_screen == 3:
        st.title("Screen 3: Excel Report and QIF Results File")
        st.write(f"### Part Number: {st.session_state.part_number}")
        st.file_uploader("Excel report", key="excel_report")
        st.file_uploader("QIF results file", key="qif_results_file")
        
        # Signature and authorisation section
        st.subheader("Authorisation")
        st.markdown(f"**Authorised by:** John Doe")
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.markdown(f"**Date and Time:** {current_time}")
        st.write("Sign below:")
        canvas_result = st_canvas(
            fill_color="white",  # White background
            stroke_width=2,
            stroke_color="black",  # Black stroke color
            background_color="white",  # White background
            update_streamlit=True,
            height=150,
            drawing_mode="freedraw",
            key="canvas"
        )
        
        col1, col2 = st.columns([1, 1])
        with col1:
            st.button("Back", on_click=prev_screen)
        with col2:
            if st.button("Submit"):
                st.session_state.submitted = True
                st.session_state.howden_demo_screen = 4
                st.experimental_rerun()

    # Loading screen (Screen 4)
    elif st.session_state.howden_demo_screen == 4:
        st.title("Submitting Data...")
        with st.spinner("Please wait while we process your data."):
            time.sleep(10)  # Simulate waiting for data processing
            st.session_state.submitted = False
            st.session_state.howden_demo_screen = 5
            st.experimental_rerun()

    # Confirmation screen (Screen 5)
    elif st.session_state.howden_demo_screen == 5:
        st.title("Data Submitted")
        st.success("Your data has been submitted and is pending authorization. Please wait for authorisation, which could take up to 72 hours.")
        
        st.markdown("### Summary of Submitted Data")
        st.write(f"**Part Number:** {st.session_state.part_number}")
        st.write(f"**Part Description:** {st.session_state.part_description}")
        st.write(f"**Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        st.button("Back to Home", on_click=lambda: st.session_state.update(howden_demo_screen=1))

# Add the new function to the list of imports in your main app file
