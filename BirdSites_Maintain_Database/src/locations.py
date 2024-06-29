'''locations.py  
Jira Task S8S4-8 User Story: As an Administrator, I want to create or edit the records in the Locations table so that I can add to or modify the information stored in the table.
Acceptance Criteria:
Given:  the BirdSites.db database exists and the Locations table exists
When: the administrator clicks on the create or modify locations records 
Then: then administrator can create or modify records in the Locations table
Variables: database name, database location
Parameters:'''

import sqlite3
import streamlit as st
import pandas as pd


def main():
    # Connect to the SQLite database
    conn = sqlite3.connect(
        r'C:\Users\freib\Desktop\PENN_STATE\SWENG_894_Capstone\BirdSites_Database\BirdSites.db')

    # Perform query and get data into a DataFrame
    query = "SELECT * FROM locations"
    df = pd.read_sql(query, conn)

    st.title("BirdSites Database")
    st.header("Locations Table")

    with st.form("data_editor_form"):
        st.caption("Edit the dataframe below")
        edited_df = st.data_editor(df,
                                   column_config={
                                       "location_id": "ID",
                                       "location_full_name": "Full Location Name",
                                       "county": "Full County Name",
                                       "state_full": "Full State Name",
                                       "geographic_coordinates": st.column_config.NumberColumn("Geo Coords"),
                                       "link_to_NWS": st.column_config.LinkColumn("NWS Link"),
                                       "link_to_park": st.column_config.LinkColumn("Park Link"),
                                       "link_to_eBird": st.column_config.LinkColumn("eBird Link"),
                                       "link_to_BirdCast": st.column_config.LinkColumn("BirdCast Link"),
                                   },
                                   use_container_width=True,
                                   num_rows="dynamic")

        submitted = st.form_submit_button("Submit")

        if submitted:
            # Update the database with the edited DataFrame
            edited_df.to_sql('locations', conn,
                             if_exists='replace', index=False)
            st.success("Database successfully updated!")

    # Close the database connection
    conn.close()


if __name__ == "__main__":
    main()
