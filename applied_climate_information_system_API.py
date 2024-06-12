'''Jira Task S8S4-159 As a User, I want a connection to the Applied Climate Information 
System (ACIS) http://data.rcc-acis.org/StnData so that I can automatically receive a 
report with the individual historical mean daily high temperature, low 
temperature, and precipitation for a period of 7 days starting from a future 
date that I specify for a weather station linked to a record in the BirdSites 
database.  I want to see the results displayed on the dashboard for a birding 
site record that I’ve selected from the BirdSites database.
Acceptance Criteria:
Given: the BirdSites database 
When: the User selects a birding site to display from a list of sites that 
match the User's selected parameters (future date, groups selection)
Then: the historical mean daily high temperature, low temperature, and precipitation for 
a period of 7 days starting from the User's future date are displayed on the 
dashboard for the selected birding site
Variables: database_name (BirdSites)
Parameters: "sid": sid,  # Station ID
            "sdate": sdate.strftime('%Y-%m-%d'),
            "edate": edate,
            "elems": [elem_template(field) for field in elems]'''

import json
from urllib.parse import urlencode
import requests
import pandas as pd
import streamlit as st


def elem_template(field):
    '''Set up the template used for the params in fetch_historical_weather '''
    return {
        "name": field,
        "interval": [1, 0, 0],
        "duration": 1,
        "reduce": "mean"
    }


def fetch_historical_weather(start_month: int, start_day: int, sid: str):
    '''Fetch average historical weather data for a given future start date 
    and the following seven days from a specific weather station.'''

    urlbase = "http://data.rcc-acis.org/StnData"
    elems = ["maxt", "mint", "pcpn"]

    results = []

    # Loop to get data for the given date and the 7 days following
    # using the max historical year of 1860 (%Y)
    for offset in range(8):
        sdate = pd.Timestamp(year=1860, month=start_month,
                             day=start_day) + pd.Timedelta(days=offset)
        edate = pd.Timestamp.today().strftime('%Y-%m-%d')

        params = {
            "sid": sid,  # Station ID
            "sdate": sdate.strftime('%Y-%m-%d'),
            "edate": edate,
            "elems": [elem_template(field) for field in elems]
        }

        query = urlencode({"params": json.dumps(params)})

        url = f"{urlbase}?{query}"

        response = requests.get(url)
        response_data = response.json()

        if 'data' not in response_data:
            ''' if it can't find the month/day in the database for the weather site'''
            raise ValueError(
                f"No data found for the date {sdate.strftime('%m-%d')}.")  # month/day

        # Convert response data into a DataFrame
        df = pd.DataFrame(response_data["data"], columns=["Date", *elems])

        # Convert values to numeric, coerce errors to NaN and drop Date column for mean calculation
        df[elems] = df[elems].apply(pd.to_numeric, errors='coerce')

        # Calculate the mean, skipping NaN values
        column_means = df[elems].mean()

        # Add the date to the means for clarity, but only the month & day
        column_means["Date"] = sdate.strftime('%m-%d')
        results.append(column_means)

    # Combine the results into a single DataFrame
    final_df = pd.DataFrame(results)

    return final_df


# Fetch average historical weather data for June 1st and the following seven 
# days for station ID "strc3"
# REMOVE THIS WHEN DONE - this is the sample function call and display
historical_means = fetch_historical_weather(6, 1, "336346 2")
print(historical_means)
# display on streamlit
st.dataframe(historical_means)
