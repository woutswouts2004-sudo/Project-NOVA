import tempfile
import unittest
from pathlib import Path
from project_nova.agent import Agent
from project_nova.broker import Broker, Denied
from project_nova.llm import Model
from project_nova.memory import Journal

class FoundationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.broker = Broker(self.root)
        self.journal = Journal(self.root / "data" / "test.sqlite3")

    def tearDown(self):
        self.tmp.cleanup()

    def test_demo_journals(self):
        result = Agent(self.journal, Model(), self.broker).step()
        self.assertEqual(result["mode"], "demo")
        self.assertEqual(self.journal.status()["events"], 1)

    def test_notes_within_workspace(self):
        self.assertEqual(self.broker.write_note("ideas/one.md", "hello")["saved"], "ideas/one.md")
        with self.assertRaises(Denied):
            self.broker.write_note("../policy/capabilities.json", "{}")
        with self.assertRaises(Denied):
            self.broker.write_note("code.py", "print(1)")

    def test_purchase_and_shell_denied(self):
        with self.assertRaises(Denied):
            self.broker.request_purchase()
        with self.assertRaises(Denied):
            self.broker.request_shell("ls")

    def test_private_network_denied(self):
        for url in ["http://example.com", "https://127.0.0.1/",
                    "https://localhost/", "https://169.254.169.254/"]:
            with self.assertRaises(Denied):
                self.broker.check_research_url(url)

if __name__ == "__main__":
    unittest.main()
