import sqlite3
import os
import pytest
from BirdSites_Database.src.create_birdsites_database import create_birdsites
from BirdSites_Database.src.make_admin_table import make_admin_table
from BirdSites_Database.src.make_locations_table import make_locations_table
from BirdSites_Database.src.make_groups_table import make_groups_table
from BirdSites_Database.src.make_locations_groups_table import make_locations_groups_table

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