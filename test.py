from dataclasses import asdict
from streamlit_keycloak import login
import streamlit as st


def main():
    st.subheader(f"Welcome {keycloak.user_info['preferred_username']}!")
    st.write(f"Here is your user information:")
    st.write(asdict(keycloak))


st.title("Streamlit Keycloak example")
keycloak = login(
    url="http://localhost:8080",
    realm="myrealm",
    client_id="myclient",
)

if keycloak.authenticated:
    main()