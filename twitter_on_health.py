#!/usr/bin/env python3
# coding: utf-8

# (c) 2023 scopalaffairs

import json
import os
import random
import zipfile
from copy import deepcopy
from urllib.request import urlopen

import gdown
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import streamlit as st

### CONSTANTS

# colors
white = "rgb(255, 255, 255)"
blueish = "rgb(200, 200, 255)"
vintage_brown = "rgb(255,250,240)"
coastlinecolor = "rgb(205,133,63)"

# strings
title = "Dissecting the public health discourse in the post-pandemic era"
header = "Analysing emotion related hashtags across the globe"

# Add title and header, define layout
st.set_page_config(page_title=title, layout='wide')
st.title(title)
st.header(header)
st.sidebar.header("Emotions across the globe tagged by")


# Setting up columns
left_column, middle_column, right_column = st.columns([1, 3, 1])

# Loading dataframes
@st.cache
def load_data(path):
    df = pd.read_json(path, lines=True)
    return df


with urlopen(
    'https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson'
) as response:
    geojson = json.load(response)

json_dir = "./data-final/"
df_dict = {}
for root, dirs, files in os.walk(json_dir):
    for file_name in files:
        if file_name.endswith(".json"):
            file_path = os.path.join(root, file_name)
            name = os.path.splitext(file_name)[0]
            df_dict[name] = load_data(path=file_path)

df = deepcopy(df_dict)

# Clean dataframe
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
    # else
    if row["lang"] in countries.keys():
        random_country = random.choice(countries[row["lang"]])
        return random_country
    else:
        return "Unknown"


def extract_emotions(emotion_dict):
    return pd.Series(emotion_dict)

df = df_dict["processed_processed_twitter-who"]
df2 = df_dict["processed_processed_tw_hshtag_monkeypox"]
df3 = df_dict["processed_processed_tw_hshtag_covid19"]
df4 = df_dict["processed_processed_tw_hshtag_flu"]
