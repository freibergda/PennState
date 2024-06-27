import os
import pytest
#from src.create_birdsites_database import create_birdsites
#from src.make_admin_table import make_admin_table
#from src.make_locations_table import make_locations_table
#from src.make_groups_table import make_groups_table
#from src.make_locations_groups_table import make_locations_groups_table
#from src.display_birdsites_database_tables import display_all_tables

@pytest.fixture(scope="module")
def setup_database():
    database_name = "uat_BirdSites.db"
    if os.path.exists(database_name):
        os.remove(database_name)
    yield database_name
    if os.path.exists(database_name):
        os.remove(database_name)