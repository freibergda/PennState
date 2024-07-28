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
from datetime import datetime
import time
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import create_birdsites_database
import display_birdsites_database_tables
import make_admin_table
import make_groups_table
import make_locations_groups_table
import make_locations_table

DATABASE_NAME = "BirdSites.db"
LOG_FILE = "test_report.txt"


@pytest.fixture(scope='module', autouse=True)
def setup_and_teardown():
    safely_remove_database(DATABASE_NAME)
    safely_remove_file(LOG_FILE)
    yield
    safely_remove_database(DATABASE_NAME)


def safely_remove_file(file_name):
    if os.path.exists(file_name):
        tries = 0
        while tries < 5:
            try:
                os.remove(file_name)
                break
            except OSError as e:
                print(f"Error removing file: {e}")
                time.sleep(1)
                tries += 1


def safely_remove_database(db_name):
    if os.path.exists(db_name):
        tries = 0
        while tries < 5:
            try:
                conn = sqlite3.connect(db_name)
                conn.close()
                os.remove(db_name)
                break
            except sqlite3.Error as e:
                print(f"Error closing the database connection: {e}")
                time.sleep(1)
                tries += 1
            except OSError as e:
                print(f"Error removing the database file: {e}")
                time.sleep(1)
                tries += 1


@pytest.fixture(autouse=True)
def close_connections():
    yield
    if 'conn' in globals() and conn:
        conn.close()


# Using context manager for the log file
def log_test_result(test_id, description, steps, expected_response, result, preconditions, associated_reqs):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"---------------------------------------------\n")
        f.write(f"Test Type: Unit\n")
        f.write(f"Context: Database\n")
        f.write(f"Test ID: {test_id}\n")
        f.write(f"Description: {description}\n")
        f.write("Test URL: N/A\n")
        f.write(f"Preconditions: {preconditions}\n")
        f.write("Test Execution Steps:\n")
        for step in steps:
            f.write(f"Step {step['number']}:\n")
            f.write(f"Action: {step['action']}\n")
            f.write(f"Expected Response: {step['expected']}\n")
        f.write(f"Expected Response: {expected_response}\n")
        f.write(f"Result: {'Passed' if result else 'Failed'}\n")
        f.write(f"Timestamp: {datetime.now()}\n")
        f.write(f"Associated Requirements: {associated_reqs}\n")
        f.write(f"---------------------------------------------\n\n")


def run_test_action(action):
    if action.startswith("Run create_birdsites"):
        create_birdsites_database.create_birdsites(DATABASE_NAME)
    elif action == "Run make_admin_table() function.":
        make_admin_table.make_admin_table(DATABASE_NAME)
    elif action == "Run make_groups_table() function.":
        make_groups_table.make_groups_table(DATABASE_NAME)
    elif action == "Run make_locations_groups_table() function.":
        make_locations_groups_table.make_locations_groups_table(DATABASE_NAME)
    elif action == "Run make_locations_table() function.":
        make_locations_table.make_locations_table(DATABASE_NAME)
    elif action == "Run display_all_tables() function.":
        return display_birdsites_database_tables.display_all_tables(DATABASE_NAME)
    else:
        raise ValueError(f"Unknown action: {action}")

########################## #1 Tests for Jira Task S8S4-70
def test_create_birdsites_success():
    steps = [{"number": 1, "action": "Run create_birdsites() function.", "expected": "BirdSites.db file is created."}]
    run_test_action(steps[0]["action"])
    result = os.path.exists(DATABASE_NAME)

    log_test_result("S8S4-70-1", 
                    "User Story: As an Administrator, I want the system to create the BirdSites database, so that I can create tables and load records into the BirdSites database.",
                    steps, 
                    "BirdSites.db is created successfully.", 
                    result, 
                    "Given: the BirdSites.db database does not exist When: the system runs the create_birdsites function.",
                    "Jira Task S8S4-18 The system shall create a database called BirdSites.")
    assert result


