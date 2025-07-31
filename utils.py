#!/usr/bin/env python3
# coding: utf-8

# (c) 2023 scopalaffairs

import json
import random
from urllib.request import urlopen

import pandas as pd

# colors
white = "rgb(255, 255, 255)"
blueish = "rgb(200, 200, 255)"
vintage_brown = "rgb(255,250,240)"
coastlinecolor = "rgb(205,133,63)"

with urlopen(
    'https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson'
) as response:
    geojson = json.load(response)

countries = {
    'es': [
        'Argentina',
        'Bolivia',
        'Chile',
        'Colombia',
        'Costa Rica',
        'Cuba',
        'Dominican Republic',
        'Ecuador',
        'El Salvador',
        'Equatorial Guinea',
        'Guatemala',
        'Honduras',
        'Mexico',
        'Nicaragua',
        'Panama',
        'Paraguay',
        'Peru',
        'Spain',
        'Uruguay',
        'Venezuela',
        'Puerto Rico',
    ],
    'fr': ["France", "Canada", "Cameroon", "Ivory Coast", "Niger", "Senegal"],
    'en': [
        "India",
        "United States of America",
        "Pakistan",
        "Nigeria",
        "Bangladesh",
        "United Kingdom",
        "Philippines",
        "Canada",
        "Australia",
        "South Africa",
    ],
    'in': ["Indonesia"],
    'nl': ["Belgium", "Netherlands", "Suriname"],
    'qht': ["Hashtag Only"],
    'qme': ["Media Only"],
    'ja': ["Japan"],
    'it': ["Italy"],
    'pt': ["Angola", "Brazil", "Portugal"],
    'de': [
        "Austria",
        "Belgium",
        "Germany",
        "Liechtenstein",
        "Luxembourg",
        "Switzerland",
    ],
    'und': ["Unknown"],
    'sl': ["Slovenia"],
    'ca': ["Spain"],
    'bn': ["Bangladesh", "India"],
    'fi': ["Finland"],
    'ru': ["Russia", "Belarus", "Kazakhstan", "Kyrgyzstan"],
    'pl': ["Poland"],
}

# country lookup optimized
plotly_countries_set = set(
    pd.read_csv(
        'https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv'
    ).COUNTRY
)

# fast mapper
def map_country(location, lang):
    try:
        for word in location.split():
            if word in plotly_countries_set:
                return word
    except:
        pass
    if lang in countries:
        return random.choice(countries[lang])
    return "Unknown"
