import importlib.util
import csv
from datetime import date
from pathlib import Path
import unittest

PATH = Path(__file__).with_name("trust_workflow.py")
SPEC = importlib.util.spec_from_file_location("trust_workflow", PATH)
trust = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(trust)


class TrustWorkflowTests(unittest.TestCase):
    def test_current_ledgers_are_valid(self):
        self.assertEqual(trust.audit(date(2026, 9, 6))["errors"], [])

    def test_source_requires_attribution_and_https(self):
        self.assertFalse(trust.valid_source({"url": "http://example.com"}))
        self.assertTrue(trust.valid_source({
            "url": "https://example.com/fact", "publisher": "Example",
            "source_family": "example", "evidence": "Explicit fact"
        }))

    def test_silver_lake_content_stays_in_whatcom_county(self):
        with (PATH.parent / "data" / "campgrounds.csv").open(newline="", encoding="utf-8-sig") as source:
            row = next(item for item in csv.DictReader(source) if item["Slug"] == "silver-lake-park")
        combined = " ".join(row.values()).lower()
        self.assertNotIn("cowlitz", combined)
        self.assertNotIn("mount st. helens", combined)
        self.assertIn("whatcom", combined)


if __name__ == "__main__":
    unittest.main()
