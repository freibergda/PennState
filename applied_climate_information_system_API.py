''''''
import requests
import json
import pandas as pd
from urllib.parse import urlencode

def elem_template(field):
    return {
        "name": field,
        "interval": [1, 0, 0],
        "duration": 1,
        "reduce": "mean"
    }

def fetch_historical_weather(start_month: int, start_day: int, sid: str):
    """
    Fetch average historical weather data for a given start date and the following seven days from a specific station.
    """
    urlbase = "http://data.rcc-acis.org/StnData"
    elems = ["maxt", "mint", "pcpn"]

    results = []

    # Loop to get data for the given date and the 7 days following
    for offset in range(8):
        sdate = pd.Timestamp(year=1860, month=start_month, day=start_day) + pd.Timedelta(days=offset)
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
            raise ValueError(f"No data found for the date {sdate.strftime('%Y-%m-%d')}.")

        # Convert response data into a DataFrame
        df = pd.DataFrame(response_data["data"], columns=["Date", *elems])

        # Convert values to numeric, coerce errors to NaN and drop Date column for mean calculation
        df[elems] = df[elems].apply(pd.to_numeric, errors='coerce')

        # Calculate the mean, skipping NaN values
        column_means = df[elems].mean()
        
        # Add the date to the means for clarity
        column_means["Date"] = sdate.strftime('%Y-%m-%d')
        results.append(column_means)

    # Combine the results into a single DataFrame
    final_df = pd.DataFrame(results)

    return final_df

# Fetch average historical weather data for June 1st and the following seven days for station ID "strc3"
historical_means = fetch_historical_weather(6, 1, "336346 2")
print(historical_means)