import streamlit as st
import uuid

def generate_unique_code():
    return str(uuid.uuid4())

def show_create_dpp_page():
    st.title("Create Digital Product Passport")
    
    st.write("Fill in the following information to create a new Digital Product Passport:")
    
    product_name = st.text_input("Product Name")
    manufacturer = st.text_input("Manufacturer")
    production_date = st.date_input("Production Date")
    description = st.text_area("Product Description")
    
    if st.button("Create DPP"):
        if product_name and manufacturer:
            unique_code = generate_unique_code()
            dpp_data = {
                "unique_code": unique_code,
                "product_name": product_name,
                "manufacturer": manufacturer,
                "production_date": str(production_date),
                "description": description
            }
            st.session_state['dpp_data'] = dpp_data
            st.success(f"DPP created successfully! Unique Code: {unique_code}")
            st.info("You can now use this code to access the DPP via the 'Scan QR Code' page.")
        else:
            st.error("Please fill in at least the Product Name and Manufacturer fields.")

if __name__ == "__main__":
    show_create_dpp_page()