'''app.py
Jira Task S8S4-67  User Story:  As an Administrator, I want 
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
selection.'''

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
