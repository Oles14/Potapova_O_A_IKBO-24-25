
"""Автоматические тесты четвёртого этапа."""

import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_PATH))

from vfs import VirtualFileSystem
from commands import ShellCommands, CommandError


class TestStage4(unittest.TestCase):

    def setUp(self):
        vfs_path = (
            PROJECT_ROOT / "scripts" / "vfs_stage4.json"
        )

        self.vfs = VirtualFileSystem(vfs_path)
        self.shell = ShellCommands(self.vfs)

    def test_ls_root(self):
        result = self.shell.execute("ls", [])

        self.assertIn("home/", result)
        self.assertIn("etc/", result)
        self.assertNotIn(".hidden.txt", result)

    def test_ls_hidden(self):
        result = self.shell.execute("ls", ["-a"])

        self.assertIn(".hidden.txt", result)

    def test_cd_absolute(self):
        self.shell.execute(
            "cd",
            ["/home/student/documents"]
        )

        self.assertEqual(
            self.shell.current_path(),
            "/home/student/documents"
        )

    def test_cd_relative(self):
        self.shell.execute("cd", ["/home/student"])
        self.shell.execute("cd", ["documents"])

        self.assertEqual(
            self.shell.current_path(),
            "/home/student/documents"
        )

    def test_cd_parent(self):
        self.shell.execute(
            "cd",
            ["/home/student/documents"]
        )

        self.shell.execute("cd", [".."])

        self.assertEqual(
            self.shell.current_path(),
            "/home/student"
        )

    def test_cd_missing(self):
        with self.assertRaises(CommandError):
            self.shell.execute(
                "cd",
                ["/not_existing"]
            )

    def test_cd_file_error(self):
        with self.assertRaises(CommandError):
            self.shell.execute(
                "cd",
                ["/readme.txt"]
            )

    def test_tail_last_three(self):
        self.shell.execute(
            "cd",
            ["/home/student/documents"]
        )

        result = self.shell.execute(
            "tail",
            ["-n", "3", "notes.txt"]
        )

        self.assertEqual(
            result,
            "Line 10\nLine 11\nLine 12"
        )

    def test_tail_default(self):
        result = self.shell.execute(
            "tail",
            ["/home/student/documents/notes.txt"]
        )

        self.assertEqual(
            len(result.splitlines()),
            10
        )

    def test_tail_zero(self):
        result = self.shell.execute(
            "tail",
            ["-n", "0", "/readme.txt"]
        )

        self.assertEqual(result, "")

    def test_tail_invalid_number(self):
        with self.assertRaises(CommandError):
            self.shell.execute(
                "tail",
                ["-n", "abc", "/readme.txt"]
            )

    def test_uptime(self):
        result = self.shell.execute(
            "uptime",
            []
        )

        self.assertIn(
            "Время работы эмулятора:",
            result
        )

    def test_unknown_command(self):
        with self.assertRaises(CommandError):
            self.shell.execute(
                "unknown",
                []
            )

    def test_original_json_unchanged(self):
        import hashlib

        path = (
            PROJECT_ROOT / "scripts" / "vfs_stage4.json"
        )

        before = hashlib.sha256(
            path.read_bytes()
        ).hexdigest()

        self.shell.execute("ls", [])
        self.shell.execute("cd", ["/home"])
        self.shell.execute("uptime", [])

        after = hashlib.sha256(
            path.read_bytes()
        ).hexdigest()

        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
