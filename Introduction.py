import streamlit as st
# Importing libraries
import pandas as pd
import numpy as np
import geopandas as gpd
import gc
# import folium
# from folium.plugins import FastMarkerCluster
# from streamlit_folium import st_folium

# import streamlit as st
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime
# import pickle

from helper_functions import add_logo



# m = folium.Map(location=[50.435, -5.09426], #50.26656, -5.09426
#                zoom_start=9.4)

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

add_logo()

gc.collect()

@st.cache_data
def load_data():
    df = pd.read_csv("data/stats19_collision_2022_minimal.csv")
    return df

stats19_collision = load_data()

stats19_collision = stats19_collision[(stats19_collision["latitude"].notnull())&
                                      (stats19_collision["longitude"].notnull())]



# m.add_child(FastMarkerCluster(stats19_collision[['latitude', 'longitude']].values.tolist()))

# markers = [[location_info[0], location_info[1]]
#  for location_info 
#  in stats19_collision[['latitude', 'longitude']].values.tolist()]

# [folium.Marker(i).add_to(m) for i in markers] 
# for index, location_info in stats19_collision[(stats19_collision["latitude"].notnull())&
#                                                (stats19_collision["longitude"].notnull())].iterrows():
#     folium.Marker([location_info["latitude"], location_info["longitude"]]).add_to(m)

# for i in markers:
#     folium.Marker(i).add_to(m)


# stats19_collision[(stats19_collision["latitude"].notnull())&(stats19_collision["longitude"].notnull())]


# map_data = st_folium(m, key="fig1", width=700, height=700)

# cols_to_stringify = stats19_collision.drop(columns=["accident_index","accident_reference", "longitude", "latitude", "lsoa_of_accident_location"]).columns.tolist()

# stats19_collision[cols_to_stringify] = stats19_collision[cols_to_stringify].astype(str)

colour_points_by = st.radio(
    label="Choose a value to colour the points by",
    options=stats19_collision.drop(columns=["accident_index","accident_reference", "longitude", "latitude", "lsoa_of_accident_location", "time", "date"]).columns.tolist(),
    horizontal=True
)

filter_points_by = st.multiselect(label="Filter", 
                                  options=stats19_collision[colour_points_by].drop_duplicates().sort_values().to_list(),
                                  default=stats19_collision[colour_points_by].drop_duplicates().sort_values().to_list())

stats19_collision = stats19_collision[stats19_collision[colour_points_by].isin(filter_points_by)]

date_filter = st.slider("Filter by date", 
                        min_value = datetime.strptime(stats19_collision['date'].min(), "%Y-%m-%d"), 
                        max_value=datetime.strptime(stats19_collision['date'].max(), "%Y-%m-%d"),
                        value=(datetime.strptime(stats19_collision['date'].min(), "%Y-%m-%d"), datetime.strptime(stats19_collision['date'].max(), "%Y-%m-%d")))

stats19_collision["date"] = pd.to_datetime(stats19_collision["date"], 
                                           format="%Y-%m-%d").astype("datetime64[ns]")

stats19_collision = stats19_collision[
    (stats19_collision["date"] >= date_filter[0]) & 
    (stats19_collision["date"] <= date_filter[1])
    ]

# filtered = stats19_collision[['longitude',
#                               'latitude',
#                               colour_points_by]]

filtered = stats19_collision.drop(columns=["accident_index","accident_reference", "lsoa_of_accident_location", "date"])
# filtered = filtered.astype(str) 


map_1 = KeplerGl()
map_1.add_data(data=filtered,
               name="collisions")

map_1.layout

config = {
    'version': 'v1',
    'config': {
        'mapState': {
            'latitude': 55.435,
            'longitude': -2.09426,
            'zoom': 4.75
        }
    }
}

map_1.config = config

keplergl_static(map_1, height=800)

del filtered
gc.collect()

st.markdown(
    """
    Data provided under OGL v3.0. 
    www.nationalarchives.gov.uk/doc/open-government-licence/version/3/

    Data gathered using R stats19 package.

    https://github.com/ropensci/stats19
    
    Lovelace, Robin, Malcolm Morgan, Layik Hama, Mark Padgham, and M Padgham. 2019. “Stats19 A Package for Working with Open Road Crash Data.” Journal of Open Source Software 4 (33): 1181. https://doi.org/10.21105/joss.01181.
    """
)