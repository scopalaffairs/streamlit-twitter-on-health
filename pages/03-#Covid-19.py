#!/usr/bin/env python3
# coding: utf-8

# (c) 2023 scopalaffairs

import pandas as pd
import plotly.express as px
import streamlit as st

from utils import geojson, map_country

title = "Sentiment Analysis of Tweets Tagged with #covid19"
header = "Assessing Public Sentiments towards COVID-19 Outbreaks on Twitter using Sentiment Analysis"

st.set_page_config(page_title=title, layout='wide')
st.title(title)
st.header(header)

filename = "./data-final/tw_hshtag_covid19.json"

@st.cache_data
def load_data(filename):
    return pd.read_json(filename, lines=True)

df = load_data(filename)

# vectorized transformations
with st.spinner('Processing data...'):
    df["country"] = [map_country(loc, lang) for loc, lang in zip(df["location"], df["lang"])]
    emotions_df = pd.json_normalize(df["analyseEmotion"])
    df[["Happy", "Angry", "Surprise", "Sad", "Fear"]] = emotions_df

    # group and reshape
    grouped = df.groupby('country')[["Happy", "Angry", "Surprise", "Sad", "Fear"]].mean().reset_index()
    melted = pd.melt(grouped, id_vars='country', var_name='emotion', value_name='mean')

# plot: stacked bar
stacked_bar3 = px.bar(
    melted,
    x='country',
    y='mean',
    color='emotion',
    color_discrete_sequence=px.colors.sequential.Agsunset,
    barmode='stack',
    title="Emotions of Tweets across the globe tagged #covid19",
    width=960,
    height=600,
)
st.plotly_chart(stacked_bar3)

# plot: choropleth (optional inside expander)
with st.expander("Show interactive world map"):
    # find dominant emotion per country
    dominant = melted.loc[melted.groupby('country')["mean"].idxmax()].reset_index(drop=True)

    globe_plot3 = px.choropleth_mapbox(
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
        title='Emotion Analysis by Country related to tweets tagged #covid19',
        width=960,
        height=600,
    )
    st.plotly_chart(globe_plot3)
