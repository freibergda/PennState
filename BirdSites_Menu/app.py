'''app.py
Jira Task S8S4-67  User Story:  As an Administrator, I want 
to either view the BirdSites database structure or 
create/modify records in the BirdSites database.  
Unit Tests: 
System Test:
Acceptance Criteria:  The menus function correctly and 
either display the database structure or allow the 
administrator to create or modify records.
Given:  The BirdSites database exists, has tables loaded 
and the individual has an admin login.
When:  The menu app is activated and admin functions are 
selected.
Then:  The administrator is presented with the choice of 
either seeing the display of the BirdSites database structure 
or of creating/modifying records in the BirdSites database.
Variables: link to the locations where the code that displays 
the BirdSites database structure or the code that allows 
the creating/modifying of records in the BirdSites database.'''

# https://docs.streamlit.io/develop/tutorials/multipage/st.page_link-nav
import streamlit as st
from menu import menu

# Initialize st.session_state.role to None
if "role" not in st.session_state:
    st.session_state.role = None

# Retrieve the role from Session State to initialize the widget
st.session_state._role = st.session_state.role


def set_role():
    # Callback function to save the role selection to Session State
    st.session_state.role = st.session_state._role


st.title('BirdSites Database')

menu()  # Render the dynamic menu
