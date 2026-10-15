#!/usr/bin/env python3
"""Self-test for data-boundary-guard.py -- every rule watched failing, not only passing.

    python3 harness/hooks/test_data_boundary_guard.py

Drives the hook exactly as a harness does: JSON on stdin, then the exit code and
stderr read back. Standard library only. Every path it checks is built under a
temporary directory and none is ever opened -- the guard judges paths, not file
contents. The gitignore cases need git; without it they are skipped, and
unittest reports them as skipped. A skipped test is not a passed one.
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

GUARD = Path(__file__).resolve().parent / "data-boundary-guard.py"


def call(payload=None, raw: str | None = None, override: str | None = None) -> subprocess.CompletedProcess:
    env = {key: value for key, value in os.environ.items() if key != "KEEL_DATA_BOUNDARY_OVERRIDE"}
    if override is not None:
        env["KEEL_DATA_BOUNDARY_OVERRIDE"] = override
    data = raw if raw is not None else json.dumps(payload)
    result = subprocess.run([sys.executable, "-B", str(GUARD)], input=data.encode("utf-8"),
                            capture_output=True, env=env)
    result.stdout = result.stdout.decode("utf-8", errors="replace")
    result.stderr = result.stderr.decode("utf-8", errors="replace")
    return result


class TempDirTest(unittest.TestCase):
    def setUp(self):
        self.tmp = os.path.realpath(tempfile.mkdtemp(prefix="dbg-test-"))
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)

    def at(self, *parts: str) -> str:
        return os.path.join(self.tmp, *parts)

    def assertBlocked(self, result, *fragments: str):
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("BLOCKED by data-boundary-guard", result.stderr)
        for fragment in fragments:
            self.assertIn(fragment, result.stderr)

    def assertAllowed(self, result):
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        self.assertEqual(result.stdout, "")


class ArmedCheck(TempDirTest):
    """The two commands DATA-BOUNDARY.md tells a human to run before trusting the hook."""

    def test_env_file_is_blocked(self):
        self.assertBlocked(call({"tool_input": {"file_path": "/path/to/some/.env"}}))

    def test_normal_file_is_allowed_silently(self):
        self.assertAllowed(call({"tool_input": {"file_path": "/path/to/some/normal/file.md"}}))


class SecretShapes(TempDirTest):
    BLOCKED = [
        ".env", ".env.production", "secrets.yaml", "aws-credentials.txt", "db_password.txt",
        "old.passwd", "my_api_key.txt", "server.pem", "prod.key", "cert.p12", "cert.pfx",
        "store.jks", "app.keystore", "id_rsa", "id_ed25519", ".npmrc", ".pypirc", ".netrc",
        ".git-credentials", "credentials", "config", "kubeconfig", "terraform.tfstate",
        "terraform.tfstate.backup", "gcp-service-account.json", "backup.gpg", "pubkey.asc",
        "wallet-main.json", "login.keychain-db",
    ]
    ALLOWED = [
        "README.md", "app.py", "keyboard.py", "monkey.txt",
        ".env.example", ".env.sample", "credentials.template", "secrets.dist",
    ]

    def test_secret_shaped_names_are_blocked(self):
        for name in self.BLOCKED:
            with self.subTest(name=name):
                self.assertBlocked(call({"tool_input": {"file_path": self.at(name)}}), "secret-shaped pattern")

    def test_ordinary_and_shareable_names_pass(self):
        for name in self.ALLOWED:
            with self.subTest(name=name):
                self.assertAllowed(call({"tool_input": {"file_path": self.at(name)}}))


class SensitiveDirectories(TempDirTest):
    def test_files_inside_credential_directories_are_blocked(self):
        for parts in [(".aws", "sso-cache.json"), (".ssh", "known_hosts"), (".kube", "cache.json"),
                      (".gnupg", "pubring.kbx"), (".config", "gcloud", "configurations.json")]:
            with self.subTest(path="/".join(parts)):
                self.assertBlocked(call({"tool_input": {"file_path": self.at(*parts)}}), "sensitive directory")


@unittest.skipUnless(shutil.which("git"), "git is not installed, so the gitignore cases did not run")
class Gitignore(TempDirTest):
    def setUp(self):
        super().setUp()
        subprocess.run(["git", "init", "-q", self.tmp], check=True, capture_output=True)
        Path(self.at(".gitignore")).write_text("build/\nlocal.txt\n")
        os.makedirs(self.at("build"))
        os.makedirs(self.at("src"))

    def test_ignored_paths_are_blocked(self):
        self.assertBlocked(call({"tool_input": {"file_path": self.at("local.txt")}}), "matches this repo's .gitignore")
        self.assertBlocked(call({"tool_input": {"file_path": self.at("build", "out.js")}}), ".gitignore")

    def test_tracked_paths_pass(self):
        self.assertAllowed(call({"tool_input": {"file_path": self.at("src", "main.py")}}))

    def test_relative_paths_resolve_against_the_hook_cwd(self):
        result = call({"cwd": self.tmp, "tool_input": {"file_path": "local.txt"}})
        self.assertBlocked(result, self.at("local.txt"))


class Allowlist(TempDirTest):
    def setUp(self):
        super().setUp()
        os.makedirs(self.at(".git"))  # all the repo-root search looks for
        os.makedirs(self.at(".keel"))
        Path(self.at(".keel", "data-boundary-allow")).write_text("# reviewed 2026-10-14\n\n.env.test\n")

    def test_listed_path_passes(self):
        self.assertAllowed(call({"tool_input": {"file_path": self.at(".env.test")}}))

    def test_unlisted_path_is_still_blocked_and_told_how(self):
        self.assertBlocked(call({"tool_input": {"file_path": self.at(".env")}}),
                           'add ".env" to .keel/data-boundary-allow')


class Override(TempDirTest):
    def test_override_set_by_a_human_allows(self):
        for value in ("1", "true", "YES", "on"):
            with self.subTest(value=value):
                self.assertAllowed(call({"tool_input": {"file_path": self.at(".env")}}, override=value))

    def test_any_other_value_does_not(self):
        for value in ("0", "false", "", "please"):
            with self.subTest(value=value):
                self.assertBlocked(call({"tool_input": {"file_path": self.at(".env")}}, override=value))


class BashCoverage(TempDirTest):
    def bash(self, command: str):
        return call({"cwd": self.tmp, "tool_input": {"command": command}})

    def touch(self, name: str):
        Path(self.at(name)).write_text("")  # an empty stand-in; nothing reads it

    def test_path_shaped_tokens_are_checked(self):
        for command in ["cat .env", "grep TOKEN ~/.aws/credentials", "source '.env.local'"]:
            with self.subTest(command=command):
                self.assertBlocked(self.bash(command))

    def test_ordinary_commands_pass(self):
        for command in ["ls -la src/", "echo hello", "git status", "cat .env.example",
                        "curl https://example.com/.env"]:
            with self.subTest(command=command):
                self.assertAllowed(self.bash(command))

    def test_plain_words_that_name_a_real_secret_file_are_checked(self):
        for name in ("id_rsa", "config", "credentials.json"):
            self.touch(name)
        for command in ["cp id_rsa /tmp/x", "cat config", "less credentials.json"]:
            with self.subTest(command=command):
                self.assertBlocked(self.bash(command), "secret-shaped pattern")

    def test_plain_words_that_are_not_files_pass(self):
        # The .js blocks every one of these; the owner chose to narrow it (2026-10-14).
        for command in ["git config user.name", "kubectl config get-contexts", "npm config get registry",
                        "grep -rn secret src/", "git commit -m fix-password-reset"]:
            with self.subTest(command=command):
                self.assertAllowed(self.bash(command))

    def test_a_directory_named_like_a_secret_is_not_a_file(self):
        os.makedirs(self.at("config"))  # as in a Rails or Phoenix app
        self.assertAllowed(self.bash("git config user.name"))


@unittest.skipUnless(shutil.which("git"), "git is not installed, so the tool-folder cases did not run")
class ToolFolders(TempDirTest):
    """A project's own tool folders are gitignored but must stay usable by commands (2026-10-15)."""

    def setUp(self):
        super().setUp()
        subprocess.run(["git", "init", "-q", self.tmp], check=True, capture_output=True)
        Path(self.at(".gitignore")).write_text(".venv/\nnode_modules/\nlocal.txt\n")
        for folder in (".venv/bin", ".venv/lib", "node_modules/.bin"):
            os.makedirs(self.at(folder))

    def bash(self, command: str):
        return call({"cwd": self.tmp, "tool_input": {"command": command}})

    def test_commands_can_run_the_project_s_own_tools(self):
        for command in [".venv/bin/python -m pytest tests -q", "source .venv/bin/activate",
                        "venv/bin/python -m mypy .", "node_modules/.bin/eslint src"]:
            with self.subTest(command=command):
                self.assertAllowed(self.bash(command))

    def test_the_file_tools_stay_strict_inside_tool_folders(self):
        self.assertBlocked(call({"tool_input": {"file_path": self.at(".venv", "bin", "python")}}), ".gitignore")

    def test_the_rest_of_a_virtualenv_stays_blocked(self):
        self.assertBlocked(self.bash("cat .venv/lib/site.py"), ".gitignore")

    def test_no_climbing_out_of_a_tool_folder(self):
        self.assertBlocked(self.bash("cat .venv/bin/../../local.txt"), ".gitignore")
        self.assertBlocked(self.bash(f"cat {self.at('.venv', 'bin')}/../../local.txt"), ".gitignore")

    def test_a_secret_is_still_a_secret_next_to_a_tool(self):
        self.assertBlocked(self.bash(".venv/bin/python read_it.py .env"), "secret-shaped pattern")


