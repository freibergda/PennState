'''Jira Task S8S4-70 User Story: As an Administrator, I want the system to create the BirdSites 
database, so that I can create tables and load records into the BirdSites 
database
Acceptance Criteria
Given:  the BirdSites.db database does not exist
When:  the system runs the create_birdsites function
Then:  the BirdSites.db database is created
variables: database_name = BirdSites.db 
parameters: none'''
import sqlite3
from datetime import datetime

def create_birdsites(database_name):
    '''Create the database if it doesn't exist'''

    try:
        conn = sqlite3.connect(database_name)
        curr_datetime = datetime.now()
        print("Database", database_name, "created.", curr_datetime)
        conn.close()
        print("The SQLite connection is closed", curr_datetime)
    except sqlite3.Error as error:
        curr_datetime = datetime.now()
        print(error, "Database BirdSites.db not created.", curr_datetime)

    return database_name
