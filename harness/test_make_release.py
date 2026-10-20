#!/usr/bin/env python3
"""Self-test for make_release.py, in temporary git repositories only.

    python3 harness/test_make_release.py

Never runs a real kit's make_release.py. Each test copies the make_release.py beside this
file into a stand-in master, <tmp>/work/KEEL-FACTORY/, which holds a VERSION of 9.9.9,
release notes, a manual and a stub for every self-test and for check_kit.py, and runs that
copy. A release it cuts therefore lands in <tmp>/work/KEEL-FACTORY-releases/, and every
run asserts first that the copy's master is inside <tmp>. Each run gets HOME, TMPDIR and
an empty git config inside <tmp>, and no GIT_* variable from the caller, so a setting
such as tag.gpgSign can neither block nor change it. Standard library only, plus git.
"""

from __future__ import annotations

import ast
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "make_release.py"
KIT = SCRIPT.parent.parent
VERSION = "9.9.9"
TAG = f"v{VERSION}"
STUB_OK = "import sys\nsys.exit(0)\n"
STUB_FAIL = "import sys\nsys.exit(1)\n"
MANUAL = "# Stand-in manual\n\n## 3. Setting up a machine\n\nClone the bundle.\n"
# Not covered by the house rule (a test_*.py beside each script): git's own folder,
# scratch work, bytecode, and the vendored board skills, which keep their upstream layout.
NOT_KIT = {".git", ".scratch", "__pycache__"}
VENDORED = Path("keel") / "skills-board"


def self_tests(script: Path) -> list[str]:
    """SELF_TESTS as the script lists it, read with ast, so none of its code runs."""
    tree = ast.parse(script.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
                isinstance(target, ast.Name) and target.id == "SELF_TESTS" for target in node.targets):
            return ast.literal_eval(node.value)
    raise AssertionError(f"{script} has no SELF_TESTS list")


