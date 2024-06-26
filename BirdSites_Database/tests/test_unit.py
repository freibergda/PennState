'''test_unit.py'''
import sqlite3
import os
import pytest
from src.create_birdsites_database import create_birdsites
from src.make_admin_table import make_admin_table
from src.make_locations_table import make_locations_table
from src.make_groups_table import make_groups_table
from src.make_locations_groups_table import make_locations_groups_table
from src.display_birdsites_database_tables import display_all_tables

@pytest.fixture(scope="module")
def setup_database():
    database_name = "test_BirdSites.db"
    if os.path.exists(database_name):
        os.remove(database_name)
    yield database_name
    if os.path.exists(database_name):
        os.remove(database_name)

def test_create_birdsites_database(setup_database):
    database_name = setup_database
    create_birdsites(database_name)
    assert os.path.exists(database_name), "Database was not created"

def test_create_admin_table(setup_database):
    database_name = setup_database
    make_admin_table(database_name)

    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='administrator_records'")
    assert cursor.fetchone() is not None, "Administrator table was not created"
    conn.close()

def test_create_locations_table(setup_database):
    database_name = setup_database
    make_locations_table(database_name)

    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='locations'")
    assert cursor.fetchone() is not None, "Locations table was not created"
    conn.close()

def test_create_groups_table(setup_database):
    database_name = setup_database
    make_groups_table(database_name)

    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='groups'")
    assert cursor.fetchone() is not None, "Groups table was not created"
    conn.close()

def test_create_locations_groups_table(setup_database):
    database_name = setup_database
    make_locations_groups_table(database_name)

    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='locations_groups'")
    assert cursor.fetchone() is not None, "Locations_Groups table was not created"
    conn.close()

def test_display_all_tables(setup_database):
    database_name = setup_database
    output = display_all_tables(database_name)
    expected_output = [
        ('administrator_records', ['id', 'login', 'email']),
        ('locations', ['location_id', 'location_full_name', 'county', 'state_full', 'geographic_coordinates',
                      'link_to_NWS', 'link_to_park', 'link_to_eBird', 'link_to_BirdCast']),
        ('groups', ['group_id', 'spring_migration', 'fall_migration', 'summer', 'winter',
                   'atlantic_flyway', 'pacific_flyway']),
        ('locations_groups', ['location_id', 'group_id'])
    ]
    assert output == expected_output, "The display output doesn't match what is expected"