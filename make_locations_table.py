'''Jira Task S8S4-15 User Story:  As an Administrator, I want the system to create a table called 
the Locations table in the BirdSites database, so that every record in the 
table will contain the following columns:
a.       location table primary key
b.       location full name
c.       county
d.       state
e.       geographic coordinates
f.       link to NWS nearest site
g.       link to park website
h.       link to the eBird site specific to the location
i.       link to the BirdCast site specific to the location
Acceptance Criteria
Given:  the BirdSites.db database exists and the Locations table does not exist
When:  the system runs the make_location_table module
Then: the locations table is created in the BirdSites.db database
variables: database_name
parameters: none'''

import sqlite3
from datetime import datetime

def make_locations_table(database_name):
    '''This module will create the locations table in the BirdSites database'''
    # call sqlite3 and attempt to create table
    try:

        con = sqlite3.connect(database_name)
        cur = con.cursor()
        cur.execute("CREATE TABLE if not exists locations(pk_loc INTEGER PRIMARY KEY AUTOINCREMENT,\
                    loc_full_name TEXT NOT NULL UNIQUE, county_name TEXT, state_name TEXT NOT NULL, geolocation REAL,\
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
