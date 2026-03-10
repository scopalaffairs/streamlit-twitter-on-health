#!/usr/bin/env python3
# coding: utf-8

# (c) 2023 scopalaffairs

import pandas as pd
import plotly.express as px
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
    df["country"] = [map_country(loc, lang) for loc, lang in zip(df["location"], df["lang"])]
    df = df[df["country"] != "Unknown"].reset_index(drop=True)
    emotions_df = pd.json_normalize(df["analyseEmotion"])
    df[["Happy", "Angry", "Surprise", "Sad", "Fear"]] = emotions_df
    grouped = df.groupby('country')[["Happy", "Angry", "Surprise", "Sad", "Fear"]].mean().reset_index()
    return pd.melt(grouped, id_vars='country', var_name='emotion', value_name='mean')


melted = load_data(filename)

stacked_bar = px.bar(
    melted,
    x='country',
    y='mean',
    color='emotion',
    color_discrete_sequence=px.colors.sequential.Agsunset,
    barmode='stack',
    title="Emotions across the globe tagged #WHO",
    height=600,
)
st.plotly_chart(stacked_bar, use_container_width=True)

with st.expander("Show interactive world map"):
    dominant = melted.loc[melted.groupby('country')["mean"].idxmax()].reset_index(drop=True)

    globe_plot = px.choropleth_mapbox(
        dominant,
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
        height=600,
    )
    st.plotly_chart(globe_plot, use_container_width=True)
