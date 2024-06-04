'''This module creates the BirdSites database'''

import sqlite3
from datetime import datetime

def create_birdsites():
    '''Create the database if it doesn't exist'''
    # database name
    database_name = "BirdSites.db"

    try:
        conn = sqlite3.connect(database_name)
        # Getting current date/time to confirm creation
        curr_datetime = datetime.now()
        print("Database ",database_name," created.",curr_datetime)
    except sqlite3.Error as error:
        # database already exists or some other error occurred
        curr_datetime = datetime.now()
        print(error, "Database BirdSites.db not created.",curr_datetime )
    finally:
        # This will always execute.  If connection is open, close it
        curr_datetime = datetime.now()
        if conn:
            # using close() method, close the connection
            conn.close()
            print("the sqlite connection is closed",curr_datetime)
        else:
            print(curr_datetime)
    return database_name
