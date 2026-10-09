import json
import tempfile
import unittest
from datetime import date
from pathlib import Path
from project_nova.public_studies import make_study, publish

class PublicStudiesTests(unittest.TestCase):
    def test_deterministic_and_transparent(self):
        day = date(2026, 10, 9)
        self.assertEqual(make_study(day), make_study(day))
        self.assertFalse(make_study(day)["model_used"])
        self.assertIn("algorithmically", make_study(day)["kind"])
    def test_publish_once(self):
        with tempfile.TemporaryDirectory() as directory:
            first = publish(directory, date(2026, 10, 9))
            self.assertEqual(first["status"], "created")
            note = Path(directory) / "docs" / "field-notes" / "2026-10-09.json"
            self.assertTrue(note.is_file())
            self.assertEqual(json.loads(note.read_text())["date"], "2026-10-09")
            second = publish(directory, date(2026, 10, 9))
            self.assertEqual(second["status"], "already_exists")

if __name__ == "__main__":
    unittest.main()
