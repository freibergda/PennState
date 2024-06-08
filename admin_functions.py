'''This modules tests the admin functions.py'''
import sqlite3
from datetime import datetime
import streamlit as st
import create_birdsites_database
import make_locations_table
import make_groups_table
import make_locations_groups_table


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

    # create all database tables

    make_locations_table.make_locations_table(database_name)

    make_groups_table.make_groups_table(database_name)

    make_locations_groups_table.make_locations_groups_table(database_name)

    # mimic the administrator by loading the locations table
    # load_locations_table()

    # Display the locations table (static, final will be dynamic so that Administrator can create or edit)
    # Set page variables
    st.set_page_config(layout="wide")
    st.title("BirdSites Database")

    # open the sqlite3 database
    try:
        # Making a connection between sqlite3 database and Python Program
        conn = sqlite3.connect(database_name)

        # If sqlite3 makes a connection with python
        # program then it will print "Connected to SQLite"
        # Otherwise it will show errors
        curr_datetime = datetime.now()
        print("Connected to ", database_name, " at: ", curr_datetime)

        # Getting a list of all tables from sqlite_schema, don't include sqlite internal tables
        # https://database.guide/2-ways-to-list-tables-in-sqlite-database/
        sql_query = """SELECT name FROM sqlite_schema 
                    WHERE type = ('table') 
                    AND name NOT LIKE 'sqlite_%'
                    ORDER BY name;"""

        # Creating cursor object using connection object
        cursor = conn.cursor()

        # executing our sql query
        cursor.execute(sql_query)

        # send it to streamlit
        st.write("List of tables\n")

        # printing a list of all current tables
        list_tables = (cursor.fetchall())

        # send it to streamlit
        # add header
        # (https://docs.streamlit.io/develop/api-reference/data/st.dataframe)
        st.dataframe(list_tables,
            column_config={ "name": "Table Name"}
            )

        # close the connection
        conn.close()
        curr_datetime = datetime.now()
        print("the sqlite connection for admin functions is closed at:", curr_datetime)

    except sqlite3.Error as error:
        print("Failed to execute the above query", error)

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
