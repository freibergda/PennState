'''This modules tests the admin functions.py'''
import sqlite3
import streamlit as st
import create_birdsites_database
#import make_locations_table


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

    # make_locations_table.make_locations_table()

    # mimic the administrator by loading the locations table
    # load_locations_table()

    # Display the locations table (static, final will be dynamic so that Administrator can create or edit)
    # Set page variables
    st.set_page_config(layout="wide")
    st.title("BirdSites Database")
    st.title("Locations Table")

    # The following sets up a connection to BirdSites_db using a SQLAlchemy Engine
    # Create the SQL connection as specified in the /.streamlit/secrets.toml file.

    try:
        # Making a connection between sqlite3
        # database and Python Program
        conn = st.connection(database_name, type='sql')

        # If sqlite3 makes a connection with python
        # program then it will print "Connected to SQLite"
        # Otherwise it will show errors
        print("Connected to ", database_name)

        # Getting all tables from sqlite_master
        sql_query = """SELECT name FROM "+database_name + 
        " WHERE type='table';"""

        # Creating cursor object using connection object
        cursor = conn.cursor()

        # executing our sql query
        cursor.execute(sql_query)
        print("List of tables\n")

        # printing all tables list
        print(cursor.fetchall())

    except sqlite3.Error as error:
        print("Failed to execute the above query", error)

    finally:

        # Inside Finally Block, If connection is
        # open, we need to close it
        if conn:

            # using close() method, we will close
            # the connection
            conn.close()

            # After closing connection object, we
            # will print "the sqlite connection is
            # closed"
            print("the sqlite connection is closed")

    # st.dataframe(locations)
    # if starting from blank, there should be no locations table

    # Drop the table so that the data loaded by script won't accumulate
    # con = sqlite3.connect("BirdSites.db")
    # con.execute("DROP TABLE locations")
    # con.commit()
    # con.close()


if __name__ == "__main__":
    main()
