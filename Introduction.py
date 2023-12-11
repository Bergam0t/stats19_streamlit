import streamlit as st
from helper_functions import add_logo
import gc


st.set_page_config(layout="wide", initial_sidebar_state="expanded")

gc.collect()

add_logo()

# Import the stylesheet
with open("style.css") as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

st.header("Stats19 Data Explorer")

st.markdown(
    """
    This app accompanies the HSMA 6 open day QGIS workshop on 13/12/2023.
    """
)

st.subheader("Credits and References")

st.markdown(
    """
    Data provided under OGL v3.0. 
    www.nationalarchives.gov.uk/doc/open-government-licence/version/3/

    Data gathered using R stats19 package.

    https://github.com/ropensci/stats19
    
    Lovelace, Robin, Malcolm Morgan, Layik Hama, Mark Padgham, and M Padgham. 2019. “Stats19 A Package for Working with Open Road Crash Data.” Journal of Open Source Software 4 (33): 1181. https://doi.org/10.21105/joss.01181.
    """
)

gc.collect()