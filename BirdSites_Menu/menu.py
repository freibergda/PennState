'''menu.py  Jira Task S8S4-67'''
import streamlit as st
# https://docs.streamlit.io/knowledge-base/deploy/authentication-without-sso
# https://www.geeksforgeeks.org/what-is-hmachash-based-message-authentication-code/

import hmac

def authenticated_menu():
    # Show a navigation menu for authenticated users
    st.sidebar.page_link("pages/admin.py", label="Database Administrator")
    st.sidebar.page_link("pages/user.py", label="User")

def unauthenticated_menu():
    '''Show a navigation menu for unauthenticated users'''
    if "role" not in st.session_state or st.session_state.role is None:
        def check_password():
            """Returns `True` if the user had a correct password."""

            def login_form():
                """Form with widgets to collect user information"""
                with st.form("Credentials"):
                    st.text_input("Username", key="username")
                    st.text_input("Password", type="password", key="password")
                    st.form_submit_button("Log in", on_click=password_entered)

            def password_entered():
                """Checks whether a password entered by the user is correct."""
                if st.session_state["username"] in st.secrets[
                    "passwords"
                ] and hmac.compare_digest(
                    st.session_state["password"],
                    st.secrets.passwords[st.session_state["username"]],
                ):
                    st.session_state["password_correct"] = True
                    del st.session_state["password"]  # Don't store the username or password.
                    del st.session_state["username"]
                else:
                    st.session_state["password_correct"] = False

            # Return True if the username + password is validated.
            if st.session_state.get("password_correct", False):
                st.session_state.role = "admin"

                authenticated_menu()
                # invalid but left for structure
                return True

            # Show inputs for username + password.
            login_form()
            if "password_correct" in st.session_state:
                #st.error("User not known or password incorrect")
                st.session_state.role = "user"              
                return False

        if not check_password():
            st.stop()
    
def menu():
    '''Determine if a user is logged in or not, then show the correct
    navigation menu'''
    if "role" not in st.session_state or st.session_state.role is None:
        unauthenticated_menu()
        return
    authenticated_menu()

def menu_with_redirect():
    '''Redirect users to the main page if not logged in, otherwise continue to
    render the navigation menu'''
    menu()
    if "role" not in st.session_state or st.session_state.role is None:
        st.switch_page("app.py")