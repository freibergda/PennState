'''This modules tests the admin functions.py'''
import sqlite3
from datetime import datetime
import streamlit as st
import create_birdsites_database
import make_locations_table
import make_groups_table
import make_locations_groups_table
import display_birdsites_database_tables

def load_locations_table():
    '''Put the data into the database (mimic the adminstrator)'''
    con = sqlite3.connect("BirdSites.db")
    cur = con.cursor()
    cur.execute("""
    INSERT INTO locations VALUES
        (1,'Cape May Bird Observatory', 'Cape May', 'New Jersey', 12345678, '', 'https://njaudubon.org/centers/cape-may-bird-observatory/',' ', ' '),
        (2,'Magee Marsh', 'Ottawa', 'Ohio', 87654321, '', 'https://www.mageemarsh.org/',' ', ' '),
        (3,'Ottawa National Wildlife Refuge', 'Ottawa', 'Ohio', 899999, '', 'https://www.fws.gov/refuge/ottawa', ' ', ' ')
""")
    con.commit()
    con.close()


def main():
    '''this is the main module, which will test the admin functions'''
    database_name = create_birdsites_database.create_birdsites()

    # create the administrator listing table
    
    
    # create all user data tables

    make_locations_table.make_locations_table(database_name)

    make_groups_table.make_groups_table(database_name)

    make_locations_groups_table.make_locations_groups_table(database_name)

    # Set page variables
    st.set_page_config(layout="wide")
    st.title("BirdSites Database")

    # display the list of all tables in the database 
    display_birdsites_database_tables.display_all_tables(database_name)    

    # mimic the administrator by loading the locations table
    # load_locations_table()

    # Display the locations table (static, final will be dynamic so that Administrator can create or edit)
    

    # st.title("Locations Table")
    # st.dataframe(locations)
    # if starting from blank, there should be no locations table

    # Drop the table so that the data loaded by script won't accumulate
    # con = sqlite3.connect("BirdSites.db")
    # con.execute("DROP TABLE locations")
    # con.commit()
    # con.close()


if __name__ == "__main__":
    main()
