#!/usr/bin/env python3
"""Self-test for keel_hook.py -- the plugin's two hooks, watched failing as well as passing.

    python3 harness/hooks/test_keel_hook.py

Drives the hook the way Claude Code and Codex do: JSON on stdin, then the exit code,
stdout and stderr read back. Every project is a temporary folder, and every run sets
HOME, CLAUDE_PLUGIN_ROOT and CLAUDE_PROJECT_DIR itself, so nothing on this machine leaks
in; no file in a project is ever opened by the guard. The git cases need git and are
skipped without it; the real v1.0 file needs this kit's own git history. A skipped test
is not a passed one.

The letter-case cases (a sibling named `KEEL-FACTORY`, a folder named `.KEEL`) prove the
exact-name test on a case-insensitive filesystem such as macOS's APFS. On a case-sensitive
filesystem they pass trivially, because there `keel-factory` cannot match them at all.

The hostile role files (nested too deep, a named pipe, a link to /dev/zero) run each hook
under a short timeout, so a hang fails the test instead of stalling the suite; the pipe
cases are skipped without os.mkfifo, the device case without /dev/zero. A few cases call
guard() and patch_paths() in this process instead, for errors no file on disk can cause:
they patch one function with unittest.mock, give the call a cleared environment of its
own and capture its stderr. Standard library only.
"""

from __future__ import annotations

import contextlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.dont_write_bytecode = True
HOOKS = Path(__file__).resolve().parent
sys.path.insert(0, str(HOOKS))
import keel_hook  # noqa: E402  -- the in-process cases
from keel_hook import LAYER_MARK, ROLE_CAP  # noqa: E402  -- one source for the mark and the cap

HOOK = HOOKS / "keel_hook.py"
GUARD = HOOKS / "data-boundary-guard.py"
KIT = HOOKS.parent.parent
HAS_GIT = shutil.which("git") is not None
V1_PHRASE = "This project was started from KEEL FACTORY."
CLEAN_ENV = {k: v for k, v in os.environ.items()
             if k not in ("CLAUDE_PROJECT_DIR", "CLAUDE_PLUGIN_ROOT", "HOME", "KEEL_GUARD",
                          "KEEL_DATA_BOUNDARY_OVERRIDE")}


def run(args, payload=None, raw=None, env=None, hook=None, cwd=None, timeout=60):
    """Run the hook. An env value of None removes that variable."""
    data = raw if raw is not None else ("" if payload is None else json.dumps(payload))
    full_env = dict(CLEAN_ENV)
    for key, value in (env or {}).items():
        if value is None:
            full_env.pop(key, None)
        else:
            full_env[key] = value
    result = subprocess.run([sys.executable, "-B", str(hook or HOOK), *args], input=data.encode("utf-8"),
                            capture_output=True, env=full_env, cwd=cwd, timeout=timeout)
    result.stdout = result.stdout.decode("utf-8", errors="replace")
    result.stderr = result.stderr.decode("utf-8", errors="replace")
    return result


def patch(*headers: str, body: str = "@@\n-a\n+b\n") -> str:
    lines = ["*** Begin Patch"]
    for header in headers:
        lines.append(header)
        lines.append(body.rstrip("\n"))
    lines.append("*** End Patch")
    return "\n".join(lines) + "\n"


def after_add(line: str) -> str:
    """A patch that adds notes.txt, then `line`, where Codex's Add File hunk has ended."""
    return f"*** Begin Patch\n*** Add File: notes.txt\n+hi\n{line}\n*** End Patch\n"


class Project(unittest.TestCase):
    HOOK_TIMEOUT = 60  # seconds for one hook run

    def setUp(self):
        self.tmp = Path(os.path.realpath(tempfile.mkdtemp(prefix="keel-hook-test-")))
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.home = self.tmp / "home"
        self.home.mkdir()
        self.proj = self.tmp / "proj"
        self.proj.mkdir()

    def hook(self, args, payload=None, raw=None, env=None, hook=None):
        full = {"HOME": str(self.home), "CLAUDE_PLUGIN_ROOT": str(KIT)}
        full.update(env or {})
        return run(args, payload, raw=raw, env=full, hook=hook, cwd=self.tmp,
                   timeout=self.HOOK_TIMEOUT)

    def git(self, *args, cwd: Path):
        env = dict(CLEAN_ENV, HOME=str(self.home), GIT_CONFIG_NOSYSTEM="1")
        subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", "-c", "init.defaultBranch=main",
                        *args], cwd=cwd, env=env, check=True, capture_output=True, timeout=60)

    def repo_with_worktree(self, main: Path, wt: Path):
        main.mkdir(parents=True, exist_ok=True)
        self.git("init", "-q", cwd=main)
        self.git("commit", "-q", "--allow-empty", "-m", "init", cwd=main)
        self.git("worktree", "add", "-q", str(wt), cwd=main)

    def switch_on(self, role: str | None = "owner", where: Path | None = None):
        keel = (where or self.proj) / ".keel"
        keel.mkdir(parents=True, exist_ok=True)
        if role is not None:
            (keel / "keel.json").write_text(json.dumps({"role": role}), encoding="utf-8")

    def link_kit(self, where: Path | None = None):
        """A `keel-factory` link to this kit, whose CLAUDE.md carries the mark."""
        (where or self.proj).joinpath("keel-factory").symlink_to(KIT, target_is_directory=True)

    def kit_copy(self, kit: Path) -> Path:
        """Lay `kit` out as a copy of this kit's hooks and layer; returns the copied hook."""
        hooks = kit / "harness" / "hooks"
        hooks.mkdir(parents=True, exist_ok=True)
        shutil.copy(HOOK, hooks / "keel_hook.py")
        shutil.copy(GUARD, hooks / "data-boundary-guard.py")
        shutil.copy(KIT / "CLAUDE.md", kit / "CLAUDE.md")
        return hooks / "keel_hook.py"

    def guard(self, tool_input, tool_name="Read", cwd=None, env=None, project=None, args=(), hook=None):
        payload = {"hook_event_name": "PreToolUse", "tool_name": tool_name, "tool_input": tool_input,
                   "cwd": str(cwd or self.proj)}
        return self.hook(["guard", *args], payload,
                         env=dict({"CLAUDE_PROJECT_DIR": str(project or self.proj)}, **(env or {})), hook=hook)

    def session(self, env=None, cwd=None, harness=None, hook=None):
        payload = {"hook_event_name": "SessionStart", "source": "startup", "cwd": str(cwd or self.proj)}
        args = ["session"] + (["--harness", harness] if harness else [])
        return self.hook(args, payload, env=env, hook=hook)

    def context(self, result) -> str:
        self.assertEqual(result.returncode, 0, result.stderr)
        out = json.loads(result.stdout)
        self.assertEqual(out["hookSpecificOutput"]["hookEventName"], "SessionStart")
        return out["hookSpecificOutput"]["additionalContext"]

    def assertBlocked(self, result):
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertTrue(result.stderr.strip(), "a block must say why: Codex ignores exit 2 with empty stderr")
        self.assertIn("BLOCKED", result.stderr)

    def assertAllowed(self, result):
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr, "")

    def assertSilent(self, result):
        self.assertEqual((result.returncode, result.stdout, result.stderr), (0, "", ""))

    def assertDormant(self, start: Path, env=None, hook=None):
        """Neither hook acts with `start` as the project: no context, and a Read of .env allowed."""
        env = dict({"CLAUDE_PROJECT_DIR": str(start)}, **(env or {}))
        self.assertSilent(self.session(env=env, cwd=start, hook=hook))
        self.assertAllowed(self.guard({"file_path": str(start / ".env")}, cwd=start, project=start, env=env,
                                      hook=hook))


