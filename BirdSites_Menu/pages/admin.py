'''Jira Task S8S4-67 
menu calling the various admin capabilities 
from the BirdSites_Database'''
import importlib.util
import os
import sys  # Add this line
import streamlit as st
from menu import menu_with_redirect

# Add the src directory to the system path
sys.path.insert(0, "C:/Users/freib/Desktop/PENN_STATE/SWENG_894_Capstone/BirdSites_Database/src")

def administrator_menu():
    ''' Show a navigation menu for authenticated users'''
    st.sidebar.selectbox("Select role", options=["Switch accounts", "Your profile", 
                                                 "Display Database Structure",
                                                 "Create/modify Location Records", 
                                                 "Create/modify Group Records", 
                                                 "Create/modify Location_Group Records",], index=0)

# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()

# Verify the user's role
if st.session_state.role not in ["admin", "super-admin"]:
    st.warning("You do not have permission to view this page.")
    st.stop()

st.markdown(f"You are currently logged with the role of {st.session_state.role}.")

# Verify that the main.py path is correct
main_py_path = "C:/Users/freib/Desktop/PENN_STATE/SWENG_894_Capstone/BirdSites_Database/src/main.py"
if not os.path.exists(main_py_path):
    st.error(f"The path '{main_py_path}' does not exist.")
    st.stop()

# Pass the file name and path as argument
spec = importlib.util.spec_from_file_location("main", main_py_path)
if spec is None or spec.loader is None:
    st.error(f"Unable to find the module at '{main_py_path}'.")
    st.stop()

# Importing the module as structure
structure = importlib.util.module_from_spec(spec)
spec.loader.exec_module(structure)

# Calling the main function of main.py
structure.main()