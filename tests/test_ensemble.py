import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from project_nova.ensemble import Ensemble

class Fake:
    enabled = True
    def __init__(self, name, fail=False):
        self.name, self.fail, self.calls = name, fail, []
    def respond(self, system, prompt):
        self.calls.append(prompt)
        if self.fail:
            raise OSError("offline")
        return self.name

class EnsembleTests(unittest.TestCase):
    def test_route_to_coding(self):
        coding, general = Fake("code"), Fake("general")
        engine = Ensemble([("general", general), ("coding", coding)])
        self.assertEqual(engine.respond("system", "Fix my python code"), "code")
        self.assertEqual(len(general.calls), 0)
    def test_fallback(self):
        engine = Ensemble([("coding", Fake("down", True)), ("general", Fake("backup"))])
        self.assertEqual(engine.respond("system", "Fix python"), "backup")
    def test_collaboration_review(self):
        engine = Ensemble([("general", Fake("first")), ("reasoning", Fake("second")), ("review", Fake("merged"))], "collaborate")
        self.assertEqual(engine.respond("system", "hello"), "merged")
    def test_missing_credentials(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.json"
            path.write_text(json.dumps({"models":[{"role":"general","base":"https://example.com/v1","model":"test","key_env":"NOVA_TEST_MISSING_KEY"}]}))
            with patch.dict(os.environ, {}, clear=True):
                self.assertFalse(Ensemble.from_config(path).enabled)

if __name__ == "__main__":
    unittest.main()
