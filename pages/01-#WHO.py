#!/usr/bin/env python3
# coding: utf-8

# (c) 2023 scopalaffairs

import pandas as pd
import plotly.express as px
import streamlit as st


title = "Sentiment Analysis of Tweets Tagged with #WHO"
header = "Exploring Public Sentiments towards the World Health Organization on Twitter"

st.set_page_config(page_title=title, layout='wide', page_icon="Hospital")
st.title(title)
st.header(header)


@st.cache_data
def load_data():
    return pd.read_csv("./data-final/melted_who.csv")


@st.cache_data
def make_bar(melted):
    return px.bar(
        melted,
        x='country', y='mean', color='emotion',
        color_discrete_sequence=px.colors.sequential.Agsunset,
        barmode='stack',
        title="Emotions across the globe tagged #WHO",
        height=600,
    )


melted = load_data()
st.plotly_chart(make_bar(melted), use_container_width=True)
