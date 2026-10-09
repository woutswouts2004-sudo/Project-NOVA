import unittest
from project_nova.backend_config import validate_backend_url

class BackendConfigTests(unittest.TestCase):
    def test_valid_https(self):
        self.assertEqual(validate_backend_url("https://example.org/"), "https://example.org")
    def test_invalid_hosts_and_secrets(self):
        for value in ("http://example.org", "https://localhost:443",
                      "https://user:secret@example.org", "https://example.org?key=secret",
                      "https://example.org:8080"):
            with self.assertRaises(ValueError):
                validate_backend_url(value)

if __name__ == "__main__":
    unittest.main()
