import streamlit as st
from streamlit_option_menu import option_menu
from pages.home import show_home
from pages.data_input import show_data_input
from pages.data_visualisation import show_data_visualisation
from pages.additional_page import show_additional_page
from pages.advanced_visualisation import show_advanced_visualisation
from pages.login import show_login
from pages.model_viewer import show_model_viewer
from pages.factory_data import show_factory_data
from pages.sustainability import show_sustainability_info
from pages.company_info import show_company_info
from pages.customisation import show_customisation  # Import the new function

# Ensure this is the first Streamlit command
st.set_page_config(page_title="MES DPP - NMIS", layout="wide")

def main():
    # Sidebar Navigation with option_menu
    with st.sidebar:
        selected = option_menu(
            "Main Menu", 
            ["Login", "Home", "Data Input", "Data Visualisation", "Additional Page", "Advanced Visualisation", "3D Model Viewer", "Factory Data", "Sustainability Info", "Company Info", "Customisation"], 
            icons=['person', 'house', 'input-cursor-text', 'bar-chart-line', 'file-earmark-plus', 'graph-up', 'cube', 'database', 'leaf', 'building', 'wrench'], 
            menu_icon="cast", 
            default_index=0
        )

    # Display selected page
    if selected == "Login":
        show_login()
    elif selected == "Home":
        show_home()
    elif selected == "Data Input":
        show_data_input()
    elif selected == "Data Visualisation":
        show_data_visualisation()
    elif selected == "Additional Page":
        show_additional_page()
    elif selected == "Advanced Visualisation":
        show_advanced_visualisation()
    elif selected == "3D Model Viewer":
        show_model_viewer()
    elif selected == "Factory Data":
        show_factory_data()
    elif selected == "Sustainability Info":
        show_sustainability_info()
    elif selected == "Company Info":
        show_company_info()
    elif selected == "Customisation":
        show_customisation()

    st.sidebar.info('Developed by National Manufacturing Institute Scotland')

if __name__ == "__main__":
    main()
