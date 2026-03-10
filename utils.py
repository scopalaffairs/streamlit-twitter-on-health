#!/usr/bin/env python3
# coding: utf-8

# (c) 2023 scopalaffairs

import json
from pathlib import Path

_DATA = Path(__file__).parent / "data-final"

# loaded once per process via Python's module cache
with open(_DATA / "countries.geojson") as f:
    geojson = json.load(f)