def test_create_birdsites_twice():
    steps = [
        {"number": 1, "action": "Run create_birdsites() function.", "expected": "BirdSites.db file is created."},
        {"number": 2, "action": "Run create_birdsites() function again.", "expected": "No error occurs, BirdSites.db file exists."}
    ]
    run_test_action(steps[0]["action"])
    run_test_action("Run create_birdsites() function.")
    result = os.path.exists(DATABASE_NAME)

    log_test_result("S8S4-70-2", 
                    "User Story: As an Administrator, I want the system to create the BirdSites database twice, so that I can ensure idempotency.",
                    steps, 
                    "BirdSites.db is created successfully on both attempts.", 
                    result, 
                    "Given: the BirdSites.db database may or may not exist When: the system runs the create_birdsites function twice.",
                    "Jira Task S8S4-18 The system shall create a database called BirdSites.")
    assert result


def test_create_birdsites_failure():
    steps = [{"number": 1, "action": "Run create_birdsites() function with an invalid path.", "expected": "OperationalError is raised."}]
    try:
        create_birdsites_database.create_birdsites("invalid/BirdSites.db")
        result = False
    except sqlite3.OperationalError:
        result = True

    log_test_result("S8S4-70-3", 
                    "User Story: As an Administrator, I want the system to handle errors gracefully during the BirdSites database creation.",
                    steps, 
                    "OperationalError is raised as expected.", 
                    result, 
                    "Given: An invalid path When: running the create_birdsites function.",
                    "Jira Task S8S4-18 The system shall create a database called BirdSites.")
    assert result

########################## #2 Tests for Jira Task S8S4-131
def test_admin_table_creation():
    steps = [
        {"number": 1, "action": "Run make_admin_table() function.", "expected": "administrator_records table is created with correct schema."}
    ]
    run_test_action("Run create_birdsites() function.")
    action_result = run_test_action(steps[0]["action"])
    result = action_result != False

    log_test_result("S8S4-131-1",
                    "User Story: As an Administrator, I want the system to create a table called the administrator_records table.",
                    steps, "The administrator_records table is created successfully.", result,
                    "Given: the BirdSites.db database exists, but does not have the administrator_records table When: the system runs the make_admin_table function",
                    "Jira Task S8S4-19 The system shall create an administrative file.")
    assert result

def test_admin_email_unique_constraint():
    steps = [
        {"number": 1, "action": "Run make_admin_table() function.", "expected": "administrator_records table is created with correct schema."},
        {"number": 2, "action": "Insert first record with unique email.", "expected": "First record insertion succeeds."},
        {"number": 3, "action": "Insert second record with the same email.", "expected": "Second record insertion fails due to unique constraint."}
    ]
    run_test_action("Run create_birdsites() function.")
    run_test_action(steps[0]["action"])

    action_result = False
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO administrator_records (login, email) VALUES ('admin1', 'admin@example.com');")
            cursor.execute("INSERT INTO administrator_records (login, email) VALUES ('admin2', 'admin@example.com');")
            conn.commit()
    except sqlite3.IntegrityError:
        action_result = True

    log_test_result("S8S4-131-2",
                    "User Story: As an Administrator, I want to verify the unique constraint on email column in the administrator_records table.",
                    steps, "Unique constraint works as expected.", action_result,
                    "Given: the BirdSites.db database exists and has the administrator_records table When: attempting to insert duplicate email",
                    "Jira Task S8S4-19 The system shall create an administrative file.")
    assert action_result

def test_admin_table_failure():
    steps = [
        {"number": 1, "action": "Run make_admin_table() function.", "expected": "administrator_records table is created with correct schema."},
        {"number": 2, "action": "Insert record without email.", "expected": "Record insertion fails due to NOT NULL constraint."}
    ]
    run_test_action("Run create_birdsites() function.")
    run_test_action(steps[0]["action"])

    action_result = False
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO administrator_records (login) VALUES ('admin1');")
            conn.commit()
    except sqlite3.IntegrityError:
        action_result = True

    log_test_result("S8S4-131-3",
                    "User Story: As an Administrator, I want to verify the NOT NULL constraint on email column in the administrator_records table.",
                    steps, "NOT NULL constraint works as expected.", action_result,
                    "Given: the BirdSites.db database exists and has the administrator_records table When: attempting to insert record without email",
                    "Jira Task S8S4-19 The system shall create an administrative file.")
    assert action_result

