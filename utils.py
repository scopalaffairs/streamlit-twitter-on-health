#!/usr/bin/env python3
# coding: utf-8

# (c) 2023 scopalaffairs

import json
from urllib.request import urlopen

import pandas as pd
import streamlit as st

# colors
white = "rgb(255, 255, 255)"
blueish = "rgb(200, 200, 255)"
vintage_brown = "rgb(255,250,240)"
coastlinecolor = "rgb(205,133,63)"

@st.cache_resource
def _load_geojson():
    with urlopen(
        'https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson'
    ) as response:
        return json.load(response)


@st.cache_resource
def _load_plotly_countries():
    return set(
        pd.read_csv(
            'https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv'
        ).COUNTRY
    )


geojson = _load_geojson()
plotly_countries_set = _load_plotly_countries()

# fast mapper
def map_country(location, lang):
    try:
        for word in location.split():
            if word in plotly_countries_set:
                return word
    except Exception:
        pass
    return "Unknown"
