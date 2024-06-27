'''main.py  
Jira Task S8S4-8 User Story: As an Administrator, I want to create or edit the records in the Locations table so that I can add to or modify the information stored in the table.
Acceptance Criteria:
Given:  the BirdSites.db database exists and the Locations table exists
When: the administrator clicks on the create or modify locations records 
Then: then administrator can create or modify records in the Locations table
Variables: database name, database location
Parameters:'''

import streamlit as st
import sqlite3
import pandas as pd

def main():
    # Connect to the SQLite database
    conn = sqlite3.connect(r'C:\Users\freib\Desktop\PENN_STATE\SWENG_894_Capstone\BirdSites_Database\BirdSites.db')
    # Perform query and get data into a DataFrame
    query = "SELECT * FROM locations"
    df = pd.read_sql(query, conn)
    # Close the database connection
    conn.close()
    # Display the DataFrame in Streamlit
    st.dataframe(df)

if __name__ == "__main__":
    main()
