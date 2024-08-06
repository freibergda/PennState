'''Jira Task S8S4-67  User Story:  As an Administrator, I want 
to either view the BirdSites database structure or 
create/modify records in the BirdSites database.  Alternatively,
as a Administrator or User, I want to access the User menu.
Unit Tests: 
System Test:
Acceptance Criteria:  The menus function correctly and 
either display the database structure, allow the 
administrator to create or modify records.  Alternatively, 
the system will allow the Administrator or User to access 
the User menu.

Given:  The BirdSites database exists, has tables loaded 
and the individual has an admin login.  Alternatively, 
the individual has a user login.

When:  The menu app is activated, the user logs in, and
the system selects the available actions based on the login 
(administrator or user).

Then:  Based on the login role, the administrator is presented 
with the choice of either seeing the display of the BirdSites database structure 
or of then creating/modifying records in the BirdSites 
database. The administrator or the user is presented with 
the BirdSites database with selection options.

Variables: link to the locations where the code that displays 
the BirdSites database structure, the code that allows 
the creating/modifying of records in the BirdSites database, 
or the code that presents the BirdSites database for user 
selection.

Jira Task S8S4-4 User Story:  As an Administrator, I want to create or modify an administrator 
access the secrets file in the system .streamlit folder to grant 
myself or others Administrator access.
Acceptance Criteria
Given: the BirdSites.db database exists with a system folder called .streamlit
When: an administrator enters a login and password into the .streamlit/secrets file
Then: a record has been created or modified in the .streamlit/secrets file
variables: database_name = BirdSites.db
parameters: none'''

import streamlit as st
# https://docs.streamlit.io/knowledge-base/deploy/authentication-without-sso
# https://www.geeksforgeeks.org/what-is-hmachash-based-message-authentication-code/

import hmac

st.set_page_config(
page_title = 'BirdSites Database',
page_icon = '✅',
layout = 'wide'
)   

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
                    # Don't store the username or password.
                    del st.session_state["password"]
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
                # st.error("User not known or password incorrect")
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
