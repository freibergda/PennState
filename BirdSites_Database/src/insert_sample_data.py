
import sqlite3

def insert_sample_data(database_name):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO locations (location_full_name, county, state_full, geographic_coordinates, link_to_NWS, link_to_park, link_to_eBird, link_to_BirdCast)
                      VALUES 
                      ('Sample Location 1', 'County A', 'State A', 'Coordinates A', 'link_nws_A', 'link_park_A', 'link_ebird_A', 'link_birdcast_A'),
                      ('Sample Location 2', 'County B', 'State B', 'Coordinates B', 'link_nws_B', 'link_park_B', 'link_ebird_B', 'link_birdcast_B')''')
    conn.commit()
    conn.close()

# Insert sample data
if __name__ == "__main__":
    insert_sample_data(r"C:\Users\freib\Desktop\PENN_STATE\SWENG_894_Capstone\BirdSites_Database\BirdSites.db")
   # insert_sample_data(r"C:\Users\freib\Desktop\PENN_STATE\SWENG_894_Capstone\BirdSites_Database\BirdSites.db")
