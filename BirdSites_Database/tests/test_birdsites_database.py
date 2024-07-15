'''test_birdsites_database.py
Jira task S8S4-167
Test Type: Unit
Context: BirdSites Database
Test ID: UT1 – Database and Table Creation

Description:
This test suite checks the creation and structure of the BirdSites database and its tables. 
It ensures that the database is created and contains all the necessary tables with expected columns.

Test URL:
Include the commit or link to the git repository where the file implementing the test case is located.

Preconditions:
- The file to be tested is located in the 'src' directory.
- SQLite3 and pytest should be installed.
- The BirdSites.db database doesn’t exist before starting the test.

Test Execution Steps:
Step    Action                                                          Expected Response
1.      Run the main function that creates the database and tables.     The BirdSites.db file is created.
2.      Connect to the database and fetch the list of tables.           Tables `administrator_records`, `locations`, `groups`, and `locations_groups` exist.
3.      Verify that each table has the expected columns.                Columns match the specifications.
'''

import os
import sqlite3
import pytest

from src import admin_functions, create_birdsites_database, make_admin_table, make_locations_table, make_groups_table, make_locations_groups_table

DATABASE_NAME = "BirdSites.db"

@pytest.fixture(scope="module")
def setup_birdsites_db():
    if os.path.exists(DATABASE_NAME):
        os.remove(DATABASE_NAME)
    create_birdsites_database.create_birdsites(DATABASE_NAME)
    make_admin_table.make_admin_table(DATABASE_NAME)
    make_locations_table.make_locations_table(DATABASE_NAME)
    make_groups_table.make_groups_table(DATABASE_NAME)
    make_locations_groups_table.make_locations_groups_table(DATABASE_NAME)
    yield
    if os.path.exists(DATABASE_NAME):
        os.remove(DATABASE_NAME)

def test_database_creation(setup_birdsites_db):
    assert os.path.exists(DATABASE_NAME), "Database file has not been created."

def test_tables_creation(setup_birdsites_db):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    table_names = [table[0] for table in tables]
    
    expected_tables = [
        'administrator_records',
        'locations',
        'groups',
        'locations_groups'
    ]
    
    for table in expected_tables:
        assert table in table_names, f"Table '{table}' does not exist in the database."
    
    conn.close()

def test_table_columns(setup_birdsites_db):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    table_columns = {
        'administrator_records': {'id', 'login', 'email'},
        'locations': {'location_id', 'location_full_name', 'county', 'state_full', 'latitude', 'longitude', 'link_to_NWS', 'link_to_park', 'link_to_eBird', 'link_to_BirdCast'},
        'groups': {'group_id', 'spring_migration', 'fall_migration', 'summer', 'winter', 'atlantic_flyway', 'central_flyway', 'pacific_flyway'},
        'locations_groups': {'location_id', 'group_id'}
    }
    
    for table, columns in table_columns.items():
        actual_columns = cursor.execute(f"PRAGMA table_info({table});").fetchall()
        actual_columns = {col[1] for col in actual_columns}
        assert columns == actual_columns, f"Table '{table}' does not have the expected columns. Expected: {columns}, Found: {actual_columns}"
    
    conn.close()

def test_execution_and_save_output():
    from io import StringIO
    import sys

    pytest_output = StringIO()
    result = pytest.main(["-v"], stdout=pytest_output)
    
    with open("test_results.txt", "w") as f:
        f.write(pytest_output.getvalue())

if __name__ == "__main__":
    test_execution_and_save_output()