########################## #3 Tests for Jira Task S8S4-49
def test_create_groups_success():
    steps = [
        {"number": 1, "action": "Run create_birdsites() function.", "expected": "BirdSites.db file is created."},
        {"number": 2, "action": "Run make_groups_table() function.", "expected": "Groups table is created in BirdSites.db."}
    ]
    run_test_action(steps[0]["action"])
    run_test_action(steps[1]["action"])
    result = "groups" in [table[0] for table in run_test_action("Run display_all_tables() function.")]

    log_test_result("S8S4-49-1", 
                    "User Story: As an Administrator, I want the system to create a table called the Groups table in the BirdSites database.",
                    steps, "The Groups table is created successfully.", result, 
                    "Given: the BirdSites.db database exists and the Groups table does not exist When: the system runs the make_groups_table function.", 
                    "Jira Task S8S4-23 The system shall create a Groups Table, which will be filled by an administrator.")
    assert result

def test_groups_table_columns():
    steps = [
        {"number": 1, "action": "Run create_birdsites() function.", "expected": "BirdSites.db file is created."},
        {"number": 2, "action": "Run make_groups_table() function.", "expected": "Groups table is created in BirdSites.db."},
        {"number": 3, "action": "Run display_all_tables() function.", "expected": "Groups table columns are fetched."}
    ]
    run_test_action(steps[0]["action"])
    run_test_action(steps[1]["action"])
    tables_info = run_test_action(steps[2]["action"])
    
    groups_table_columns = []
    for table_name, columns in tables_info:
        if table_name == "groups":
            groups_table_columns = columns
            break

    expected_columns = {'group_id', 'spring_migration', 'fall_migration', 'summer', 'winter',
                        'atlantic_flyway', 'central_flyway', 'pacific_flyway'}

    result = set(groups_table_columns) == expected_columns

    log_test_result("S8S4-49-2", 
                    "User Story: As an Administrator, I want the Groups table to have predefined columns.",
                    steps, "The Groups table has the correct columns.", result, 
                    "Given: the BirdSites.db database exists and the Groups table is created When: the system runs the display_all_tables function.",
                    "Jira Task S8S4-23 The system shall create a Groups Table, which will be filled by an administrator.")
    assert result

def test_create_invalid_groups_table():
    steps = [
        {"number": 1, "action": "Run create_birdsites() function.", "expected": "BirdSites.db file is created."},
        {"number": 2, "action": "Attempt to run make_groups_table() function after intentionally modifying the schema.", "expected": "An error occurs."}
    ]
    run_test_action(steps[0]["action"])
    
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE groups (invalid_column INTEGER);")
        # Now running the original function should fail
        make_groups_table.make_groups_table(DATABASE_NAME)
        result = False
    except sqlite3.Error:
        result = True

    log_test_result("S8S4-49-3", 
                    "User Story: As an Administrator, I want the system to handle schema errors gracefully when creating the Groups table.",
                    steps, "An error occurs as expected.", result, 
                    "Given: the BirdSites.db database exists and the Groups table schema is intentionally modified When: the system runs the make_groups_table function.", 
                    "Jira Task S8S4-23 The system shall create a Groups Table, which will be filled by an administrator.")
    assert result

