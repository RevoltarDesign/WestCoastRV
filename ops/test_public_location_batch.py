import csv
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


class PublicLocationBatchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with (HERE / "data" / "campgrounds.csv").open(newline="", encoding="utf-8-sig") as source:
            cls.rows = {row["Slug"]: row for row in csv.DictReader(source)}

    def test_all_eight_records_have_current_location_and_route_provenance(self):
        slugs = {
            "hozomeen-campground", "big-creek-campground", "twin-harbors-state-park",
            "grayland-beach-state-park", "cape-disappointment-state-park", "silver-lake-park",
            "dosewallips-state-park", "fort-flagler-historical-state-park",
        }
        for slug in slugs:
            with self.subTest(slug=slug):
                row = self.rows[slug]
                self.assertEqual(row["Coordinates checked"], "2026-09-12")
                self.assertEqual(row["Drive time checked"], "2026-09-12")
                self.assertTrue(row["Coordinates source"])
                self.assertTrue(row["Drive time source"].startswith("https://router.project-osrm.org/"))
                self.assertGreaterEqual(int(row["Drive Time Minutes"]), int(row["Drive route minutes"]))

    def test_current_closures_are_prominent_and_not_routed_as_open(self):
        for slug in ("hozomeen-campground", "cape-disappointment-state-park"):
            row = self.rows[slug]
            self.assertEqual(row["RV Access"], "no")
            self.assertIn("closed", row["Reservation window"].lower())
            page = (ROOT / "campground" / f"{slug}.html").read_text(encoding="utf-8")
            self.assertIn("Vehicle access closed", page)
            self.assertNotIn("Get Directions", page)
            self.assertNotIn("Open in Google Maps", page)
            self.assertNotIn('"hasMap"', page)

    def test_stale_coastal_addresses_were_replaced(self):
        self.assertEqual(self.rows["twin-harbors-state-park"]["Address"], "3120 WA-105, Westport, WA 98595")
        self.assertEqual(self.rows["grayland-beach-state-park"]["Address"], "925 Cranberry Beach Road, Grayland, WA 98547")


if __name__ == "__main__":
    unittest.main()
