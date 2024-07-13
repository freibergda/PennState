'''Jira Task S8S4-178
User Story: As a User, I want the BirdSites database to create
a drop down box of states, for optional selection by the
User, and counties within a state, if a state is selected.
Unit Tests:
System Test:
Acceptance Criteria:
Given: A user wants to travel within the next 24 hours
When:  The user selects the User Path from the Menu (User Path 2)
Then:  The system creates a drop down box of all states in
the BirdSites database, and counties in the state, if selected
Variables: none
Parameters: none'''
from datetime import datetime
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
flyway_choice = 'None'
flyway_choice = st.sidebar.radio("Select flyway", flyway)
st.write("You selected:", flyway_choice)
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
state_choice = st.sidebar.multiselect("Select State", state_list)
st.write("You selected:", state_choice)

now = datetime.now()

month = now.strftime("%m")
st.write("month:", month)

if int(month) < 3:
    season = "winter"
elif int(month) >= 3 and int(month) < 6:
    season = "spring_migration"
elif int(month) >= 6 and int(month) < 9:
    season = "summer"
elif int(month) >= 9 & int(month) < 11:
    season = "fall_migration"
else:
    season = "winter"

st.write("season: ", season)

df = pd.read_sql_query("SELECT * FROM locations", conn)
st.write(df)
state_set = df.loc[df['state_full'].isin(state_choice)]
st.write(state_set)

gr = pd.read_sql_query("SELECT * FROM groups", conn)
st.write(gr)

st.write(flyway_choice_corr)

# https://stackoverflow.com/questions/36921951/truth-value-of-a-series-is-ambiguous-use-a-empty-a-bool-a-item-a-any-o
if flyway_choice_corr != 'None':
    if flyway_choice_corr == 'atlantic_flyway':
        st.write("Atlantic: ", flyway_choice_corr, "season: ", season)
        if season == 'spring_migration':
            gr_a_pick = gr.loc[(gr['atlantic_flyway'] == 'Y')
                               & (gr['spring_migration'] == 'Y')]
            gr_a_pick_num = gr_a_pick['group_id']
        elif season == 'fall_migration':
            gr_a_pick = gr.loc[(gr['atlantic_flyway'] == 'Y')
                               & (gr['fall_migration'] == 'Y')]
            gr_a_pick_num = gr_a_pick['group_id']
        elif season == 'summer':
            gr_a_pick = gr.loc[(gr['atlantic_flyway'] == 'Y')
                               & (gr['summer'] == 'Y')]
            gr_a_pick_num = gr_a_pick['group_id']
        elif season == 'winter':
            gr_a_pick = gr.loc[(gr['atlantic_flyway'] == 'Y')
                               & (gr['winter'] == 'Y')]
            gr_a_pick_num = gr_a_pick['group_id']
        st.write(gr_a_pick)
        st.write(gr_a_pick_num)
    elif flyway_choice_corr == 'central_flyway':
        st.write("Central: ", flyway_choice_corr, "season: ", season)
        if season == 'spring_migration':
            gr_c_pick = gr.loc[(gr['central_flyway'] == 'Y')
                               & (gr['spring_migration'] == 'Y')]
            gr_c_pick_num = gr_c_pick['group_id']
        elif season == 'fall_migration':
            gr_c_pick = gr.loc[(gr['central_flyway'] == 'Y')
                               & (gr['fall_migration'] == 'Y')]
            gr_c_pick_num = gr_c_pick['group_id']
        elif season == 'summer':
            gr_c_pick = gr.loc[(gr['central_flyway'] == 'Y')
                               & (gr['summer'] == 'Y')]
            gr_c_pick_num = gr_c_pick['group_id']
        elif season == 'winter':
            gr_c_pick = gr.loc[(gr['central_flyway'] == 'Y')
                               & (gr['winter'] == 'Y')]
            gr_c_pick_num = gr_c_pick['group_id']
        st.write(gr_c_pick)
        st.write(gr_c_pick_num)        
    elif flyway_choice_corr == 'pacific_flyway':
        st.write("Pacific:  ", flyway_choice_corr)
        if season == 'spring_migration':
            gr_p_pick = gr.loc[(gr['pacific_flyway'] == 'Y')
                               & (gr['spring_migration'] == 'Y')]
            gr_p_pick_num = gr_p_pick['group_id']
        elif season == 'fall_migration':
            gr_p_pick = gr.loc[(gr['pacific_flyway'] == 'Y')
                               & (gr['fall_migration'] == 'Y')]
            gr_p_pick_num = gr_p_pick['group_id']
        elif season == 'summer':
            gr_p_pick = gr.loc[(gr['pacific_flyway'] == 'Y')
                               & (gr['summer'] == 'Y')]
            gr_p_pick_num = gr_p_pick['group_id']
        elif season == 'winter':
            gr_p_pick = gr.loc[(gr['pacific_flyway'] == 'Y')
                               & (gr['winter'] == 'Y')]
            gr_p_pick_num = gr_p_pick['group_id']
        st.write(gr_p_pick)
        st.write(gr_p_pick_num)
    else:
        st.write("Error!")

lg = pd.read_sql_query("SELECT * FROM locations_groups", conn)
st.write(lg)
