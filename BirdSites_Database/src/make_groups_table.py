'''Jira Task S8S4-49 User Story: As an Administrator, I want the system to create a table called  
the Groups table in the BirdSites database, so that every record in the table  
will contain the following columns: 
a. groups table primary key 
b. spring migration 
c. fall migration 
d. summer 
e. winter 
f. Atlantic flyway 
g. Central flyway 
h. Pacific flyway  
Acceptance Criteria 
Given:  the BirdSites.db database exists and the Groups table does not exist 
When:  the system runs the make_groups_table function 
Then: the Groups table has been created in the  BirdSites.db database  
variables: database_name 
parameters: none 
Associated Requirements: 
Jira Task S8S4-23 The system shall create a Groups Table,  
which will be filled by an administrator.''' 
 
import sqlite3 
 
def make_groups_table(database_name): 
    try: 
        conn = sqlite3.connect(database_name) 
        cursor = conn.cursor() 
        cursor.execute('''CREATE TABLE IF NOT EXISTS groups ( 
                          group_id INTEGER PRIMARY KEY, 
                          spring_migration TEXT, 
                          fall_migration TEXT, 
                          summer TEXT, 
                          winter TEXT, 
                          atlantic_flyway, 
                          central_flyway, 
                          pacific_flyway)''') 
        conn.commit() 
    finally: 
        if 'conn' in locals() and conn: 
            conn.close()