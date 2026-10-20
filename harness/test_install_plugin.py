#!/usr/bin/env python3
"""Self-test for install_plugin.py, against temporary home folders only.

    python3 harness/test_install_plugin.py

Never touches the real ~/.claude, ~/.agents or ~/.codex: every run sets HOME to a
temporary folder and drops CODEX_HOME from its environment (a test sets its own), and
passes --claude-home and --agents-home pointing into that folder. Every run but the two
tests of the Codex-home default also passes --codex-home there. Write errors are staged by
making temporary folders or files read-only, restored before cleanup; those tests are
skipped as root or on Windows, where chmod does not deny the write. Standard library only.
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

SCRIPT = Path(__file__).resolve().parent / "install_plugin.py"
MASTER = SCRIPT.parent.parent
CORE = ["helm", "keel", "keel-prove", "crew", "deep-research", "reverse-engineering",
        "commit", "focused-implementation", "handoff", "orchestrate-implementation",
        "post-creation-audit", "resume-handoff", "spike", "task-board-init",
        "task-board-triage", "task-interview", "to-follow-on", "to-task"]
DOCS = ["diataxis-audit-docs", "diataxis-manage-docs", "diataxis-migrate-docs", "diataxis-update-docs"]

# A stub keel_hook.py: exits 7 for "session --harness codex", 8 for "guard --harness
# codex", 3 for anything else. Reaching it with the right arguments is the proof.
STUB_HOOK = """import sys
args = sys.argv[1:]
sys.exit(7 if args == ["session", "--harness", "codex"] else
         8 if args == ["guard", "--harness", "codex"] else 3)
"""

# The v1.0 form of the Codex hook commands: unquoted path, no --harness.
OLD_SESSION = 'g="/old/master/harness/hooks/keel_hook.py"; [ -f "$g" ] || exit 0; exec python3 "$g" session'
OLD_GUARD = 'g="/old/master/harness/hooks/keel_hook.py"; [ -f "$g" ] || exit 0; exec python3 "$g" guard'

# Runs the installer in-process with Path.symlink_to raising the error Windows gives
# without Developer Mode, for links under the folder named in argv[1] only.
SYMLINK_FAILS = """import pathlib, runpy, sys
script, fail_under = sys.argv[1], sys.argv[2]
real = pathlib.Path.symlink_to
def symlink_to(self, target, target_is_directory=False):
    if str(self).startswith(fail_under):
        raise OSError(1, "A required privilege is not held by the client")
    return real(self, target, target_is_directory)
