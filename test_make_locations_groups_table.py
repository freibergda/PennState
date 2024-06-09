'''test_make_locations_groups_table'''
import unittest
import sqlite3
from make_locations_groups_table import make_locations_groups_table

class TestMakeLocationsGroupsTable(unittest.TestCase):
    '''test'''
    def setUp(self):
        # Creating a test database
        self.database_name = "BirdSites_test.db"
        self.conn = sqlite3.connect(self.database_name)
        self.create_dependencies()

    def create_dependencies(self):
        """Creates the necessary dependent tables for the test."""
        with self.conn:
            cur = self.conn.cursor()
            cur.execute('''CREATE TABLE IF NOT EXISTS locations(
                            pk_loc INTEGER PRIMARY KEY AUTOINCREMENT)''')
            cur.execute('''CREATE TABLE IF NOT EXISTS groups(
                            pk_grp INTEGER PRIMARY KEY AUTOINCREMENT)''')
    
    def test_make_locations_groups_table(self):
        """Test if the locations_groups table is created correctly."""
        # Run the function to test
        make_locations_groups_table(self.database_name)
        
        # Verify the table creation
        with self.conn:
            cur = self.conn.cursor()
            
            # Check if the table exists
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='locations_groups';")
            table_exists = cur.fetchone()
            self.assertIsNotNone(table_exists, "Table locations_groups was not created.")
            
            # Check the table schema
            cur.execute("PRAGMA table_info('locations_groups');")
            columns = cur.fetchall()
            expected_columns = ['pk_loc_grp', 'loc_id', 'grp_id']
            
            created_columns = [column[1] for column in columns]
            
            for col in expected_columns:
                self.assertIn(col, created_columns, f"Column {col} is missing in the locations_groups table.")
            
            # Check foreign keys
            cur.execute("PRAGMA foreign_key_list('locations_groups');")
            foreign_keys = cur.fetchall()
            
            self.assertTrue(any(fk[3] == 'locations' and fk[4] == 'pk_loc' for fk in foreign_keys),
                            "Foreign key to locations(pk_loc) is missing.")
            self.assertTrue(any(fk[3] == 'groups' and fk[4] == 'pk_grp' for fk in foreign_keys),
                            "Foreign key to groups(pk_grp) is missing.")
    
    def tearDown(self):
        """Clean up the database after tests."""
        with self.conn:
            cur = self.conn.cursor()
            cur.execute("DROP TABLE IF EXISTS locations_groups;")
            cur.execute("DROP TABLE IF EXISTS locations;")
            cur.execute("DROP TABLE IF EXISTS groups;")
        self.conn.close()

if __name__ == '__main__':
    unittest.main()