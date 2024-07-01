'''locations_groups.py  
Jira Task S8S4-50 User Story: User Story:  As an Administrator, I want to create 
or edit the records in the Locations_Groups table, so that 
I can add to or modify the information stored in the table.
Unit Tests:
System Test:
Acceptance Criteria:
Given:  the BirdSites.db database exists and the Locations_Groups table exists
When: the administrator clicks on the create or modify locations_groups records
Then: then administrator can create or modify records in the Locations_Groups table
Variables: BirdSites.db, locations_groups
Parameters:'''

import sqlite3
import streamlit as st
import pandas as pd

def main():
    # Connect to the SQLite database
    conn = sqlite3.connect(
        r'C:\Users\freib\Desktop\PENN_STATE\SWENG_894_Capstone\BirdSites_Database\BirdSites.db')

    # Perform query and get data into a DataFrame
    query = "SELECT * FROM locations_groups"
    df = pd.read_sql(query, conn)

    st.title("BirdSites Database")
    st.header("Locations_Groups Table")

    with st.form("data_editor_form"):
        st.caption("Edit the dataframe below")
        edited_df = st.data_editor(df,
                                   column_config={
                                       "location_id": "Location_id",
                                       "group_id":"Group_id",
                      
                      #FOREIGN KEY (location_id) REFERENCES locations(location_id),
                      #FOREIGN KEY (group_id) REFERENCES groups(group_id),
                      #PRIMARY KEY (location_id, group_id))
     
                                   },
                                   use_container_width=True,
                                   num_rows="dynamic")

        submitted = st.form_submit_button("Submit")

        if submitted:
            # Update the database with the edited DataFrame
            edited_df.to_sql('locations_groups', conn,
                             if_exists='replace', index=False)
            st.success("Database successfully updated!")

    # Close the database connection
    conn.close()


if __name__ == "__main__":
    main()
