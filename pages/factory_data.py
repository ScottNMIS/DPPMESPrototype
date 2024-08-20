import streamlit as st
from fetch_data import fetch_data_from_basyx

def show_factory_data():
    st.title("Factory Data")

    st.subheader("Fetch data from BaSyx AAS Environment")

    default_url = "http://your-basyx-server/?aas=http://your-basyx-server/shells/aHR0cHM6Ly9hY3BsdC5vcmcvUGFydElEX0FGNTY4OTY3OTA&path=http://your-basyx-server/submodels/aHR0cHM6Ly9hY3BsdC5vcmcvVGVzdF9TdWJtb2RlbA/submodel-elements/ExampleCapability"
    endpoint = st.text_input("Enter the BaSyx AAS Environment endpoint", default_url)
    
    if st.button("Fetch Data"):
        st.write(f"Endpoint entered: {endpoint}")
        data = fetch_data_from_basyx(endpoint)
        if data:
            st.json(data)
        else:
            st.write("No data fetched or an error occurred.")

# Function call for testing in standalone mode
if __name__ == "__main__":
    show_factory_data()
