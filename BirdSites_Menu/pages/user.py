'''Jira Task S8S4-61, S8S4-178, S8S4-63
User Story: As a User, I want the BirdSites database to create
a drop down box of states, for optional selection by the
User, alternatively, to display a drop down list of migratory 
flyways for User selection.  I want to display the results in a 
dashboard.
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

# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()

st.title("This page is available to all users")
st.markdown(
    f"You are currently logged in with the role of {st.session_state.role}.")

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

state_choice = 'None'
state_list = pd.read_sql_query(
    "select distinct state_full from locations", conn)
state_choice = st.sidebar.multiselect("Select State", state_list['state_full'].tolist())

now = datetime.datetime.now()
month = now.strftime("%m")

if int(month) < 3:
    season = "winter"
elif int(month) >= 3 and int(month) < 6:
    season = "spring_migration"
elif int(month) >= 6 and int(month) < 9:
    season = "summer"
elif int(month) >= 9 and int(month) < 11:
    season = "fall_migration"
else:
    season = "winter"

# Load the locations data
df = pd.read_sql_query("SELECT * FROM locations", conn)

# Load the groups data
gr = pd.read_sql_query("SELECT * FROM groups", conn)

# Handle flyway selection
if flyway_choice_corr != 'None':
    if flyway_choice_corr == 'atlantic_flyway':
        if season == 'spring_migration':
            gr_pick = gr.loc[(gr['atlantic_flyway'] == 'Y') & (gr['spring_migration'] == 'Y')]
        elif season == 'fall_migration':
            gr_pick = gr.loc[(gr['atlantic_flyway'] == 'Y') & (gr['fall_migration'] == 'Y')]
        elif season == 'summer':
            gr_pick = gr.loc[(gr['atlantic_flyway'] == 'Y') & (gr['summer'] == 'Y')]
        elif season == 'winter':
            gr_pick = gr.loc[(gr['atlantic_flyway'] == 'Y') & (gr['winter'] == 'Y')]
    elif flyway_choice_corr == 'central_flyway':
        if season == 'spring_migration':
            gr_pick = gr.loc[(gr['central_flyway'] == 'Y') & (gr['spring_migration'] == 'Y')]
        elif season == 'fall_migration':
            gr_pick = gr.loc[(gr['central_flyway'] == 'Y') & (gr['fall_migration'] == 'Y')]
        elif season == 'summer':
            gr_pick = gr.loc[(gr['central_flyway'] == 'Y') & (gr['summer'] == 'Y')]
        elif season == 'winter':
            gr_pick = gr.loc[(gr['central_flyway'] == 'Y') & (gr['winter'] == 'Y')]
    elif flyway_choice_corr == 'pacific_flyway':
        if season == 'spring_migration':
            gr_pick = gr.loc[(gr['pacific_flyway'] == 'Y') & (gr['spring_migration'] == 'Y')]
        elif season == 'fall_migration':
            gr_pick = gr.loc[(gr['pacific_flyway'] == 'Y') & (gr['fall_migration'] == 'Y')]
        elif season == 'summer':
            gr_pick = gr.loc[(gr['pacific_flyway'] == 'Y') & (gr['summer'] == 'Y')]
        elif season == 'winter':
            gr_pick = gr.loc[(gr['pacific_flyway'] == 'Y') & (gr['winter'] == 'Y')]
    
    lg = pd.read_sql_query("SELECT * FROM locations_groups", conn)

    grp_ids = lg[lg['group_id'].isin(gr_pick['group_id'])]

    selected_rows = df[df['location_id'].isin(grp_ids['location_id'])]

elif state_choice:
    selected_rows = df[df['state_full'].isin(state_choice)]

else:
    selected_rows = df.copy()

st.dataframe(selected_rows)