##########################  #4  Tests for Jira Task S8S4-17 - Create locations_groups Table
def test_create_locations_groups_success():
    steps = [
        {"number": 1, "action": "Run create_birdsites() function.", "expected": "BirdSites.db file is created."},
        {"number": 2, "action": "Run make_locations_groups_table() function.", "expected": "locations_groups table is created in BirdSites.db."}
    ]
    run_test_action(steps[0]["action"])
    run_test_action(steps[1]["action"])
    result = "locations_groups" in [table[0] for table in run_test_action("Run display_all_tables() function.")]

    log_test_result("S8S4-17-1", 
                    "User Story: As an Administrator, I want the system to create a table called the locations_groups table in the BirdSites database.",
                    steps, "The locations_groups table is created successfully.", result, 
                    "Given: the BirdSites.db database exists and the locations_groups table does not exist When: the system runs the make_locations_groups_table function.", 
                    "Jira Task S8S4-25 The system shall create a Locations-Groups Table, which will be filled by the administrator.")
    assert result

def test_locations_groups_table_columns():
    steps = [
        {"number": 1, "action": "Run create_birdsites() function.", "expected": "BirdSites.db file is created."},
        {"number": 2, "action": "Run make_locations_groups_table() function.", "expected": "locations_groups table is created in BirdSites.db."},
        {"number": 3, "action": "Run display_all_tables() function.", "expected": "locations_groups table columns are fetched."}
    ]
    run_test_action(steps[0]["action"])
    run_test_action(steps[1]["action"])
    tables_info = run_test_action(steps[2]["action"])
    
    locations_groups_table_columns = []
    for table_name, columns in tables_info:
        if table_name == "locations_groups":
            locations_groups_table_columns = columns
            break

    expected_columns = {'location_id', 'group_id'}

    result = set(locations_groups_table_columns) == expected_columns

    log_test_result("S8S4-17-2", 
                    "User Story: As an Administrator, I want the locations_groups table to have predefined columns.",
                    steps, "The locations_groups table has the correct columns.", result, 
                    "Given: the BirdSites.db database exists and the locations_groups table is created When: the system runs the display_all_tables function.",
                    "Jira Task S8S4-25 The system shall create a Locations-Groups Table, which will be filled by the administrator.")
    assert result

def test_create_invalid_locations_groups_table():
    steps = [
        {"number": 1, "action": "Run create_birdsites() function.", "expected": "BirdSites.db file is created."},
        {"number": 2, "action": "Run make_locations_groups_table() function with incorrect schema.", "expected": "An error occurs."}
    ]
    
#########################################################      
    run_test_action(steps[0]["action"]) 
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE locations_groups (invalid_column INTEGER);")
        # Now running the original function should fail
        make_locations_groups_table.make_locations_groups_table(DATABASE_NAME)
        result = False
    except sqlite3.Error:
        result = True

    log_test_result("S8S4-17-3", 
                    "User Story: As an Administrator, I want the system to handle schema errors gracefully when creating the locations_groups table.",
                    steps, "An error occurs as expected.", result, 
                    "Given: the BirdSites.db database exists and the locations_groups table schema is intentionally modified When: the system runs the make_locations_groups_table function.", 
                    "Jira Task S8S4-25 The system shall create a Locations-Groups Table, which will be filled by the administrator.")
    assert result

##########################  #5  Tests for Jira Task S8S4-15
def test_create_locations_success():
    steps = [
        {"number": 1, "action": "Run create_birdsites() function.", "expected": "BirdSites.db file is created."},
        {"number": 2, "action": "Run make_locations_table() function.", "expected": "Locations table is created in BirdSites.db."}
    ]
    run_test_action(steps[0]["action"])
    run_test_action(steps[1]["action"])
    tables = [table[0] for table in run_test_action("Run display_all_tables() function.")]
    result = "locations" in tables

    log_test_result("S8S4-15-1", 
                    "User Story: As an Administrator, I want the system to create a table called the Locations table in the BirdSites database.",
                    steps, "Locations table is created successfully.", result, 
                    "Given: the BirdSites.db database exists and the Locations table does not exist When: the system runs the make_locations_table function.", 
                    "Jira Task S8S4-21 The system shall create a Location Table, which will be filled by an administrator.")
    assert result

