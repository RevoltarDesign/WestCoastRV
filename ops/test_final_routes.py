import csv
import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

class FinalRouteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.review = json.loads((HERE / "final-route-reviews.json").read_text(encoding="utf-8"))["reviews"]
        with (HERE / "data" / "campgrounds.csv").open(newline="", encoding="utf-8-sig") as source:
            cls.rows = {row["Slug"]: row for row in csv.DictReader(source)}

    def test_queue_has_seventeen_unique_records(self):
        self.assertEqual(len(self.review), 17)
        self.assertEqual(len({item["slug"] for item in self.review}), 17)

    def test_every_route_is_sourced_and_conservative(self):
        for item in self.review:
            row = self.rows[item["slug"]]
            with self.subTest(slug=item["slug"]):
                self.assertEqual(row["Drive time checked"], "2026-09-13")
                self.assertEqual(row["Drive time origin"], "Seattle, Washington")
                self.assertTrue(row["Drive time source"].startswith("https://router.project-osrm.org/"))
                self.assertGreaterEqual(int(row["Drive Time Minutes"]), int(row["Drive route minutes"]))
                self.assertEqual(row["Access checked"], "2026-09-13")
                self.assertIn(row["RV Access"], {"yes", "no"})

    def test_ohanapecosh_closure_suppresses_directions(self):
        row = self.rows["ohanapecosh-campground"]
        self.assertEqual(row["RV Access"], "no")
        self.assertIn("closed", row["Reservation window"].lower())
        page = (ROOT / "campground" / "ohanapecosh-campground.html").read_text(encoding="utf-8")
        self.assertIn("Vehicle access closed", page)
        self.assertNotIn("Get Directions", page)
        self.assertNotIn("Open in Google Maps", page)
        self.assertNotIn('"hasMap"', page)
        self.assertNotIn("RVs and trailers are not allowed", page)

    def test_every_inaccessible_listing_suppresses_route_actions(self):
        for slug, row in self.rows.items():
            if row.get("Archived") == "true" or row.get("RV Access") != "no":
                continue
            with self.subTest(slug=slug):
                page = (ROOT / "campground" / f"{slug}.html").read_text(encoding="utf-8")
                self.assertIn("Vehicle access closed", page)
                self.assertNotIn("Get Directions", page)
                self.assertNotIn("Open in Google Maps", page)
                self.assertNotIn('"hasMap"', page)

    def test_current_national_park_season_details(self):
        self.assertEqual(self.rows["white-river-campground"]["Number of RV campsites"], "88")
        self.assertIn("first-come", self.rows["white-river-campground"]["Reservation window"].lower())
        self.assertIn("september 14", self.rows["colonial-creek-north-campground"]["Reservation window"].lower())
        self.assertIn("september 27", self.rows["newhalem-creek-campground"]["Reservation window"].lower())

if __name__ == "__main__": unittest.main()
