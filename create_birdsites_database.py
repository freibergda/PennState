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
        curr_datetime = datetime.now()
        conn.close()
        print("the sqlite connection is closed",curr_datetime)
    except sqlite3.Error as error:
        # database already exists or some other error occurred
        curr_datetime = datetime.now()
        print(error, "Database BirdSites.db not created.",curr_datetime )

    return database_name
