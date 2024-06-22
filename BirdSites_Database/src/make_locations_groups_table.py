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

def make_locations_groups_table(database_name):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS locations_groups (
                      location_id INTEGER,
                      group_id INTEGER,
                      FOREIGN KEY (location_id) REFERENCES locations(location_id),
                      FOREIGN KEY (group_id) REFERENCES groups(group_id),
                      PRIMARY KEY (location_id, group_id))''')
    conn.commit()
    conn.close()