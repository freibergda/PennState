'''This module will create the locations table in the BirdSites database'''
import sqlite3


def make_locations_table(database_name):
    '''this module creates the locations table'''
    # call sqlite3
    try:
        #con = sqlite3.connect("BirdSites.db")
        con = sqlite3.connect(database_name)
        cur = con.cursor()
        cur.execute("CREATE TABLE if not exists locations(pk_loc INTEGER PRIMARY KEY,\
                    loc_full_name TEXT NOT NULL, county_name TEXT, state_name TEXT NOT NULL, geolocation REAL,\
                    linkToNWSSite TEXT, linkToParkWebSite TEXT, linkToeBirdSite TEXT,\
                    linkToBirdCastSite TEXT)")
        con.commit()
        con.close()
        print("The SQLite connection is closed")

    except sqlite3.Error as error:
        print("Error while connecting to SQLite, make_locations_table", error)

    return