class StructuredFields(TempDirTest):
    def test_every_structured_field_is_checked(self):
        for tool_input in [
            {"pattern": "*", "path": self.at(".ssh")},  # Glob
            {"pattern": "TOKEN", "path": self.at("secrets") + "/"},  # Grep, trailing slash
            {"notebook_path": self.at("credentials.ipynb")},  # NotebookEdit
            {"file": self.at("prod.pem")},
        ]:
            with self.subTest(tool_input=tool_input):
                self.assertBlocked(call({"tool_input": tool_input}))


class FailsClosed(TempDirTest):
    """The deliberate departures from the JavaScript version, each closing a way through."""

    def test_unparseable_input_is_blocked(self):
        for raw in ("{not json", '["a list"]', "42"):
            with self.subTest(raw=raw):
                self.assertBlocked(call(raw=raw), "could not evaluate")

    def test_input_over_one_mebibyte_is_still_checked(self):
        # The JavaScript version keeps the first 1 MiB of stdin, fails to parse
        # the remainder, and allows the call unchecked. This must block on the path.
        big = {"tool_name": "Write", "tool_input": {"file_path": self.at(".env"), "content": "x" * (2 * 1024 * 1024)}}
        self.assertBlocked(call(big), self.at(".env"), "secret-shaped pattern")

    def test_large_benign_input_is_allowed(self):
        big = {"tool_name": "Write", "tool_input": {"file_path": self.at("notes.md"), "content": "x" * (2 * 1024 * 1024)}}
        self.assertAllowed(call(big))

    def test_empty_input_is_allowed(self):
        self.assertAllowed(call(raw=""))


if __name__ == "__main__":
    unittest.main(verbosity=2)
