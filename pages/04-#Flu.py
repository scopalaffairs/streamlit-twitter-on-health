#!/usr/bin/env python3
# coding: utf-8

# (c) 2023 scopalaffairs

import pandas as pd
import plotly.express as px
import streamlit as st

from utils import geojson

title = "Sentiment Analysis of Tweets Tagged with #Influenza"
header = "Analyzing Public Sentiments towards Influenza Outbreaks on Social Media through Sentiment Analysis"

st.set_page_config(page_title=title, layout='wide')
st.title(title)
st.header(header)


@st.cache_data
def load_data():
    return pd.read_csv("./data-final/melted_flu.csv")


@st.cache_data
def make_bar(melted):
    return px.bar(
        melted,
        x='country', y='mean', color='emotion',
        color_discrete_sequence=px.colors.sequential.Agsunset,
        barmode='stack',
        title="Emotions across the globe tagged #flu",
        height=600,
    )


@st.cache_data
def make_globe(melted):
    dominant = melted.loc[melted.groupby('country')["mean"].idxmax()].reset_index(drop=True)
    return px.choropleth_mapbox(
        dominant,
        geojson=geojson,
        locations='country',
        featureidkey='properties.ADMIN',
        mapbox_style='carto-positron',
        zoom=1, center={'lat': 30, 'lon': 0}, opacity=0.5,
        color="emotion", hover_name='country',
        color_discrete_sequence=px.colors.sequential.Agsunset,
        title='Emotion by Country related to tweets tagged #flu',
        height=600,
    )


melted = load_data()
st.plotly_chart(make_bar(melted), use_container_width=True)

with st.expander("Show interactive world map"):
    st.plotly_chart(make_globe(melted), use_container_width=True)
