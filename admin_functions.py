'''This is the admin_functions.py'''
import sqlite3
import streamlit as st


def make_database():
    '''this module creates the database'''
    # call sqlite3
    con = sqlite3.connect("BirdSites.db")
    cur = con.cursor()
    cur.execute("drop table if exists locations")
    cur.execute("CREATE TABLE if not exists locations(pk_loc, loc_full_name, county_name, state_name, geolocation, linkToNWSSite, linkToParkWebSite, linkToeBirdSite, linkToBirdCastSite)")
    con.commit()
    con.close()
    return

def fill_database():
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
    '''this is the main module'''
    make_database()
    fill_database()
    st.set_page_config(layout="wide")
    st.title("BirdSites Database")
    new_con = sqlite3.connect("BirdSites.db")
    new_cur = new_con.cursor()
    for row in new_cur.execute("SELECT pk_loc, loc_full_name, county_name, state_name, geolocation, linkToNWSSite, linkToParkWebSite, linkToeBirdSite, linkToBirdCastSite FROM locations"):
        # print(row)
        # st.write(row)
        # st.write(str(row))
        # converted = ''.join([str(x) for x in row])
        # st.write(converted)
        # disp_row = ''
        # for i in range(len(row)):
        # disp_row = disp_row + str(row[i]) +'\t'
        # st.write(disp_row)
        disp_row = 'hello '
        for i in range(len(row)):
            disp_row = disp_row + (str(row[i]))
        st.write(disp_row)

if __name__ == "__main__":
    main()
