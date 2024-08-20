import streamlit as st
import cv2
from pyzbar.pyzbar import decode
import numpy as np
import time

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
        st.text("Keep scanning the QR code until it is detected")

        # Button to start the QR scanning process
        if st.button("Start QR Scanning"):
            qr_detected = False
            while not qr_detected:
                qr_code_image = st.camera_input("Scan QR Code")

                if qr_code_image:
                    file_bytes = np.asarray(bytearray(qr_code_image.read()), dtype=np.uint8)
                    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

                    qr_codes = decode(img)
                    if qr_codes:
                        for qr_code in qr_codes:
                            data = qr_code.data.decode('utf-8')
                            st.success(f"QR Code detected: {data}")
                            qr_detected = True
                            break
                    else:
                        st.info("No QR code detected. Retrying in 1 second...")
                        time.sleep(1)  # Wait for 1 second before trying again

                    # Display the captured image
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    st.image(img)

# Function call for testing in standalone mode
if __name__ == "__main__":
    show_login()
