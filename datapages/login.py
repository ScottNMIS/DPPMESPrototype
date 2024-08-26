import streamlit as st
import cv2
from pyzbar.pyzbar import decode
import numpy as np
import requests
from streamlit_extras.app_logo import add_logo

# Initialize session state variables
def init_session_state():
    session_vars = {
        'is_logged_in': False,
        'access_token': None,
        'username': None,
        'dpp_data': None
    }
    for var, default_value in session_vars.items():
        if var not in st.session_state:
            st.session_state[var] = default_value

# Function to scan a QR code from an image
def scan_qr_code(image):
    qr_codes = decode(image)
    if qr_codes:
        for qr_code in qr_codes:
            data = qr_code.data.decode('utf-8')
            return data
    return None

# Function to authenticate user via FastAPI
def authenticate_user(username, password):
    url = "http://130.159.132.19:8000/token"  # FastAPI login endpoint
    payload = {
        "grant_type": "password",
        "username": username,
        "password": password
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, data=payload, headers=headers)
    
    if response.status_code == 200:
        token_data = response.json()
        return token_data["access_token"]
    else:
        return None

# Function to register a new user via FastAPI
def register_user(email, password):
    url = "http://130.159.132.19:8000/users"  # FastAPI register endpoint
    payload = {
        "email": email,
        "password": password
    }
    response = requests.post(url, json=payload)
    
    return response.status_code == 201

# Function to save login info to session state
def save_login_info(username, access_token):
    st.session_state['is_logged_in'] = True
    st.session_state['access_token'] = access_token
    st.session_state['username'] = username
    st.session_state['selected_page'] = "Scan QR Code"  # Set default page after login

# Function to log out the user
def logout():
    st.session_state['is_logged_in'] = False
    st.session_state['access_token'] = None
    st.session_state['username'] = None

# Function to get current login details
def get_login_details():
    return {
        "is_logged_in": st.session_state.get('is_logged_in', False),
        "username": st.session_state.get('username', None),
        "access_token": st.session_state.get('access_token', None)
    }

# Login and Register screens
def show_login_register():
    st.title("Digital Product Passport Scanner")
    add_logo("https://www.example.com/logo.png")  # Replace with your logo URL
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.subheader("Login")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login", use_container_width=True):
            access_token = authenticate_user(username, password)
            if access_token:
                save_login_info(username, access_token)
                st.success("Logged in successfully")
                st.rerun()
            else:
                st.error("Invalid username or password")

    with tab2:
        st.subheader("Register")
        email = st.text_input("Email", key="register_email")
        password = st.text_input("Password", type="password", key="register_password")
        if st.button("Register", use_container_width=True):
            if register_user(email, password):
                st.success("User registered successfully. Please login.")
            else:
                st.error("Failed to register user. Please try again.")

# QR Scanner
def show_qr_scanner():
    st.title("Digital Product Passport QR Scanner")
    st.write("Use your camera to scan the QR code of a digital product passport")
    
    qr_code_image = st.camera_input("Scan QR Code")
    
    if qr_code_image is not None:
        file_bytes = np.asarray(bytearray(qr_code_image.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        qr_data = scan_qr_code(img)
        if qr_data:
            st.success("Digital Product Passport QR Code detected!")
            st.session_state['dpp_data'] = qr_data  # Store DPP data in session state
            st.session_state['selected_page'] = "Dashboard"  # Transition to DPP dashboard
            st.rerun()
        else:
            st.error("No QR code detected. Please try again.")

# Main app logic
def main_login():
    init_session_state()  # Initialize session state
    
    if not st.session_state['is_logged_in']:
        show_login_register()
    else:
        st.sidebar.title(f"Welcome, {st.session_state['username']}!")
        if st.sidebar.button("Logout"):
            logout()
            st.rerun()
        
        show_qr_scanner()

if __name__ == "__main__":
    main_login()