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
            tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
            for table in tables.fetchall():
                table_names.append(table[0])
            print(table_names)
            return table_names

        def get_column_names(conn, table_name):
            """Return a list of column names."""
            column_names = []
            columns = conn.execute(f"PRAGMA table_info('{table_name}');").fetchall()
            for col in columns:
                column_names.append(col[1])
            print(column_names)
            return column_names

        def get_database_info(conn):
            """Return a list of dicts containing the table name and columns for each table in the database."""
            table_dicts = []
            for table_name in get_table_names(conn):
                columns_names = get_column_names(conn, table_name)
                table_dicts.append({"table_name": table_name, "column_names": columns_names})
            print(table_dicts)
            return table_dicts
        database_schema_dict = get_database_info(conn)
        database_schema_string = "\n".join(
            [
                f"Table: {table['table_name']}\nColumns: {', '.join(table['column_names'])}"
                for table in database_schema_dict
            ]
        )
        print(database_schema_dict) 
        print(database_schema_string)
        ###############################################################
        
        # Set streamlit page variables
        st.set_page_config(layout="wide")
        st.title("BirdSites Database")

        # send it to streamlit
        st.header("List of tables\n")

        # printing a list of all current tables
#        list_tables = (cursor.fetchall())
        # testing what it looks like in print
#        print(list_tables)
        # send it to streamlit
        # https://docs.streamlit.io/develop/concepts/design/dataframes
        #st.dataframe(list_tables)  # this also works and has only top blank
        st.dataframe(database_schema_string)
        # close the connection
        conn.close()
        curr_datetime = datetime.now()
        print("the sqlite connection for admin functions is closed at:", curr_datetime)

    except sqlite3.Error as error:
        print("Failed to execute the above query", error)
    return
