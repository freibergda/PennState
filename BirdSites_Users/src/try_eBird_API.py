# try eBird API
from ebird.api import get_nearby_observations
import streamlit as st
# Get the most recent sightings of all species seen in the last week within 
# 10km of Point Reyes National Seashore.
# st.secrets gets the API key from the global secrets file (%userprofile%/.streamlit/secrets.toml)
point_reyes_records = get_nearby_observations(st.secrets["eBird_API"], 38.05, -122.94, dist=10, back=7)

print("Point Reyes: ")
print(point_reyes_records)

#dallas_records = get_nearby_observations("bqrqjm1r32an", 32.7767,-96.7970, dist=20, back=7)

#print("Dallas: ")
#print(dallas_records)
