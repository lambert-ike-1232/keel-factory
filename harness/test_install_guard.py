#!/usr/bin/env python3
"""Self-test for install_guard.py, run against temporary settings files only.

    python3 harness/test_install_guard.py

Every run passes --settings pointing into a temporary folder, so the real
~/.claude/settings.json is never read or written. The installed command is run with sh
in a temporary project. Most cases install from a temporary master whose path holds a
space, a $ and a quote, with a stub guard that exits 7, while the project's own
keel-factory/ copy is a stub that exits 9 and leaves a mark: reaching 7 with no mark is
the proof that the hook runs the master's guard, never the project's. The guard path no
longer depends on the project, so the KEEL-FACTORY negative case is a real check on
every file system. One end-to-end case runs this kit's real guard: it must block a Read
of a fake .env even though the project's copy would allow everything. The OPERATOR.md
test compares the documented command, its placeholder replaced by this master's
shell-quoted guard path, with the one installed.
"""

from __future__ import annotations

import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE / "install_guard.py"
GUARD = "harness/hooks/data-boundary-guard.py"
# What OPERATOR.md shows in place of the master's guard path.
PLACEHOLDER = "'/ABSOLUTE/PATH/TO/harness/hooks/data-boundary-guard.py'"


def temp_home_env(home: Path) -> dict[str, str]:
    """HOME points into the temp folder, so even a broken --settings cannot reach ~/.claude."""
    return {**os.environ, "HOME": str(home)}


# The command v1.0 installed: no exact-name test, and it ran the project's copy.
V1_COMMAND = ('g="$CLAUDE_PROJECT_DIR/keel-factory/harness/hooks/data-boundary-guard.py"; '
              '[ -f "$g" ] || exit 0; exec python3 "$g"')
# The command the early v1.1 build installed: the exact-name test, still the project's copy.
EARLY_V11_COMMAND = ('ls -1 "$CLAUDE_PROJECT_DIR" 2>/dev/null | grep -qxF keel-factory || exit 0; '
                     + V1_COMMAND)
OLDER = {"v1.0": V1_COMMAND, "early v1.1": EARLY_V11_COMMAND}
# The current form, installed from a master somewhere else.
ELSEWHERE_COMMAND = ('ls -1 "$CLAUDE_PROJECT_DIR" 2>/dev/null | grep -qxF keel-factory || exit 0; '
                     'g=/old/master/harness/hooks/data-boundary-guard.py; [ -f "$g" ] || exit 0; '
                     'exec python3 "$g"')


class InstallGuard(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="install-guard-test-"))
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.settings = self.tmp / "settings.json"
        self.backup = self.tmp / "settings.json.before-keel-guard"

    def run_it(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, "-B", str(SCRIPT), "--settings", str(self.settings), *args],
                              capture_output=True, text=True, env=temp_home_env(self.tmp))

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
        self.assertEqual(json.loads(self.backup.read_text()), original)

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
        self.assertIn(PLACEHOLDER, documented, "OPERATOR.md shows the master's path as a placeholder")
        here = documented.replace(PLACEHOLDER, shlex.quote(str(HERE.parent / GUARD)))
        self.assertEqual(self.commands(), [here])

    def test_the_command_runs_this_masters_guard_never_the_projects(self):
        self.run_it()
        [command] = self.commands()
        self.assertIn(f"g={shlex.quote(str(HERE.parent / GUARD))};", command)
        self.assertNotIn("$CLAUDE_PROJECT_DIR/keel-factory/harness", command)

    def write_entry(self, command: str) -> dict:
        original = {"model": "opus", "hooks": {"PreToolUse": [
            {"matcher": "Bash", "hooks": [{"type": "command", "command": "team-hook"}]},
            {"matcher": "Read|Edit|Write|NotebookEdit|Glob|Grep|Bash",
             "hooks": [{"type": "command", "command": command}]}]}}
        self.settings.write_text(json.dumps(original))
        self.backup.unlink(missing_ok=True)
        return original

    def assertUpdatedInPlace(self, original: dict, old: str):
        result = self.run_it()
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("updated", result.stdout)
        current = self.commands()
        self.assertEqual(len(current), 2, current)
        self.assertEqual(current[0], "team-hook")
        self.assertNotEqual(current[1], old)
        self.assertIn("grep -qxF keel-factory", current[1])
        self.assertIn(f"g={shlex.quote(str(HERE.parent / GUARD))};", current[1])
        self.assertEqual(json.loads(self.settings.read_text())["model"], "opus")
        self.assertEqual(json.loads(self.backup.read_text()), original)
        again = self.run_it()
        self.assertIn("already installed", again.stdout)

    def test_an_older_entry_is_updated_in_place(self):
        for form, old in OLDER.items():
            with self.subTest(form=form):
                self.assertUpdatedInPlace(self.write_entry(old), old)

    def test_an_entry_from_another_master_is_repointed_here(self):
        self.assertUpdatedInPlace(self.write_entry(ELSEWHERE_COMMAND), ELSEWHERE_COMMAND)
        self.assertNotIn("/old/master", self.commands()[1])

    def test_remove_takes_out_an_older_entry(self):
        for form, old in {**OLDER, "another master": ELSEWHERE_COMMAND}.items():
            with self.subTest(form=form):
                self.write_entry(old)
                self.assertEqual(self.run_it("--remove").returncode, 0)
                self.assertEqual(self.commands(), ["team-hook"])

    def test_a_hand_wired_bare_guard_is_not_keels_entry(self):
        for bare in ("python3 /x/harness/hooks/data-boundary-guard.py",
                     "python3 /x/keel-factory/harness/hooks/data-boundary-guard.py"):
            with self.subTest(bare=bare):
                self.settings.write_text(json.dumps({"hooks": {"PreToolUse": [
                    {"matcher": "Read", "hooks": [{"type": "command", "command": bare}]}]}}))
                result = self.run_it()
                self.assertIn("installed KEEL's guard", result.stdout)
                current = self.commands()
                self.assertEqual(len(current), 2, current)
                self.assertEqual(current[0], bare)
                self.assertEqual(self.run_it("--remove").returncode, 0)
                self.assertEqual(self.commands(), [bare])


