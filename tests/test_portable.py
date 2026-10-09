import json
import tempfile
import unittest
from pathlib import Path
from project_nova.memory import Journal
from project_nova.portable import export_archive, restore_archive
from project_nova.autonomy import choose_goal

class PortableTests(unittest.TestCase):
    def test_backup_restore_and_checksum(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            source = Journal(root / "a.sqlite3")
            source.add("goal", "draw a city")
            path = root / "backup.json"
            export_archive(source, path)
            target = Journal(root / "b.sqlite3")
            self.assertEqual(restore_archive(target, path)["restored"], 1)
            self.assertEqual(target.recent()[0]["content"], "draw a city")
            blob = json.loads(path.read_text())
            blob["payload"]["events"][0]["content"] = "tampered"
            path.write_text(json.dumps(blob))
            with self.assertRaises(ValueError):
                restore_archive(target, path)

    def test_goal_rotation(self):
        with tempfile.TemporaryDirectory() as d:
            j = Journal(Path(d) / "a.sqlite3")
            first = choose_goal(j)
            j.add("goal", first["area"])
            second = choose_goal(j)
            self.assertNotEqual(first["area"], second["area"])

if __name__ == "__main__":
    unittest.main()
