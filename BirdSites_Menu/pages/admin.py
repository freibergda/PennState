'''Jira Task S8S4-67 
menu calling the various admin capabilities 
from the BirdSites_Database'''
import importlib.util
import os
import sys
import streamlit as st
from menu import menu_with_redirect

# Add BirdSites_Database/src and BirdSites_Maintain_Database/src to the system path
sys.path.insert(0, r"C:/Users/freib/Desktop/PENN_STATE/SWENG_894_Capstone/BirdSites_Database/src")
sys.path.insert(0, r"C:/Users/freib/Desktop/PENN_STATE/SWENG_894_Capstone/BirdSites_Maintain_Database/src")

import display_birdsites_database_tables
import locations
import groups
import locations_groups

def display_structure():
    '''Display BirdSites_Database/src main'''
    main_py_path = (
        r"C:/Users/freib/Desktop/PENN_STATE/SWENG_894_Capstone/BirdSites_Database/src/main.py")
    if not os.path.exists(main_py_path):
        st.error(f"The path '{main_py_path}' does not exist.")
        st.stop()

    spec = importlib.util.spec_from_file_location("main", main_py_path)
    if spec is None or spec.loader is None:
        st.error(f"Unable to find the module at '{main_py_path}'.")
        st.stop()

    structure = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(structure)
    structure.main()

def location_records():
    '''Create/modify BirdSites_Database location records'''
    locations.main()

def group_records():
    '''Create/modify BirdSites_Database group records'''
    groups.main()

def location_group_records():
    '''Create/modify BirdSites_Database locations_groups records'''
    locations_groups.main()

def administrator_menu():
    ''' Show a navigation menu for authenticated users'''
    task = st.sidebar.selectbox("Select a task", [
        "Display Database Structure",
        "Create/modify Location Records",
        "Create/modify Group Records",
        "Create/modify Location_Group Records",
    ], index=0)

    if task == "Display Database Structure":
        display_structure()
    elif task == "Create/modify Location Records":
        location_records()
    elif task == "Create/modify Group Records":
        group_records()
    elif task == "Create/modify Location_Group Records":
        location_group_records()

menu_with_redirect()

if st.session_state.role not in ["admin", "super-admin"]:
    st.warning("You do not have permission to view this page.")
    st.stop()

st.title("This page is only available to admins and super-admins")
st.markdown(
    f"You are currently logged in with the role of {st.session_state.role}."
)

administrator_menu()