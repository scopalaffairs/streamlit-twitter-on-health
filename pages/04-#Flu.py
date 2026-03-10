#!/usr/bin/env python3
# coding: utf-8

# (c) 2023 scopalaffairs

import pandas as pd
import plotly.express as px
import streamlit as st


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


melted = load_data()
st.plotly_chart(make_bar(melted), use_container_width=True)
