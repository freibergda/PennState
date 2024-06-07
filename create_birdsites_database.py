'''This module creates the BirdSites database'''

import sqlite3


def create_birdsites():
    '''Create the database if it doesn't exist'''
    # database name
    database_name = "BirdSites.db"
    # Initialize the connection variable

    try:
        conn = sqlite3.connect(database_name)
        print("Database BirdSites.db created or opened.")
        ######################
        # just for testing out
        # list all tables
        sql_query = """SELECT name FROM sqlite_master  
        WHERE type='table';"""
        cursor = conn.cursor()
        cursor.execute(sql_query)
        print(cursor.fetchall())
        #########################
        conn.close()
        print("the sqlite connection is closed")
    except sqlite3.Error as error:
        # database already exists or some other error occurred
        print(error, "Database BirdSites.db not created.")

    return database_name