pathlib.Path.symlink_to = symlink_to
sys.argv = [script] + sys.argv[3:]
runpy.run_path(script, run_name="__main__")
"""


class Homes(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(os.path.realpath(tempfile.mkdtemp(prefix="keel-install-test-")))
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.home = self.tmp / "home"
        self.home.mkdir()
        self.claude = self.tmp / "claude"
        self.agents = self.tmp / "agents"
        self.codex = self.tmp / "codex"

    def env(self, **extra: str) -> dict[str, str]:
        """The environment for every run: HOME is the temp home and CODEX_HOME is unset."""
        env = {k: v for k, v in os.environ.items() if k != "CODEX_HOME"}
        env["HOME"] = str(self.home)
        env.update(extra)
        return env

    def homes(self, codex_home: bool = True) -> list[str]:
        flags = ["--claude-home", str(self.claude), "--agents-home", str(self.agents)]
        return flags + (["--codex-home", str(self.codex)] if codex_home else [])

    def run_it(self, *args, script: Path = SCRIPT, codex_home: bool = True, env=None):
        cmd = [sys.executable, "-B", str(script), *self.homes(codex_home), *args]
        return subprocess.run(cmd, capture_output=True, text=True, env=env or self.env())

    def hooks(self):
        return json.loads((self.codex / "hooks.json").read_text(encoding="utf-8"))

    def keel_commands(self):
        return [h["command"] for entries in self.hooks()["hooks"].values()
                for entry in entries for h in entry["hooks"] if "keel_hook.py" in h["command"]]

    def assertOk(self, result):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def assertRefused(self, result):
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("refused", result.stdout + result.stderr)


class ClaudeCode(Homes):
    def test_links_master_as_skills_dir_plugin(self):
        self.assertOk(self.run_it())
        link = self.claude / "skills" / "keel"
        self.assertTrue(link.is_symlink())
        self.assertEqual(link.resolve(), MASTER)
        self.assertFalse((self.agents / "skills").exists(), "Codex links need --codex")

    def test_twice_changes_nothing(self):
        self.assertOk(self.run_it())
        second = self.run_it()
        self.assertOk(second)
        self.assertIn("already", second.stdout)

    def test_refuses_a_real_folder_in_the_way(self):
        (self.claude / "skills" / "keel").mkdir(parents=True)
        self.assertRefused(self.run_it())
        self.assertTrue((self.claude / "skills" / "keel").is_dir())

    def test_refuses_a_foreign_link_in_the_way(self):
        (self.claude / "skills").mkdir(parents=True)
        elsewhere = self.tmp / "other"
        elsewhere.mkdir()
        (self.claude / "skills" / "keel").symlink_to(elsewhere)
        self.assertRefused(self.run_it())
        self.assertEqual((self.claude / "skills" / "keel").resolve(), elsewhere)

    def test_remove_unlinks_and_leaves_master(self):
        self.assertOk(self.run_it())
        self.assertOk(self.run_it("--remove"))
        self.assertFalse((self.claude / "skills" / "keel").exists())
        self.assertTrue((MASTER / ".claude-plugin" / "plugin.json").is_file())

    def test_remove_leaves_a_foreign_folder(self):
        (self.claude / "skills" / "keel").mkdir(parents=True)
        self.assertRefused(self.run_it("--remove"))
        self.assertTrue((self.claude / "skills" / "keel").is_dir())

    def test_with_docs_adds_the_four_docs_skills(self):
        self.assertOk(self.run_it("--with-docs"))
        for name in DOCS:
            link = self.claude / "skills" / name
            self.assertTrue(link.is_symlink(), name)
            self.assertTrue((link / "SKILL.md").is_file(), name)


class Codex(Homes):
    def test_links_every_core_skill(self):
        self.assertOk(self.run_it("--codex"))
        skills = self.agents / "skills"
        self.assertEqual(sorted(p.name for p in skills.iterdir()), sorted(CORE))
        for name in CORE:
            self.assertTrue((skills / name).is_symlink(), name)
            self.assertTrue((skills / name / "SKILL.md").is_file(), name)

    def test_vendored_skills_come_from_the_codex_copies(self):
        self.assertOk(self.run_it("--codex"))
        target = (self.agents / "skills" / "commit").resolve()
        self.assertEqual(target, MASTER / "keel" / "skills-board" / "codex" / "commit")

    def test_taken_name_is_skipped_not_overwritten(self):
        (self.agents / "skills" / "spike").mkdir(parents=True)
        (self.agents / "skills" / "spike" / "SKILL.md").write_text("theirs", encoding="utf-8")
        result = self.run_it("--codex")
        self.assertOk(result)
        self.assertIn("skipped spike", result.stdout)
        self.assertNotIn("warning", result.stdout, "only KEEL's own skills warn")
        self.assertEqual((self.agents / "skills" / "spike" / "SKILL.md").read_text(), "theirs")

    def test_a_taken_name_among_keels_own_skills_warns(self):
        theirs = "---\nname: helm\ndescription: Kubernetes Helm charts\n---\n"
        (self.agents / "skills" / "helm").mkdir(parents=True)
        (self.agents / "skills" / "helm" / "SKILL.md").write_text(theirs, encoding="utf-8")
        result = self.run_it("--codex")
        self.assertOk(result)
        warnings = [line for line in result.stdout.splitlines() if line.startswith("warning:")]
        self.assertEqual(len(warnings), 1, result.stdout)
        self.assertIn("KEEL's own skill helm", warnings[0])
        self.assertIn(str(self.agents / "skills" / "helm"), warnings[0])
        self.assertIn("$keel:helm will not work", warnings[0])
        self.assertEqual((self.agents / "skills" / "helm" / "SKILL.md").read_text(), theirs)
        for name in CORE:
            if name != "helm":
                self.assertTrue((self.agents / "skills" / name).is_symlink(), name)

    def test_with_docs_adds_docs_skills_for_codex(self):
        self.assertOk(self.run_it("--codex", "--with-docs"))
        for name in DOCS:
            self.assertTrue((self.agents / "skills" / name).is_symlink(), name)

    def test_remove_takes_only_our_links(self):
        (self.agents / "skills" / "theirs").mkdir(parents=True)
        self.assertOk(self.run_it("--codex"))
        self.assertOk(self.run_it("--codex", "--remove"))
        left = sorted(p.name for p in (self.agents / "skills").iterdir())
        self.assertEqual(left, ["theirs"])


class LinkErrors(Homes):
    """A link the system will not make (Windows without Developer Mode) is a clean refusal."""

    def run_failing(self, fail_under: Path, *args):
        cmd = [sys.executable, "-B", "-c", SYMLINK_FAILS, str(SCRIPT), str(fail_under),
               *self.homes(), *args]
        return subprocess.run(cmd, capture_output=True, text=True, env=self.env())

    def test_claude_link_error_is_refused_without_a_traceback(self):
        result = self.run_failing(self.claude)
        self.assertRefused(result)
        self.assertIn("could not make the link", result.stdout)
        self.assertIn("Developer Mode", result.stdout)
        self.assertIn("A required privilege is not held", result.stdout)
        self.assertNotIn("Traceback", result.stderr)
        self.assertFalse((self.claude / "skills" / "keel").exists())

    def test_codex_link_error_stops_at_the_first_link(self):
        result = self.run_failing(self.agents, "--codex")
        self.assertRefused(result)
        self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(result.stdout.count("could not make the link"), 1, result.stdout)
        self.assertTrue((self.claude / "skills" / "keel").is_symlink(), "the Claude link was allowed")


class CodexHooks(Homes):
    def test_writes_both_hooks_with_absolute_paths(self):
        result = self.run_it("--codex-hooks")
        self.assertOk(result)
        self.assertIn(str(self.codex / "hooks.json"), result.stdout, "print the path written")
        data = self.hooks()["hooks"]
        self.assertIn("SessionStart", data)
        self.assertIn("PreToolUse", data)
        self.assertIn("apply_patch", data["PreToolUse"][0]["matcher"])
        for command in self.keel_commands():
            self.assertIn(str(MASTER / "harness" / "hooks" / "keel_hook.py"), command)
            self.assertIn("[ -f", command, "must disarm itself if the master moves")
        self.assertTrue(data["SessionStart"][0]["hooks"][0]["command"].endswith(
            '"$g" session --harness codex'))
        self.assertTrue(data["PreToolUse"][0]["hooks"][0]["command"].endswith(
            '"$g" guard --harness codex'))

    def test_keeps_existing_hooks_and_backs_up_once(self):
        self.codex.mkdir(parents=True)
        mine = {"hooks": {"Stop": [{"hooks": [{"type": "command", "command": "echo mine"}]}]}}
        (self.codex / "hooks.json").write_text(json.dumps(mine), encoding="utf-8")
        self.assertOk(self.run_it("--codex-hooks"))
        self.assertIn("Stop", self.hooks()["hooks"])
        self.assertTrue((self.codex / "hooks.json.before-keel").is_file())
        self.assertOk(self.run_it("--codex-hooks"))
        self.assertEqual(len(self.keel_commands()), 2, "twice must not duplicate")
        backup = json.loads((self.codex / "hooks.json.before-keel").read_text(encoding="utf-8"))
        self.assertEqual(backup, mine, "the backup is the user's file, as it was before KEEL")

    def test_a_second_run_saves_no_backup_of_keels_own_hooks(self):
        self.assertOk(self.run_it("--codex-hooks"))
        second = self.run_it("--codex-hooks")
        self.assertOk(second)
        self.assertNotIn("saved the original", second.stdout)
        self.assertFalse((self.codex / "hooks.json.before-keel").exists())
        self.assertEqual(len(self.keel_commands()), 2)

    def test_remove_takes_out_only_keel_entries(self):
        self.codex.mkdir(parents=True)
        mine = {"hooks": {"Stop": [{"hooks": [{"type": "command", "command": "echo mine"}]}]}}
        (self.codex / "hooks.json").write_text(json.dumps(mine), encoding="utf-8")
        self.assertOk(self.run_it("--codex-hooks"))
        result = self.run_it("--codex-hooks", "--remove")
        self.assertOk(result)
        self.assertIn(str(self.codex / "hooks.json"), result.stdout)
        self.assertEqual(self.hooks(), mine)

    def write_old_form(self):
        self.codex.mkdir(parents=True)
        mine = {"hooks": {"Stop": [{"hooks": [{"type": "command", "command": "echo mine"}]}]}}
        old = json.loads(json.dumps(mine))
        old["hooks"]["SessionStart"] = [{"hooks": [{"type": "command", "command": OLD_SESSION}]}]
        old["hooks"]["PreToolUse"] = [{"matcher": "Bash|apply_patch",
                                       "hooks": [{"type": "command", "command": OLD_GUARD}]}]
        (self.codex / "hooks.json").write_text(json.dumps(old), encoding="utf-8")
        return mine

    def test_remove_recognizes_the_old_unquoted_form(self):
        mine = self.write_old_form()
        self.assertOk(self.run_it("--codex-hooks", "--remove"))
        self.assertEqual(self.hooks(), mine)

    def test_install_replaces_the_old_form(self):
        self.write_old_form()
        self.assertOk(self.run_it("--codex-hooks"))
        commands = self.keel_commands()
        self.assertEqual(len(commands), 2, commands)
        for command in commands:
            self.assertIn("--harness codex", command)
            self.assertNotIn("/old/master", command)

    def test_refuses_unreadable_hooks_file(self):
        self.codex.mkdir(parents=True)
        (self.codex / "hooks.json").write_text("{not json", encoding="utf-8")
        self.assertRefused(self.run_it("--codex-hooks"))
        self.assertEqual((self.codex / "hooks.json").read_text(), "{not json")


@unittest.skipIf(os.name == "nt" or os.geteuid() == 0,
                 "chmod does not deny writes to root or on Windows, so the errors cannot be staged")
class HooksWriteErrors(Homes):
    """A hooks.json, its backup or a Codex home that cannot be written is a clean refusal."""

    def read_only(self, path: Path, mode: int = 0o555):
        restore = 0o755 if path.is_dir() else 0o644
        os.chmod(path, mode)
        self.addCleanup(os.chmod, path, restore)  # runs before setUp's rmtree

    def assertWriteRefused(self, result, path: Path):
        self.assertRefused(result)
        self.assertNotIn("Traceback", result.stderr)
        lines = [line for line in result.stdout.splitlines() if line.startswith("refused: could not write")]
        self.assertEqual(lines, [f"refused: could not write {path} (Permission denied)"], result.stdout)
        self.assertNotIn("wrote KEEL's", result.stdout)

    def test_unwritable_codex_home_is_refused_without_a_traceback(self):
        self.codex.mkdir()
        self.read_only(self.codex)
        self.assertWriteRefused(self.run_it("--codex-hooks"), self.codex / "hooks.json")
        self.assertFalse((self.codex / "hooks.json").exists())

    def test_unwritable_backup_is_refused_and_hooks_json_kept(self):
        self.codex.mkdir()
        mine = json.dumps({"hooks": {"Stop": [{"hooks": [{"type": "command", "command": "echo mine"}]}]}})
        (self.codex / "hooks.json").write_text(mine, encoding="utf-8")
        self.read_only(self.codex)
        self.assertWriteRefused(self.run_it("--codex-hooks"), self.codex / "hooks.json.before-keel")
        self.assertEqual((self.codex / "hooks.json").read_text(encoding="utf-8"), mine)
        self.assertFalse((self.codex / "hooks.json.before-keel").exists())

    def test_unwritable_hooks_json_on_remove_is_refused_and_kept(self):
        self.codex.mkdir()
        mine = {"hooks": {"Stop": [{"hooks": [{"type": "command", "command": "echo mine"}]}]}}
        (self.codex / "hooks.json").write_text(json.dumps(mine), encoding="utf-8")
        self.assertOk(self.run_it("--codex-hooks"))
        installed = (self.codex / "hooks.json").read_text(encoding="utf-8")
        self.read_only(self.codex / "hooks.json", 0o444)
        self.assertWriteRefused(self.run_it("--codex-hooks", "--remove"), self.codex / "hooks.json")
        self.assertEqual((self.codex / "hooks.json").read_text(encoding="utf-8"), installed)

    def test_codex_home_that_cannot_be_made_is_refused(self):
        locked = self.tmp / "locked"
        locked.mkdir()
        self.read_only(locked)
        self.codex = locked / "codex"
        self.assertWriteRefused(self.run_it("--codex-hooks"), self.codex)
        self.assertFalse(self.codex.exists())


class CodexHome(Homes):
    """Where hooks.json goes: --codex-home, else $CODEX_HOME, else $HOME/.codex."""

    def test_codex_home_env_is_honored(self):
        chosen = self.tmp / "codex-home-env"
        result = self.run_it("--codex-hooks", codex_home=False, env=self.env(CODEX_HOME=str(chosen)))
        self.assertOk(result)
        self.assertTrue((chosen / "hooks.json").is_file())
        self.assertFalse((self.home / ".codex").exists())
        self.assertIn(str(chosen / "hooks.json"), result.stdout)

    def test_the_flag_wins_over_the_env(self):
        chosen = self.tmp / "codex-home-env"
        result = self.run_it("--codex-hooks", env=self.env(CODEX_HOME=str(chosen)))
        self.assertOk(result)
        self.assertTrue((self.codex / "hooks.json").is_file())
        self.assertFalse(chosen.exists())

    def test_falls_back_to_home_dot_codex(self):
        for value in (None, ""):
            with self.subTest(CODEX_HOME=value):
                env = self.env() if value is None else self.env(CODEX_HOME=value)
                result = self.run_it("--codex-hooks", codex_home=False, env=env)
                self.assertOk(result)
                self.assertTrue((self.home / ".codex" / "hooks.json").is_file())
                self.assertIn(str(self.home / ".codex" / "hooks.json"), result.stdout)
                shutil.rmtree(self.home / ".codex")


class ShellUnsafeMaster(Homes):
    """A master whose path holds a space, a $ and a quote still reaches its hook."""

    def test_commands_reach_the_hook_through_sh(self):
        master = self.tmp / "KEEL $HOME o'clock"
        (master / "harness" / "hooks").mkdir(parents=True)
        script = master / "harness" / "install_plugin.py"
        shutil.copy2(SCRIPT, script)
        (master / "harness" / "hooks" / "keel_hook.py").write_text(STUB_HOOK, encoding="utf-8")
        self.assertOk(self.run_it("--codex-hooks", script=script))
        data = self.hooks()["hooks"]
        expected = {"SessionStart": 7, "PreToolUse": 8}
        for event, code in expected.items():
            command = data[event][0]["hooks"][0]["command"]
            with self.subTest(event=event, command=command):
                ran = subprocess.run(["sh", "-c", command], input="{}", capture_output=True,
                                     text=True, env=self.env())
                self.assertEqual(ran.returncode, code, ran.stdout + ran.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=1)
