from dataclasses import asdict
from streamlit_keycloak import login
import streamlit as st

def show_keycloak_test():
    st.title("Streamlit Keycloak Example")

    keycloak = login(
        url="https://<your-keycloak-server-url>/auth",
        realm="<your-realm-name>",
        client_id="<your-client-id>",
    )

    if keycloak.authenticated:
        st.subheader(f"Welcome {keycloak.user_info['preferred_username']}!")
        st.write("Here is your user information:")
        st.write(asdict(keycloak))
    else:
        st.error("Not logged in")
        if st.button("Login"):
            st.experimental_rerun()

if __name__ == "__main__":
    show_keycloak_test()
