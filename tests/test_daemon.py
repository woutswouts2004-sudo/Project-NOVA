import tempfile
import unittest
from pathlib import Path
from project_nova.daemon import Inbox, process_task

class FakeModel:
    enabled = True
    def respond(self, system, prompt):
        return "NOVA processed: " + prompt[-12:]

class FakeJournal:
    def __init__(self):
        self.events = []
    def add(self, kind, content):
        self.events.append((kind, content))

class DaemonTests(unittest.TestCase):
    def test_queue_and_process(self):
        with tempfile.TemporaryDirectory() as directory:
            inbox = Inbox(Path(directory) / "inbox.db")
            task_id = inbox.submit("Please investigate memory")
            journal = FakeJournal()
            self.assertTrue(process_task(inbox, FakeModel(), journal))
            item = inbox.recent()[0]
            self.assertEqual(item["id"], task_id)
            self.assertEqual(item["status"], "done")
            self.assertTrue(journal.events)
            self.assertFalse(process_task(inbox, FakeModel(), journal))
    def test_invalid_task(self):
        with tempfile.TemporaryDirectory() as directory:
            inbox = Inbox(Path(directory) / "inbox.db")
            with self.assertRaises(ValueError):
                inbox.submit("  ")

if __name__ == "__main__":
    unittest.main()
