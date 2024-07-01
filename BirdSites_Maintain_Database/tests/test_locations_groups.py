'''Jira Task S8S4-175 Test Suite for Sprint 2 Administrator Stories '''
import sqlite3
import pandas as pd
import os

def test_locations_groups_table_exist():
    conn = sqlite3.connect(
        r'C:\Users\freib\Desktop\PENN_STATE\SWENG_894_Capstone\BirdSites_Database\BirdSites.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='locations_groups';")
    table_exists = cursor.fetchone()
    conn.close()
    assert table_exists is not None, "Table 'locations_groups' does not exist."

def test_locations_groups_data_fetched():
    conn = sqlite3.connect(
        r'C:\Users\freib\Desktop\PENN_STATE\SWENG_894_Capstone\BirdSites_Database\BirdSites.db')
    df = pd.read_sql("SELECT * FROM locations_groups", conn)
    conn.close()
    assert not df.empty, "No data found in 'locations_groups' table."