'''Jira Task S8S4-139 User Story: As an Administrator, I want the system to show me a list of 
all the current tables in the BirdSites database, so that I can verify that 
all tables needed to operate the BirdSites database are present.
Acceptance Criteria:
Given: the BirdSites database 
When: The system runs the display_all_tables function
Then: The system displays all of the tables currently in the BirdSites database
Variables: database_name (BirdSites)
Parameters: none
Associated Requirements:
Jira Task S8S4-46 The system shall display the complete 
database structure for the Administrator's verification'''

import sqlite3

def display_all_tables(database_name):
    try:
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()
        tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        result = []
        for table_name in tables:
            table_name = table_name[0]
            columns = cursor.execute(f"PRAGMA table_info({table_name});").fetchall()
            columns = [col[1] for col in columns]
            result.append((table_name, columns))
    finally:
        if 'conn' in locals() and conn:
            conn.close()
    return result

def write_output_to_file(output, log_file):
    '''Utility function to write the output to a log file'''
    with open(log_file, "a") as f:
        for table, cols in output:
            f.write(f"Table: {table}, Columns: {cols}\n")
        f.close()

    ############################################################
    # https://cookbook.openai.com/examples/how_to_call_functions_with_chat_models
    # https://database.guide/2-ways-to-list-tables-in-sqlite-database/

    # PRAGMA https://database.guide/4-ways-to-get-information-about-a-tables-structure-in-sqlite/
    
    # https://docs.streamlit.io/develop/concepts/design/dataframes