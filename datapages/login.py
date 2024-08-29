import streamlit as st
from extra_streamlit_components import CookieManager
import requests
#from streamlit_extras.app_logo import add_logo
import cv2
import numpy as np
from pyzbar.pyzbar import decode
import re  # For email validation

# Initialize cookie manager
cookie_manager = CookieManager()

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

# Function to authenticate user via FastAPI
def authenticate_user(email, password):
    url = "http://130.159.132.19:8000/token"
    payload = {
        "grant_type": "password",
        "username": email,
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
    url = "http://130.159.132.19:8000/users"
    payload = {
        "email": email,
        "password": password
    }
    response = requests.post(url, json=payload)
    
    # Check if registration was successful
    if response.status_code == 201:
        return True  # Registration successful
    elif response.status_code == 422:
        # This error often occurs when validation fails (e.g., email already exists)
        return {"error": "Validation Error. Please check the data provided."}
    else:
        return {"error": "Failed to register user. Please try again."}

# Function to save login info to session state and cookies
def save_login_info(email, access_token):
    st.session_state['is_logged_in'] = True
    st.session_state['access_token'] = access_token
    st.session_state['username'] = email
    st.session_state['selected_page'] = "Scan QR Code"  # Set default page after login
    
    # Save login state in cookies
    cookie_manager.set(
        "login_info",
        {
            "username": email,
            "access_token": access_token,
            "is_logged_in": "True"
        },
        key="set_login_info"
    )

def load_login_info_from_cookies():
    login_info = cookie_manager.get("login_info")
    if login_info and login_info.get("is_logged_in") == "True":
        # Check if the session state doesn't match the cookie state
        if not st.session_state.get('is_logged_in'):
            st.session_state['is_logged_in'] = True
            st.session_state['username'] = login_info.get("username")
            st.session_state['access_token'] = login_info.get("access_token")
            st.rerun()  # Force a rerun to update the page
        else:
            # Update session state if it's not already set
            st.session_state['username'] = login_info.get("username")
            st.session_state['access_token'] = login_info.get("access_token")

# Function to log out the user
def logout():
    st.session_state['is_logged_in'] = False
    st.session_state['access_token'] = None
    st.session_state['username'] = None
    
    # Clear cookies
    cookie_manager.delete("login_info", key="delete_login_info")

# Function to get current login details
def get_login_details():
    return {
        "is_logged_in": st.session_state.get('is_logged_in', False),
        "username": st.session_state.get('username', None),
        "access_token": st.session_state.get('access_token', None)
    }

# Helper function to validate email format
def is_valid_email(email):
    email_regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.match(email_regex, email)

# Login and Register screens
def show_login_register():
    st.title("NMIS Digital Product Passport")
   # add_logo("images/nmis_short.png")  # Replace with your logo URL
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.subheader("Login")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login", key="login_button"):
            if not is_valid_email(email):
                st.error("Please enter a valid email address.")
            else:
                access_token = authenticate_user(email, password)
                if access_token:
                    save_login_info(email, access_token)
                    st.success("Logged in successfully")
                    st.rerun()
                else:
                    st.error("Invalid email or password")

    with tab2:
        st.subheader("Register")
        email = st.text_input("Email", key="register_email")
        password = st.text_input("Password", type="password", key="register_password")
        
        if st.button("Register", key="register_button"):
            if not is_valid_email(email):
                st.error("Please enter a valid email address.")
            elif len(password) < 5:
                st.error("Password must be at least 5 characters long.")
            else:
                registration_result = register_user(email, password)
                
                if registration_result is True:
                    st.success("User registered successfully. Please login.")
                elif isinstance(registration_result, dict) and "error" in registration_result:
                    st.error(registration_result["error"])
                else:
                    st.error("An unexpected error occurred. Please try again.")

# QR Scanner
def show_qr_scanner():
    st.title("Digital Product Passport QR Scanner")
    st.write("Use your camera to scan the QR code of a digital product passport")
    
    qr_code_image = st.camera_input("Scan QR Code")
    
    if qr_code_image is not None:
        file_bytes = np.asarray(bytearray(qr_code_image.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        qr_data = decode(img)
        if qr_data:
            st.success("Digital Product Passport QR Code detected!")
            st.session_state['dpp_data'] = qr_data[0].data.decode('utf-8')  # Store DPP data in session state
            st.session_state['selected_page'] = "Dashboard"  # Transition to DPP dashboard
            st.rerun()
        else:
            st.error("No QR code detected. Please try again.")

def main_login():
    init_session_state()  # Initialize session state
    
    # Load login info from cookies if available
    load_login_info_from_cookies()

    if not st.session_state['is_logged_in']:
        show_login_register()
    else:
        st.sidebar.title(f"Welcome, {st.session_state['username']}!")
        if st.sidebar.button("Logout", key="logout_button"):
            logout()
            st.rerun()
        
        show_qr_scanner()

if __name__ == "__main__":
    main_login()