class Dormant(Project):
    """Where KEEL is off, both hooks are silent and allow everything."""

    def test_guard_allows_env_read_without_marker(self):
        self.assertAllowed(self.guard({"file_path": str(self.proj / ".env")}))

    def test_session_says_nothing_without_marker(self):
        result = self.session()
        self.assertEqual((result.returncode, result.stdout, result.stderr), (0, "", ""))

    def test_marker_above_the_repo_does_not_count(self):
        self.switch_on(where=self.tmp)
        (self.proj / ".git").mkdir()
        self.assertAllowed(self.guard({"file_path": str(self.proj / ".env")}))

    def test_unreadable_input_allowed_where_keel_is_off(self):
        result = self.hook(["guard"], raw="{not json", env={"CLAUDE_PROJECT_DIR": str(self.proj)})
        self.assertAllowed(result)

    def test_unknown_subcommand_is_an_error_not_a_block(self):
        result = self.hook(["nonsense"], payload={})
        self.assertEqual(result.returncode, 1)


class SwitchOn(Project):
    """The switch-on rule: exact names, the git root, $HOME, the kit root, worktrees."""

    def test_sibling_named_KEEL_FACTORY_outside_git_is_dormant(self):
        parent = self.tmp / "Parent"
        (parent / "KEEL-FACTORY").mkdir(parents=True)
        self.assertDormant(parent)

    def test_sibling_named_KEEL_FACTORY_inside_git_is_dormant(self):
        parent = self.tmp / "Parent"
        (parent / "KEEL-FACTORY").mkdir(parents=True)
        (parent / ".git").mkdir()
        child = parent / "child"
        child.mkdir()
        self.assertDormant(child)

    def test_non_git_child_beside_KEEL_FACTORY_is_dormant(self):
        parent = self.tmp / "Parent"
        (parent / "KEEL-FACTORY").mkdir(parents=True)
        child = parent / "child"
        child.mkdir()
        self.assertDormant(child)

    def test_folder_named_upper_KEEL_is_dormant(self):
        (self.proj / ".KEEL").mkdir()
        self.assertDormant(self.proj)

    def test_non_git_child_below_a_marker_is_dormant(self):
        for name in (".keel", "keel-factory"):
            with self.subTest(marker=name):
                above = self.tmp / f"above{name}"
                (above / name).mkdir(parents=True)
                child = above / "b" / "c"
                child.mkdir(parents=True)
                self.assertDormant(child)

    def test_home_marker_does_not_count(self):
        self.switch_on(where=self.home)
        with self.subTest(start="home itself"):
            self.assertDormant(self.home)
        with self.subTest(start="a non-git folder under home"):
            pkg = self.home / "Downloads" / "pkg"
            pkg.mkdir(parents=True)
            self.assertDormant(pkg)
        with self.subTest(start="home as the git root"):
            (self.home / ".git").mkdir()
            sub = self.home / "sub"
            sub.mkdir()
            self.assertDormant(sub)

    def test_start_inside_kit_root_is_dormant(self):
        kit = self.tmp / "kit"
        app = kit / "app"
        (app / ".git").mkdir(parents=True)
        self.switch_on(where=app)
        self.switch_on(where=kit)
        env = {"CLAUDE_PLUGIN_ROOT": str(kit)}
        with self.subTest(start="kit/app"):
            self.assertDormant(app, env=env)
        with self.subTest(start="the kit root"):
            self.assertDormant(kit, env=env)

    def test_kit_inside_a_keel_repo_is_dormant(self):
        outer = self.tmp / "outer"
        (outer / ".git").mkdir(parents=True)
        self.switch_on(where=outer)
        app = outer / "kit" / "app"
        app.mkdir(parents=True)
        self.assertDormant(app, env={"CLAUDE_PLUGIN_ROOT": str(outer / "kit")})

    def test_kit_root_through_a_link_is_dormant(self):
        kit = self.tmp / "kit"
        app = kit / "app"
        app.mkdir(parents=True)
        self.switch_on(where=app)
        link = self.tmp / "plugin-link"
        link.symlink_to(kit, target_is_directory=True)
        self.assertDormant(app, env={"CLAUDE_PLUGIN_ROOT": str(link)})

    def test_kit_own_folder_named_keel_factory_is_dormant(self):
        """The master's own git checkout, named keel-factory, seen from the folder holding it."""
        parent = self.tmp / "Parent"
        kit = parent / "keel-factory"
        (kit / ".git").mkdir(parents=True)
        copied = self.kit_copy(kit)
        for where in ("outside git", "inside git"):
            if where == "inside git":
                (parent / ".git").mkdir()
            with self.subTest(parent=where, kit_root="CLAUDE_PLUGIN_ROOT"):
                self.assertDormant(parent, env={"CLAUDE_PLUGIN_ROOT": str(kit)})
            with self.subTest(parent=where, kit_root="the kit's own hook"):
                self.assertDormant(parent, env={"CLAUDE_PLUGIN_ROOT": None}, hook=copied)

    @unittest.skipUnless(HAS_GIT, "git not installed")
    def test_master_worktree_named_keel_factory_is_dormant(self):
        """A linked worktree of the master is the master too, not a copy."""
        parent = self.tmp / "Parent"
        parent.mkdir()
        kit = parent / "keel-factory"
        self.repo_with_worktree(self.tmp / "master", kit)
        self.assertTrue((kit / ".git").is_file())
        copied = self.kit_copy(kit)
        with self.subTest(kit_root="CLAUDE_PLUGIN_ROOT"):
            self.assertDormant(parent, env={"CLAUDE_PLUGIN_ROOT": str(kit)})
        with self.subTest(kit_root="the kit's own hook"):
            self.assertDormant(parent, env={"CLAUDE_PLUGIN_ROOT": None}, hook=copied)

    def test_copied_kit_with_hooks_from_the_copy_switches_on(self):
        """The documented copy (an rsync that leaves .git out) at keel-factory/, wired from itself."""
        (self.proj / ".git").mkdir()
        kit = self.proj / "keel-factory"
        copied = self.kit_copy(kit)
        no_plugin = {"CLAUDE_PLUGIN_ROOT": None}
        for path in (str(self.proj / ".env"), "keel-armed-check/.env"):
            with self.subTest(path=path, form="claude"):
                self.assertBlocked(self.guard({"file_path": path}, env=no_plugin, hook=copied))
            with self.subTest(path=path, form="codex"):
                payload = {"tool_name": "Read", "tool_input": {"file_path": path}, "cwd": str(self.proj)}
                self.assertBlocked(self.hook(["guard", "--harness", "codex"], payload, env=no_plugin,
                                             hook=copied))
        for harness, env in (("claude", dict(no_plugin, CLAUDE_PROJECT_DIR=str(self.proj))),
                             ("codex", no_plugin)):
            with self.subTest(session=harness):
                text = self.context(self.session(env=env, harness=harness, hook=copied))
                self.assertIn("role: kit", text)
                self.assertIn(f"KEEL kit root for this session: {kit}.", text)
                self.assertIn("(a link or a copy)", text)
                self.assertIn(LAYER_MARK, text)

    def test_submodule_vendored_kit_switches_on(self):
        """A submodule's .git file has no commondir behind it, so the kit is the project's copy."""
        (self.proj / ".git" / "modules" / "keel-factory").mkdir(parents=True)
        kit = self.proj / "keel-factory"
        copied = self.kit_copy(kit)
        (kit / ".git").write_text("gitdir: ../.git/modules/keel-factory\n", encoding="utf-8")
        for name, env, hook in (("CLAUDE_PLUGIN_ROOT", {"CLAUDE_PLUGIN_ROOT": str(kit)}, None),
                                ("the kit's own hook", {"CLAUDE_PLUGIN_ROOT": None}, copied)):
            with self.subTest(kit_root=name):
                text = self.context(self.session(env=dict(env, CLAUDE_PROJECT_DIR=str(self.proj)), hook=hook))
                self.assertIn("role: kit", text)
                self.assertBlocked(self.guard({"file_path": str(self.proj / ".env")}, env=env, hook=hook))

    def test_link_to_the_kit_switches_on(self):
        kit = self.tmp / "kit"
        (kit / ".git").mkdir(parents=True)  # the master's own checkout: only a link reaches it
        (self.proj / "keel-factory").symlink_to(kit, target_is_directory=True)
        env = {"CLAUDE_PLUGIN_ROOT": str(kit)}
        self.assertIn("role: kit", self.context(self.session(env=env)))
        self.assertBlocked(self.guard({"file_path": str(self.proj / ".env")}, env=env))

    @unittest.skipUnless(HAS_GIT, "git not installed")
    def test_worktree_finds_the_main_checkout_marker(self):
        main, wt = self.tmp / "main", self.tmp / "wt"
        self.repo_with_worktree(main, wt)
        self.switch_on("owner", where=main)
        self.assertTrue((wt / ".git").is_file())
        self.assertFalse((wt / ".keel").exists())
        self.assertBlocked(self.guard({"file_path": str(wt / ".env")}, cwd=wt, project=wt))
        text = self.context(self.session(env={"CLAUDE_PROJECT_DIR": str(wt)}, cwd=wt))
        self.assertIn("role: owner", text)
        self.assertIn(f"({main})", text)
        sub = wt / "src"
        sub.mkdir()
        payload = {"tool_name": "Read", "tool_input": {"file_path": str(sub / ".env")}, "cwd": str(sub)}
        self.assertBlocked(self.hook(["guard"], payload))  # no CLAUDE_PROJECT_DIR: Codex's case

    @unittest.skipUnless(HAS_GIT, "git not installed")
    def test_worktree_carry_check_reads_its_own_root(self):
        main, wt = self.tmp / "main", self.tmp / "wt"
        self.repo_with_worktree(main, wt)
        self.switch_on("owner", where=main)
        (wt / "CLAUDE.md").write_text(f"{LAYER_MARK}\n# Ours\n", encoding="utf-8")
        text = self.context(self.session(env={"CLAUDE_PROJECT_DIR": str(wt)}, cwd=wt))
        self.assertIn("role: owner", text)
        self.assertNotIn(LAYER_MARK, text)

    @unittest.skipUnless(HAS_GIT, "git not installed")
    def test_worktree_import_with_the_link_only_in_main_injects_the_layer(self):
        """The import resolves from the worktree, which has no keel-factory/: nothing to import."""
        main, wt = self.tmp / "main", self.tmp / "wt"
        self.repo_with_worktree(main, wt)
        self.link_kit(where=main)
        for root in (main, wt):
            (root / "CLAUDE.md").write_text("# Ours\n\n@keel-factory/CLAUDE.md\n", encoding="utf-8")
        text = self.context(self.session(env={"CLAUDE_PROJECT_DIR": str(wt)}, cwd=wt))
        self.assertIn("role: kit", text)
        self.assertIn(LAYER_MARK, text)
        with self.subTest(control="the main checkout, where the import resolves"):
            self.assertNotIn(LAYER_MARK, self.context(self.session(env={"CLAUDE_PROJECT_DIR": str(main)},
                                                                   cwd=main)))

    @unittest.skipUnless(HAS_GIT, "git not installed")
    def test_worktree_of_the_kit_is_dormant(self):
        kit, wt = self.tmp / "kit", self.tmp / "kit-wt"
        self.repo_with_worktree(kit, wt)
        self.switch_on(where=kit)
        self.assertDormant(wt, env={"CLAUDE_PLUGIN_ROOT": str(kit)})

    @unittest.skipUnless(HAS_GIT, "git not installed")
    def test_worktree_of_home_is_dormant(self):
        wt = self.tmp / "home-wt"
        self.repo_with_worktree(self.home, wt)
        self.switch_on(where=self.home)
        self.assertDormant(wt)

    def test_submodule_does_not_reach_the_superproject(self):
        sup = self.tmp / "super"
        (sup / ".git" / "modules" / "sub").mkdir(parents=True)
        self.switch_on(where=sup)
        sub = sup / "sub"
        sub.mkdir()
        (sub / ".git").write_text("gitdir: ../.git/modules/sub\n", encoding="utf-8")
        self.assertDormant(sub)

    def test_plugin_root_unset_names_this_kit(self):
        self.switch_on()
        text = self.context(self.session(env={"CLAUDE_PLUGIN_ROOT": None}))
        self.assertIn(f"KEEL kit root for this session: {KIT}.", text)
        self.assertIn(LAYER_MARK, text)

    def test_bad_harness_is_a_usage_error(self):
        self.switch_on()
        for args in (["session", "--harness", "nope"], ["guard", "--harness", "nope"],
                     ["session", "--harness"], ["guard", "codex"]):
            with self.subTest(args=args):
                result = self.hook(args, payload={"cwd": str(self.proj)},
                                   env={"CLAUDE_PROJECT_DIR": str(self.proj)})
                self.assertEqual(result.returncode, 1)
                self.assertIn("usage:", result.stderr)

    def test_guard_takes_harness_codex(self):
        self.switch_on()
        self.assertBlocked(self.guard({"file_path": str(self.proj / ".env")}, args=("--harness", "codex")))
        self.assertAllowed(self.guard({"file_path": str(self.proj / "README.md")}, args=("--harness", "codex")))


