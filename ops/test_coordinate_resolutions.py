import csv
import json
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent


class CoordinateResolutionTests(unittest.TestCase):
    def test_reviewed_queue_matches_canonical_data(self):
        review = json.loads((HERE / "coordinate-resolutions.json").read_text(encoding="utf-8"))
        resolutions = review["resolutions"]
        self.assertEqual(15, len(resolutions))
        self.assertEqual(15, len({item["slug"] for item in resolutions}))
        with (HERE / "data" / "campgrounds.csv").open(newline="", encoding="utf-8-sig") as source:
            rows = {row["Slug"]: row for row in csv.DictReader(source)}
        for item in resolutions:
            with self.subTest(slug=item["slug"]):
                row = rows[item["slug"]]
                self.assertAlmostEqual(item["latitude"], float(row["Latitude"]), places=6)
                self.assertAlmostEqual(item["longitude"], float(row["Longitude"]), places=6)
                self.assertIn(f"{float(row['Latitude']):.7f},{float(row['Longitude']):.7f}", row["Google Maps Link"])
                self.assertGreaterEqual(int(row["Drive Time Minutes"]), int(row["Drive route minutes"]))
                self.assertEqual("Seattle, Washington", row["Drive time origin"])
                self.assertTrue(item["named_map_url"].startswith("https://www.google.com/maps/"))
                self.assertTrue(item["reason"])


if __name__ == "__main__":
    unittest.main()
