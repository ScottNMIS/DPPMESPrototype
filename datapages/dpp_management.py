import streamlit as st
import requests

def show_dpp_management():
    st.title("DPP Management")
    st.write("Manage Data Processing Plans (DPPs) in the system.")

    # Input box for FastAPI base URL
    api_base_url = st.text_input("Enter the API Base URL", value="http://130.159.132.19:8000")

    # Buttons for actions
    col1, col2 = st.columns(2)
    with col1:
        view_button = st.button("View All DPPs")
    with col2:
        create_button = st.button("Create New DPP")

    # Function to get all DPPs
    def get_all_dpps(api_base_url):
        try:
            response = requests.get(f"{api_base_url}/dpps")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Error retrieving DPPs: {e}")
            return None

    # Function to create a new DPP
    def create_dpp(api_base_url, dpp_name, dpp_description):
        new_dpp = {"name": dpp_name, "description": dpp_description}
        try:
            response = requests.post(f"{api_base_url}/dpps", json=new_dpp)
            response.raise_for_status()
            st.success("DPP created successfully!")
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Error creating DPP: {e}")
            return None

    # If the "View All DPPs" button is clicked
    if view_button:
        st.subheader("View All DPPs")
        dpps = get_all_dpps(api_base_url)
        if dpps:
            st.write("### DPPs List")
            st.table(dpps)  # Display DPPs in a table format

    # If the "Create New DPP" button is clicked
    if create_button:
        st.subheader("Create a New DPP")
        
        # Input fields for new DPP
        dpp_name = st.text_input("DPP Name", "")
        dpp_description = st.text_area("DPP Description", "")

        # Submit button for creating a new DPP
        if st.button("Submit New DPP"):
            if dpp_name and dpp_description:
                created_dpp = create_dpp(api_base_url, dpp_name, dpp_description)
                if created_dpp:
                    st.json(created_dpp)
            else:
                st.warning("Please enter both a name and description for the DPP.")

