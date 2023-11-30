import streamlit as st
import geopandas as gpd
import gc
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from helper_functions import add_logo

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

add_logo()

if 'map_kepler' in globals():
    del map_kepler
gc.collect()

map_kepler = KeplerGl()

@st.cache_data
def load_data():
    df = gpd.read_file('data/msoa_casualties_5yr_quantile.geojson')[["geometry", "casualty_counts_5_years_n", "collision_counts_5_years_n"]]
    return df

gj = load_data()

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

map_kepler.config = config

map_kepler.add_data(data=gj, name='geojson')

keplergl_static(map_kepler, height=800)

st.markdown(
    """
    Data provided under OGL v3.0. 
    www.nationalarchives.gov.uk/doc/open-government-licence/version/3/

    Data gathered using R stats19 package.

    https://github.com/ropensci/stats19
    
    Lovelace, Robin, Malcolm Morgan, Layik Hama, Mark Padgham, and M Padgham. 2019. “Stats19 A Package for Working with Open Road Crash Data.” Journal of Open Source Software 4 (33): 1181. https://doi.org/10.21105/joss.01181.
    """
)