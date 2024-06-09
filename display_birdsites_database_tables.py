'''Jira S8S4-139: As an Administrator, I want the system to show me a list of 
all the current tables in the BirdSites database, so that I can verify that 
all tables needed to operate the BirdSites database are present.'''
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

        # Getting a list of all tables from sqlite_schema, don't include sqlite internal tables
        # https://database.guide/2-ways-to-list-tables-in-sqlite-database/
        sql_query = """SELECT name FROM sqlite_schema 
                    WHERE type = ('table') 
                    AND name NOT LIKE 'sqlite_%'
                    ORDER BY name;"""

        # Creating cursor object using connection object
        cursor = conn.cursor()

        # executing our sql query
        cursor.execute(sql_query)

        # send it to streamlit
        st.header("List of tables\n")

        # printing a list of all current tables
        list_tables = (cursor.fetchall())
        # testing what it looks like in print
        print(list_tables)
        # send it to streamlit
        # add header
        # https://docs.streamlit.io/develop/api-reference/data/st.table
        #st.table(list_tables) - this works but has index on both sides 
        #st.write(list_tables) - that didn't work (list type from db)
        # https://docs.streamlit.io/develop/concepts/design/dataframes
        st.dataframe(list_tables) # this also works and has only top blank
        # close the connection
        conn.close()
        curr_datetime = datetime.now()
        print("the sqlite connection for admin functions is closed at:", curr_datetime)

    except sqlite3.Error as error:
        print("Failed to execute the above query", error)
    return
