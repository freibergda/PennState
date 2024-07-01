'''groups.py  
Jira Task S8S4-16 User Story: As an Administrator, I want to create or edit 
the records in the Groups table so that I can add to or 
modify the information stored in the table.
Acceptance Criteria:
Given:  the BirdSites.db database exists and the Groups table exists
When: the administrator clicks on the create or modify groups records 
Then: then administrator can create or modify records in the Groups table
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
    query = "SELECT * FROM groups"
    df = pd.read_sql(query, conn)

    st.title("BirdSites Database")
    st.header("Groups Table")

    with st.form("data_editor_form"):
        st.caption("Edit the dataframe below")
        edited_df = st.data_editor(df,
                                   column_config={
                                       "group_id": "ID",
                                       "spring_migration": "Spring Migration",
                                       "fall_migration": "Fall Migration",
                                       "summer": "Summer Season",
                                       "winter": "Winter Season",
                                       "atlantic_flyway": "Atlantic Fkyway",
                                       "pacific_flyway": "Pacific Flyway",
                                   },
                                   use_container_width=True,
                                   num_rows="dynamic")

        submitted = st.form_submit_button("Submit")

        if submitted:
            # Update the database with the edited DataFrame
            edited_df.to_sql('groups', conn,
                             if_exists='replace', index=False)
            st.success("Database successfully updated!")

    # Close the database connection
    conn.close()


if __name__ == "__main__":
    main()
