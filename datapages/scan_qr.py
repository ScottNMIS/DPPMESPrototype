import streamlit as st
import cv2
from pyzbar.pyzbar import decode
import numpy as np

# Function to check if a QR code is valid
def is_qr_code_valid(qr_code_data):
    """
    This function checks if a scanned or entered QR code is valid. Need to validate.
    """
    # Placeholder for future logic. Right now, it always returns True.
    return True

def scan_qr_code(image):
    qr_codes = decode(image)
    if qr_codes:
        for qr_code in qr_codes:
            data = qr_code.data.decode('utf-8')
            return data
    return None

def show_scan_qr_page():
    st.title("Scan QR Code or Enter Code")
    
    tab1, tab2 = st.tabs(["Scan QR", "Enter Code"])
    
    with tab1:
        st.subheader("Scan QR Code")
        qr_code_image = st.camera_input("Scan QR Code")
        
        if qr_code_image is not None:
            file_bytes = np.asarray(bytearray(qr_code_image.read()), dtype=np.uint8)
            img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            qr_data = scan_qr_code(img)
            
            if qr_data:
                if is_qr_code_valid(qr_data):  # Use the new validation function
                    st.success(f"QR Code scanned successfully! Data: {qr_data}")
                    st.session_state['dpp_data'] = qr_data  # Store the actual QR code data
                    st.session_state['is_qr_valid'] = True  # Set the flag to true for valid QR scan
                    st.rerun()
                else:
                    st.error("The QR code is not valid. Please try again.")
            else:
                st.error("No valid QR code detected. Please try again.")
    
    with tab2:
        st.subheader("Enter QR Code String")
        qr_string = st.text_input("Enter the QR code string")
        if st.button("Submit"):
            if qr_string:
                if is_qr_code_valid(qr_string):  # Use the new validation function
                    st.session_state['dpp_data'] = qr_string
                    st.session_state['is_qr_valid'] = True
                    st.success(f"QR Code submitted successfully! Data: {qr_string}")
                    st.rerun()
                else:
                    st.error("The QR code is not valid. Please try again.")
            else:
                st.error("Please enter a valid QR code string.")
