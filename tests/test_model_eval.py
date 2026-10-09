import unittest
from project_nova.dataset_manifest import validate_manifest

class DatasetManifestTests(unittest.TestCase):
    def test_valid_original_data(self):
        data = {"source": "Author-written experimental corpus",
                "license": "ORIGINAL-OWNED", "contains_private_chats": False,
                "visitor_consent_required": False, "permission_confirmed": True}
        self.assertEqual(validate_manifest(data), data)
    def test_reject_private_or_unlicensed(self):
        base = {"source": "author", "license": "ORIGINAL-OWNED",
                "contains_private_chats": False, "visitor_consent_required": False,
                "permission_confirmed": True}
        for change in ({"contains_private_chats": True},
                       {"license": "unknown"}, {"permission_confirmed": False},
                       {"visitor_consent_required": True}):
            with self.assertRaises(ValueError):
                validate_manifest({**base, **change})