class Armed(Project):
    """Where KEEL is on, the unchanged guard decides."""

    def test_keel_folder_arms_the_guard(self):
        self.switch_on()
        self.assertBlocked(self.guard({"file_path": str(self.proj / ".env")}))

    def test_linked_kit_arms_the_guard(self):
        (self.proj / "keel-factory").mkdir()
        self.assertBlocked(self.guard({"file_path": str(self.proj / ".env")}))

    def test_normal_file_allowed_silently(self):
        self.switch_on()
        self.assertAllowed(self.guard({"file_path": str(self.proj / "README.md")}))

    def test_subfolder_session_finds_the_marker(self):
        (self.proj / ".git").mkdir()
        self.switch_on()
        sub = self.proj / "src" / "deep"
        sub.mkdir(parents=True)
        payload = {"tool_name": "Read", "tool_input": {"file_path": str(sub / ".env")}, "cwd": str(sub)}
        self.assertBlocked(self.hook(["guard"], payload))  # no CLAUDE_PROJECT_DIR: Codex's case

    def test_keel_guard_always_arms_everywhere(self):
        self.assertBlocked(self.guard({"file_path": str(self.proj / ".env")}, env={"KEEL_GUARD": "always"}))

    def test_keel_guard_always_fails_closed_in_a_dormant_folder(self):
        """No marker here, but KEEL_GUARD=always: an error blocks, as it does where KEEL is on."""
        always = {"CLAUDE_PROJECT_DIR": str(self.proj), "KEEL_GUARD": "always"}
        with self.subTest(error="unreadable input"):
            self.assertBlocked(self.hook(["guard"], raw="{not json", env=always))
        with self.subTest(error="a missing guard"):
            lonely = self.tmp / "lonely" / "harness" / "hooks"
            lonely.mkdir(parents=True)
            shutil.copy(HOOK, lonely / "keel_hook.py")
            payload = {"tool_name": "Read", "tool_input": {"file_path": str(self.proj / "README.md")},
                       "cwd": str(self.proj)}
            self.assertBlocked(self.hook(["guard"], payload, env=always, hook=lonely / "keel_hook.py"))

    def test_bash_command_reading_env_blocked(self):
        self.switch_on()
        self.assertBlocked(self.guard({"command": "cat .env"}, tool_name="Bash"))

    def test_list_shaped_command_is_joined(self):
        self.switch_on()
        self.assertBlocked(self.guard({"command": ["cat", ".env"]}, tool_name="shell"))

    def test_unreadable_input_blocked_where_keel_is_on(self):
        self.switch_on()
        self.assertBlocked(self.hook(["guard"], raw="{not json", env={"CLAUDE_PROJECT_DIR": str(self.proj)}))

    def test_missing_guard_fails_closed_in_keel_project(self):
        lonely = self.tmp / "lonely" / "harness" / "hooks"
        lonely.mkdir(parents=True)
        shutil.copy(HOOK, lonely / "keel_hook.py")
        self.switch_on()
        payload = {"tool_name": "Read", "tool_input": {"file_path": str(self.proj / "README.md")}, "cwd": str(self.proj)}
        self.assertBlocked(self.hook(["guard"], payload, hook=lonely / "keel_hook.py"))

    def test_missing_guard_allows_where_keel_is_off(self):
        lonely = self.tmp / "lonely" / "harness" / "hooks"
        lonely.mkdir(parents=True)
        shutil.copy(HOOK, lonely / "keel_hook.py")
        payload = {"tool_name": "Read", "tool_input": {"file_path": str(self.proj / ".env")}, "cwd": str(self.proj)}
        self.assertAllowed(self.hook(["guard"], payload, hook=lonely / "keel_hook.py"))

    def test_override_still_honored(self):
        self.switch_on()
        self.assertAllowed(self.guard({"file_path": str(self.proj / ".env")},
                                      env={"KEEL_DATA_BOUNDARY_OVERRIDE": "1"}))


