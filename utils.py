#!/usr/bin/env python3
# coding: utf-8

# (c) 2023 scopalaffairs

from pathlib import Path

import pandas as pd
import streamlit as st

DATA_DIR = Path(__file__).parent / "data-final"


@st.cache_data
def load_melted_csv(filename):
    path = DATA_DIR / filename
    if not path.exists():
        st.warning(f"{filename} is missing. Run python preprocess.py first.")
        return pd.DataFrame(columns=["country", "emotion", "mean"])

    return pd.read_csv(path)
