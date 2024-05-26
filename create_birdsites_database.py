'''This module creates the BirdSites database'''

import sqlite3


def create_birdsites():
    '''Create the database if it doesn't exist'''
    # database name
    database_name = "BirdSites.db"

    try:
        conn = sqlite3.connect(database_name)
        print("Database BirdSites.db created.")
        conn.close()
    except sqlite3.Error as error:
        # database already exists or some other error occurred
        print(error,"Database BirdSites.db not created.")

    return
