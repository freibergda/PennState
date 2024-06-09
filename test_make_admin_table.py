'''test_make_admin_table'''
import unittest
import sqlite3
import os
from make_admin_table import make_admin_table

class TestMakeAdminTable(unittest.TestCase):

    def setUp(self):
        """Set up the test environment, including creating a test database."""
        self.test_db = "test_BirdSites.db"
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
        # Create a test database
        conn = sqlite3.connect(self.test_db)
        conn.close()

    def tearDown(self):
        """Tear down the test environment, including deleting the test database."""
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_make_admin_table(self):
        """Test creating the `administrator_records` table."""
        make_admin_table(self.test_db)

        conn = sqlite3.connect(self.test_db)
        cur = conn.cursor()

        # Check if the table has been created
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='administrator_records';")
        table = cur.fetchone()
        self.assertIsNotNone(table, "The administrator_records table should be created.")

        # Check the table schema
        cur.execute("PRAGMA table_info(administrator_records);")
        columns = cur.fetchall()
        expected_columns = [
            (0, 'pk_admin', 'INTEGER', 0, None, 1),
            (1, 'administrator_login', 'TEXT', 0, None, 0),
            (2, 'administrator_email', 'TEXT', 0, None, 0)
        ]
        self.assertEqual(columns, expected_columns, "The administrator_records table schema does not match.")

        conn.close()

if __name__ == '__main__':
    unittest.main()