class CodexPatches(Project):
    """Codex sends apply_patch as patch text in tool_input.command, with no file_path."""

    def setUp(self):
        super().setUp()
        self.switch_on()

    def test_patch_to_env_blocked(self):
        self.assertBlocked(self.guard({"command": patch("*** Update File: .env")}, tool_name="apply_patch"))

    def test_patch_moving_to_secret_blocked(self):
        text = patch("*** Update File: notes.txt").replace("*** End Patch", "*** Move to: secrets.yaml\n*** End Patch")
        self.assertBlocked(self.guard({"command": text}, tool_name="apply_patch"))

    def test_patch_adding_key_blocked(self):
        self.assertBlocked(self.guard({"command": patch("*** Add File: deploy/prod.pem", body="+x\n")},
                                      tool_name="apply_patch"))

    def test_patch_whose_text_mentions_env_allowed(self):
        text = patch("*** Update File: README.md", body="@@\n-old\n+copy .env.local from .env and keep ~/.ssh/id_rsa safe\n")
        self.assertAllowed(self.guard({"command": text}, tool_name="apply_patch"))

    def test_the_raw_guard_would_have_blocked_that_patch(self):
        """Why the adapter exists: the guard alone reads patch text as a shell command."""
        text = patch("*** Update File: README.md", body="@@\n-old\n+copy .env.local from .env\n")
        payload = {"tool_name": "apply_patch", "tool_input": {"command": text}, "cwd": str(self.proj)}
        raw = subprocess.run([sys.executable, "-B", str(GUARD)], input=json.dumps(payload).encode(),
                             capture_output=True, env=dict(CLEAN_ENV, HOME=str(self.home)), timeout=60)
        self.assertEqual(raw.returncode, 2)

    def test_patch_recognized_by_tool_name_without_begin_line(self):
        text = "*** Update File: README.md\n@@\n-old\n+see .env for the variables\n"
        self.assertAllowed(self.guard({"command": text}, tool_name="apply_patch"))
        self.assertBlocked(self.guard({"command": "*** Update File: .env\n@@\n+x\n"}, tool_name="apply_patch"))

    def test_patch_recognized_by_text_when_tool_name_differs(self):
        self.assertBlocked(self.guard({"command": patch("*** Delete File: id_rsa")}, tool_name="Edit"))

    @unittest.skipUnless(HAS_GIT, "git not installed")
    def test_patch_into_gitignored_path_blocked(self):
        # The folder must exist: the guard asks git from the file's folder, so a path in a
        # gitignored folder that does not exist yet is not judged ignored. Nothing can be
        # read from a file that is not there; the guard is unchanged on purpose.
        self.git("init", "-q", cwd=self.proj)
        (self.proj / ".gitignore").write_text("build/\n", encoding="utf-8")
        (self.proj / "build").mkdir()
        self.assertBlocked(self.guard({"command": patch("*** Add File: build/out.js", body="+x\n")},
                                      tool_name="apply_patch"))

    def apply_patch(self, text: str):
        return self.guard({"command": text}, tool_name="apply_patch")

    def test_padded_header_after_a_hunk_blocked(self):
        """Codex strips each line before it reads a header, so padding hides no file."""
        for pad in (" ", "  ", "\t", "\v", "\f", "\r", "\xa0", "　"):
            text = after_add(f"{pad}*** Update File: .env\n@@\n-A=1\n+A=2")
            with self.subTest(pad=repr(pad)):
                self.assertBlocked(self.apply_patch(text))

    def test_other_padded_headers_blocked(self):
        cases = {"an indented Delete after an Add hunk": after_add(" *** Delete File: .env"),
                 "an indented first header, then a plain one":
                     "*** Begin Patch\n  *** Update File: .env\n@@\n-A=1\n+A=2\n"
                     "*** Add File: notes.txt\n+hi\n*** End Patch\n",
                 "two spaces before the path": patch("*** Update File:  .env")}
        for name, text in cases.items():
            with self.subTest(case=name):
                self.assertBlocked(self.apply_patch(text))

    def test_unreadable_patch_line_blocked(self):
        """A stripped line starting `***` that is no header and no frame: the hook can't read it."""
        for line in ("*** update file: .env", "*** Add File:.env", " *** Bogus marker", "***Update File: .env"):
            with self.subTest(line=line):
                result = self.apply_patch(after_add(line))
                self.assertBlocked(result)
                self.assertIn("could not evaluate", result.stderr)

    def test_frame_and_context_lines_allowed(self):
        """Codex reads a space-led line in an Update File hunk as file context, never a header."""
        cases = {"a Markdown rule as context":
                     patch("*** Update File: README.md", body="@@\n # Title\n ***\n-old\n+new\n"),
                 "context after a Move to": patch("*** Update File: a.md").replace(
                     "@@", "*** Move to: b.md\n@@\n ***", 1),
                 "End of File": patch("*** Update File: README.md", body="@@\n-old\n+new\n*** End of File\n"),
                 "Environment ID": patch("*** Update File: README.md").replace(
                     "*** Begin Patch", "*** Begin Patch\n*** Environment ID: env-123", 1)}
        for name, text in cases.items():
            with self.subTest(case=name):
                self.assertAllowed(self.apply_patch(text))

    def test_every_header_kind_on_ordinary_files_allowed(self):
        text = ("*** Begin Patch\n*** Add File: docs/setup.md\n+copy .env.example to .env\n"
                "*** Delete File: old.txt\n"
                "*** Update File: notes.txt\n*** Move to: notes2.txt\n@@\n-see .env\n+see .env.example\n"
                "*** End Patch\n")
        self.assertAllowed(self.apply_patch(text))

    def test_patch_without_a_header_checked_as_it_stands(self):
        self.assertBlocked(self.apply_patch("cat .env"))

    def test_other_tool_starting_as_a_patch_checked_as_it_stands(self):
        """A shell runs every line, the one after `*** End Patch` too."""
        text = patch("*** Add File: notes.txt", body="+hi\n") + "cat .env"
        with self.subTest(form="claude", tool="Bash"):
            self.assertBlocked(self.guard({"command": text}, tool_name="Bash"))
        with self.subTest(form="codex", tool="shell"):
            payload = {"tool_name": "shell", "tool_input": {"command": text}, "cwd": str(self.proj)}
            self.assertBlocked(self.hook(["guard", "--harness", "codex"], payload))

    def test_patch_paths_strips_all_rust_white_space(self):
        """Rust's trim strips Unicode White_Space; Python's strip must strip at least that."""
        rust_white_space = "\t\v\f\r \x85\xa0 " + "".join(map(chr, range(0x2000, 0x200B))) + \
            "    　"
        for ws in rust_white_space:
            with self.subTest(ws=hex(ord(ws))):
                text = after_add(f"{ws}*** Update File: .env{ws}")
                self.assertEqual(keel_hook.patch_paths(text), ["notes.txt", ".env"])


