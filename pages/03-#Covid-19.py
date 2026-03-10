#!/usr/bin/env python3
# coding: utf-8

# (c) 2023 scopalaffairs

import pandas as pd
import plotly.express as px
import streamlit as st

from utils import geojson

title = "Sentiment Analysis of Tweets Tagged with #covid19"
header = "Assessing Public Sentiments towards COVID-19 Outbreaks on Twitter using Sentiment Analysis"

st.set_page_config(page_title=title, layout='wide')
st.title(title)
st.header(header)


@st.cache_data
def load_data():
    return pd.read_csv("./data-final/melted_covid19.csv")


@st.cache_data
def make_bar(melted):
    return px.bar(
        melted,
        x='country', y='mean', color='emotion',
        color_discrete_sequence=px.colors.sequential.Agsunset,
        barmode='stack',
        title="Emotions of Tweets across the globe tagged #covid19",
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
        title='Emotion Analysis by Country related to tweets tagged #covid19',
        height=600,
    )


melted = load_data()
st.plotly_chart(make_bar(melted), use_container_width=True)

with st.expander("Show interactive world map"):
    st.plotly_chart(make_globe(melted), use_container_width=True)
