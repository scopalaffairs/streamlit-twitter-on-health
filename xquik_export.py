"""Normalize saved Xquik tweet exports for the health dashboard."""

from __future__ import annotations

import re
from collections import Counter
from collections.abc import Iterable, Mapping
from typing import Any

TEXT_FIELDS = ("tweet_text", "full_text", "text", "content", "body")
AUTHOR_FIELDS = ("username", "author_username", "screen_name", "user")
LOCATION_FIELDS = ("location", "user_location", "place", "country")
DATE_FIELDS = ("created_at", "timestamp", "date")
TRACKED_HASHTAGS = ("who", "monkeypox", "covid", "covid19", "flu", "influenza")


def _first_value(row: Mapping[str, Any], fields: Iterable[str]) -> str:
    for field in fields:
        value = row.get(field)
        if value is None:
            continue

        text = str(value).strip()
        if text:
            return text

    return ""


def _hashtags(text: str) -> list[str]:
    found = []
    for value in re.findall(r"#([A-Za-z0-9_]+)", text):
        normalized = value.lower()
        if normalized in TRACKED_HASHTAGS:
            found.append(normalized)

    return found


def normalize_xquik_rows(rows: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []

    for row in rows:
        text = _first_value(row, TEXT_FIELDS)
        if not text:
            continue

        normalized.append(
            {
                "text": text,
                "author": _first_value(row, AUTHOR_FIELDS),
                "location": _first_value(row, LOCATION_FIELDS),
                "created_at": _first_value(row, DATE_FIELDS),
                "hashtags": _hashtags(text),
            }
        )

    return normalized


def summarize_xquik_rows(rows: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    records = list(rows)
    hashtag_counts: Counter[str] = Counter()
    location_counts: Counter[str] = Counter()

    for row in records:
        hashtag_counts.update(row.get("hashtags", []))
        location = row.get("location")
        if isinstance(location, str) and location:
            location_counts[location] += 1

    return {
        "rows": len(records),
        "with_location": sum(1 for row in records if row.get("location")),
        "hashtag_counts": dict(hashtag_counts),
        "top_locations": dict(location_counts.most_common(10)),
    }
