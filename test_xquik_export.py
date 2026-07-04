import unittest

from xquik_export import normalize_xquik_rows, summarize_xquik_rows


class XquikExportTest(unittest.TestCase):
    def test_normalizes_health_hashtags_and_metadata(self):
        rows = [
            {
                "tweet_text": "New #WHO guidance for #COVID19 monitoring",
                "username": "analyst",
                "location": "Germany",
                "created_at": "2026-07-04T10:00:00Z",
            },
            {"full_text": "  "},
            {"content": "#flu trend update", "country": "France"},
        ]

        normalized = normalize_xquik_rows(rows)

        self.assertEqual(
            normalized,
            [
                {
                    "text": "New #WHO guidance for #COVID19 monitoring",
                    "author": "analyst",
                    "location": "Germany",
                    "created_at": "2026-07-04T10:00:00Z",
                    "hashtags": ["who", "covid19"],
                },
                {
                    "text": "#flu trend update",
                    "author": "",
                    "location": "France",
                    "created_at": "",
                    "hashtags": ["flu"],
                },
            ],
        )

    def test_summarizes_hashtags_and_locations(self):
        summary = summarize_xquik_rows(
            [
                {"location": "Germany", "hashtags": ["who", "covid19"]},
                {"location": "Germany", "hashtags": ["who"]},
                {"location": "", "hashtags": ["flu"]},
            ]
        )

        self.assertEqual(summary["rows"], 3)
        self.assertEqual(summary["with_location"], 2)
        self.assertEqual(summary["hashtag_counts"], {"who": 2, "covid19": 1, "flu": 1})
        self.assertEqual(summary["top_locations"], {"Germany": 2})


if __name__ == "__main__":
    unittest.main()
