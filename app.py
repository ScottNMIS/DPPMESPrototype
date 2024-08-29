import streamlit as st
from streamlit_option_menu import option_menu
from datapages.dpp_dashboard import show_dpp_dashboard
from datapages.scan_qr import show_scan_qr_page
from datapages.create_dpp import show_create_dpp_page
from datapages.login import main_login, init_session_state, get_login_details, logout
from datapages.generic_data import show_footer, load_css, top_banner_main
from datapages.dataholder import MOCK_DATA
from datapages.data_loading import auto_download_session_state
from datapages.data_input import show_data_input_page
from datapages.dpp_advanceddashboard import show_advanced_dpp_dashboard

st.set_page_config(page_title="MES DPP - NMIS", layout="wide")

def render_sidebar():
    with st.sidebar:
        login_details = get_login_details()
        if login_details["is_logged_in"]:
            st.sidebar.title(f"Welcome, {login_details['username']}!")
            
            # Should display current QR code data if available
            if 'dpp_data' in st.session_state and st.session_state['dpp_data']:
                st.sidebar.subheader("Current DPP Data")
                dpp_data = st.session_state['dpp_data']
                
                if isinstance(dpp_data, dict):
                    st.sidebar.text(f"Name: {dpp_data.get('title', 'N/A')}")
                    st.sidebar.text(f"QR Code: {dpp_data.get('qrcode', 'N/A')}")
                elif isinstance(dpp_data, str):
                    st.sidebar.text(f"DPP Data: {dpp_data}")
                else:
                    st.sidebar.text("DPP Data format is unknown")
            
            if 'is_qr_valid' in st.session_state and st.session_state['is_qr_valid']:
                selected = option_menu(
                    "Main Menu", 
                    ["Scan QR Code", "Create DPP", "Dashboard", "Advanced Dashboard", "Input Data"],
                    icons=['qr-code', 'plus-square', 'house', 'bar-chart', 'file-text'],
                    menu_icon="cast", 
                    default_index=2
                )
            else:
                selected = option_menu(
                    "Main Menu", 
                    ["Scan QR Code", "Create DPP"],
                    icons=['qr-code', 'plus-square'],
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
    init_session_state()
    load_css()
    selected = render_sidebar()

    login_details = get_login_details()
    if not login_details["is_logged_in"]:
        main_login()
    else:
        if selected == "Scan QR Code":
            show_scan_qr_page()
        elif selected == "Create DPP":
            show_create_dpp_page()
        elif selected == "Dashboard" and 'is_qr_valid' in st.session_state and st.session_state['is_qr_valid']:
            show_dpp_dashboard()
        elif selected == "Advanced Dashboard" and 'is_qr_valid' in st.session_state and st.session_state['is_qr_valid']:
            show_advanced_dpp_dashboard()
        elif selected == "Input Data" and 'is_qr_valid' in st.session_state and st.session_state['is_qr_valid']:
            show_data_input_page()

    show_footer()
    auto_download_session_state()

if __name__ == "__main__":
    main()