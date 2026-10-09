import tempfile
import unittest
from pathlib import Path
from project_nova.workspace_editor import write_project_file

class WorkspaceEditorTests(unittest.TestCase):
    def test_create_and_replace_with_backup(self):
        with tempfile.TemporaryDirectory() as directory:
            first = write_project_file(directory, "my_project/main.py", "print('one')\n")
            self.assertFalse(first["backup"])
            second = write_project_file(directory, "my_project/main.py", "print('two')\n")
            self.assertTrue(second["backup"])
            target = Path(directory) / "my_project" / "main.py"
            self.assertEqual(target.read_text(), "print('two')\n")
            self.assertEqual(target.with_name("main.py.nova-backup").read_text(), "print('one')\n")
    def test_reject_escape(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(PermissionError):
                write_project_file(directory, "../outside.txt", "bad")
    def test_reject_invalid_python_without_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            write_project_file(directory, "test.py", "x = 1\n")
            with self.assertRaises(SyntaxError):
                write_project_file(directory, "test.py", "def broken(:\n")
            self.assertEqual((Path(directory) / "test.py").read_text(), "x = 1\n")

if __name__ == "__main__":
    unittest.main()
