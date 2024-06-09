'''Jira Task S8S4-17 User Story:  As an Administrator, I want the system to 
create a table called the locations_groups table in the BirdSites database, 
so that every record in the table will contain the following columns:
a.  a locations_groups primary key
b.  the primary key of the Locations table as a foreign key,
c.  the primary key of matching records in the Groups table as a foreign key 
Acceptance Criteria
Given: the BirdSites.db database exists and the Locations_Groups table does not exist
When: the system runs the make_locations_groups_table function 
Then: the locations_groups table has been created in the BirdSites.db database
variables: database _name
parameters: none'''

import sqlite3
from datetime import datetime

def make_locations_groups_table(database_name):
    '''this module creates the locations_groups table, 
    joining the many-to-many relationship between the locations and groups tables'''
    # call sqlite3 and attempt to create table
    try:

        con = sqlite3.connect(database_name)
        cur = con.cursor()
        cur.execute("CREATE TABLE if not exists locations_groups(pk_loc_grp INTEGER PRIMARY KEY AUTOINCREMENT,\
                    loc_id INTEGER,\
                    grp_id INTEGER,\
                    FOREIGN KEY(loc_id) REFERENCES locations(pk_loc),\
                    FOREIGN KEY(grp_id) REFERENCES groups(pk_grp))")
        con.commit()
        con.close()
        curr_datetime = datetime.now()
        print("The SQLite connection table locations_groups is closed at: ", curr_datetime)

    except sqlite3.Error as error:
        curr_datetime = datetime.now()
        print("Error while connecting to SQLite make_groups_table ", error, curr_datetime)

    return
