import csv
import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SLUGS = {
    "pine-village-koa-holiday", "thousand-trails-leavenworth", "tall-chief-rv-park-campground",
    "packwood-rv-park-campground", "american-heritage-campground", "andersens-oceanside-rv-park",
    "beachside-rv-park", "sunnyside-rv-park", "north-whidbey-rv-park",
    "whidbey-island-fairgrounds-campground",
}

class PrivateCoordinateFinalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with (HERE / "data" / "campgrounds.csv").open(newline="", encoding="utf-8-sig") as source:
            cls.rows = {row["Slug"]: row for row in csv.DictReader(source)}

    def test_all_records_have_current_coordinate_and_route_provenance(self):
        for slug in SLUGS:
            with self.subTest(slug=slug):
                row = self.rows[slug]
                self.assertEqual(row["Coordinates checked"], "2026-09-12")
                self.assertEqual(row["Drive time checked"], "2026-09-12")
                self.assertTrue(row["Coordinates source"])
                self.assertTrue(row["Coordinate precision"])
                self.assertTrue(row["Drive time source"].startswith("https://router.project-osrm.org/"))
                self.assertGreaterEqual(int(row["Drive Time Minutes"]), int(row["Drive route minutes"]))
                self.assertTrue(row["Google Maps Link"].startswith("https://www.google.com/maps/dir/"))

    def test_material_location_corrections(self):
        expected = {
            "pine-village-koa-holiday": ("308 Zelt Strasse, Leavenworth, WA 98826", 47.599283, -120.640569),
            "tall-chief-rv-park-campground": ("29290 SE 8th Street, Fall City, WA 98024", 47.5955, -121.9393),
            "packwood-rv-park-campground": ("12985 US Highway 12, Packwood, WA 98361", 46.606501, -121.670644),
            "sunnyside-rv-park": ("609 Scoon Road, Sunnyside, WA 98944", 46.33293933, -120.02119382),
        }
        for slug, (address, lat, lon) in expected.items():
            row = self.rows[slug]
            self.assertEqual(row["Address"], address)
            self.assertAlmostEqual(float(row["Latitude"]), lat, places=6)
            self.assertAlmostEqual(float(row["Longitude"]), lon, places=6)

    def test_known_stale_claims_are_absent(self):
        text = "\n".join(" ".join(self.rows[s].values()) for s in SLUGS).lower()
        for stale in ("membership required", "sites near icicle creek", "snoqualmie river sites", "mini golf\nVintage playground", "13085 us-12"):
            self.assertNotIn(stale.lower(), text)
        self.assertIn("no sewer sites", self.rows["tall-chief-rv-park-campground"]["Long description"].lower())
        self.assertIn("no membership is needed", self.rows["thousand-trails-leavenworth"]["Long description"].lower())

    def test_scrub_ledger_counts_match_findings(self):
        report = json.loads((HERE / "private-final-scrub-findings.json").read_text(encoding="utf-8"))
        count = sum(item["count"] for item in report["findings"])
        self.assertEqual(count, report["summary"]["issues_found"])
        self.assertEqual(report["summary"]["issues_found"], report["summary"]["issues_fixed"])

    def test_ferry_uncertainty_is_visible(self):
        row = self.rows["whidbey-island-fairgrounds-campground"]
        self.assertGreaterEqual(int(row["Drive Time Minutes"]), 120)
        self.assertIn("ferry", row["Time from Seattle"].lower())
        self.assertIn("queue", row["Drive time note"].lower())

if __name__ == "__main__":
    unittest.main()
