import streamlit as st
import cv2
import numpy as np
from pyzbar.pyzbar import decode

def show_login():
    st.title("Login Screen")

    # Split the page into two columns
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Login with Username and Password")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username == "admin" and password == "password":
                st.success("Logged in successfully")
            else:
                st.error("Invalid username or password")

    with col2:
        st.subheader("Login with QR Code")
        st.text("Scan the QR code to log in")

        qr_code = st.camera_input("Scan QR Code")
        if qr_code:
            file_bytes = np.asarray(bytearray(qr_code.read()), dtype=np.uint8)
            img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            qr_data = decode_qr_code(img)
            if qr_data:
                st.success(f"QR code scanned successfully: {qr_data}")
            else:
                st.error("No QR code detected or unreadable QR code")

def decode_qr_code(img):
    qr_codes = decode(img)
    for qr_code in qr_codes:
        return qr_code.data.decode('utf-8')
    return None

# Function call for testing in standalone mode
if __name__ == "__main__":
    show_login()
