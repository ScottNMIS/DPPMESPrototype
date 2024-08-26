import streamlit as st
from streamlit_option_menu import option_menu
from datapages.dpp_dashboard import *
from datapages.scan_qr import show_scan_qr_page
from datapages.create_dpp import show_create_dpp_page
from datapages.login import main_login, init_session_state, get_login_details, logout
from datapages.generic_data import show_footer, load_css, top_banner_main
from datapages.dataholder import MOCK_DATA
from datapages.data_loading import auto_download_session_state

# Ensure this is the first Streamlit command
st.set_page_config(page_title="MES DPP - NMIS", layout="wide")

def render_sidebar():
    with st.sidebar:
        login_details = get_login_details()
        if login_details["is_logged_in"]:

            st.sidebar.title(f"Welcome, {login_details['username']}!")
            
            selected = option_menu(
                "Main Menu", 
                ["Scan QR Code", "Create DPP", "Dashboard"],
                icons=['qr-code', 'plus-square', 'house'],
                menu_icon="cast", 
                default_index=0
            )
            
            if st.sidebar.button("Logout"):
                logout()
                st.rerun()
            
            return selected
        else:
            return "Login"

        st.sidebar.info('Developed by National Manufacturing Institute Scotland')

def main():
    init_session_state()  # Initialize session state
    
    load_css()
    
    # Display the top banner
    #top_banner_main()

    # Render sidebar and get selected option
    selected = render_sidebar()

    # Page routing
    login_details = get_login_details()
    if not login_details["is_logged_in"]:
        main_login()
    else:
        if selected == "Scan QR Code":
            show_scan_qr_page()
        elif selected == "Create DPP":
            show_create_dpp_page()
        elif selected == "Dashboard":
            show_dpp_dashboard()



    show_footer(MOCK_DATA)

    auto_download_session_state()

if __name__ == "__main__":
    main()