''' test_admin_functions.py THIS IS THE SYSTEM TEST!'''

import unittest
import os
import sqlite3
from datetime import datetime
import admin_functions

class TestAdminFunctions(unittest.TestCase):
    '''test '''
    @classmethod
    def setUpClass(cls):
        '''Set up the preconditions for the tests'''
        cls.database_name = "BirdSites.db"
        
    def test_database_creation(self):
        '''Test ID: UT3-DB-01 - Test the creation of BirdSites database'''
        
        # Clean up from any previous runs
        if os.path.exists(self.database_name):
            os.remove(self.database_name)
        
        # Run main to create the database
        admin_functions.main()

        # Check if the database file was created
        self.assertTrue(os.path.exists(self.database_name), "Database file was not created")

        # Connect to database and check if the tables were created
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        expected_tables = {'administrator_records', 'locations', 'groups', 'locations_groups'}
        created_tables = {table[0] for table in tables}
        self.assertTrue(expected_tables.issubset(created_tables), f"Not all tables were created: Missing {expected_tables - created_tables}")
        
        conn.close()

    @classmethod
    def tearDownClass(cls):
        '''Clean up after the tests'''
        if os.path.exists(cls.database_name):
            os.remove(cls.database_name)

if __name__ == '__main__':
    unittest.main()