class Allowlist(Project):
    """Where KEEL is on, only the user edits the guard's allowlist."""

    def setUp(self):
        super().setUp()
        self.switch_on()
        self.allow = self.proj / ".keel" / "data-boundary-allow"

    def assertAllowlistBlocked(self, result):
        self.assertBlocked(result)
        self.assertIn("only the user", result.stderr)
        self.assertIn("ask the user", result.stderr)

    def test_write_tools_blocked(self):
        for tool, key in (("Write", "file_path"), ("Edit", "file_path"), ("MultiEdit", "file_path"),
                          ("NotebookEdit", "notebook_path")):
            with self.subTest(tool=tool):
                self.assertAllowlistBlocked(self.guard({key: str(self.allow)}, tool_name=tool))

    def test_mixed_case_path_blocked(self):
        self.assertAllowlistBlocked(self.guard({"file_path": str(self.proj / ".KEEL" / "Data-Boundary-Allow")},
                                               tool_name="Write"))

    def test_relative_paths_blocked(self):
        cases = (("data-boundary-allow", self.proj / ".keel"), ("./.keel/data-boundary-allow", self.proj),
                 (".keel/./data-boundary-allow", self.proj), ("../proj/.keel/data-boundary-allow", self.proj))
        for path, cwd in cases:
            with self.subTest(path=path):
                self.assertAllowlistBlocked(self.guard({"file_path": path}, tool_name="Edit", cwd=cwd))

    def test_link_to_the_allowlist_blocked(self):
        self.allow.write_text("# test\n", encoding="utf-8")
        link = self.proj / "notes.txt"
        link.symlink_to(self.allow)
        self.assertAllowlistBlocked(self.guard({"file_path": str(link)}, tool_name="Write"))

    def test_patches_naming_the_allowlist_blocked(self):
        moved = patch("*** Update File: notes.txt").replace(
            "*** End Patch", "*** Move to: .keel/data-boundary-allow\n*** End Patch")
        for text in (patch("*** Add File: .keel/data-boundary-allow", body="+.env\n"),
                     patch("*** Update File: .keel/data-boundary-allow"), moved):
            with self.subTest(patch=text.splitlines()[1]):
                self.assertAllowlistBlocked(self.guard({"command": text}, tool_name="apply_patch"))

    def test_padded_patch_naming_the_allowlist_blocked(self):
        """Codex strips the line, so a tab hides nothing, even under the override."""
        cases = {"a tab before the header": after_add("\t*** Add File: .keel/data-boundary-allow\n+.env"),
                 "two spaces before the path": patch("*** Add File:  .keel/data-boundary-allow", body="+.env\n")}
        for name, text in cases.items():
            for env in ({}, {"KEEL_DATA_BOUNDARY_OVERRIDE": "1"}):
                with self.subTest(case=name, env=env):
                    self.assertAllowlistBlocked(self.guard({"command": text}, tool_name="apply_patch", env=env))

    def test_command_starting_as_a_patch_naming_it_blocked(self):
        text = patch("*** Add File: notes.txt", body="+hi\n") + "echo .env > .keel/data-boundary-allow"
        self.assertAllowlistBlocked(self.guard({"command": text}, tool_name="Bash"))

    def test_commands_naming_the_allowlist_blocked(self):
        for tool, command in (("Bash", "cat .keel/data-boundary-allow"),
                              ("Bash", "echo .env >> .KEEL/Data-Boundary-Allow"),
                              ("shell", ["sh", "-c", "echo .env >> .keel/data-boundary-allow"])):
            with self.subTest(command=command):
                self.assertAllowlistBlocked(self.guard({"command": command}, tool_name=tool))

    def test_keel_guard_always_blocks_it_in_a_dormant_folder(self):
        other = self.tmp / "other"
        other.mkdir()
        self.assertAllowlistBlocked(self.guard({"file_path": str(other / ".keel" / "data-boundary-allow")},
                                               tool_name="Write", cwd=other, project=other,
                                               env={"KEEL_GUARD": "always"}))

    def test_override_does_not_unlock_it(self):
        self.assertAllowlistBlocked(self.guard({"file_path": str(self.allow)}, tool_name="Write",
                                               env={"KEEL_DATA_BOUNDARY_OVERRIDE": "1"}))

    def test_reading_it_allowed(self):
        self.assertAllowed(self.guard({"file_path": str(self.allow)}, tool_name="Read"))

    def test_other_keel_files_allowed(self):
        for path in (self.proj / ".keel" / "keel.json", self.proj / ".keel" / "ops" / "notes.md"):
            with self.subTest(path=path.name):
                self.assertAllowed(self.guard({"file_path": str(path)}, tool_name="Write"))

    def test_unrelated_command_allowed(self):
        self.assertAllowed(self.guard({"command": "git status"}, tool_name="Bash"))

    def test_patch_whose_text_mentions_it_allowed(self):
        text = patch("*** Update File: README.md", body="@@\n-old\n+only the user edits .keel/data-boundary-allow\n")
        self.assertAllowed(self.guard({"command": text}, tool_name="apply_patch"))

    def test_allowed_where_keel_is_off(self):
        off = self.tmp / "off"
        off.mkdir()
        self.assertAllowed(self.guard({"file_path": str(off / ".keel" / "data-boundary-allow")},
                                      tool_name="Write", cwd=off, project=off))


