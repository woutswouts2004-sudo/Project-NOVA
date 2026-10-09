import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from project_nova.consent import ConsentRegistry, ConsentDenied

class ConsentTests(unittest.TestCase):
    def test_default_denial_and_scoped_grant(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "consent.json"
            registry = ConsentRegistry(path)
            with self.assertRaises(ConsentDenied):
                registry.check("drive", "document-1", "summarize")
            expiry = (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()
            path.write_text(json.dumps({"grants": [{
                "source": "drive", "resource": "document-1",
                "purposes": ["summarize"], "expires_at": expiry,
                "revoked": False
            }]}))
            self.assertTrue(registry.check("drive", "document-1", "summarize"))
            for source, resource, purpose in [
                ("drive", "document-2", "summarize"),
                ("drive", "document-1", "publish"),
                ("email", "document-1", "summarize")
            ]:
                with self.assertRaises(ConsentDenied):
                    registry.check(source, resource, purpose)

    def test_expired_grant_denied(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "consent.json"
            path.write_text(json.dumps({"grants": [{
                "source": "email", "resource": "inbox", "purposes": ["read"],
                "expires_at": "2020-01-01T00:00:00+00:00", "revoked": False
            }]}))
            with self.assertRaises(ConsentDenied):
                ConsentRegistry(path).check("email", "inbox", "read")

if __name__ == "__main__":
    unittest.main()
