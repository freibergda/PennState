'''This modules tests the admin functions.py'''
import sqlite3
import streamlit as st
import create_birdsites_database
import make_locations_table

def load_locations_table():
    '''Put the data into the database (mimic the adminstrator)'''
    con = sqlite3.connect("BirdSites.db")
    cur = con.cursor()
    cur.execute("""
    INSERT INTO locations VALUES
        (1,'Cape May Bird Observatory', 'Cape May', 'New Jersey', 12345678, '', 'https://njaudubon.org/centers/cape-may-bird-observatory/',' ', ' '),
        (2,'Magee Marsh', 'Ottawa', 'Ohio', 87654321, '', 'https://www.mageemarsh.org/',' ', ' ')
""")
    con.commit()
    con.close()


def main():
    '''this is the main module, which will test the admin functions'''
    create_birdsites_database.create_birdsites()
    
    make_locations_table.make_locations_table()

    # mimic the administrator by loading the locations table
    load_locations_table()

    # Display the locations table (static, final will be dynamic so that Administrator can create or edit)
    # Set page variables
    st.set_page_config(layout="wide")
    st.title("BirdSites Database")
    st.title("Locations Table")

    # The following sets up a connection to BirdSites_db using a SQLAlchemy Engine
    # Create the SQL connection as specified in the /.streamlit/secrets.toml file.
    conn = st.connection('BirdSites_db', type='sql')

    # Query and display the locations data
    locations = conn.query("select * from locations")
    st.dataframe(locations)

    # Drop the table so that the data loaded by script won't accumulate
    con = sqlite3.connect("BirdSites.db")
    con.execute("DROP TABLE locations")
    con.commit()
    con.close()


if __name__ == "__main__":
    main()
