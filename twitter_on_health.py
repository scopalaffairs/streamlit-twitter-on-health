#!/usr/bin/env python3
# coding: utf-8

# (c) 2023 scopalaffairs

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

st.set_page_config(page_title=title, layout='wide')
st.title(title)
st.header(header)

st.write(
    """Our results highlight a range of emotional responses towards COVID-19 and Monkeypox across different countries. These variations, ranging from fear to happiness, may be linked not only to the lifting of travel bans but also to the relaxation of tourism restrictions, potentially impacting the hospitality sector."""
)
st.write(
    """Our analysis is based on a sample of tweets collected between November 2022 and February 2023."""
)
st.write("""Team: Nefeli Dellepiani, Dora Kohalmi PhD, Daniel Herrmann""")
