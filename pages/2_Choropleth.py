import gc
import streamlit as st
import geopandas as gpd
# from streamlit_keplergl import keplergl_static
# from keplergl import KeplerGl
from helper_functions import add_logo, center_running
import leafmap.kepler as leafmap


st.set_page_config(layout="wide", initial_sidebar_state="expanded")

add_logo()

center_running()

# Import the stylesheet
with open("style.css") as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

gc.collect()

st.title("Choropleth - Collisions and Casualties in the UK by MSOA: 2018 - 2022 inclusive")

@st.cache_data(ttl=0.5*3600, max_entries=5)
def load_data(path):
    df = gpd.read_file(path)[["geometry", "casualty_counts_5_years_n", "collision_counts_5_years_n"]]
    return df

colour_by = st.radio("Colour areas by which count?", 
                     ["casualty_counts_5_years_n", 
                     "collision_counts_5_years_n"],
                     format_func= lambda x: x.replace("_n", "").replace("_", " ").title(),
                     horizontal=True)

gj = load_data('data/msoa_casualties_5yr_quantile.geojson')

value_filter = st.slider("Filter by value", 
                        min_value = gj[colour_by].min(), 
                        max_value=gj[colour_by].max(),
                        value=(gj[colour_by].min(), gj[colour_by].max()))

gj_filtered = gj[
    (gj[colour_by] >= value_filter[0]) & 
    (gj[colour_by] <= value_filter[1])
    ]

# map_kepler = KeplerGl()
map_kepler = leafmap.Map()

config = {'version': 'v1',
 'config': {'visState': {'filters': [],
   'layers': [{'id': 'o9ae87',
     'type': 'geojson',
     'config': {'dataId': 'geojson',
      'label': 'geojson',
      'color': [18, 147, 154],
      'highlightColor': [252, 242, 26, 255],
      'columns': {'geojson': 'geometry'},
      'isVisible': True,
      'visConfig': {'opacity': 0.8,
       'strokeOpacity': 0.8,
       'thickness': 0.5,
       'strokeColor': [221, 178, 124],
       'colorRange': {'name': 'ColorBrewer Reds-6',
        'type': 'singlehue',
        'category': 'ColorBrewer',
        'colors': ['#fee5d9',
         '#fcbba1',
         '#fc9272',
         '#fb6a4a',
         '#de2d26',
         '#a50f15']},
       'strokeColorRange': {'name': 'Global Warming',
        'type': 'sequential',
        'category': 'Uber',
        'colors': ['#5A1846',
         '#900C3F',
         '#C70039',
         '#E3611C',
         '#F1920E',
         '#FFC300']},
       'radius': 10,
       'sizeRange': [0, 10],
       'radiusRange': [0, 50],
       'heightRange': [0, 500],
       'elevationScale': 5,
       'enableElevationZoomFactor': True,
       'stroked': False,
       'filled': True,
       'enable3d': False,
       'wireframe': False},
      'hidden': False,
      'textLabel': [{'field': None,
        'color': [255, 255, 255],
        'size': 18,
        'offset': [0, 0],
        'anchor': 'start',
        'alignment': 'center'}]},
     'visualChannels': {'colorField': {'name': f'{colour_by}',
       'type': 'integer'},
      'colorScale': 'quantile',
      'strokeColorField': None,
      'strokeColorScale': 'quantile',
      'sizeField': None,
      'sizeScale': 'linear',
      'heightField': None,
      'heightScale': 'linear',
      'radiusField': None,
      'radiusScale': 'linear'}}],
   'interactionConfig': {'tooltip': {'fieldsToShow': {'geojson': [{'name': 'casualty_counts_5_years_n',
        'format': None},
       {'name': 'collision_counts_5_years_n', 'format': None}]},
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
#    'latitude': 54.19397555891801,
#    'longitude': -0.7912245261020198,
   'pitch': 0,
#    'zoom': 5.531214148679788,
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
   
      "mapStyles": {
        # "vw22uhl": {
        #   "accessToken": "pk.eyJ1IjoidWJlcmRhdGEiLCJhIjoidGllX1gxUSJ9.gElUooDF7u51guCQREmAhg",
        #   "custom": true,
        #   "icon": "https://api.mapbox.com/styles/v1/uberdata/ck14353fm0vml1dqttzcnzgm7/static/-122.3391,37.7922,9,0,0/400x300?access_token=pk.eyJ1IjoidWJlcmRhdGEiLCJhIjoidGllX1gxUSJ9.gElUooDF7u51guCQREmAhg&logo=false&attribution=false",
        #   "id": "vw22uhl",
        #   "label": "Kepler.gl Flight Map",
        #   "url": "mapbox://styles/uberdata/ck14353fm0vml1dqttzcnzgm7"
        # },
        "rjoz7wd": {
          "accessToken": None,
          "custom": True,
          "icon": "",
          "id": "rjoz7wd",
          "label": "Street",
          "url": "mapbox://styles/mapbox/streets-v12"
        }
   
   }
   }}}

map_kepler.config = config

map_kepler.add_data(data=gj_filtered, name='geojson')
del gj_filtered
gc.collect()

# keplergl_static(map_kepler, height=800)
map_kepler.to_streamlit(height=800)

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