#!/usr/bin/env python3
"""Self-test for install_guard.py, run against temporary settings files only.

    python3 harness/test_install_guard.py
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE / "install_guard.py"


class InstallGuard(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="install-guard-test-"))
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.settings = self.tmp / "settings.json"

    def run_it(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, "-B", str(SCRIPT), "--settings", str(self.settings), *args],
                              capture_output=True, text=True)

    def commands(self) -> list[str]:
        data = json.loads(self.settings.read_text())
        return [h["command"] for e in data.get("hooks", {}).get("PreToolUse", []) for h in e["hooks"]]

    def test_creates_the_file_when_there_is_none(self):
        self.assertEqual(self.run_it().returncode, 0)
        self.assertEqual(len(self.commands()), 1)

    def test_keeps_everything_else_and_saves_the_original(self):
        original = {"model": "opus", "env": {"SECRET_TOKEN": "do-not-print"},
                    "hooks": {"PreToolUse": [{"matcher": "Bash", "hooks": [{"type": "command", "command": "team-hook"}]}],
                              "Stop": [{"matcher": "*", "hooks": [{"type": "command", "command": "notify"}]}]}}
        self.settings.write_text(json.dumps(original))
        result = self.run_it()
        self.assertEqual(result.returncode, 0)
        self.assertNotIn("do-not-print", result.stdout)
        data = json.loads(self.settings.read_text())
        self.assertEqual(data["model"], "opus")
        self.assertEqual(data["env"], {"SECRET_TOKEN": "do-not-print"})
        self.assertEqual(data["hooks"]["Stop"], original["hooks"]["Stop"])
        self.assertIn("team-hook", self.commands())
        self.assertEqual(json.loads((self.tmp / "settings.json.before-keel-guard").read_text()), original)

    def test_running_twice_changes_nothing(self):
        self.run_it()
        before = self.settings.read_text()
        result = self.run_it()
        self.assertIn("already installed", result.stdout)
        self.assertEqual(self.settings.read_text(), before)

    def test_remove_takes_out_only_keels_entry(self):
        self.settings.write_text(json.dumps({"model": "opus", "hooks": {"PreToolUse": [
            {"matcher": "Bash", "hooks": [{"type": "command", "command": "team-hook"}]}]}}))
        self.run_it()
        self.assertEqual(self.run_it("--remove").returncode, 0)
        self.assertEqual(self.commands(), ["team-hook"])
        self.assertEqual(json.loads(self.settings.read_text())["model"], "opus")

    def test_a_malformed_file_is_refused_and_left_alone(self):
        for text in ("{not json", '["a list"]', '{"hooks": "not an object"}'):
            with self.subTest(text=text):
                self.settings.write_text(text)
                result = self.run_it()
                self.assertEqual(result.returncode, 1)
                self.assertEqual(self.settings.read_text(), text)

    def test_the_installed_command_is_the_one_operator_md_documents(self):
        self.run_it()
        operator = (HERE.parent / "OPERATOR.md").read_text()
        block = json.loads(re.search(r"```json\n(.*?)```", operator, re.S).group(1))
        documented = block["hooks"]["PreToolUse"][0]["hooks"][0]["command"]
        self.assertEqual(self.commands(), [documented])


if __name__ == "__main__":
    unittest.main(verbosity=2)
