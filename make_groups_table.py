'''This module will create the groups table in the BirdSites database '''
import sqlite3


def make_groups_table(database_name):
    '''this module creates the groups table'''
    # call sqlite3
    try:
        #con = sqlite3.connect("BirdSites.db")
        con = sqlite3.connect(database_name)
        cur = con.cursor()
        cur.execute("CREATE TABLE if not exists groups(pk_grp INTEGER PRIMARY KEY,\
                    spring_migration TEXT, fall_migration TEXT, summer TEXT, \
                    winter TEXT, atlantic_flyway TEXT, pacific_flyway TEXT)")
        con.commit()
        con.close()
        print("The SQLite connection is closed")

    except sqlite3.Error as error:
        print("Error while connecting to SQLite make_groups_table ", error)

    return
