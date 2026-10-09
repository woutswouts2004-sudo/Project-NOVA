import tempfile
import unittest
from pathlib import Path
from project_nova.self_development import EDITABLE, proposal_prompt, propose_improvement

class StubModel:
    enabled = True
    def respond(self, system, prompt):
        return "def choose_goal(journal):\n    return {'area': 'art', 'prompt': 'Draw something.'}\n"

class DisabledModel:
    enabled = False

class SelfDevelopmentTests(unittest.TestCase):
    def test_only_allowlisted_targets(self):
        for target in ("project_nova/broker.py", "project_nova/public_api.py",
                       "../private.py", ".github/workflows/tests.yml"):
            with self.assertRaises(ValueError):
                proposal_prompt(target, "x", [])
        for target in EDITABLE:
            self.assertIn(target, proposal_prompt(target, "x", []))
    def test_requires_model(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(RuntimeError):
                propose_improvement(directory, DisabledModel(), EDITABLE[0])
    def test_creates_inert_proposal(self):
        with tempfile.TemporaryDirectory() as directory:
            result = propose_improvement(directory, StubModel(), EDITABLE[0])
            self.assertEqual(result["status"], "awaiting_external_review")
            workspace = Path(directory) / "workspace" / "proposals"
            self.assertEqual(len(list(workspace.glob("*.txt"))), 1)
            self.assertEqual(len(list(workspace.glob("*.json"))), 1)

if __name__ == "__main__":
    unittest.main()
