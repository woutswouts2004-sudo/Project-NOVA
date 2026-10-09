import unittest
from project_nova.host_finder import assess

class HostFinderTests(unittest.TestCase):
    def test_strict_requirements(self):
        results = assess()
        eligible = {r["name"] for r in results if r["meets_requirements"]}
        self.assertIn("Owner-operated Docker host", eligible)
        self.assertIn("Oracle Cloud Always Free ARM VM", eligible)
        self.assertNotIn("Render free web service", eligible)
        self.assertNotIn("GitHub Actions scheduled runner", eligible)
    def test_relaxed_requirements(self):
        self.assertTrue(all(r["meets_requirements"] for r in assess(False, False, False)))

if __name__ == "__main__":
    unittest.main()
