import streamlit as st
import requests
from beauhurst_api import get_company_data

def show_company_info():
    st.title("Company Information")

    beauhurst_api_key = st.text_input("Enter your Beauhurst API key", type="password")
    company_id = st.text_input("Enter the company ID")

    if st.button("Get Company Info"):
        if beauhurst_api_key and company_id:
            with st.spinner("Fetching company information..."):
                response = get_company_data(beauhurst_api_key, company_id)
                
                if response.status_code == 200:
                    company_data = response.json().get('results', [{}])[0]
                    display_company_info(company_data)
                else:
                    st.error(f"API call failed with status code {response.status_code}")
                    st.text(response.text)
        else:
            st.error("Please provide all required inputs.")

def display_company_info(company_data):
    st.markdown(f"## {company_data.get('name', 'Company Information')}")
    
    if company_data.get('basic'):
        st.markdown("### Basic Information")
        st.write(f"**Registered Name:** {company_data['basic'].get('registered_name', 'N/A')}")
        st.write(f"**Companies House ID:** {company_data['basic'].get('companies_house_id', 'N/A')}")
        st.write(f"**Website:** {company_data['basic'].get('website', 'N/A')}")
        st.write(f"**Beauhurst URL:** {company_data['basic'].get('beauhurst_url', 'N/A')}")
        
        ultimate_parent = company_data['basic'].get('ultimate_parent_company', {})
        if ultimate_parent.get('name'):
            st.write(f"**Ultimate Parent Company Name:** {ultimate_parent.get('name', 'N/A')}")
            st.write(f"**Ultimate Parent Company ID:** {ultimate_parent.get('companies_house_id', 'N/A')}")

    if company_data.get('classification'):
        st.markdown("### Classification")
        classification_info = company_data['classification']
        if classification_info.get('buzzwords'):
            st.write(f"**Buzzwords:** {', '.join(classification_info.get('buzzwords', []))}")

    if company_data.get('contact_information'):
        st.markdown("### Contact Information")
        contact_info = company_data['contact_information']
        if contact_info.get('address'):
            st.write(f"**Address:** {contact_info.get('address', 'N/A')}")
        if contact_info.get('postcode'):
            st.write(f"**Postcode:** {contact_info.get('postcode', 'N/A')}")
        if contact_info.get('telephone'):
            st.write(f"**Telephone:** {contact_info.get('telephone', 'N/A')}")
        if contact_info.get('emails'):
            st.write(f"**Email:** {', '.join(contact_info.get('emails', []))}")

    if company_data.get('financials'):
        st.markdown("### Financials")
        financials = company_data['financials']
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Turnover:** {financials.get('turnover', 'N/A')}")
            st.write(f"**EBITDA:** {financials.get('ebitda', 'N/A')}")
            st.write(f"**Total Assets:** {financials.get('total_assets', 'N/A')}")
            st.write(f"**Cash:** {financials.get('cash', 'N/A')}")
        with col2:
            st.write(f"**Total Liabilities:** {financials.get('total_liabilities', 'N/A')}")
            st.write(f"**Net Assets:** {financials.get('net_assets', 'N/A')}")
            st.write(f"**Research & Development:** {financials.get('research_and_development', 'N/A')}")
            st.write(f"**Export:** {financials.get('export', 'N/A')}")

    if company_data.get('social_media'):
        st.markdown("### Social Media")
        social_media = company_data['social_media']
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"**Twitter:** {social_media.get('twitter_handle', 'N/A')}")
            st.write(f"**Instagram:** {social_media.get('instagram_handle', 'N/A')}")
        with col2:
            st.write(f"**LinkedIn:** {social_media.get('linkedin_url', 'N/A')}")
        with col3:
            st.write(f"**Facebook:** {social_media.get('facebook_url', 'N/A')}")
            st.write(f"**Pinterest:** {social_media.get('pinterest_handle', 'N/A')}")

    if company_data.get('transactions'):
        st.markdown("### Transactions")
        transactions = company_data['transactions']
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Number of Fundraisings:** {transactions.get('n_fundraisings', 'N/A')}")
            st.write(f"**Total Amount Raised:** {transactions.get('total_amount_fundraisings', 'N/A')}")
        with col2:
            st.write(f"**Number of Grants:** {transactions.get('n_grants', 'N/A')}")
            st.write(f"**Total Amount of Grants:** {transactions.get('total_amount_grants', 'N/A')}")

if __name__ == "__main__":
    show_company_info()
