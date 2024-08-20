import streamlit as st
import requests
import random
from io import BytesIO

# Define FastAPI URLs
USER_API_URL = "http://130.159.132.19:8000/users"
DPP_API_URL = "http://130.159.132.19:8000/dpps"

# Function to create a user with success/failure feedback
def create_user(email, password):
    try:
        # Send POST request to FastAPI to create a user
        response = requests.post(
            USER_API_URL,
            json={"email": email, "password": password}
        )
        
        # Check for a successful response
        if response.status_code == 201:
            st.success("User created successfully!")
            st.json(response.json())  # Display the response JSON
        elif response.status_code == 422:
            st.error("Validation Error: Check input values.")
            st.json(response.json())  # Display the error response JSON
        else:
            st.error(f"Failed to create user. Status code: {response.status_code}")
            st.json(response.json())  # Display the error response JSON
    except Exception as e:
        st.error(f"Error: {str(e)}")

# Function to create a Dpp with success/failure feedback
def create_dpp(title, qrcode):
    try:
        # Send POST request to FastAPI to create a Dpp
        response = requests.post(
            DPP_API_URL,
            json={"title": title, "qrcode": qrcode}
        )
        
        # Check for a successful response
        if response.status_code == 201:
            st.success("Dpp created successfully!")
            st.json(response.json())  # Display the response JSON
        elif response.status_code == 422:
            st.error("Validation Error: Check input values.")
            st.json(response.json())  # Display the error response JSON
        else:
            st.error(f"Failed to create Dpp. Status code: {response.status_code}")
            st.json(response.json())  # Display the error response JSON
    except Exception as e:
        st.error(f"Error: {str(e)}")

# Streamlit app to input email and password for user creation
def user_creation_ui():
    st.subheader("Create a New User")

    # Input fields for email and password
    email = st.text_input("Email", value="user@example.com")
    password = st.text_input("Password", type="password")

    # Button to create user
    if st.button("Create User"):
        if email and password:
            create_user(email, password)
        else:
            st.warning("Please fill in both the email and password fields.")

# Streamlit app to input title and qrcode for Dpp creation
def dpp_creation_ui():
    st.subheader("Create a New Dpp")

    # Input fields for title and qrcode
    title = st.text_input("Title", value="Dpp Title")
    qrcode = st.text_input("QR Code", value="QR12345")

    # Button to create Dpp
    if st.button("Create Dpp"):
        if title and qrcode:
            create_dpp(title, qrcode)
        else:
            st.warning("Please fill in both the title and QR code fields.")

# Generate dummy data for submission
def generate_dummy_data():
    """ Function to generate dummy data for testing, including fake files """
    
    # Create a fake binary file for testing (e.g., a simple text converted to bytes)
    def create_fake_file(filename):
        fake_file = BytesIO()
        fake_file.write(f"This is a dummy {filename} file.".encode('utf-8'))
        fake_file.seek(0)  # Move to the start of the file after writing
        return fake_file

    dummy_data = {
        'part_number': f"PN-{random.randint(1000, 9999)}",
        'part_description': f"Part description for test part {random.randint(1000, 9999)}",
        'mass': f"{random.uniform(10, 50):.2f} kg",
        'material': f"Material-{random.randint(1, 5)}",
        'hardness': f"{random.randint(50, 100)} HRC",
        'cad_file': create_fake_file("CAD_STEP_file_finish.step"),  # Fake STEP file
        'mbd_qif_file': create_fake_file("MBD_QIF_file.qif"),  # Fake QIF file
        'pdf_3d': create_fake_file("3D_PDF_file.pdf"),  # Fake 3D PDF file
        'cad_file_remake': create_fake_file("CAD_STEP_file_remake.step"),  # Fake STEP remake file
        'mbd_qif_file_remake': create_fake_file("MBD_QIF_file_remake.qif"),  # Fake QIF remake file
        'pdf_3d_remake': create_fake_file("3D_PDF_file_remake.pdf"),  # Fake 3D PDF remake file
        'repair_guideline': create_fake_file("Repair_Guideline.pdf"),  # Fake repair guideline PDF
        'excel_report_template': create_fake_file("Excel_Report_Template.xlsx"),  # Fake Excel report template
        'excel_report': create_fake_file("Excel_Report.xlsx"),  # Fake Excel report
        'qif_results_file': create_fake_file("QIF_Results_File.qif")  # Fake QIF results file
    }
    
    return dummy_data

# Function to send dummy data to FastAPI with success/failure feedback
def submit_dummy_data(data):
    try:
        # Simulate a POST request to FastAPI (replace this URL with your actual endpoint)
        response = requests.post(DPP_API_URL, json={"dummy_data": "data"})
        
        # Check for a successful response
        if response.status_code == 200:
            st.success("Dummy data submitted successfully!")
            st.json(response.json())  # Display the response
        else:
            st.error(f"Failed to submit data. Status code: {response.status_code}")
            st.json(response.json())  # Display error
    except Exception as e:
        st.error(f"Error submitting data: {str(e)}")

# Main function to run the app
def main_test():
    st.title("Create User and Dpp")

    # Render the User Creation form
    user_creation_ui()

    # Separator
    st.markdown("---")

    # Render the Dpp Creation form
    dpp_creation_ui()

    # Separator
    st.markdown("---")

    # Add a button to generate and show dummy data
    generate_data = st.button("Generate Dummy Data")
    
    if "dummy_data" not in st.session_state:
        st.session_state.dummy_data = None

    if generate_data:
        st.session_state.dummy_data = generate_dummy_data()
    
    if st.session_state.dummy_data:
        st.subheader("Generated Dummy Data")

        # Display the dummy data
        st.json({
            "part_number": st.session_state.dummy_data['part_number'],
            "part_description": st.session_state.dummy_data['part_description'],
            "mass": st.session_state.dummy_data['mass'],
            "material": st.session_state.dummy_data['material'],
            "hardness": st.session_state.dummy_data['hardness']
        })

        # Submit Button to send the dummy data
        if st.button("Submit Data"):
            submit_dummy_data(st.session_state.dummy_data)

# Function call for testing in standalone mode
if __name__ == "__main__":
    main_test()
