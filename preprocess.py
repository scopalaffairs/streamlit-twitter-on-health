#!/usr/bin/env python3
"""
Run once to pre-aggregate the raw JSON files into small CSVs.
After this, the Streamlit pages load kilobytes instead of hundreds of megabytes.

Usage:
    python preprocess.py
"""

import json
from pathlib import Path

import pandas as pd

DATA = Path(__file__).parent / "data-final"

with open(DATA / "plotly_countries.csv") as f:
    plotly_countries_set = set(pd.read_csv(DATA / "plotly_countries.csv").COUNTRY)


def map_country(location, lang):
    try:
        for word in str(location).split():
            if word in plotly_countries_set:
                return word
    except Exception:
        pass
    return "Unknown"


def process(src: Path, dest: Path):
    print(f"Processing {src.name} ...")
    df = pd.read_json(src, lines=True)
    df["country"] = [map_country(loc, lang) for loc, lang in zip(df["location"], df["lang"])]
    df = df[df["country"] != "Unknown"].reset_index(drop=True)
    emotions_df = pd.json_normalize(df["analyseEmotion"])
    df[["Happy", "Angry", "Surprise", "Sad", "Fear"]] = emotions_df
    grouped = df.groupby("country")[["Happy", "Angry", "Surprise", "Sad", "Fear"]].mean().reset_index()
    melted = pd.melt(grouped, id_vars="country", var_name="emotion", value_name="mean")
    melted.to_csv(dest, index=False)
    print(f"  -> {dest.name} ({dest.stat().st_size // 1024} KB)")


files = [
    ("twitter-who.json",        "melted_who.csv"),
    ("tw_hshtag_monkeypox.json","melted_monkeypox.csv"),
    ("tw_hshtag_covid19.json",  "melted_covid19.csv"),
    ("tw_hshtag_flu.json",      "melted_flu.csv"),
]

for src_name, dest_name in files:
    process(DATA / src_name, DATA / dest_name)

print("Done. You can now deploy without the raw JSON files.")
