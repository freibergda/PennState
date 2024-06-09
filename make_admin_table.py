'''Jira Task S8S4-131 User Story:  As an Administrator, I want the system to 
create a table called the administrator_records table, so that every record 
in the table contains:
a.  a primary key
b.  an administrator login
c.  an administrator email address
Acceptance Criteria
Given:  the BirdSites.db database exists, but does not have the 
administrator_records table
When:  the system runs the make_admin_table function 
Then:  the administrator_records table has been added to the BirdSites database
variables: database_name
parameters: none'''

import sqlite3
from datetime import datetime

def make_admin_table(database_name):
    '''This module will create the administrator_records table in the BirdSites database'''
    # call sqlite3 and attempt to create table
    try:

        con = sqlite3.connect(database_name)
        cur = con.cursor()
        cur.execute("CREATE TABLE if not exists administrator_records(pk_admin INTEGER PRIMARY KEY AUTOINCREMENT,\
                    administrator_login TEXT UNIQUE, administrator_email TEXT UNIQUE)")    
        con.commit()
        con.close()
        curr_datetime = datetime.now()
        print("The SQLite connection table administrator_records is closed at: ", curr_datetime)

    except sqlite3.Error as error:
        curr_datetime = datetime.now()
        print("Error while connecting to SQLite make_admin_table ",
              error, curr_datetime)

    return    