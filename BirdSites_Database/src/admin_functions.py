'''Jira Task S8S4-147 User Story: As an Administrator, I want a BirdSites 
database created with administrator, locations, groups and locations_groups 
tables and display verification of tables, so that I can create or modify 
records that will provide a positive birdwatching user experience.
Acceptance Criteria:
Given:  The BirdSites database and its tables do not exist.
When: The Administrator executes the admin_functions function
Then: The admin_function (the system) will create the BirdSites database, 
the administrator_records, locations, groups, and locations_groups tables 
inside the database and display a list of all tables and the columns in those tables.
Variables: none
Parameters: none'''

import create_birdsites_database
import make_admin_table
import make_locations_table
import make_groups_table
import make_locations_groups_table
import display_birdsites_database_tables

def main():
    '''This is the main module, which will create the database, the 
    administrator_records table, the locations table, the groups table 
    and the locations_groups table'''
    database_name = "BirdSites.db"
    create_birdsites_database.create_birdsites(database_name)

    # Create the administrator listing table
    make_admin_table.make_admin_table(database_name)

    # Create all user data tables
    make_locations_table.make_locations_table(database_name)
    make_groups_table.make_groups_table(database_name)
    make_locations_groups_table.make_locations_groups_table(database_name)

    # Display the list of all tables in the database
    tables_output = display_birdsites_database_tables.display_all_tables(database_name)

if __name__ == "__main__":
    
    main()