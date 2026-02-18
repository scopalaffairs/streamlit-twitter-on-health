#!/usr/bin/env python3
# coding: utf-8

# (c) 2023 scopalaffairs

import json
from pathlib import Path

import pandas as pd

_DATA = Path(__file__).parent / "data-final"

# colors
white = "rgb(255, 255, 255)"
blueish = "rgb(200, 200, 255)"
vintage_brown = "rgb(255,250,240)"
coastlinecolor = "rgb(205,133,63)"

# loaded once per process via Python's module cache (files are local — no network at startup)
with open(_DATA / "countries.geojson") as f:
    geojson = json.load(f)

plotly_countries_set = set(pd.read_csv(_DATA / "plotly_countries.csv").COUNTRY)

# fast mapper
def map_country(location, lang):
    try:
        for word in location.split():
            if word in plotly_countries_set:
                return word
    except Exception:
        pass
    return "Unknown"
