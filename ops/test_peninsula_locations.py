import csv
import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent

class PeninsulaLocationTests(unittest.TestCase):
    def test_reviewed_locations_match_canonical_data(self):
        review = json.loads((HERE / "peninsula-location-reviews.json").read_text(encoding="utf-8"))
        with (HERE / "data" / "campgrounds.csv").open(newline="", encoding="utf-8-sig") as source:
            rows = {row["Slug"]: row for row in csv.DictReader(source)}
        self.assertEqual(7, len(review["reviews"]))
        for item in review["reviews"]:
            with self.subTest(slug=item["slug"]):
                row = rows[item["slug"]]
                self.assertAlmostEqual(item["latitude"], float(row["Latitude"]), places=6)
                self.assertAlmostEqual(item["longitude"], float(row["Longitude"]), places=6)
                self.assertEqual(item["address"], row["Address"])
                self.assertGreaterEqual(int(row["Drive Time Minutes"]), int(row["Drive route minutes"]))
                self.assertEqual("Seattle, Washington", row["Drive time origin"])
                self.assertTrue(row["Coordinates source"])
                self.assertTrue(item["named_map_url"].startswith("https://www.google.com/maps/place/"))

if __name__ == "__main__":
    unittest.main()
