import importlib.util
from pathlib import Path
import unittest


PATH = Path(__file__).with_name("content_scrub.py")
SPEC = importlib.util.spec_from_file_location("content_scrub", PATH)
scrub = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(scrub)


class ContentScrubTests(unittest.TestCase):
    def test_current_dataset_has_no_known_contamination(self):
        result = scrub.audit()
        self.assertGreaterEqual(result["campgrounds_checked"], 126)
        self.assertEqual(result["errors"], [])


if __name__ == "__main__":
    unittest.main()
