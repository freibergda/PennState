'''This module creates the BirdSites database'''

import sqlite3


def create_birdsites():
    '''Create the database if it doesn't exist'''
    # database name
    database_name = "BirdSites.db"

    try:
        conn = sqlite3.connect(database_name)
        print("Database BirdSites.db created.")
    except sqlite3.Error as error:
        # database already exists or some other error occurred
        print(error, "Database BirdSites.db not created.")
    finally:
        # This will always execute.  If connection is open, close it
        if conn:
            # using close() method, close the connection
            conn.close()
            print("the sqlite connection is closed")
    return