class InstalledCommand(unittest.TestCase):
    """The installed command, run with sh, arms only for an exact keel-factory/ folder and
    then runs the master's guard, never the project's copy."""

    def setUp(self):
        self.tmp = Path(os.path.realpath(tempfile.mkdtemp(prefix="install-guard-cmd-")))
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        master = self.tmp / "KEEL $HOME o'clock"
        (master / "harness" / "hooks").mkdir(parents=True)
        shutil.copy2(SCRIPT, master / "harness" / "install_guard.py")
        self.master_guard = master / GUARD
        self.master_guard.write_text("import sys\nsys.exit(7)\n", encoding="utf-8")
        self.ran = self.tmp / "RAN-PROJECT-COPY"
        settings = self.tmp / "settings.json"
        subprocess.run([sys.executable, "-B", str(master / "harness" / "install_guard.py"),
                        "--settings", str(settings)],
                       capture_output=True, text=True, check=True, env=temp_home_env(self.tmp))
        data = json.loads(settings.read_text())
        self.command = data["hooks"]["PreToolUse"][0]["hooks"][0]["command"]

    def project(self, *names: str, guard_in: str | None = None) -> Path:
        project = self.tmp / "project"
        project.mkdir()
        for name in names:
            (project / name).mkdir()
        if guard_in is not None:
            stub = project / guard_in / GUARD
            stub.parent.mkdir(parents=True)
            stub.write_text(f"import pathlib, sys\npathlib.Path({str(self.ran)!r}).write_text('ran')\n"
                            "sys.exit(9)\n", encoding="utf-8")
        return project

    def run_command(self, project: Path | None) -> int:
        env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": str(self.tmp),
               "PYTHONDONTWRITEBYTECODE": "1"}
        if project is not None:
            env["CLAUDE_PROJECT_DIR"] = str(project)
        return subprocess.run(["sh", "-c", self.command], input="{}", env=env,
                              capture_output=True, text=True).returncode

    def test_arms_for_an_exact_keel_factory(self):
        self.assertEqual(self.run_command(self.project(guard_in="keel-factory")), 7)

    def test_never_runs_the_projects_own_copy(self):
        self.assertEqual(self.run_command(self.project(guard_in="keel-factory")), 7)
        self.assertFalse(self.ran.exists(), "the project's keel-factory/ guard ran")

    def test_does_not_arm_for_another_letter_case(self):
        self.assertEqual(self.run_command(self.project(guard_in="KEEL-FACTORY")), 0)

    def test_does_not_arm_for_a_name_that_only_contains_it(self):
        project = self.project("old-keel-factory", guard_in="KEEL-FACTORY")
        self.assertEqual(self.run_command(project), 0)

    def test_disarms_when_the_masters_guard_is_gone(self):
        self.master_guard.unlink()
        self.assertEqual(self.run_command(self.project(guard_in="keel-factory")), 0)
        self.assertFalse(self.ran.exists(), "the project's keel-factory/ guard ran")

    def test_does_nothing_without_a_project_dir(self):
        self.assertEqual(self.run_command(None), 0)


class EndToEnd(unittest.TestCase):
    """This kit's real guard blocks a Read of a fake .env in a project whose own
    keel-factory/ guard would allow everything."""

    def test_the_masters_guard_blocks_even_when_the_projects_copy_allows(self):
        tmp = Path(os.path.realpath(tempfile.mkdtemp(prefix="install-guard-e2e-")))
        self.addCleanup(shutil.rmtree, tmp, ignore_errors=True)
        settings = tmp / "settings.json"
        subprocess.run([sys.executable, "-B", str(SCRIPT), "--settings", str(settings)],
                       capture_output=True, text=True, check=True, env=temp_home_env(tmp))
        command = json.loads(settings.read_text())["hooks"]["PreToolUse"][0]["hooks"][0]["command"]
        project = tmp / "project"
        allow_all = project / "keel-factory" / GUARD
        allow_all.parent.mkdir(parents=True)
        allow_all.write_text("import sys\nsys.exit(0)\n", encoding="utf-8")
        fake = project / ".env"
        fake.write_text("DUMMY=not-a-real-value\n", encoding="utf-8")
        payload = json.dumps({"tool_name": "Read", "tool_input": {"file_path": str(fake)},
                              "cwd": str(project)})
        env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": str(tmp),
               "PYTHONDONTWRITEBYTECODE": "1", "CLAUDE_PROJECT_DIR": str(project)}
        ran = subprocess.run(["sh", "-c", command], input=payload, env=env, capture_output=True, text=True)
        self.assertEqual(ran.returncode, 2, ran.stdout + ran.stderr)
        self.assertIn("BLOCKED by data-boundary-guard", ran.stderr)
        self.assertIn("secret-shaped", ran.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
