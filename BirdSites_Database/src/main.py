import streamlit as st
from display_birdsites_database_tables import display_all_tables
import create_birdsites_database
import make_admin_table
import make_locations_table
import make_groups_table
import make_locations_groups_table

#https://discuss.streamlit.io/t/how-to-increase-the-width-of-web-page/7697
st.set_page_config(layout="wide")
st.title('BirdSites Database')

def main():
    database_name = "BirdSites.db"
    create_birdsites_database.create_birdsites(database_name)
    make_admin_table.make_admin_table(database_name)
    make_locations_table.make_locations_table(database_name)
    make_groups_table.make_groups_table(database_name)
    make_locations_groups_table.make_locations_groups_table(database_name)

    tables = display_all_tables(database_name)
    
    st.header('List of tables')
    for (table_name, columns) in tables:
        st.subheader(table_name)
        st.markdown(', '.join(columns))

if __name__ == "__main__":
    main()