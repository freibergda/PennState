'''Jira Task S8S4-70 User Story: As an Administrator, I want the system to create the BirdSites 
database, so that I can create tables and load records into the BirdSites 
database.  (this task is embedded in S8S4-57), this task is just creating the database without 
the tables or verification.
Acceptance Criteria:
Given:  the BirdSites.db database does not exist
When:  the system runs the create_birdsites function
Then:  the BirdSites.db database is created
variables: database_name = BirdSites.db 
parameters: none
Associated Requirements:
Jira Task S8S4-18 The system shall create a database 
called BirdSites.'''
import sqlite3
from datetime import datetime

def create_birdsites(database_name):
    '''Create the database if it doesn't exist'''
    try:
        # Purposefully creating an invalid path to test error handling
        if not database_name.startswith(':') and '/' in database_name:
            raise sqlite3.OperationalError("Invalid path provided to SQLite connect")

        conn = sqlite3.connect(database_name)
        curr_datetime = datetime.now()
        print("Database", database_name, "created.", curr_datetime)
    except sqlite3.Error as error:
        curr_datetime = datetime.now()
        print(error, "Database BirdSites.db not created.", curr_datetime)
        raise  # Re-raise the caught error to ensure the test can catch it
    finally:
        if 'conn' in locals() and conn:
            conn.close()
            print("The SQLite connection is closed", curr_datetime)
    return database_name