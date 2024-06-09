'''TestDisplayBirdSitesDatabaseTables'''

import unittest
from unittest.mock import patch
import sqlite3
import display_birdsites_database_tables

class TestDisplayBirdSitesDatabaseTables(unittest.TestCase):
    
    def setUp(self):
        # Set up an in-memory SQLite database for testing
        self.database_name = ":memory:"
        self.conn = sqlite3.connect(self.database_name)
        self.create_tables()
        
    def tearDown(self):
        # Close the database connection after each test
        self.conn.close()
        
    def create_tables(self):
        # Create tables in the in-memory database
        with self.conn:
            self.conn.execute("""
                CREATE TABLE administrator_records (
                    pk_admin INTEGER PRIMARY KEY AUTOINCREMENT,
                    administrator_login TEXT UNIQUE, 
                    administrator_email TEXT UNIQUE
                )
            """)
            self.conn.execute("""
                CREATE TABLE groups (
                    pk_grp INTEGER PRIMARY KEY AUTOINCREMENT,
                    spring_migration TEXT, 
                    fall_migration TEXT, 
                    summer TEXT, 
                    winter TEXT, 
                    atlantic_flyway TEXT, 
                    pacific_flyway TEXT
                )
            """)
            self.conn.execute("""
                CREATE TABLE locations (
                    pk_loc INTEGER PRIMARY KEY AUTOINCREMENT,
                    loc_full_name TEXT NOT NULL UNIQUE, 
                    county_name TEXT, 
                    state_name TEXT NOT NULL, 
                    geolocation REAL,
                    linkToNWSSite TEXT, 
                    linkToParkWebSite TEXT, 
                    linkToeBirdSite TEXT,
                    linkToBirdCastSite TEXT
                )
            """)
            self.conn.execute("""
                CREATE TABLE locations_groups (
                    pk_loc_grp INTEGER PRIMARY KEY AUTOINCREMENT,
                    loc_id INTEGER,
                    grp_id INTEGER,
                    FOREIGN KEY(loc_id) REFERENCES locations(pk_loc),
                    FOREIGN KEY(grp_id) REFERENCES groups(pk_grp)
                )
            """)
    
    @patch('streamlit.set_page_config')
    @patch('streamlit.title')
    @patch('streamlit.header')
    @patch('streamlit.dataframe')
    def test_display_all_tables(self, mock_dataframe, mock_header, mock_title, mock_set_page_config):
        # Test the display_all_tables function
        display_birdsites_database_tables.display_all_tables(self.database_name)
        
        # Verify that streamlit components are called correctly
        mock_set_page_config.assert_called_once_with(layout="wide")
        mock_title.assert_called_once_with("BirdSites Database")
        mock_header.assert_called_once_with("List of tables\n")
        
        # Verify that dataframe is called with the correct data
        expected_tables = [
            ('administrator_records',), 
            ('groups',), 
            ('locations',), 
            ('locations_groups',)
        ]
        mock_dataframe.assert_called_once_with(expected_tables)
        
if __name__ == '__main__':
    unittest.main()
