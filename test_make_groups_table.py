'''test_make_groups_table'''
import unittest
import sqlite3
import os
from datetime import datetime
from make_groups_table import make_groups_table

class TestMakeGroupsTable(unittest.TestCase):

    def setUp(self):
        # Set up a temporary database for testing purposes
        self.database_name = "test_BirdSites.db"
        conn = sqlite3.connect(self.database_name)
        conn.execute("CREATE TABLE IF NOT EXISTS administrator_records(pk_admin INTEGER PRIMARY KEY AUTOINCREMENT, administrator_login TEXT UNIQUE, administrator_email TEXT UNIQUE)")
        conn.execute("CREATE TABLE IF NOT EXISTS locations(pk_loc INTEGER PRIMARY KEY AUTOINCREMENT, loc_full_name TEXT NOT NULL UNIQUE, county_name TEXT, state_name TEXT NOT NULL, geolocation REAL, linkToNWSSite TEXT, linkToParkWebSite TEXT, linkToeBirdSite TEXT, linkToBirdCastSite TEXT)")
        conn.execute("CREATE TABLE IF NOT EXISTS locations_groups(pk_loc_grp INTEGER PRIMARY KEY AUTOINCREMENT, loc_id INTEGER, grp_id INTEGER, FOREIGN KEY(loc_id) REFERENCES locations(pk_loc), FOREIGN KEY(grp_id) REFERENCES groups(pk_grp))")
        conn.commit()
        conn.close()

    def tearDown(self):
        # Clean up and delete the temporary database
        os.remove(self.database_name)

    def test_make_groups_table(self):
        # Check the database before the table creation
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()

        # Verify the 'groups' table does not exist initially
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='groups'")
        self.assertEqual(cursor.fetchone(), None, "The groups table should not initially exist.")

        conn.close()

        # Run the make_groups_table function to create the 'groups' table
        make_groups_table(self.database_name)

        # Verify the 'groups' table has been created
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='groups'")
        self.assertIsNot(cursor.fetchone(), None, "The groups table should have been created.")

        # Check the structure of the 'groups' table
        cursor.execute("PRAGMA table_info(groups)")
        columns = [desc[1] for desc in cursor.fetchall()]
        expected_columns = ['pk_grp', 'spring_migration', 'fall_migration', 'summer', 'winter', 'atlantic_flyway', 'pacific_flyway']
        self.assertEqual(columns, expected_columns, "The columns in the groups table do not match the expected schema.")

        conn.close()

if __name__ == "__main__":
    unittest.main()