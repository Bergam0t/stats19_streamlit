import gc
from datetime import datetime
import streamlit as st
import pandas as pd
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from helper_functions import add_logo

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

add_logo()

@st.cache_data(ttl=0.5*3600, max_entries=10)
def load_data(path):
    df = pd.read_csv(path)
    return df

stats19_collision = load_data("data/stats19_collision_2022_minimal.csv")

stats19_collision = stats19_collision[(stats19_collision["latitude"].notnull())&
                                      (stats19_collision["longitude"].notnull())]

options = stats19_collision.drop(
  columns=["accident_index","accident_reference", "longitude", 
           "latitude", "lsoa_of_accident_location", "time", "date"]).columns.tolist()
options.remove("accident_severity")
options.insert(0, "accident_severity")

colour_points_by = st.radio(
    label="Choose a value to colour the points by",
    options=options,
    horizontal=True, 
    format_func = lambda x: x.replace("_", " ").title()
)

del options
gc.collect()

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

filtered = stats19_collision[[colour_points_by,
                              'longitude',
                              'latitude'
                             ]]

select_display_method = st.radio(
    "Select display type", 
    ["point", "hexagon", "heatmap"], 
    format_func = lambda x: x.title(),     
    horizontal=True)

map_kepler = KeplerGl()
map_kepler.add_data(data=filtered,
               name="collisions")
      
del filtered
gc.collect()

config = {'version': 'v1',
 'config': {'visState': {'filters': [],
   'layers': [{'id': 's5bh44p',
     'type': f'{select_display_method}',
     'config': {'dataId': 'collisions',
      'label': 'Point',
      'color': [18, 147, 154],
      'highlightColor': [252, 242, 26, 255],
      'columns': {'lat': 'latitude', 'lng': 'longitude', 'altitude': None},
      'isVisible': True,
      'visConfig': {'radius': 10,
       'fixedRadius': False,
       'opacity': 0.8,
       'outline': False,
       'thickness': 2,
       'strokeColor': None,
       'colorRange': {'name': 'Global Warming',
        'type': 'sequential',
        'category': 'Uber',
        'colors': ['#5A1846',
         '#900C3F',
         '#C70039',
         '#E3611C',
         '#F1920E',
         '#FFC300']},
       'strokeColorRange': {'name': 'Global Warming',
        'type': 'sequential',
        'category': 'Uber',
        'colors': ['#5A1846',
         '#900C3F',
         '#C70039',
         '#E3611C',
         '#F1920E',
         '#FFC300']},
       'radiusRange': [0, 50],
       'filled': True},
      'hidden': False,
      'textLabel': [{'field': None,
        'color': [255, 255, 255],
        'size': 18,
        'offset': [0, 0],
        'anchor': 'start',
        'alignment': 'center'}]},
     'visualChannels': {'colorField': {'name': f'{colour_points_by}',
       'type': 'string'},
      'colorScale': 'ordinal',
      'strokeColorField': None,
      'strokeColorScale': 'quantile',
      'sizeField': None,
      'sizeScale': 'linear'}}],
   'interactionConfig': {'tooltip': {'fieldsToShow': {'collisions': [{'name': 'accident_severity',
        'format': None}]},
     'compareMode': False,
     'compareType': 'absolute',
     'enabled': True},
    'brush': {'size': 0.5, 'enabled': False},
    'geocoder': {'enabled': False},
    'coordinate': {'enabled': False}},
   'layerBlending': 'normal',
   'splitMaps': [],
   'animationConfig': {'currentTime': None, 'speed': 1}},
  'mapState': {'bearing': 0,
   'dragRotate': False,
  #  'latitude': 54.2017205,
  #  'longitude': -1.9605770000000002,
   'pitch': 0,
  #  'zoom': 5,
      'latitude': 55.435,
    'longitude': -2.09426,
    'zoom': 4.75,
   'isSplit': False},
  'mapStyle': {'styleType': 'dark',
   'topLayerGroups': {},
   'visibleLayerGroups': {'label': True,
    'road': True,
    'border': False,
    'building': True,
    'water': True,
    'land': True,
    '3d building': False},
   'threeDBuildingColor': [9.665468314072013,
    17.18305478057247,
    31.1442867897876],
   'mapStyles': {}}}}

map_kepler.config = config

keplergl_static(map_kepler, height=800)

st.download_button('Download config', str(map_kepler.config))

del map_kepler
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