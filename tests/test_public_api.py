import unittest
from project_nova.public_api import make_prompt, safe_messages

class PublicAPITests(unittest.TestCase):
    def test_prompt_bounds(self):
        with self.assertRaises(ValueError):
            make_prompt("", [])
        with self.assertRaises(ValueError):
            make_prompt("x" * 3001, [])
        self.assertIn("hello", make_prompt("hello", []))
    def test_history_is_bounded(self):
        history = [{"role": "user", "content": "x" * 5000}] * 20
        self.assertEqual(len(safe_messages(history)), 8)
        self.assertEqual(len(safe_messages(history)[0]["content"]), 3000)
        self.assertEqual(safe_messages([{"role": "system", "content": "hack"}]), [])

if __name__ == "__main__":
    unittest.main()