class Hostile(Project):
    """A role file or hook input built to crash or hang the hook does neither: KEEL stays on,
    the guard blocks, and the session reports the role as not recorded."""

    HOOK_TIMEOUT = 10  # a hang fails fast instead of stalling the suite
    DEEP = 20000  # far past where json.loads raises RecursionError

    def setUp(self):
        super().setUp()
        (self.proj / ".keel").mkdir()
        self.role_file = self.proj / ".keel" / "keel.json"

    def assertArmedNotRecorded(self):
        for path in (str(self.proj / ".env"), "keel-armed-check/.env"):
            for form in ("claude", "codex"):
                with self.subTest(path=path, form=form):
                    if form == "claude":
                        self.assertBlocked(self.guard({"file_path": path}))
                    else:
                        payload = {"tool_name": "Read", "tool_input": {"file_path": path}, "cwd": str(self.proj)}
                        self.assertBlocked(self.hook(["guard", "--harness", "codex"], payload))
        text = self.context(self.session())
        self.assertIn("role: not recorded", text)
        self.assertIn(LAYER_MARK, text)

    def test_deeply_nested_role_file(self):
        nested = "[" * self.DEEP + "]" * self.DEEP
        self.role_file.write_text(f'{{"role": "operator", "pad": {nested}}}', encoding="utf-8")
        self.assertLess(self.role_file.stat().st_size, ROLE_CAP, "it must be parsed, not refused for size")
        self.assertArmedNotRecorded()

    def test_role_file_past_the_cap(self):
        """Valid JSON padded with spaces: read at the cap, refused one byte past it."""
        valid = '{"role": "owner"}'
        with self.subTest(size="exactly the cap"):
            self.role_file.write_text(valid.ljust(ROLE_CAP), encoding="utf-8")
            self.assertIn("role: owner", self.context(self.session()))
        with self.subTest(size="one byte past the cap"):
            self.role_file.write_text(valid.ljust(ROLE_CAP + 1), encoding="utf-8")
            self.assertArmedNotRecorded()

    @unittest.skipUnless(hasattr(os, "mkfifo"), "no named pipes here")
    def test_named_pipe_role_file_with_no_writer(self):
        os.mkfifo(self.role_file)
        self.assertArmedNotRecorded()

    @unittest.skipUnless(hasattr(os, "mkfifo"), "no named pipes here")
    def test_named_pipe_role_file_is_never_read(self):
        """A valid role already waits in the pipe: only a regular file is read."""
        os.mkfifo(self.role_file)
        fd = os.open(self.role_file, os.O_RDWR | os.O_NONBLOCK)
        self.addCleanup(os.close, fd)
        os.write(fd, b'{"role": "owner"}')
        self.assertIn("role: not recorded", self.context(self.session()))

    @unittest.skipUnless(os.path.exists("/dev/zero"), "no /dev/zero here")
    def test_role_file_linked_to_a_device(self):
        self.role_file.symlink_to("/dev/zero")
        self.assertArmedNotRecorded()

    def test_deeply_nested_input(self):
        """Stdin nested too deep is unreadable input: blocked where KEEL is on, ignored where off."""
        self.role_file.write_text(json.dumps({"role": "owner"}), encoding="utf-8")
        nested = "[" * self.DEEP + "]" * self.DEEP
        raw = f'{{"tool_name": "Read", "tool_input": {{"file_path": "README.md"}}, "pad": {nested}}}'
        self.assertBlocked(self.hook(["guard"], raw=raw, env={"CLAUDE_PROJECT_DIR": str(self.proj)}))
        self.assertIn("role: owner", self.context(self.hook(["session"], raw=raw,
                                                            env={"CLAUDE_PROJECT_DIR": str(self.proj)})))
        off = self.tmp / "off"
        off.mkdir()
        for command in ("guard", "session"):
            with self.subTest(keel="off", command=command):
                self.assertSilent(self.hook([command], raw=raw, env={"CLAUDE_PROJECT_DIR": str(off)}))


