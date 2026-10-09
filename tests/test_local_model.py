import unittest
from project_nova.local_model import LocalModel

class LocalModelTests(unittest.TestCase):
    def test_local_endpoint_only(self):
        self.assertTrue(LocalModel("example-model").enabled)
        for base in ["https://example.com", "http://192.168.1.1:11434",
                     "http://localhost:1234", "http://127.0.0.1:11434/extra"]:
            with self.assertRaises(ValueError):
                LocalModel("example-model", base)
    def test_missing_model_rejected(self):
        with self.assertRaises(ValueError):
            LocalModel("")

if __name__ == "__main__":
    unittest.main()
