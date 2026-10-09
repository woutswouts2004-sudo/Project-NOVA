import tempfile
import unittest
from pathlib import Path
from project_nova.broker import Broker
from project_nova.proposals import propose_code_change

class ProposalTests(unittest.TestCase):
    def test_editable_code_proposal(self):
        with tempfile.TemporaryDirectory() as directory:
            broker = Broker(Path(directory))
            result = propose_code_change(broker, "project_nova/agent.py",
                                         "VALUE = 1\n", "experiment")
            self.assertEqual(result["status"], "awaiting_external_review")
            self.assertTrue(list((Path(directory) / "workspace" / "proposals").glob("*.txt")))

    def test_protected_files_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            broker = Broker(Path(directory))
            for target in ["project_nova/broker.py", "project_nova/../policy/evil.py",
                           "policy/capabilities.py"]:
                with self.assertRaises(ValueError):
                    propose_code_change(broker, target, "VALUE = 1\n", "test")

if __name__ == "__main__":
    unittest.main()
