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

plotly_countries = pd.read_csv(
    'https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv'
)
plotly_countries = plotly_countries.COUNTRY.to_list()


def change_to_country(row):
    split_location = row["location"].split()
    for word in split_location:
        if word in plotly_countries:
            return word
    if row["lang"] in countries.keys():
        random_country = random.choice(countries[row["lang"]])
        return random_country
    else:
        return "Unknown"


def extract_emotions(emotion_dict):
    return pd.Series(emotion_dict)