class InProcess(Project):
    """guard() called in this process, for errors no file on disk can cause."""

    def call_guard(self, project: Path, plugin_root: Path = KIT, **raising) -> tuple[int, str]:
        """Run guard() on a Read of README.md, with each named function raising its error."""
        env = {"HOME": str(self.home), "CLAUDE_PLUGIN_ROOT": str(plugin_root),
               "CLAUDE_PROJECT_DIR": str(project), "PATH": os.environ.get("PATH", "/usr/bin:/bin")}
        raw = json.dumps({"tool_name": "Read", "tool_input": {"file_path": str(project / "README.md")},
                          "cwd": str(project)})
        err = io.StringIO()
        with contextlib.ExitStack() as stack:
            stack.enter_context(mock.patch.dict(os.environ, env, clear=True))
            for name, error in raising.items():
                stack.enter_context(mock.patch.object(keel_hook, name, side_effect=error))
            stack.enter_context(contextlib.redirect_stderr(err))
            code = keel_hook.guard(raw)
        return code, err.getvalue()

    def test_control_no_error(self):
        self.switch_on()
        self.assertEqual(self.call_guard(self.proj), (0, ""))

    def test_error_after_a_keel_folder_blocks(self):
        self.switch_on()
        code, err = self.call_guard(self.proj, role_of=RuntimeError("the role file blew up"))
        self.assertEqual(code, 2)
        self.assertIn("could not evaluate", err)

    @unittest.skipUnless(HAS_GIT, "git not installed")
    def test_error_after_the_main_checkout_marker_blocks(self):
        """A linked worktree whose marker is in its main checkout, met after the walk."""
        main, wt = self.tmp / "main", self.tmp / "wt"
        self.repo_with_worktree(main, wt)
        self.switch_on(where=main)
        code, err = self.call_guard(wt, role_of=RuntimeError("the role file blew up"))
        self.assertEqual(code, 2)
        self.assertIn("could not evaluate", err)

    def test_error_after_a_keel_factory_entry_blocks(self):
        """The entry is the kit root itself, so the master-checkout test runs, and raises."""
        kit = self.proj / "keel-factory"
        kit.mkdir()
        code, err = self.call_guard(self.proj, plugin_root=kit, master_checkout=ValueError("odd checkout"))
        self.assertEqual(code, 2)
        self.assertIn("could not evaluate", err)

    def test_error_before_any_marker_allows(self):
        """KEEL is off as far as anyone can tell: no other project on the machine is touched."""
        self.assertEqual(self.call_guard(self.proj, git_root=OSError("no git here")), (0, ""))


class Session(Project):
    """Where KEEL is on, the session hook injects the always-on layer once."""

    def test_owner_project_gets_the_layer(self):
        self.switch_on("owner")
        text = self.context(self.session())
        self.assertIn(LAYER_MARK, text)
        self.assertIn("role: owner", text)
        self.assertIn(str(KIT), text)

    def test_operator_role_points_at_operator_protocol(self):
        self.switch_on("operator")
        text = self.context(self.session())
        self.assertIn("role: operator", text)
        self.assertIn("OPERATOR.md", text)
        self.assertIn("Notes go in `<ops>`: `keel-factory/.ops/` where the project holds a "
                      "`keel-factory/`, else `.keel/ops/`.", text)

    def test_unrecorded_role_sends_to_helm(self):
        self.switch_on(role=None)
        text = self.context(self.session())
        self.assertIn("role: not recorded", text)

    def test_linked_kit_is_role_kit(self):
        (self.proj / "keel-factory").mkdir()
        self.assertIn("role: kit", self.context(self.session()))

    def test_layer_fits_its_budget(self):
        self.switch_on()
        self.assertLessEqual(len(self.context(self.session())), 7000)

    def test_header_only_when_project_imports_the_layer(self):
        self.switch_on()
        self.link_kit()
        (self.proj / "CLAUDE.md").write_text("# Ours\n\n@keel-factory/CLAUDE.md\n", encoding="utf-8")
        text = self.context(self.session())
        self.assertNotIn(LAYER_MARK, text)
        self.assertIn("role: owner", text)

    def test_header_only_when_agents_md_carries_the_layer(self):
        """Codex reads AGENTS.md; with the mark there, the layer is already in context."""
        self.switch_on()
        (self.proj / "AGENTS.md").write_text(f"# Ours\n\n{LAYER_MARK}\nrules\n", encoding="utf-8")
        self.assertNotIn(LAYER_MARK, self.context(self.session(harness="codex")))

    def test_plugin_root_env_names_the_kit(self):
        self.switch_on()
        fake = self.tmp / "fake-kit"
        fake.mkdir()
        text = self.context(self.session(env={"CLAUDE_PLUGIN_ROOT": str(fake)}))
        self.assertIn(str(fake), text)
        self.assertNotIn(LAYER_MARK, text)  # no CLAUDE.md there: header only, no crash

    def test_project_dir_env_wins_over_cwd(self):
        self.switch_on()
        elsewhere = self.tmp / "elsewhere"
        elsewhere.mkdir()
        result = self.session(env={"CLAUDE_PROJECT_DIR": str(self.proj)}, cwd=elsewhere)
        self.assertIn("role: owner", self.context(result))


