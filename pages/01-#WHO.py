#!/usr/bin/env python3
# coding: utf-8

# (c) 2023 scopalaffairs

import os

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from utils import *

title = "Sentiment Analysis of Tweets Tagged with #WHO"
header = "Exploring Public Sentiments towards the World Health Organization on Twitter"

st.set_page_config(page_title=title, layout='wide', page_icon="Hospital")
st.title(title)
st.header(header)

filename = "./data-final/twitter-who.json"


@st.cache_data
def load_data(filename):
    df = pd.read_json(filename, lines=True)
    return df


df = load_data(filename)
with st.spinner('Loading...'):
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
        title="Emotions across the globe tagged #WHO",
        width=1440,
        height=800,
    )

    st.plotly_chart(
        stacked_bar,
    )

with st.spinner('Loading...'):
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
        title='Emotion by Country related to tweets tagged #WHO',
        width=1440,
        height=800,
    )

    st.plotly_chart(
        globe_plot,
    )
