import csv
import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SLUGS = {
    "cougar-rock-campground", "ohanapecosh-campground", "white-river-campground",
    "newhalem-creek-campground", "goodell-creek-campground",
    "colonial-creek-south-campground", "colonial-creek-north-campground",
}
CRITICAL = {"operating_status", "rv_access", "reservation_method", "max_rv_length", "hookups"}


class NationalParkTrustPhaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with (HERE / "data" / "campgrounds.csv").open(newline="", encoding="utf-8-sig") as source:
            cls.rows = {row["Slug"]: row for row in csv.DictReader(source)}
        cls.evidence = json.loads((HERE / "verification-evidence.json").read_text(encoding="utf-8"))["observations"]

    def test_all_seven_have_complete_current_critical_evidence(self):
        for slug in SLUGS:
            with self.subTest(slug=slug):
                observations = {o["field"]: o for o in self.evidence if o.get("slug") == slug and o.get("field") in CRITICAL}
                self.assertEqual(set(observations), CRITICAL)
                self.assertTrue(all(o["checked_on"] == "2026-09-19" for o in observations.values()))
                self.assertTrue(all(o["sources"] for o in observations.values()))

    def test_goodell_uses_current_twenty_foot_limit(self):
        row = self.rows["goodell-creek-campground"]
        self.assertEqual(row["Max RV length"], "20")
        self.assertNotIn("38", row["Long description"])

    def test_current_colonial_closures_suppress_routes(self):
        for slug in ("colonial-creek-north-campground", "colonial-creek-south-campground"):
            with self.subTest(slug=slug):
                self.assertEqual(self.rows[slug]["RV Access"], "no")
                page = (ROOT / "campground" / f"{slug}.html").read_text(encoding="utf-8")
                self.assertIn("Vehicle access closed", page)
                self.assertNotIn("Get Directions", page)
                self.assertNotIn("Open in Google Maps", page)
                self.assertNotIn('"hasMap"', page)
                self.assertEqual(self.rows[slug]["Amenities: Drinking water"], "false")
                self.assertNotEqual(self.rows[slug]["Amenities: Fire pits"], "true")

        self.assertEqual(self.rows["colonial-creek-south-campground"]["Dump station on site"], "false")

    def test_newhalem_partial_opening_is_explicit(self):
        row = self.rows["newhalem-creek-campground"]
        self.assertIn("Loops A and B", row["Reservation window"])
        self.assertIn("Loop C is closed", row["Reservation window"])
        self.assertEqual(row["Number of RV campsites"], "")


if __name__ == "__main__":
    unittest.main()