class Harness(Project):
    """Which of the project's own files count depends on the harness that loads them."""

    def setUp(self):
        super().setUp()
        self.switch_on()

    def write(self, name: str, text: str):
        path = self.proj / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def layer_injected(self, harness: str) -> bool:
        text = self.context(self.session(harness=harness))
        self.assertIn("role: owner", text)
        return LAYER_MARK in text

    def test_codex_ignores_a_claude_import(self):
        self.link_kit()
        self.write("CLAUDE.md", "# Ours\n\n@keel-factory/CLAUDE.md\n")
        self.assertTrue(self.layer_injected("codex"))
        self.assertFalse(self.layer_injected("claude"))

    def test_codex_ignores_claude_md_even_with_the_mark(self):
        self.write("CLAUDE.md", f"{LAYER_MARK}\n# KEEL\n")
        self.assertTrue(self.layer_injected("codex"))
        self.assertFalse(self.layer_injected("claude"))

    def test_codex_needs_the_mark_not_the_import_text(self):
        """Codex has no @import: even a line that would resolve for Claude Code does not count."""
        self.link_kit()
        self.write("AGENTS.md", "# Ours\n\n@keel-factory/CLAUDE.md\n\nRead keel-factory/CLAUDE.md first.\n")
        self.assertTrue(self.layer_injected("codex"))

    def test_dangling_import_injects_the_layer(self):
        """No keel-factory/ beside the file (a plugin project, a fresh clone): nothing to import."""
        self.write("CLAUDE.md", "# Ours\n\n@keel-factory/CLAUDE.md\n")
        self.assertTrue(self.layer_injected("claude"))

    def test_import_of_a_file_without_the_mark_injects_the_layer(self):
        self.write("keel-factory/CLAUDE.md", "# Not KEEL's layer\n")
        self.write("CLAUDE.md", "# Ours\n\n@keel-factory/CLAUDE.md\n")
        self.assertTrue(self.layer_injected("claude"))

    def test_prose_mention_injects_the_layer(self):
        """Only a line that is the import counts; the path in a sentence imports nothing."""
        self.link_kit()
        self.write(".claude/keel-factory/CLAUDE.md", f"{LAYER_MARK}\n# KEEL\n")
        for name in ("CLAUDE.md", "CLAUDE.local.md", ".claude/CLAUDE.md"):
            with self.subTest(file=name, control="the import line itself counts"):
                self.write(name, "# Ours\n\n@keel-factory/CLAUDE.md\n")
                self.assertFalse(self.layer_injected("claude"))
            for prose in ("We stopped using keel-factory/CLAUDE.md long ago.\n",
                          "See @keel-factory/CLAUDE.md for the method.\n",
                          "Import `@keel-factory/CLAUDE.md` here.\n"):
                with self.subTest(file=name, prose=prose):
                    self.write(name, f"# Ours\n\n{prose}")
                    self.assertTrue(self.layer_injected("claude"))
            (self.proj / name).unlink()

    def test_dot_slash_import_counts(self):
        self.link_kit()
        for line in ("@./keel-factory/CLAUDE.md", "@keel-factory/CLAUDE.md \t"):
            with self.subTest(line=line):
                self.write("CLAUDE.md", f"# Ours\n\n{line}\n")
                self.assertFalse(self.layer_injected("claude"))

    def test_dot_claude_import_resolves_from_its_own_folder(self):
        """.claude/CLAUDE.md imports from .claude/, so a link at the root is not what it reaches."""
        self.link_kit()
        self.write(".claude/CLAUDE.md", "@keel-factory/CLAUDE.md\n")
        self.assertTrue(self.layer_injected("claude"))

    def test_claude_ignores_a_lone_agents_md(self):
        """Claude Code reads AGENTS.md only through an @AGENTS.md import (deliberately narrow)."""
        self.write("AGENTS.md", f"# Ours\n\n{LAYER_MARK}\nrules\n")
        self.assertTrue(self.layer_injected("claude"))

    def test_claude_ignores_agents_md_beside_its_own_claude_md(self):
        self.write("CLAUDE.md", "# Ours\n")
        self.write("AGENTS.md", f"{LAYER_MARK}\nrules\n")
        self.assertTrue(self.layer_injected("claude"))

    def test_claude_counts_agents_md_it_imports(self):
        self.write("CLAUDE.md", "# Ours\n\n@AGENTS.md\n")
        self.write("AGENTS.md", f"{LAYER_MARK}\nrules\n")
        self.assertFalse(self.layer_injected("claude"))

    def test_claude_counts_dot_claude_claude_md(self):
        self.write(".claude/CLAUDE.md", "@keel-factory/CLAUDE.md\n")
        self.write(".claude/keel-factory/CLAUDE.md", f"{LAYER_MARK}\n# KEEL\n")
        self.assertFalse(self.layer_injected("claude"))

    def test_claude_counts_claude_local_md(self):
        self.write("CLAUDE.local.md", f"{LAYER_MARK}\nrules\n")
        self.assertFalse(self.layer_injected("claude"))

    def test_default_harness_is_claude(self):
        self.link_kit()
        self.write("CLAUDE.md", "@keel-factory/CLAUDE.md\n")
        self.assertNotIn(LAYER_MARK, self.context(self.session()))

    def test_v1_copy_gets_the_upgrade_note(self):
        """With keel-factory/ beside the file, Claude Code is offered the import; Codex never is."""
        self.link_kit()
        v1 = f"# KEEL\n\n{V1_PHRASE} A copy of it lives in this project.\n"
        for harness, name in (("claude", "CLAUDE.md"), ("codex", "AGENTS.md")):
            with self.subTest(harness=harness):
                self.write(name, v1)
                text = self.context(self.session(harness=harness))
                self.assertNotIn(LAYER_MARK, text)
                self.assertIn("role: owner", text)
                self.assertIn(f"This project's {name} is KEEL's v1.0 copy", text)
                self.assertEqual("@keel-factory/CLAUDE.md" in text, harness == "claude")
                self.assertEqual("delete KEEL's v1.0 text" in text, harness == "codex")
                self.assertIn("v1.1 layer", text)

    def test_v1_copy_without_the_link_is_told_to_delete_it(self):
        """No keel-factory/CLAUDE.md with the mark beside the file: an import would dangle."""
        v1 = f"# KEEL\n\n{V1_PHRASE} A copy of it lives in this project.\n"
        delete = "delete KEEL's v1.0 text from that file (this hook then supplies the layer), or replace it with"
        for harness, name, layer in (("claude", "CLAUDE.md", "v1.1's `CLAUDE.md`."),
                                     ("codex", "AGENTS.md", "the v1.1 layer: the kit's CLAUDE.md")):
            with self.subTest(harness=harness):
                self.write(name, v1)
                text = self.context(self.session(harness=harness))
                self.assertNotIn(LAYER_MARK, text)
                self.assertIn(f"This project's {name} is KEEL's v1.0 copy", text)
                self.assertNotIn("@keel-factory/CLAUDE.md", text)
                self.assertIn(f"{delete} {layer}", text)
        with self.subTest(harness="claude", beside="a keel-factory/CLAUDE.md without the mark"):
            self.write("keel-factory/CLAUDE.md", "# Not KEEL's layer\n")
            text = self.context(self.session(harness="claude"))
            self.assertNotIn("@keel-factory/CLAUDE.md", text)
            self.assertIn(delete, text)

    def test_real_v1_0_copy_gets_the_note(self):
        if not (KIT / ".git").exists():
            self.skipTest("this kit has no git history, so the real v1.0 CLAUDE.md is not at hand")
        shown = subprocess.run(["git", "-C", str(KIT), "show", "e09480c:CLAUDE.md"], capture_output=True,
                               env=dict(CLEAN_ENV, HOME=str(self.home)), timeout=60)
        if shown.returncode != 0:
            self.skipTest("commit e09480c (KEEL FACTORY v1.0.0) is not in this kit's history")
        v1 = shown.stdout.decode("utf-8")
        self.assertIn(V1_PHRASE, v1)
        self.assertNotIn(LAYER_MARK, v1)
        self.write("CLAUDE.md", v1)
        with self.subTest(keel_factory="absent: the plugin's layout"):
            text = self.context(self.session())
            self.assertNotIn(LAYER_MARK, text)
            self.assertIn("KEEL's v1.0 copy", text)
            self.assertNotIn("@keel-factory/CLAUDE.md", text)
            self.assertIn("delete KEEL's v1.0 text", text)
        with self.subTest(keel_factory="a link to the kit"):
            self.link_kit()
            text = self.context(self.session())
            self.assertNotIn(LAYER_MARK, text)
            self.assertIn("KEEL's v1.0 copy", text)
            self.assertIn("@keel-factory/CLAUDE.md", text)


if __name__ == "__main__":
    unittest.main(verbosity=1)
