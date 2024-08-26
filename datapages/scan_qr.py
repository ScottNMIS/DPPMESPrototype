import streamlit as st
import cv2
from pyzbar.pyzbar import decode
import numpy as np

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
                st.success("QR Code scanned successfully!")
                st.session_state['dpp_data'] = qr_data
                st.session_state['selected_page'] = "Dashboard"
                st.rerun()
            else:
                st.error("No QR code detected. Please try again.")
    
    with tab2:
        st.subheader("Enter QR Code String")
        qr_string = st.text_input("Enter the QR code string")
        if st.button("Submit"):
            if qr_string:
                st.session_state['dpp_data'] = qr_string
                st.session_state['selected_page'] = "Dashboard"
                st.rerun()
            else:
                st.error("Please enter a valid QR code string.")

if __name__ == "__main__":
    show_scan_qr_page()