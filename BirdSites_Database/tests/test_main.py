# test_main.py
from src.display_birdsites_database_tables import display_all_tables

def main():
    import streamlit as st
    st.title("Bird Sites Database")
    st.header("Overview")
    st.subheader("Details")
    database_name = 'BirdSites.db'
    display_all_tables(database_name)