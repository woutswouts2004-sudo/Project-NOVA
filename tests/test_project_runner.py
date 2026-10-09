import tempfile
import unittest
from pathlib import Path
from project_nova.project_runner import run_steps
from project_nova.memory import Journal
from project_nova.broker import Broker

class FakeModel:
    enabled = True
    def respond(self, system, prompt):
        return "An original reflection."

class ProjectRunnerTests(unittest.TestCase):
    def test_finite_steps(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            journal = Journal(root / "journal.sqlite3")
            broker = Broker(root)
            results = run_steps(journal, FakeModel(), broker, steps=3)
            self.assertEqual([r["goal"] for r in results],
                             ["creative-writing", "visual-ideas", "philosophy"])
            self.assertEqual(journal.status()["events"], 9)
            self.assertTrue((root / "workspace" / results[0]["artifact"]).exists())
    def test_budget(self):
        for value in (0, 21, -1, 1.5):
            with self.assertRaises(ValueError):
                run_steps(None, None, None, steps=value)
