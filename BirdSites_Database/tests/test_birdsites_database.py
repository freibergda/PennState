'''Jira task S8S4-167
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
import contextlib
from datetime import datetime

# Adjust the import paths based on your environment set-up
import sys  
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import create_birdsites_database
import display_birdsites_database_tables
import make_admin_table
import make_groups_table
import make_locations_groups_table 
import make_locations_table
import main
    
DATABASE_NAME = "BirdSites.db"
LOG_FILE = "test_report.txt"

@contextlib.contextmanager
def connect_to_database(db_name):
    conn = sqlite3.connect(db_name)
    try:
        yield conn
    finally:
        conn.close()

@pytest.fixture(scope='module', autouse=True)
def setup_and_teardown():
    def assert_no_active_connections():
        try:
            os.remove(DATABASE_NAME)
        except PermissionError:
            raise AssertionError("Database has active connections.")
    if os.path.exists(DATABASE_NAME):
        assert_no_active_connections()
    yield
    if os.path.exists(DATABASE_NAME):
        assert_no_active_connections()

def log_test_result(test_id, test_description, result):
    with open(LOG_FILE, "a") as f:
        f.write(f"Test ID: {test_id}\n")
        f.write(f"Description: {test_description}\n")
        f.write(f"Result: {'Passed' if result else 'Failed'}\n")
        f.write(f"Timestamp: {datetime.now()}\n")
        f.write("-" * 50 + '\n')

# Tests for display_birdsites_database_tables.py
def test_display_tables_success():
    create_birdsites_database.create_birdsites(DATABASE_NAME)
    make_admin_table.make_admin_table(DATABASE_NAME)
    make_locations_table.make_locations_table(DATABASE_NAME)
    make_groups_table.make_groups_table(DATABASE_NAME)
    make_locations_groups_table.make_locations_groups_table(DATABASE_NAME)
    
    tables = display_birdsites_database_tables.display_all_tables(DATABASE_NAME)
    table_names = [table[0] for table in tables]
    expected_tables = {'administrator_records', 'locations', 'groups', 'locations_groups'}
    result = expected_tables.issubset(set(table_names))
    log_test_result("UT1", "Ensure all tables are created successfully.", result)
    assert result

def test_display_tables_content():
    create_birdsites_database.create_birdsites(DATABASE_NAME)
    make_admin_table.make_admin_table(DATABASE_NAME)
    make_locations_table.make_locations_table(DATABASE_NAME)
    make_groups_table.make_groups_table(DATABASE_NAME)
    make_locations_groups_table.make_locations_groups_table(DATABASE_NAME) 
    
    tables = display_birdsites_database_tables.display_all_tables(DATABASE_NAME)
    admin_columns = [col for table, cols in tables if table == 'administrator_records' for col in cols]
    result = 'login' in admin_columns and 'email' in admin_columns
    log_test_result("UT2", "Ensure 'administrator_records' table has correct columns.", result)
    assert result

def test_display_tables_fail():
    create_birdsites_database.create_birdsites(DATABASE_NAME)
    
    tables = display_birdsites_database_tables.display_all_tables(DATABASE_NAME)
    table_names = [table[0] for table in tables]
    result = 'non_existing_table' in table_names
    log_test_result("UT3", "Intentionally failing test to check non-existing table.", result)
    assert not result

def test_make_admin_table_success():
    create_birdsites_database.create_birdsites(DATABASE_NAME)
    make_admin_table.make_admin_table(DATABASE_NAME)
    with connect_to_database(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='administrator_records';")
        result = cursor.fetchall()
    log_test_result("UT1", "Ensure 'administrator_records' table is created successfully.", len(result) == 1)
    assert len(result) == 1

def test_make_admin_table_columns():
    create_birdsites_database.create_birdsites(DATABASE_NAME)
    make_admin_table.make_admin_table(DATABASE_NAME)
    with connect_to_database(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(administrator_records);")
        columns = [col[1] for col in cursor.fetchall()]
    result = 'login' in columns and 'email' in columns
    log_test_result("UT2", "Ensure 'administrator_records' table has correct columns.", result)
    assert result

def test_make_admin_table_fail():
    create_birdsites_database.create_birdsites(DATABASE_NAME)
    make_admin_table.make_admin_table(DATABASE_NAME)
    with connect_to_database(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='non_existing_table';")
        result = cursor.fetchall()
    log_test_result("UT3", "Intentionally failing test to check non-existing table.", len(result) == 1)
    assert len(result) == 0

def test_make_groups_table_success():
    create_birdsites_database.create_birdsites(DATABASE_NAME)
    make_groups_table.make_groups_table(DATABASE_NAME)
    with connect_to_database(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='groups';")
        result = cursor.fetchall()
    log_test_result("UT1", "Ensure 'groups' table is created successfully.", len(result) == 1)
    assert len(result) == 1

def test_make_groups_table_columns():
    create_birdsites_database.create_birdsites(DATABASE_NAME)
    make_groups_table.make_groups_table(DATABASE_NAME)
    with connect_to_database(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(groups);")
        columns = [col[1] for col in cursor.fetchall()]
    result = 'spring_migration' in columns and 'winter' in columns
    log_test_result("UT2", "Ensure 'groups' table has correct columns.", result)
    assert result

def test_make_groups_table_fail():
    create_birdsites_database.create_birdsites(DATABASE_NAME)
    make_groups_table.make_groups_table(DATABASE_NAME)
    with connect_to_database(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='non_existing_table';")
        result = cursor.fetchall()
    log_test_result("UT3", "Intentionally failing test to check non-existing table.", len(result) == 1)
    assert len(result) == 0

def test_make_locations_groups_table_success():
    create_birdsites_database.create_birdsites(DATABASE_NAME)
    make_locations_groups_table.make_locations_groups_table(DATABASE_NAME)
    with connect_to_database(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='locations_groups';")
        result = cursor.fetchall()
    log_test_result("UT1", "Ensure 'locations_groups' table is created successfully.", len(result) == 1)
    assert len(result) == 1

def test_make_locations_groups_table_columns():
    create_birdsites_database.create_birdsites(DATABASE_NAME)
    make_locations_groups_table.make_locations_groups_table(DATABASE_NAME)
    with connect_to_database(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(locations_groups);")
        columns = [col[1] for col in cursor.fetchall()]
    result = 'location_id' in columns and 'group_id' in columns
    log_test_result("UT2", "Ensure 'locations_groups' table has correct columns.", result)
    assert result

def test_make_locations_groups_table_fail():
    create_birdsites_database.create_birdsites(DATABASE_NAME)
    make_locations_groups_table.make_locations_groups_table(DATABASE_NAME)
    with connect_to_database(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='non_existing_table';")
        result = cursor.fetchall()
    log_test_result("UT3", "Intentionally failing test to check non-existing table.", len(result) == 1)
    assert len(result) == 0

def test_make_locations_table_success():
    create_birdsites_database.create_birdsites(DATABASE_NAME)
    make_locations_table.make_locations_table(DATABASE_NAME)
    with connect_to_database(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='locations';")
        result = cursor.fetchall()
    log_test_result("UT1", "Ensure 'locations' table is created successfully.", len(result) == 1)
    assert len(result) == 1

def test_make_locations_table_columns():
    create_birdsites_database.create_birdsites(DATABASE_NAME)
    make_locations_table.make_locations_table(DATABASE_NAME)
    with connect_to_database(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(locations);")
        columns = [col[1] for col in cursor.fetchall()]
    result = 'location_full_name' in columns and 'state_full' in columns
    log_test_result("UT2", "Ensure 'locations' table has correct columns.", result)
    assert result

def test_make_locations_table_fail():
    create_birdsites_database.create_birdsites(DATABASE_NAME)
    make_locations_table.make_locations_table(DATABASE_NAME)
    with connect_to_database(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='non_existing_table';")
        result = cursor.fetchall()
    log_test_result("UT3", "Intentionally failing test to check non-existing table.", len(result) == 1)
    assert len(result) == 0

if __name__ == "__main__":
    pytest.main()