#!/usr/bin/env python3
# coding: utf-8

# (c) 2023 scopalaffairs

import pandas as pd
import plotly.express as px
import streamlit as st

from utils import *

title = "Sentiment Analysis of Tweets Tagged with #Influenza"
header = "Analyzing Public Sentiments towards Influenza Outbreaks on Social Media through Sentiment Analysis"

st.set_page_config(page_title=title, layout='wide')
st.title(title)
st.header(header)

filename = "./data-final/tw_hshtag_flu.json"


@st.cache_data
def load_data(filename):
    df = pd.read_json(filename, lines=True)
    return df


df = load_data(filename)

with st.spinner('Processing data...'):
    df["country"] = [map_country(loc, lang) for loc, lang in zip(df["location"], df["lang"])]
    emotions_df = pd.json_normalize(df["analyseEmotion"])
    df[["Happy", "Angry", "Surprise", "Sad", "Fear"]] = emotions_df

    grouped = df.groupby('country')[["Happy", "Angry", "Surprise", "Sad", "Fear"]].mean().reset_index()
    melted = pd.melt(grouped, id_vars='country', var_name='emotion', value_name='mean')

stacked_bar4 = px.bar(
    melted,
    x='country',
    y='mean',
    color='emotion',
    color_discrete_sequence=px.colors.sequential.Agsunset,
    barmode='stack',
    title="Emotions across the globe tagged #flu",
    height=600,
)
st.plotly_chart(stacked_bar4, use_container_width=True)

with st.expander("Show interactive world map"):
    dominant = melted.loc[melted.groupby('country')["mean"].idxmax()].reset_index(drop=True)

    globe_plot4 = px.choropleth_mapbox(
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
        title='Emotion by Country related to tweets tagged #flu',
        height=600,
    )
    st.plotly_chart(globe_plot4, use_container_width=True)
