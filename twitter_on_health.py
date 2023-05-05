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
header = "Analysing hashtags across the globe"

# Add title and header, define layout
st.set_page_config(page_title=title, layout='wide')
st.title(title)
st.header(header)

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

print(df_dict)
df = df_dict["processed_processed_twitter-who"]
df2 = df_dict["processed_processed_tw_hshtag_monkeypox"]
df3 = df_dict["processed_processed_tw_hshtag_covid19"]
df4 = df_dict["processed_processed_tw_hshtag_flu"]
# hashtag_tedros = df_dict["processed_processed_twitter-drtedros"]


df["country"] = df.apply(change_to_country, axis=1)
df[['Happy', 'Angry', 'Surprise', 'Sad', 'Fear']] = df['analyseEmotion'].apply(
    extract_emotions
)

grouped = (
    df.groupby('country')[['Happy', 'Angry', 'Surprise', 'Sad', 'Fear']]
    .mean()
    .reset_index()
)
melted = pd.melt(grouped, id_vars='country', var_name='emotion', value_name='mean')

stacked_bar = px.bar(
    melted,
    x='country',
    y='mean',
    color_discrete_sequence=px.colors.sequential.Agsunset,
    color='emotion',
    barmode='stack',
    title="Emotions of Tweets across the globe tagged #WHO",
    width=1440,
    height=800,
)
st.plotly_chart(stacked_bar,)

var = list(melted["country"].unique())
agg = []
for item in var:
    t = melted[melted["country"] == item]
    agg.append(t["mean"].idxmax())
melted = melted[melted.index.isin(agg)]
melted.reset_index()

globe_plot = px.choropleth_mapbox(
    melted,
    geojson=geojson,
    locations='country',
    featureidkey='properties.ADMIN',
    mapbox_style='carto-positron',
    zoom=1,
    center={'lat': 30, 'lon': 0},
    opacity=0.5,
    color="emotion",
    hover_name='country',
    color_discrete_sequence=px.colors.sequential.Agsunset,
    # color_discrete_sequence=px.colors.sequential.Electric,
    # mapbox_style = "open-street-map",
    # projection='mercator',
    # color_continuous_scale="Viridis",
    title='Emotion Analysis by Country related to tweets tagged #WHO',
    width=1440,
    height=800,
)

st.plotly_chart(globe_plot,)





############################## 2
df2["country"] = df2.apply(change_to_country, axis=1)
df2[['Happy', 'Angry', 'Surprise', 'Sad', 'Fear']] = df2['analyseEmotion'].apply(
    extract_emotions
)

grouped = (
    df2.groupby('country')[['Happy', 'Angry', 'Surprise', 'Sad', 'Fear']]
    .mean()
    .reset_index()
)
melted = pd.melt(grouped, id_vars='country', var_name='emotion', value_name='mean')

stacked_bar2 = px.bar(
    melted,
    x='country',
    y='mean',
    color_discrete_sequence=px.colors.sequential.Agsunset,
    color='emotion',
    barmode='stack',
    title="Emotions of Tweets across the globe tagged #monkeypox",
    width=1440,
    height=800,
)
st.plotly_chart(stacked_bar2,)

var = list(melted["country"].unique())
agg = []
for item in var:
    t = melted[melted["country"] == item]
    agg.append(t["mean"].idxmax())
melted = melted[melted.index.isin(agg)]
melted.reset_index()

globe_plot2 = px.choropleth_mapbox(
    melted,
    geojson=geojson,
    locations='country',
    featureidkey='properties.ADMIN',
    mapbox_style='carto-positron',
    zoom=1,
    center={'lat': 30, 'lon': 0},
    opacity=0.5,
    color="emotion",
    hover_name='country',
    color_discrete_sequence=px.colors.sequential.Agsunset,
    # color_discrete_sequence=px.colors.sequential.Electric,
    # mapbox_style = "open-street-map",
    # projection='mercator',
    # color_continuous_scale="Viridis",
    title='Emotion Analysis by Country related to tweets tagged #monkeypox',
    width=1440,
    height=800,
)

st.plotly_chart(globe_plot2,)

###################################3

df3["country"] = df3.apply(change_to_country, axis=1)
df3[['Happy', 'Angry', 'Surprise', 'Sad', 'Fear']] = df3['analyseEmotion'].apply(
    extract_emotions
)

grouped = (
    df3.groupby('country')[['Happy', 'Angry', 'Surprise', 'Sad', 'Fear']]
    .mean()
    .reset_index()
)
melted = pd.melt(grouped, id_vars='country', var_name='emotion', value_name='mean')

stacked_bar3 = px.bar(
    melted,
    x='country',
    y='mean',
    color_discrete_sequence=px.colors.sequential.Agsunset,
    color='emotion',
    barmode='stack',
    title="Emotions of Tweets across the globe tagged #covid19",
    width=1440,
    height=800,
)
st.plotly_chart(stacked_bar3,)

var = list(melted["country"].unique())
agg = []
for item in var:
    t = melted[melted["country"] == item]
    agg.append(t["mean"].idxmax())
melted = melted[melted.index.isin(agg)]
melted.reset_index()

globe_plot3 = px.choropleth_mapbox(
    melted,
    geojson=geojson,
    locations='country',
    featureidkey='properties.ADMIN',
    mapbox_style='carto-positron',
    zoom=1,
    center={'lat': 30, 'lon': 0},
    opacity=0.5,
    color="emotion",
    hover_name='country',
    color_discrete_sequence=px.colors.sequential.Agsunset,
    # color_discrete_sequence=px.colors.sequential.Electric,
    # mapbox_style = "open-street-map",
    # projection='mercator',
    # color_continuous_scale="Viridis",
    title='Emotion Analysis by Country related to tweets tagged #covid19',
    width=1440,
    height=800,
)

st.plotly_chart(globe_plot3,)





################################ 4
df4["country"] = df4.apply(change_to_country, axis=1)
df4[['Happy', 'Angry', 'Surprise', 'Sad', 'Fear']] = df4['analyseEmotion'].apply(
    extract_emotions
)

grouped = (
    df4.groupby('country')[['Happy', 'Angry', 'Surprise', 'Sad', 'Fear']]
    .mean()
    .reset_index()
)
melted = pd.melt(grouped, id_vars='country', var_name='emotion', value_name='mean')

stacked_bar4 = px.bar(
    melted,
    x='country',
    y='mean',
    color_discrete_sequence=px.colors.sequential.Agsunset,
    color='emotion',
    barmode='stack',
    title="Emotions of Tweets across the globe tagged #flu",
    width=1440,
    height=800,
)
st.plotly_chart(stacked_bar4,)

var = list(melted["country"].unique())
agg = []
for item in var:
    t = melted[melted["country"] == item]
    agg.append(t["mean"].idxmax())
melted = melted[melted.index.isin(agg)]
melted.reset_index()

globe_plot4 = px.choropleth_mapbox(
    melted,
    geojson=geojson,
    locations='country',
    featureidkey='properties.ADMIN',
    mapbox_style='carto-positron',
    zoom=1,
    center={'lat': 30, 'lon': 0},
    opacity=0.5,
    color="emotion",
    hover_name='country',
    color_discrete_sequence=px.colors.sequential.Agsunset,
    # color_discrete_sequence=px.colors.sequential.Electric,
    # mapbox_style = "open-street-map",
    # projection='mercator',
    # color_continuous_scale="Viridis",
    title='Emotion Analysis by Country related to tweets tagged #flu',
    width=1440,
    height=800,
)

st.plotly_chart(globe_plot4,)
