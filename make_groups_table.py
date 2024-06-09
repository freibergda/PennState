'''Jira Task S8S4-49 User Story: As an Administrator, I want the system to create a table called 
the Groups table in the BirdSites database, so that every record in the table 
will contain the following columns:
a. groups table primary key
b. spring migration
c. fall migration
d. summer
e. winter
f. Atlantic flyway
g. Pacific flyway 
Acceptance Criteria
Given:  the BirdSites.db database exists and the Groups table does not exist
When:  the system runs the make_groups_table function
Then: the Groups table has been created in the  BirdSites.db database 
variables: database_name
parameters: none'''

import sqlite3
from datetime import datetime

def make_groups_table(database_name):
    '''This module will create the groups table in the BirdSites database'''
    # call sqlite3 and attempt to create table
    try:

        con = sqlite3.connect(database_name)
        cur = con.cursor()
        cur.execute("CREATE TABLE if not exists groups(pk_grp INTEGER PRIMARY KEY AUTOINCREMENT,\
                    spring_migration TEXT, fall_migration TEXT, summer TEXT, \
                    winter TEXT, atlantic_flyway TEXT, pacific_flyway TEXT)")
        con.commit()
        con.close()
        curr_datetime = datetime.now()
        print("The SQLite connection table groups is closed at: ", curr_datetime)

    except sqlite3.Error as error:
        curr_datetime = datetime.now()
        print("Error while connecting to SQLite make_groups_table ",
              error, curr_datetime)

    return
