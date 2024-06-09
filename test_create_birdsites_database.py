'''test_create_birdsites_database'''

import unittest
import os
from create_birdsites_database import create_birdsites

class TestCreateBirdsitesDatabase(unittest.TestCase):
    '''test'''
    def setUp(self):
        """Executed before each test. Deletes the BirdSites.db if it exists"""
        self.database_name = "BirdSites.db"
        if os.path.exists(self.database_name):
            os.remove(self.database_name)

    def tearDown(self):
        """Executed after each test. Deletes the BirdSites.db if it exists"""
        if os.path.exists(self.database_name):
            os.remove(self.database_name)

    def test_create_database(self):
        """Test the database is created successfully"""
        result_db_name = create_birdsites()
        self.assertEqual(result_db_name, self.database_name)
        self.assertTrue(os.path.exists(self.database_name))

    def test_database_already_exists(self):
        """Test that if the database already exists, it handles properly"""
        # Create the database first
        create_birdsites()

        # Ensure the database exists
        self.assertTrue(os.path.exists(self.database_name))

        # Run the function again
        result_db_name = create_birdsites()

        # Check the database still exists and no errors occurred
        self.assertEqual(result_db_name, self.database_name)
        self.assertTrue(os.path.exists(self.database_name))


if __name__ == '__main__':
    unittest.main()