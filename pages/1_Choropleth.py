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

from helper_functions import add_logo

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

add_logo()

gc.collect()

# import pickle 

map_2 = KeplerGl()
# with open('data/msoa_casualties_5yr_quantile.geojson', 'r') as f:
#     geojson = f.read()

gj = gpd.read_file('data/msoa_casualties_5yr_quantile.geojson')

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

map_2.config = config


map_2.add_data(data=gj, name='geojson')

del gj
gc.collect()

keplergl_static(map_2, height=800)

st.markdown(
    """
    Data provided under OGL v3.0. 
    www.nationalarchives.gov.uk/doc/open-government-licence/version/3/

    Data gathered using R stats19 package.

    https://github.com/ropensci/stats19
    
    Lovelace, Robin, Malcolm Morgan, Layik Hama, Mark Padgham, and M Padgham. 2019. “Stats19 A Package for Working with Open Road Crash Data.” Journal of Open Source Software 4 (33): 1181. https://doi.org/10.21105/joss.01181.
    """
)