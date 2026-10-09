import tempfile
import unittest
from pathlib import Path
from project_nova.conversation import converse
from project_nova.llm import Model
from project_nova.memory import Journal

class ConversationTests(unittest.TestCase):
    def test_demo_reply_and_memory(self):
        with tempfile.TemporaryDirectory() as d:
            journal = Journal(Path(d) / "journal.sqlite3")
            result = converse(journal, Model(), "Hello there")
            self.assertEqual(result["mode"], "demo")
            self.assertIn("DEMO MODE", result["reply"])
            self.assertEqual(journal.status()["events"], 2)
            self.assertIn("Hello there", journal.recent()[0]["content"])

    def test_empty_message_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            journal = Journal(Path(d) / "journal.sqlite3")
            with self.assertRaises(ValueError):
                converse(journal, Model(), "  ")

if __name__ == "__main__":
    unittest.main()
