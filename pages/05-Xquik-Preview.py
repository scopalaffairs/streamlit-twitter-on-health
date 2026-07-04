#!/usr/bin/env python3
# coding: utf-8

# (c) 2023 scopalaffairs

import pandas as pd
import plotly.express as px
import streamlit as st
from xquik_export import normalize_xquik_rows, summarize_xquik_rows

title = "Xquik Export Preview"
header = "Preview saved Xquik tweet exports before preprocessing"

st.set_page_config(page_title=title, layout="wide")
st.title(title)
st.header(header)

upload = st.file_uploader(
    "Upload a Xquik tweet CSV export",
    type=["csv"],
    help="Uses tweet_text, full_text, text, content, or body as the text column.",
)

if upload is None:
    st.info("Upload a CSV export to preview health-related hashtags and locations.")
else:
    try:
        rows = normalize_xquik_rows(pd.read_csv(upload).to_dict("records"))
        summary = summarize_xquik_rows(rows)

        col1, col2 = st.columns(2)
        col1.metric("Rows", summary["rows"])
        col2.metric("Rows With Location", summary["with_location"])

        hashtag_counts = summary["hashtag_counts"]
        if hashtag_counts:
            hashtag_df = pd.DataFrame(
                [{"hashtag": tag, "count": count} for tag, count in hashtag_counts.items()]
            )
            fig = px.bar(
                hashtag_df,
                x="hashtag",
                y="count",
                title="Tracked Health Hashtags",
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No tracked health hashtags were found in the uploaded rows.")

        st.dataframe(pd.DataFrame(rows).head(25), use_container_width=True)
    except Exception as error:
        st.error(f"Could not read Xquik export: {error}")