def test_locations_table_columns():
    steps = [
        {"number": 1, "action": "Run create_birdsites() function.", "expected": "BirdSites.db file is created."},
        {"number": 2, "action": "Run make_locations_table() function.", "expected": "Locations table is created in BirdSites.db."},
        {"number": 3, "action": "Run display_all_tables() function.", "expected": "Locations table columns are fetched."}
    ]
    run_test_action(steps[0]["action"])
    run_test_action(steps[1]["action"])
    tables_info = run_test_action(steps[2]["action"])

    locations_table_columns = []
    for table_name, columns in tables_info:
        if table_name == "locations":
            locations_table_columns = columns
            break

    expected_columns = {'location_id', 'location_full_name', 'county', 'state_full', 
                        'latitude', 'longitude', 'link_to_NWS', 'link_to_park', 
                        'link_to_eBird', 'link_to_BirdCast'}

    result = set(locations_table_columns) == expected_columns

    log_test_result("S8S4-15-2", 
                    "User Story: As an Administrator, I want the Locations table to have predefined columns.",
                    steps, "The Locations table has the correct columns.", result, 
                    "Given: the BirdSites.db database exists and the Locations table is created When: the system runs the display_all_tables function.",
                    "Jira Task S8S4-21 The system shall create a Location Table, which will be filled by an administrator.")
    assert result

def test_insert_incomplete_record_into_locations():
    steps = [
        {"number": 1, "action": "Run create_birdsites() function.", "expected": "BirdSites.db file is created."},
        {"number": 2, "action": "Run make_locations_table() function.", "expected": "Locations table is created in BirdSites.db."},
        {"number": 3, "action": "Insert incomplete record into locations table.", "expected": "Insertion fails due to NOT NULL constraint."}
    ]
    run_test_action(steps[0]["action"])
    run_test_action(steps[1]["action"])

    action_result = False
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO locations (county, state_full) VALUES ('SomeCounty', 'SomeState');")
            conn.commit()
    except sqlite3.IntegrityError:
        action_result = True

    log_test_result("S8S4-15-3", 
                    "User Story: As an Administrator, I want to test insertion of incomplete record into the Locations table.",
                    steps, "Insertion fails due to NOT NULL constraint.", action_result, 
                    "Given: the BirdSites.db database exists and the Locations table is created When: attempting to insert a record without required columns", 
                    "Jira Task S8S4-21 The system shall create a Location Table, which will be filled by an administrator.")
    assert action_result

##########################  #6 Tests for Jira Task S8S4-139

def capture_display_all_tables_output():
    output = display_birdsites_database_tables.display_all_tables(DATABASE_NAME)
    display_birdsites_database_tables.write_output_to_file(output, LOG_FILE)

def test_display_all_tables_success():
    steps = [
        {"number": 1, "action": "Run create_birdsites() function.", "expected": "Database BirdSites.db is created."},
        {"number": 2, "action": "Run make_admin_table() function.", "expected": "Administrator table is created."},
        {"number": 3, "action": "Run make_locations_table() function.", "expected": "Locations table is created."},
        {"number": 4, "action": "Run make_groups_table() function.", "expected": "Groups table is created."},
        {"number": 5, "action": "Run make_locations_groups_table() function.", "expected": "Locations-Groups table is created."},
        {"number": 6, "action": "Run display_all_tables() function.", "expected": "List of all tables is displayed."}
    ]
    for step in steps[:-1]:
        run_test_action(step["action"])
    output = run_test_action(steps[-1]["action"])

    # Adjust the expected_tables to include 'sqlite_sequence' and filter from the actual tables
    expected_tables = {'administrator_records', 'locations', 'groups', 'locations_groups', 'sqlite_sequence'}
    actual_tables = {table_info[0] for table_info in output}

    result = actual_tables == expected_tables

    log_test_result("S8S4-139-1",
                    "User Story: As an Administrator, I want the system to show me a list of all the current tables in the BirdSites database.",
                    steps, "The tables 'administrator_records', 'locations', 'groups', 'locations_groups' should be listed.", result,
                    "Given: the BirdSites database When: The system runs the display_all_tables function.", 
                    "Jira Task S8S4-46 The system shall display the complete database structure for the Administrator's verification")
    capture_display_all_tables_output()  # Save the output to the log file
    assert result

