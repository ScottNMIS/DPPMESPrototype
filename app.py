import streamlit as st
from streamlit_option_menu import option_menu
from datapages.dpp_dashboard import show_dpp_dashboard
from datapages.dpp_advanceddashboard import show_advanced_dpp_dashboard
from datapages.data_visualisation import show_data_visualisation
from datapages.additional_page import show_data_input_page
from datapages.advanced_visualisation import show_advanced_visualisation
from datapages.login import show_login
from datapages.model_viewer import show_model_viewer
from datapages.factory_data import main_test
from datapages.sustainability import show_sustainability_info
from datapages.company_info import show_company_info
from datapages.howden_demo_initial import show_howden_demo_initial
from datapages.howden_remake import show_howden_remake
from datapages.keycloak_test import show_keycloak_test
from datapages.dpp_management import show_dpp_management
from datapages.generic_data import show_footer, load_css, top_banner_main
from datapages.dataholder import MOCK_DATA

# Ensure this is the first Streamlit command
st.set_page_config(page_title="MES DPP - NMIS", layout="wide")

def main():
    load_css()
    top_banner_main()

    # Initialize session state for request access
    if 'request_access_clicked' not in st.session_state:
        st.session_state.request_access_clicked = False


    # Sidebar Navigation with option_menu
    with st.sidebar:
        # Check if the selected page is already set in session state
        if 'selected_page' not in st.session_state:
            st.session_state.selected_page = "Login"  # Default page

        selected = option_menu(
            "Main Menu", 
            ["Login", "Dashboard", "Advanced Dashboard", "Data Visualisation", "Data Input", "Advanced Visualisation", "3D Model Viewer", "Factory Data", "Sustainability Info", "Company Info", "Customisation", "Howden Demo Initial", "Howden Remake", "Keycloak Test", "DPP Management"],
            icons=['person', 'house', 'input-cursor-text', 'bar-chart-line', 'file-earmark-plus', 'graph-up', 'cube', 'database', 'leaf', 'building', 'wrench', 'key', 'file-code', 'robot'],
            menu_icon="cast", 
            default_index=0
        )

        # Update session state with the selected page from the sidebar menu
        st.session_state.selected_page = selected


    # Handle "Request Access" button click
    if st.session_state.get('request_access_clicked', False):
        st.session_state.selected_page = "Advanced Dashboard"
        st.session_state.request_access_clicked = False  # Reset the flag

    if st.session_state.selected_page == "Login":
        show_login()
    elif st.session_state.selected_page == "Dashboard":
        show_dpp_dashboard()
    elif st.session_state.selected_page == "Advanced Dashboard":
        show_advanced_dpp_dashboard()
    elif st.session_state.selected_page == "Data Visualisation":
        show_data_visualisation()
    elif st.session_state.selected_page == "Data Input":
        show_data_input_page()
    elif st.session_state.selected_page == "Advanced Visualisation":
        show_advanced_visualisation()
    elif st.session_state.selected_page == "3D Model Viewer":
        show_model_viewer()
    elif st.session_state.selected_page == "Factory Data":
        main_test()
    elif st.session_state.selected_page == "Sustainability Info":
        show_sustainability_info()
    elif st.session_state.selected_page == "Company Info":
        show_company_info()
    elif st.session_state.selected_page == "Howden Demo Initial":
        show_howden_demo_initial()
    elif st.session_state.selected_page == "Howden Remake":
        show_howden_remake()
    elif st.session_state.selected_page == "Keycloak Test":
        show_keycloak_test()
    elif st.session_state.selected_page == "DPP Management":
        show_dpp_management()

    st.sidebar.info('Developed by National Manufacturing Institute Scotland')

    show_footer(MOCK_DATA)


if __name__ == "__main__":
    main()
