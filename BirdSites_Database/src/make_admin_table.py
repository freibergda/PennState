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
parameters: none 
Associated Requirements: 
Jira Task S8S4-19 The system shall create an administrative file, which will store the logins  
and passwords of authorized administrators in hashed form.''' 
import sqlite3 
 
def make_admin_table(database_name): 
    try: 
        conn = sqlite3.connect(database_name) 
        cursor = conn.cursor() 
        cursor.execute('''CREATE TABLE IF NOT EXISTS administrator_records ( 
                          id INTEGER PRIMARY KEY, 
                          login TEXT NOT NULL, 
                          email TEXT NOT NULL UNIQUE)''') 
        conn.commit() 
    finally: 
        if 'conn' in locals() and conn: 
            conn.close()