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

def make_locations_table(database_name):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS locations (
                      location_id INTEGER PRIMARY KEY,
                      location_full_name TEXT NOT NULL,
                      county TEXT,
                      state_full TEXT,
                      geographic_coordinates INTEGER,
                      link_to_NWS TEXT,
                      link_to_park TEXT,
                      link_to_eBird TEXT,
                      link_to_BirdCast)''')
    conn.commit()
    conn.close()
