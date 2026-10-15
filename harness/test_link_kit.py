#!/usr/bin/env python3
"""Self-test for link_kit.py -- every refusal watched happening, not only the happy path.

    python3 harness/test_link_kit.py

Runs against a throwaway fake master built in a temporary folder, never against the real
one. Standard library only; the git cases are skipped, and reported as skipped, when git
is absent.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
GUARD = HERE / "hooks" / "data-boundary-guard.py"


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(os.path.realpath(tempfile.mkdtemp(prefix="link-kit-test-")))
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.master = self.tmp / "MASTER"
        (self.master / "harness" / "hooks").mkdir(parents=True)
        (self.master / "keel").mkdir()
        (self.master / ".scratch").mkdir()
        (self.master / "__pycache__").mkdir()
        shutil.copy2(HERE / "link_kit.py", self.master / "harness" / "link_kit.py")
        shutil.copy2(GUARD, self.master / "harness" / "hooks" / "data-boundary-guard.py")
        (self.master / "keel" / "rules.md").write_text("v1\n")
        (self.master / "OPERATOR.md").write_text("operator\n")
        (self.master / ".gitignore").write_text("__pycache__/\n")
        (self.master / ".scratch" / "handoff.md").write_text("factory notes\n")
        self.project = self.tmp / "project"
        self.project.mkdir()
        self.kit = self.project / "keel-factory"

    def run_kit(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, "-B", str(self.master / "harness" / "link_kit.py"), *args],
                              capture_output=True, text=True)


class LinkKit(Base):
    def test_link_makes_every_path_resolve_and_keeps_notes_local(self):
        self.assertEqual(self.run_kit(str(self.project)).returncode, 0)
        self.assertEqual((self.kit / "keel" / "rules.md").read_text(), "v1\n")
        self.assertTrue((self.kit / "OPERATOR.md").is_symlink())
        self.assertFalse((self.kit / ".scratch").exists(), "the master's own notes must not be linked in")
        self.assertFalse((self.kit / "__pycache__").exists())
        self.assertFalse((self.kit / ".gitignore").exists(), "the kit must not bring its ignore rules into a project")
        self.assertTrue((self.kit / ".ops").is_dir() and not (self.kit / ".ops").is_symlink())
        (self.kit / ".ops" / "debrief.md").write_text("mission\n")
        self.assertFalse((self.master / ".ops").exists(), "a project's notes must never land in the master")

    def test_an_edit_to_the_master_reaches_the_project(self):
        self.run_kit(str(self.project))
        (self.master / "keel" / "rules.md").write_text("v2\n")
        self.assertEqual((self.kit / "keel" / "rules.md").read_text(), "v2\n")

    def test_linking_twice_is_harmless(self):
        self.run_kit(str(self.project))
        result = self.run_kit(str(self.project))
        self.assertEqual(result.returncode, 0)
        self.assertIn("0 new link(s)", result.stdout)

    def test_a_real_copy_is_refused_and_left_alone(self):
        self.kit.mkdir()
        (self.kit / "OPERATOR.md").write_text("old full copy\n")
        for args in ([str(self.project)], [str(self.project), "--remove"]):
            with self.subTest(args=args):
                result = self.run_kit(*args)
                self.assertEqual(result.returncode, 1)
                self.assertIn("refused", result.stdout)
                self.assertEqual((self.kit / "OPERATOR.md").read_text(), "old full copy\n")

    def test_the_master_itself_is_refused(self):
        for target in (self.master, self.master / "keel", self.tmp):
            with self.subTest(target=target):
                self.assertEqual(self.run_kit(str(target)).returncode, 1)

    def test_remove_deletes_links_never_their_targets(self):
        self.run_kit(str(self.project))
        result = self.run_kit(str(self.project), "--remove")
        self.assertEqual(result.returncode, 0)
        self.assertFalse(self.kit.exists())
        self.assertEqual((self.master / "keel" / "rules.md").read_text(), "v1\n")
        self.assertEqual((self.master / ".scratch" / "handoff.md").read_text(), "factory notes\n")

    def test_remove_keeps_a_project_s_notes(self):
        self.run_kit(str(self.project))
        (self.kit / ".ops" / "debrief.md").write_text("mission\n")
        result = self.run_kit(str(self.project), "--remove")
        self.assertIn("kept", result.stdout)
        self.assertEqual((self.kit / ".ops" / "debrief.md").read_text(), "mission\n")
        self.assertFalse((self.kit / "keel").exists())

    def test_remove_unlinks_a_whole_folder_link_without_following_it(self):
        self.kit.symlink_to(self.master)
        self.assertEqual(self.run_kit(str(self.project), "--remove").returncode, 0)
        self.assertFalse(self.kit.exists() or self.kit.is_symlink())
        self.assertEqual((self.master / "keel" / "rules.md").read_text(), "v1\n")


@unittest.skipUnless(shutil.which("git"), "git is not installed, so the guard-through-links cases did not run")
class GuardThroughLinks(Base):
    def guard(self, file_path: str) -> int:
        hook = self.project / "keel-factory" / "harness" / "hooks" / "data-boundary-guard.py"
        payload = json.dumps({"cwd": str(self.project), "tool_input": {"file_path": file_path}})
        return subprocess.run([sys.executable, "-B", str(hook)], input=payload, capture_output=True,
                              text=True, env={**os.environ, "CLAUDE_PROJECT_DIR": str(self.project)}).returncode

    def test_the_guard_arms_and_judges_paths_through_the_links(self):
        subprocess.run(["git", "init", "-q", str(self.project)], check=True)
        (self.project / ".gitignore").write_text(".env\n")
        self.run_kit(str(self.project))
        # The hook's self-disarm test looks for exactly this file:
        self.assertTrue((self.project / "keel-factory/harness/hooks/data-boundary-guard.py").is_file())
        self.assertEqual(self.guard(str(self.kit / "keel" / "rules.md")), 0)
        self.assertEqual(self.guard(str(self.kit / ".ops" / "notes.md")), 0)
        self.assertEqual(self.guard(str(self.project / ".env")), 2)
        status = subprocess.run(["git", "status", "--porcelain"], cwd=self.project,
                                capture_output=True, text=True).stdout.split()
        self.assertIn("keel-factory/", status)


if __name__ == "__main__":
    unittest.main(verbosity=2)
