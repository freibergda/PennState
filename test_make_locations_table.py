'''test_make_locations_table'''
import unittest
import sqlite3
from make_locations_table import make_locations_table

class TestMakeLocationsTable(unittest.TestCase):
    '''test'''
    def setUp(self):
        # Creating a test database
        self.database_name = "BirdSites_test.db"
        self.conn = sqlite3.connect(self.database_name)
    
    def test_make_locations_table(self):
        """Test if the locations table is created correctly."""
        # Run the function to test
        make_locations_table(self.database_name)
        
        # Verify the table creation
        with self.conn:
            cur = self.conn.cursor()
            
            # Check if the table exists
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='locations';")
            table_exists = cur.fetchone()
            self.assertIsNotNone(table_exists, "Table locations was not created.")
            
            # Check the table schema
            cur.execute("PRAGMA table_info('locations');")
            columns = cur.fetchall()
            expected_columns = {'pk_loc': 'INTEGER', 'loc_full_name': 'TEXT', 'county_name': 'TEXT',
                                'state_name': 'TEXT', 'geolocation': 'REAL', 'linkToNWSSite': 'TEXT',
                                'linkToParkWebSite': 'TEXT', 'linkToeBirdSite': 'TEXT',
                                'linkToBirdCastSite': 'TEXT'}
            
            created_columns = {column[1]: column[2] for column in columns}
            
            for col, col_type in expected_columns.items():
                self.assertIn(col, created_columns, f"Column {col} is missing in the locations table.")
                self.assertEqual(col_type, created_columns[col], f"Column {col} has the wrong type.")
    
    def tearDown(self):
        """Clean up the database after tests."""
        with self.conn:
            cur = self.conn.cursor()
            cur.execute("DROP TABLE IF EXISTS locations;")
        self.conn.close()

if __name__ == '__main__':
    unittest.main()