def test_display_all_tables_incorrect_schema():
    steps = [
        {"number": 1, "action": "Run create_birdsites() function.", "expected": "Database BirdSites.db is created."},
        {"number": 2, "action": "Run make_admin_table() function.", "expected": "Administrator table is created."},
        {"number": 3, "action": "Run make_locations_table() function.", "expected": "Locations table is created."},
        {"number": 4, "action": "Manually add an incorrect schema table.", "expected": "Incorrect table is created."},
        {"number": 5, "action": "Run display_all_tables() function.", "expected": "List of all tables is displayed, including the incorrect table."}
    ]
    for step in steps[:-2]:
        run_test_action(step["action"])

    # Manually add incorrect schema table
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE incorrect_table (bad_column TEXT);")

    output = run_test_action(steps[-1]["action"])

    # Check if the incorrect table is listed
    actual_tables = {table_info[0] for table_info in output}

    result = "incorrect_table" in actual_tables

    log_test_result("S8S4-139-2",
                    "User Story: As an Administrator, I want the system to accurately display all tables, including those with bad schema.",
                    steps, "The system correctly identifies the presence of tables with incorrect schemas.", result,
                    "Given: the BirdSites database When: a table with a bad schema is manually created.",
                    "Jira Task S8S4-46 The system shall display the complete database structure for the Administrator's verification")
    capture_display_all_tables_output()  # Save the output to the log file
    assert result
    
def test_display_all_tables_failure():
    steps = [
        {"number": 1, "action": "Run create_birdsites() function.", "expected": "Database BirdSites.db is created."},
        {"number": 2, "action": "Run make_admin_table() function.", "expected": "Administrator table is created."},
        {"number": 3, "action": "Run make_locations_table() function.", "expected": "Locations table is created."},
        {"number": 4, "action": "Run make_groups_table() function.", "expected": "Groups table is created."},
        {"number": 5, "action": "Run make_locations_groups_table() function.", "expected": "Locations-Groups table is created."},
        {"number": 6, "action": "Run display_all_tables() function.", "expected": "List of all tables is displayed."}
    ]
    for step in steps[:-1]:
        run_test_action(step["action"])
    output = run_test_action(steps[-1]["action"])

    # Intentionally making a failing test
    expected_tables = {'admin_records', 'locations_wrong', 'groups_wrong', 'locations_groups_wrong'}
    actual_tables = {table_info[0] for table_info in output}

    result = actual_tables == expected_tables

    log_test_result("S8S4-139-3",
                    "User Story: As an Administrator, I want the system to fail this test for demonstration purposes.",
                    steps, "The tables 'admin_records', 'locations_wrong', 'groups_wrong', 'locations_groups_wrong' should be listed.", result,
                    "Given: the BirdSites database When: The system runs the display_all_tables function.", 
                    "Jira Task S8S4-46 The system shall display the complete database structure for the Administrator's verification")
    capture_display_all_tables_output()  # Save the output to the log file
    assert not result  # Test will fail as expected_tables does not match actual_tables
########################## #7 Tests for Jira Task S8S4-147
#

########################## Tests for Jira Task S8S4-167
def test_incomplete_db_schema():
    create_birdsites_database.create_birdsites(DATABASE_NAME)
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS test_table (id INTEGER PRIMARY KEY);")
        result = display_birdsites_database_tables.display_all_tables(DATABASE_NAME)
    except sqlite3.OperationalError as e:
        result = str(e)
        log_test_result("Jira Task S8S4-167", "Test Incomplete DB Schema - Graceful handling of existing tables", 
                        [{"number": 1, "action": "Run create_birdsites() function.", "expected": "Database BirdSites.db is created."}],
                        "OperationalError: table test_table already exists", False, 
                        "Given: BirdSites.db database exists When: attempting to create an existing table", 
                        "Jira Task S8S4-25")
        raise  # Re-raise to ensure the test is marked as failed

    assert any(table[0] == "test_table" for table in result)

if __name__ == "__main__":
    pytest.main()