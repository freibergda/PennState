'''Jira Task S8S4-139 User Story: As an Administrator, I want the system to show me a list of 
all the current tables in the BirdSites database, so that I can verify that 
all tables needed to operate the BirdSites database are present.
Acceptance Criteria:
Given: the BirdSites database 
When: The system runs the display_all_tables function
Then: The system displays all of the tables currently in the BirdSites database
Variables: database_name (BirdSites)
Parameters: none'''

import sqlite3
from datetime import datetime
import streamlit as st

def display_all_tables(database_name):
    '''This module will display a list of all the tables in the BirdSites database'''
    # open the sqlite3 database
    try:
        # Making a connection between sqlite3 database and Python Program
        conn = sqlite3.connect(database_name)

        # If sqlite3 makes a connection with python
        # program then it will print "Connected to SQLite"
        # Otherwise it will show errors
        curr_datetime = datetime.now()
        print("Connected to ", database_name, " at: ", curr_datetime)
        
        ############################################################
        #https://cookbook.openai.com/examples/how_to_call_functions_with_chat_models
        def get_table_names(conn):
            """Return a list of table names."""
            table_names = []
            # https://database.guide/2-ways-to-list-tables-in-sqlite-database/
            tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'\
                AND name NOT LIKE 'sqlite_%' Order by name;")
            for table in tables.fetchall():
                table_names.append(table[0])
            return table_names

        def get_column_names(conn, table_name):
            """Return a list of column names."""
            column_names = []
            # PRAGMA https://database.guide/4-ways-to-get-information-about-a-tables-structure-in-sqlite/
            columns = conn.execute(f"PRAGMA table_info('{table_name}');").fetchall()
            for col in columns:
                column_names.append(col[1])
            return column_names

        def get_database_info(conn):
            """Return a list of dicts containing the table name and columns for each table in the database."""
            table_dicts = []
            for table_name in get_table_names(conn):
                columns_names = get_column_names(conn, table_name)
                table_dicts.append({"table_name": table_name, "column_names": columns_names})
            return table_dicts
        database_schema_dict = get_database_info(conn)
        
        ###############################################################
        
        # Set streamlit page variables
        st.set_page_config(layout="wide")
        st.title("BirdSites Database")

        # send it to streamlit
        st.header("List of tables\n")

        # send it to streamlit
        # https://docs.streamlit.io/develop/concepts/design/dataframes
        st.dataframe(database_schema_dict)
        # close the connection
        conn.close()
        curr_datetime = datetime.now()
        print("the sqlite connection for admin functions is closed at:", curr_datetime)

    except sqlite3.Error as error:
        print("Failed to execute the above query", error)
    return

def main():
    '''This is the main module, which will display the structure of the tables
    in the database. (used for testing)'''
    # since this is for testing, the database name is hard-coded
    database_name = "BirdSites.db"
    # display the list of all tables in the database
    display_all_tables(database_name)

if __name__ == "__main__":
    main()
    