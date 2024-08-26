import streamlit as st
from streamlit_option_menu import option_menu
from datapages.dpp_dashboard import show_dpp_dashboard
from datapages.dpp_advanceddashboard import show_advanced_dpp_dashboard
from datapages.data_visualisation import show_data_visualisation
from datapages.additional_page import show_data_input_page
from datapages.advanced_visualisation import show_advanced_visualisation
from datapages.login import main_login, init_session_state, get_login_details, logout
from datapages.model_viewer import show_model_viewer
from datapages.factory_data import main_test
from datapages.sustainability import show_sustainability_info
from datapages.company_info import show_company_info
from datapages.keycloak_test import show_keycloak_test
from datapages.dpp_management import show_dpp_management
from datapages.generic_data import show_footer, load_css, top_banner_main
from datapages.dataholder import MOCK_DATA
from datapages.data_loading import auto_download_session_state
from datapages.scan_qr import show_scan_qr_page
from datapages.create_dpp import show_create_dpp_page

# Ensure this is the first Streamlit command
st.set_page_config(page_title="MES DPP - NMIS", layout="wide")

def main():
    init_session_state()  # Initialize session state
    load_css()
    
    # Display the top banner
    top_banner_main()

    # Sidebar Navigation with option_menu
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
        else:
            selected = "Login"

        st.session_state['selected_page'] = selected

    # Page routing
    if not login_details["is_logged_in"]:
        main_login()
    else:
        if st.session_state['selected_page'] == "Scan QR Code":
            show_scan_qr_page()
        elif st.session_state['selected_page'] == "Create DPP":
            show_create_dpp_page()
        elif st.session_state['selected_page'] == "Dashboard":
            show_dpp_dashboard()

    st.sidebar.info('Developed by National Manufacturing Institute Scotland')

    show_footer(MOCK_DATA)

    auto_download_session_state()

if __name__ == "__main__":
    main()