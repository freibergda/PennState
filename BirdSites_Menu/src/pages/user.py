'''Jira Task S8S4-61, S8S4-178, S8S4-176, S8S4-63
User Story: As a User, I want the BirdSites database to create
a drop down box of states, for optional selection by the
User, alternatively, to display a drop down list of migratory 
flyways for User selection.  I want to display the results in a 
dashboard, filtered also by the current season if the user chose
a flyway.
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
from menu import menu_with_redirect  # Ensure this path is correct
import plotly.express as px
import plotly.graph_objects as go
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, ColumnsAutoSizeMode
from ebird.api import get_nearby_observations
import requests

def get_current_season():
    '''Calculate the current season'''
    now = datetime.datetime.now()
    month = now.month
    if month < 3:
        return "winter"
    elif 3 <= month < 6:
        return "spring_migration"
    elif 6 <= month < 9:
        return "summer"
    elif 9 <= month < 11:
        return "fall_migration"
    return "winter"

def get_forecast_data(lat, lon):
    '''NWS API calls - calls API once, reads the returned 
    json file, finds the forecast URL for file, then calls it 
    (which in turn returns a second json file which has the 
    forecast data)'''
    points_url = f"https://api.weather.gov/points/{lat},{lon}"
    response = requests.get(points_url)
    data = response.json()

    # Extract forecast URL
    forecast_url = data['properties']['forecast']
    forecast_response = requests.get(forecast_url)
    forecast_data = forecast_response.json()

    # Extract periods information
    periods = forecast_data['properties']['periods']
    return periods

def parse_forecast_data(periods):
    '''Get the 7 day period, temp highs and lows, precips days and night'''
    dates = [period['startTime'][:10] for period in periods if period['isDaytime']]
    highs = [period['temperature'] for period in periods if period['isDaytime']]
    lows = [period['temperature'] for period in periods if not period['isDaytime']]
    precip_day = [period.get('probabilityOfPrecipitation', {}).get('value', 0) if period.get('probabilityOfPrecipitation', {}).get('value') is not None else 0 for period in periods if period['isDaytime']]
    precip_night = [period.get('probabilityOfPrecipitation', {}).get('value', 0) if period.get('probabilityOfPrecipitation', {}).get('value') is not None else 0 for period in periods if not period['isDaytime']]

    # Extract wind speed and direction data
    wind_day = [period['windSpeed'] for period in periods if period['isDaytime']]
    wind_night = [period['windSpeed'] for period in periods if not period['isDaytime']]
    dir_day = [period['windDirection'] for period in periods if period['isDaytime']]
    dir_night = [period['windDirection'] for period in periods if not period['isDaytime']]

    return {
        'dates': dates[:len(lows)],
        'highs': highs[:len(lows)],
        'lows': lows,
        'precip_day': precip_day[:len(lows)],
        'precip_night': precip_night,
        'wind_day': wind_day[:len(lows)],
        'wind_night': wind_night,
        'dir_day': dir_day[:len(lows)],
        'dir_night': dir_night[:len(lows)],
    }

def plot_forecast_data(forecast):
    '''Make a panda with the dates, highs and lows, 
    make a scatterplot'''
    if forecast:
        df = pd.DataFrame({
            'Date': forecast['dates'],
            'High': forecast['highs'],
            'Low': forecast['lows']
        })
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['Date'], y=df['High'], mode='lines+markers', name='High Temp (°F)'))
        fig.add_trace(go.Scatter(x=df['Date'], y=df['Low'], mode='lines+markers', name='Low Temp (°F)'))
        fig.update_layout(title='7-Day Temperature Forecast', xaxis_title='Date', yaxis_title='Temperature (°F)')
        st.plotly_chart(fig)
    else:
        st.error("Forecast data is empty!")

def plot_precip_data(forecast):
    '''Make a panda with the dates, day and night precip, 
    make a scatterplot'''
    if forecast:
        df = pd.DataFrame({
            'Date': forecast['dates'],
            'Precipitation Day': forecast['precip_day'],
            'Precipitation Night': forecast['precip_night']
        })
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['Date'], y=df['Precipitation Day'], mode='lines+markers', name='Precipitation Day'))
        fig.add_trace(go.Scatter(x=df['Date'], y=df['Precipitation Night'], mode='lines+markers', name='Precipitation Night'))
        fig.update_layout(title='7-Day Precipitation Forecast', xaxis_title='Date', yaxis_title='Precipitation (%)')
        st.plotly_chart(fig)
    else:
        st.error("Forecast data is empty!")

def main():
    '''Redirect to app.py if not logged in, otherwise show 
    the navigation menu'''
    menu_with_redirect()

    curr_season = get_current_season()

    st.subheader("This page is available to all users")
    st.markdown(f"You are currently logged in with the role of {st.session_state.role}.")
    st.title('Birding Locations in the Continental United States')
    st.header('Flyway choices are filtered by the current season')
    st.markdown(f'The current season is: {curr_season}')
    st.header('State choices are not filtered by the current season')

    conn = sqlite3.connect(r'C:\Users\freib\Desktop\PENN_STATE\SWENG_894_Capstone\BirdSites_Database\BirdSites.db')

    flyway = ['None', 'Atlantic Flyway', 'Central Flyway', 'Pacific Flyway']
    flyway_choice = st.sidebar.radio("Select flyway", flyway)

    flyway_dict = {
        'Atlantic Flyway': 'atlantic_flyway',
        'Central Flyway': 'central_flyway',
        'Pacific Flyway': 'pacific_flyway',
        'None': 'None'
    }

    flyway_choice_corr = flyway_dict.get(flyway_choice, 'None')

    state_list = pd.read_sql_query("SELECT DISTINCT state_full FROM locations", conn)
    state_choice = st.sidebar.multiselect("Select State", state_list['state_full'].tolist())

    df = pd.read_sql_query("SELECT * FROM locations", conn)
    gr = pd.read_sql_query("SELECT * FROM groups", conn)

    selected_rows = pd.DataFrame()

    if flyway_choice_corr != 'None':
        flyway_filter = gr[flyway_choice_corr] == 'Y'
        season_filter = gr[curr_season] == 'Y'
        gr_pick = gr[flyway_filter & season_filter]

        lg = pd.read_sql_query("SELECT * FROM locations_groups", conn)
        grp_ids = lg[lg['group_id'].isin(gr_pick['group_id'])]
        selected_rows = df[df['location_id'].isin(grp_ids['location_id'])]

    elif state_choice:
        selected_rows = df[df['state_full'].isin(state_choice)]
    else:
        selected_rows = df

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

    if not sel_rows.empty:
        selected_row = sel_rows.iloc[0]
        col1, col2, col3, col4, col5, col6 = st.columns(6)

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

        selected_geo = pd.DataFrame(sel_rows)[['location_full_name', 'latitude', 'longitude']]
        st.info("Hover over the map to see the filtered site that you have chosen and their coordinates")
        fig = px.scatter_mapbox(selected_geo, lat="latitude", lon="longitude", hover_name="location_full_name", zoom=3)
        fig.update_layout(mapbox_style="open-street-map", margin={"r":0, "t":0, "l":0, "b":0})
        st.plotly_chart(fig)

        st.info("7 Day Temperature and Precipitation forecast for: "+ selected_row['location_full_name'])
        periods = get_forecast_data(selected_row['latitude'], selected_row['longitude'])
        forecast = parse_forecast_data(periods)
        plot_forecast_data(forecast)
        plot_precip_data(forecast)

        # Extract wind data
        wind_day = forecast['wind_day']
        wind_night = forecast['wind_night']
        dir_day = forecast['dir_day']
        dir_night = forecast['dir_night']

        # Create a DataFrame for wind speed and direction
        combined_wind = pd.DataFrame({
            'Date': forecast['dates'],
            'Wind Speed Day': wind_day,
            'Wind Direction Day': dir_day,
            'Wind Speed Night': wind_night,
            'Wind Direction Night': dir_night
        })
        st.write('7 Day Wind Speed and Direction forecast')
        st.write(combined_wind)

        st.info("Current bird sightings by species within 10 miles of "+ selected_row['location_full_name'] + " during the last 7 days. Click on the icons to expand.")
        api_Key = st.secrets["my_cool_secrets"]["eBird_API"]
        records = get_nearby_observations(api_Key, selected_row['latitude'], selected_row['longitude'], dist=10, back=7)
        st.write(records)
    else:
        st.warning("No rows selected or no data available.")

if __name__ == '__main__':
    main()