class Release(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(os.path.realpath(tempfile.mkdtemp(prefix="keel-release-test-")))
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        for name in ("home", "tmpdir"):
            (self.tmp / name).mkdir()
        (self.tmp / "gitconfig").write_text("", encoding="utf-8")
        self.work = self.tmp / "work"
        self.master = self.work / "KEEL-FACTORY"
        self.script = self.master / "harness" / "make_release.py"
        self.out = self.work / "KEEL-FACTORY-releases" / TAG
        self.tests = self_tests(SCRIPT)

    def env(self) -> dict[str, str]:
        """Every git and script run: no caller GIT_* variable, config and temp files in <tmp>."""
        env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        env.update(HOME=str(self.tmp / "home"), XDG_CONFIG_HOME=str(self.tmp / "home" / ".config"),
                   TMPDIR=str(self.tmp / "tmpdir"), GIT_CONFIG_GLOBAL=str(self.tmp / "gitconfig"),
                   GIT_CONFIG_NOSYSTEM="1", GIT_CEILING_DIRECTORIES=str(self.tmp),
                   GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t",
                   GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t", PYTHONDONTWRITEBYTECODE="1")
        return env

    def git(self, *args: str, cwd: Path | None = None) -> str:
        result = subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", *args],
                                cwd=cwd or self.master, capture_output=True, text=True, env=self.env())
        self.assertEqual(result.returncode, 0, f"git {' '.join(args)}: {result.stderr}")
        return result.stdout.strip()

    def sh(self, command: str, cwd: Path) -> subprocess.CompletedProcess:
        """One README-FIRST line, pasted into /bin/sh: the shell expands "$PWD" and "~"."""
        env = {k: v for k, v in self.env().items() if k not in ("PWD", "OLDPWD")}
        return subprocess.run(["/bin/sh", "-c", command], cwd=cwd, capture_output=True, text=True, env=env)

    def make_master(self, notes: str = TAG, failing: tuple[str, ...] = (), repo: bool = True):
        """The stand-in kit, committed on main unless repo is False."""
        self.script.parent.mkdir(parents=True)
        shutil.copy2(SCRIPT, self.script)
        (self.master / "VERSION").write_text(VERSION + "\n", encoding="utf-8")
        (self.master / "RELEASES.md").write_text(f"# Releases\n\n## {notes}\n\nNotes.\n", encoding="utf-8")
        (self.master / "MANUAL.md").write_text(MANUAL, encoding="utf-8")
        for rel in self.tests + ["harness/check_kit.py"]:
            stub = self.master / rel
            stub.parent.mkdir(parents=True, exist_ok=True)
            stub.write_text(STUB_FAIL if rel in failing else STUB_OK, encoding="utf-8")
        if repo:
            self.git("init", "--quiet")
            self.git("symbolic-ref", "HEAD", "refs/heads/main")
            self.git("add", "-A")
            self.git("commit", "--quiet", "-m", "stand-in kit")

    def snapshot(self) -> dict:
        """What a release could change: the files beside the master, the tags, the tree."""
        beside = {p.relative_to(self.work).as_posix(): p.read_bytes() if p.is_file() else None
                  for p in self.work.rglob("*") if p != self.master and self.master not in p.parents}
        if not (self.master / ".git").exists():
            return {"beside": beside, "repo": False}
        return {"beside": beside, "tags": self.git("for-each-ref", "refs/tags"),
                "head": self.git("rev-parse", "HEAD"), "status": self.git("status", "--porcelain")}

    def release(self):
        """Run the copy in the stand-in master, never a real kit's script."""
        self.assertTrue(self.script.is_file())
        self.assertNotEqual(self.script.resolve(), SCRIPT)
        self.assertEqual(self.script.resolve().parent.parent, self.master, "MASTER must be the stand-in")
        self.assertIn(self.tmp, self.master.parents)
        before = self.snapshot()
        result = subprocess.run([sys.executable, "-B", str(self.script)], cwd=self.tmp,
                                capture_output=True, text=True, env=self.env())
        return before, result

    def assertRefused(self, result, *phrases: str):
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertTrue(result.stdout.startswith("refused: "), result.stdout + result.stderr)
        for phrase in phrases:
            self.assertIn(phrase, result.stdout)
        self.assertNotIn("Traceback", result.stderr)

    def assertNothingWritten(self, before: dict):
        self.assertEqual(self.snapshot(), before)

    def assertProven(self, result):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(f"release {TAG} proven", result.stdout)

    # Refusals: each one comes before anything is written.

    def test_off_main_refuses_and_writes_nothing(self):
        self.make_master()
        self.git("checkout", "--quiet", "-b", "feature")
        before, result = self.release()
        self.assertRefused(result, "releases are cut from main", "HEAD is on feature")
        self.assertNothingWritten(before)
        self.assertFalse(self.out.parent.exists())

    def test_detached_head_refuses_and_writes_nothing(self):
        self.make_master()
        self.git("checkout", "--quiet", "--detach")
        before, result = self.release()
        self.assertRefused(result, "releases are cut from main", "HEAD is detached")
        self.assertNothingWritten(before)

    def test_uncommitted_changes_refuse(self):
        self.make_master()
        (self.master / "draft.txt").write_text("not committed", encoding="utf-8")
        before, result = self.release()
        self.assertRefused(result, "uncommitted changes")
        self.assertNothingWritten(before)

    def test_missing_release_notes_refuse(self):
        self.make_master(notes="v9.9.8")
        before, result = self.release()
        self.assertRefused(result, f"RELEASES.md has no '## {TAG}' section")
        self.assertNothingWritten(before)

    def test_an_existing_release_folder_is_never_overwritten(self):
        self.make_master()
        self.out.mkdir(parents=True)
        (self.out / "keep.txt").write_text("an earlier release", encoding="utf-8")
        before, result = self.release()
        self.assertRefused(result, "already exists; a release is never overwritten")
        self.assertNothingWritten(before)

    def test_a_tag_on_another_commit_refuses_and_is_not_moved(self):
        self.make_master()
        self.git("tag", "-a", TAG, "-m", "earlier")
        self.git("commit", "--quiet", "--allow-empty", "-m", "later")
        before, result = self.release()
        self.assertRefused(result, f"tag {TAG} already exists on another commit")
        self.assertNothingWritten(before)

    def test_not_a_git_repository_refuses(self):
        self.make_master(repo=False)
        before, result = self.release()
        self.assertRefused(result, f"{self.master} is not a git repository")
        self.assertNothingWritten(before)
        self.assertFalse((self.master / ".git").exists())

    # A release cut on main, entirely inside <tmp>.

    def test_on_main_cuts_and_proves_the_release(self):
        self.make_master()
        before, result = self.release()
        self.assertProven(result)
        bundle, archive, manual = f"KEEL-FACTORY-{TAG}.bundle", f"KEEL-FACTORY-{TAG}.tar.gz", f"MANUAL-{TAG}.md"
        self.assertEqual(sorted(os.listdir(self.work)), ["KEEL-FACTORY", "KEEL-FACTORY-releases"])
        self.assertEqual(os.listdir(self.out.parent), [TAG])
        self.assertEqual(sorted(os.listdir(self.out)),
                         sorted([bundle, archive, manual, "README-FIRST.txt", "SHA256SUMS"]))
        sums = (self.out / "SHA256SUMS").read_text(encoding="utf-8").splitlines()
        self.assertEqual(sums, [f"{hashlib.sha256((self.out / name).read_bytes()).hexdigest()}  {name}"
                                for name in (bundle, archive, manual, "README-FIRST.txt")])
        self.assertEqual((self.out / manual).read_text(encoding="utf-8"), MANUAL)
        self.assertEqual(self.git("cat-file", "-t", TAG), "tag", "the tag must be annotated")
        self.assertEqual(self.git("rev-list", "-n", "1", TAG), before["head"])
        self.assertEqual(self.git("status", "--porcelain"), "")
        for test in self.tests:
            self.assertIn(f"self-test from the fresh clone: {test}: OK", result.stdout)
        self.assertIn("kit check from the fresh clone: OK", result.stdout)

    # README-FIRST, followed word for word from the release folder itself, with HOME in
    # <tmp>, so ~/GitProjects is the machine's own disk and the release folder the drive.

    def readme_first(self) -> list[str]:
        """Cut the release and return README-FIRST's command lines, pinned in order."""
        self.make_master()
        # A merged work branch still sitting at main's commit: a plain clone of the bundle
        # can land on it instead of main (measured with git 2.50.1), so README-FIRST must
        # name the branch.
        self.git("branch", "v1.1-harness-conformance")
        _, result = self.release()
        self.assertProven(result)
        readme = (self.out / "README-FIRST.txt").read_text(encoding="utf-8")
        lines = [line for line in readme.splitlines() if line.startswith("    ")]
        commands = [line.split("  (")[0].strip() for line in lines]
        self.assertEqual(commands, [
            "shasum -a 256 -c SHA256SUMS",
            f'git clone --branch main "$PWD/KEEL-FACTORY-{TAG}.bundle" ~/GitProjects/KEEL-FACTORY',
            "git -C ~/GitProjects/KEEL-FACTORY describe --tags",
            f"mkdir -p ~/GitProjects && tar -xzf KEEL-FACTORY-{TAG}.tar.gz -C ~/GitProjects",
        ], "checksums first, then git, then the no-git route, all onto the local disk\n" + readme)
        self.assertTrue(lines[2].endswith(f"(must print {TAG})"), readme)
        self.assertIn("use your own local path, never the drive", " ".join(readme.split()))
        self.assertNotIn("git checkout v", readme, "a detached HEAD breaks the upgrade pull")
        return commands

    def drive(self) -> dict:
        """The release folder's contents, byte for byte."""
        return {p.relative_to(self.out).as_posix(): p.read_bytes() if p.is_file() else None
                for p in self.out.rglob("*")}

    def follow(self, command: str) -> str:
        """Run one README-FIRST line from the release folder; it must succeed. Its output."""
        result = self.sh(command, cwd=self.out)
        self.assertEqual(result.returncode, 0, f"{command}: {result.stdout}{result.stderr}")
        return result.stdout.strip()

    def check_the_files(self, command: str):
        """README-FIRST's first line. Without shasum on PATH, the same check through hashlib."""
        sums = (self.out / "SHA256SUMS").read_text(encoding="utf-8").splitlines()
        sums = [line.split("  ", 1) for line in sums]
        self.assertEqual(sorted(name for _, name in sums), sorted(set(self.drive()) - {"SHA256SUMS"}))
        if shutil.which("shasum"):
            self.assertEqual(self.follow(command).splitlines(), [f"{name}: OK" for _, name in sums])
        else:
            for digest, name in sums:
                self.assertEqual(hashlib.sha256((self.out / name).read_bytes()).hexdigest(), digest, name)

    def restored(self) -> Path:
        return self.tmp / "home" / "GitProjects" / "KEEL-FACTORY"

    def test_readme_first_restores_onto_main_at_the_tag(self):
        checksum, clone, describe, _ = self.readme_first()
        drive = self.drive()
        self.assertEqual(sorted(drive), sorted([f"KEEL-FACTORY-{TAG}.bundle", f"KEEL-FACTORY-{TAG}.tar.gz",
                                                f"MANUAL-{TAG}.md", "README-FIRST.txt", "SHA256SUMS"]))
        self.check_the_files(checksum)
        self.follow(clone)
        self.assertEqual(self.follow(describe), TAG)
        top = Path(self.git("rev-parse", "--show-toplevel", cwd=self.restored()))
        self.assertEqual(top, self.restored())
        self.assertNotIn(self.out, top.parents, "the master must not be restored onto the drive")
        self.assertEqual(self.git("symbolic-ref", "--short", "HEAD", cwd=self.restored()), "main")
        self.assertEqual(self.drive(), drive, "README-FIRST must write nothing on the drive")

    def test_readme_first_without_git_untars_off_the_drive(self):
        checksum, _, _, untar = self.readme_first()
        drive = self.drive()
        self.check_the_files(checksum)
        self.follow(untar)
        self.assertEqual((self.restored() / "VERSION").read_text(encoding="utf-8"), VERSION + "\n")
        self.assertEqual(self.drive(), drive, "README-FIRST must write nothing on the drive")

    def test_a_tag_already_on_head_is_reused(self):
        self.make_master()
        self.git("tag", "-a", TAG, "-m", "cut by hand")
        tag_object = self.git("rev-parse", TAG)
        _, result = self.release()
        self.assertProven(result)
        self.assertEqual(self.git("rev-parse", TAG), tag_object)

    # The proof: a failure in the fresh clone leaves the release written but not proven.

    def test_a_failing_self_test_leaves_it_not_proven(self):
        failing = self.tests[-1]
        self.make_master(failing=(failing,))
        _, result = self.release()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(f"release {TAG} written to {self.out} but NOT proven", result.stdout)
        self.assertIn(f"self-test from the fresh clone: {failing}: FAILED", result.stdout)
        self.assertIn(f"{failing} failed in the clone", result.stdout)

    def test_a_failing_kit_check_leaves_it_not_proven(self):
        self.make_master(failing=("harness/check_kit.py",))
        _, result = self.release()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("NOT proven", result.stdout)
        self.assertIn("kit check from the fresh clone: FAILED", result.stdout)
        self.assertIn("check_kit.py found problems in the clone", result.stdout)


class HouseRule(unittest.TestCase):
    """Every test_*.py in the kit runs from the fresh clone, this one included."""

    def test_every_self_test_in_the_kit_is_listed(self):
        found = set()
        for root, dirs, files in os.walk(KIT):
            here = Path(root).relative_to(KIT)
            dirs[:] = [d for d in dirs if d not in NOT_KIT and here / d != VENDORED]
            found |= {(here / f).as_posix() for f in files if f.startswith("test_") and f.endswith(".py")}
        listed = self_tests(SCRIPT)
        self.assertEqual(len(listed), len(set(listed)), "a self-test is listed twice")
        self.assertEqual(sorted(listed), sorted(found))
        self.assertIn("harness/test_make_release.py", listed)


if __name__ == "__main__":
    unittest.main(verbosity=1)
