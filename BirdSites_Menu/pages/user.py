'''Jira Task S8S4-61, S8S4-178, S8S4-63
User Story: As a User, I want the BirdSites database to create
a drop down box of states, for optional selection by the
User, alternatively, to display a drop down list of migratory 
flyways for User selection.  I want to display the results in a 
dashboard, filtered also by the current season.
Unit Tests:
System Test:
Acceptance Criteria:
Given: A user wants to travel within the next 24 hours
When:  The user selects the User Path from the Menu (User Path 2)
Then:  The system creates a drop down box of all states in
the BirdSites database, and counties in the state, if selected
Variables: none
Parameters: none'''
import datetime
import sqlite3
import streamlit as st
import pandas as pd
from menu import menu_with_redirect
import plotly.express as px
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, ColumnsAutoSizeMode
from ebird.api import get_nearby_observations

# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()

# Calculate current season for display and flyway filtering
now = datetime.datetime.now()
month = now.strftime("%m")
if int(month) < 3:
    curr_season = "winter"
elif int(month) >= 3 and int(month) < 6:
    curr_season = "spring_migration"
elif int(month) >= 6 and int(month) < 9:
    curr_season = "summer"
elif int(month) >= 9 and int(month) < 11:
    curr_season = "fall_migration"
else:
    curr_season = "winter"

st.subheader("This page is available to all users")
st.markdown(f"You are currently logged in with the role of {st.session_state.role}.")
st.title('Birding Locations in the Continental United States')
st.header('Flyway choices are filtered by the current season')
st.markdown(f'The current season is: {curr_season}')
st.header('State choices are not filtered by the current season')

# Connect to the SQLite database
conn = sqlite3.connect(
    r'C:\Users\freib\Desktop\PENN_STATE\SWENG_894_Capstone\BirdSites_Database\BirdSites.db')

flyway = ['None', 'Atlantic Flyway', 'Central Flyway', 'Pacific Flyway']
flyway_choice = st.sidebar.radio("Select flyway", flyway)

if flyway_choice == 'Atlantic Flyway':
    flyway_choice_corr = 'atlantic_flyway'
elif flyway_choice == 'Central Flyway':
    flyway_choice_corr = 'central_flyway'
elif flyway_choice == 'Pacific Flyway':
    flyway_choice_corr = 'pacific_flyway'
else:
    flyway_choice_corr = 'None'

state_list = pd.read_sql_query("SELECT DISTINCT state_full FROM locations", conn)
state_choice = st.sidebar.multiselect("Select State", state_list['state_full'].tolist())

# Load the locations data
df = pd.read_sql_query("SELECT * FROM locations", conn)

# Load the groups data
gr = pd.read_sql_query("SELECT * FROM groups", conn)

# Handle flyway selection
if flyway_choice_corr != 'None':
    if flyway_choice_corr == 'atlantic_flyway':
        if curr_season == 'spring_migration':
            gr_pick = gr.loc[(gr['atlantic_flyway'] == 'Y') & (gr['spring_migration'] == 'Y')]
        elif curr_season == 'fall_migration':
            gr_pick = gr.loc[(gr['atlantic_flyway'] == 'Y') & (gr['fall_migration'] == 'Y')]
        elif curr_season == 'summer':
            gr_pick = gr.loc[(gr['atlantic_flyway'] == 'Y') & (gr['summer'] == 'Y')]
        elif curr_season == 'winter':
            gr_pick = gr.loc[(gr['atlantic_flyway'] == 'Y') & (gr['winter'] == 'Y')]
    elif flyway_choice_corr == 'central_flyway':
        if curr_season == 'spring_migration':
            gr_pick = gr.loc[(gr['central_flyway'] == 'Y') & (gr['spring_migration'] == 'Y')]
        elif curr_season == 'fall_migration':
            gr_pick = gr.loc[(gr['central_flyway'] == 'Y') & (gr['fall_migration'] == 'Y')]
        elif curr_season == 'summer':
            gr_pick = gr.loc[(gr['central_flyway'] == 'Y') & (gr['summer'] == 'Y')]
        elif curr_season == 'winter':
            gr_pick = gr.loc[(gr['central_flyway'] == 'Y') & (gr['winter'] == 'Y')]
    elif flyway_choice_corr == 'pacific_flyway':
        if curr_season == 'spring_migration':
            gr_pick = gr.loc[(gr['pacific_flyway'] == 'Y') & (gr['spring_migration'] == 'Y')]
        elif curr_season == 'fall_migration':
            gr_pick = gr.loc[(gr['pacific_flyway'] == 'Y') & (gr['fall_migration'] == 'Y')]
        elif curr_season == 'summer':
            gr_pick = gr.loc[(gr['pacific_flyway'] == 'Y') & (gr['summer'] == 'Y')]
        elif curr_season == 'winter':
            gr_pick = gr.loc[(gr['pacific_flyway'] == 'Y') & (gr['winter'] == 'Y')]

    lg = pd.read_sql_query("SELECT * FROM locations_groups", conn)

    grp_ids = lg[lg['group_id'].isin(gr_pick['group_id'])]

    selected_rows = df[df['location_id'].isin(grp_ids['location_id'])]

elif state_choice:
    selected_rows = df[df['state_full'].isin(state_choice)]
else:
    selected_rows = df.copy()

# Display filtered data in AgGrid
gb = GridOptionsBuilder.from_dataframe(selected_rows[["location_full_name", "state_full"]])
gb.configure_selection(selection_mode="single", use_checkbox=True)
gb.configure_side_bar()
gridOptions = gb.build()

data = AgGrid(
    selected_rows,
    gridOptions=gridOptions,
    enable_enterprise_modules=True,
    allow_unsafe_jscode=True,
    update_mode=GridUpdateMode.SELECTION_CHANGED,
    columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS
)

sel_rows = pd.DataFrame(data["selected_rows"])

# Ensure sel_rows is not empty
if not sel_rows.empty:
    selected_row = sel_rows.iloc[0]  # Single selection ensures only one row
    col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns(9)

    with col1:
        st.markdown("##### Site Name")
        st.markdown(f":orange[{selected_row['location_full_name']}]")
    with col2:
        st.markdown("##### County")
        st.markdown(f":orange[{selected_row['county']}]")
    with col3:
        st.markdown("##### State")
        st.markdown(f":orange[{selected_row['state_full']}]")
    with col4:
        st.markdown("##### Latitude")
        st.markdown(f":orange[{selected_row['latitude']}]")
    with col5:
        st.markdown("##### Longitude")
        st.markdown(f":orange[{selected_row['longitude']}]")
    with col6:
        st.markdown("##### Link to Park")
        st.markdown(f":orange[{selected_row['link_to_park']}]")

    # Select geo
    selected_geo = pd.DataFrame(sel_rows)[['location_full_name', 'latitude', 'longitude']]
    st.info("Hover over the map to see the filtered sites that you have chosen and their coordinates")
    fig = px.scatter_mapbox(selected_geo, lat="latitude", lon="longitude", hover_name="location_full_name", zoom=3)

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0, "t":0, "l":0, "b":0})

    st.plotly_chart(fig)
else:
    st.warning("No rows selected or no data available.")
# fix for future
#st.info('eBird demonstration nested list for 10 miles out, period last 7 days: ','latitude','','longitude')
api_Key = st.secrets["my_cool_secrets"]["eBird_API"]

# fix for future needs abs values
#records = get_nearby_observations(api_Key, 'latitude', 'longitude', dist=10, back=7)    

records = get_nearby_observations(api_Key, 39.885866, -75.262356, dist=10, back=7)
st.write(records)
