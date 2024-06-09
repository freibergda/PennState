'''Jira S8S4-15 This module will create the locations table in the BirdSites database'''
import sqlite3
from datetime import datetime

def make_locations_table(database_name):
    '''this module creates the locations table'''
    # call sqlite3
    try:

        con = sqlite3.connect(database_name)
        cur = con.cursor()
        cur.execute("CREATE TABLE if not exists locations(pk_loc INTEGER PRIMARY KEY AUTOINCREMENT,\
                    loc_full_name TEXT NOT NULL, county_name TEXT, state_name TEXT NOT NULL, geolocation REAL,\
                    linkToNWSSite TEXT, linkToParkWebSite TEXT, linkToeBirdSite TEXT,\
                    linkToBirdCastSite TEXT)")
        con.commit()
        con.close()
        curr_datetime = datetime.now()        
        print("The SQLite connection table locations is closed at: ", curr_datetime)

    except sqlite3.Error as error:
        curr_datetime = datetime.now()
        print("Error while connecting to SQLite, make_locations_table at: ", error, curr_datetime)

    return
