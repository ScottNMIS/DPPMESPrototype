import streamlit as st

# Function to show top bar
def show_top_bar():
    account_name = st.session_state.get('account_name', 'Guest')
    st.markdown(f"""
        <style>
        .top-bar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px;
            background-color: #007BFF;  /* Blue background */
            color: white;
            border-bottom: 1px solid #ccc;
        }}
        .user-info {{
            font-size: 18px;
        }}
        .button-container {{
            display: flex;
            justify-content: center;
            margin-bottom: 0px;
        }}
        .button-container button {{
            background-color: #28a745;
            color: white;
            padding: 10px 20px;
            border: none;
            cursor: pointer;
            font-size: 16px;
            border-radius: 5px;
            margin: 5px;  /* Adjust margin between buttons */
        }}
        .button-container button:hover {{
            background-color: #218838;
        }}
        </style>
        <div class="top-bar">
            <div class="user-info">Logged in as: <strong>{account_name}</strong></div>
        </div>
    """, unsafe_allow_html=True)

# Function to load button styles
def load_button_css():
    st.markdown("""
        <style>
        .full-width-button > button {
            width: 100%;
            height: 60px;  /* Set the height to 60px */
            background-color: #28a745; /* Green background */
            color: white;  /* White text */
            border: none;
            font-size: 16px; /* Adjust font size */
            border-radius: 8px; /* Optional: Rounded corners */
            margin-bottom: 0px; /* Eliminate margin at the bottom */
        }
        .full-width-button > button:hover {
            background-color: #218838; /* Darker green on hover */
        }
        .stButton {
            margin-bottom: 0px; /* Eliminate the gap between buttons and other elements */
        }
        </style>
    """, unsafe_allow_html=True)

# Function to add buttons with no gap
def add_buttons():
    # Load the CSS for full-width, green, and height-100px buttons
    load_button_css()
    col1, col2, col3 = st.columns(3)  # Equal column width
    with col1:
        if st.button("Button 1", key="btn1", help="Click to interact", use_container_width=True):
            st.write("Button 1 clicked")
    with col2:
        if st.button("Button 2", key="btn2", help="Click to interact", use_container_width=True):
            st.write("Button 2 clicked")
    with col3:
        if st.button("Button 3", key="btn3", help="Click to interact", use_container_width=True):
            st.write("Button 3 clicked")

# Function to display the login screen with minimal gap
def show_login_screen():
    st.markdown("<h2 style='margin-top: 0px;'>Login Screen</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Username")
        st.text_input("Password", type="password")
        st.button("Login")
    with col2:
        st.markdown("<h3>Login with QR Code</h3>", unsafe_allow_html=True)
        st.button("Start QR Scanning")

# Main Streamlit layout
def main():
    show_top_bar()
    add_buttons()  # Add the buttons right below the top bar
    show_login_screen()  # Display the login screen below the buttons

if __name__ == "__main__":
    main()
