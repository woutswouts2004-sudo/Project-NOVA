import tempfile
import unittest
from pathlib import Path
from project_nova.model_chat import reply
from project_nova.service_identity import register_service, list_services

class FakeModel:
    enabled = True
    def respond(self, system, prompt):
        self.prompt = prompt
        return "Hello, I'm NOVA."

class Disabled:
    enabled = False

class ModelChatTests(unittest.TestCase):
    def test_reply_uses_model(self):
        model = FakeModel()
        self.assertEqual(reply("Hello", model), "Hello, I'm NOVA.")
        self.assertIn("Hello", model.prompt)
    def test_requires_real_model(self):
        with self.assertRaises(RuntimeError):
            reply("Hello", Disabled())
    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            reply("", FakeModel())
    def test_scoped_registry(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "registry.json"
            register_service(path, "code", "GitHub", "nova-bot", ["pull_requests:write"], "authorized operator")
            data = list_services(path)
            self.assertEqual(data["code"]["status"], "registered_not_verified")
            self.assertNotIn("token", data["code"])

if __name__ == "__main__":
    unittest.main()
