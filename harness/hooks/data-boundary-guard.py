#!/usr/bin/env python3
"""Data Boundary Guard -- the Python port of data-boundary-guard.js.

Authored for KEEL FACTORY; not part of ECC. A PreToolUse hook: it reads the
hook's JSON from stdin and blocks the tool call (exit 2, reason on stderr) when
the call would touch

  1. any path git would ignore in the repository it belongs to
     (`git check-ignore`), or
  2. any path whose name is shaped like a secret or credential, whether or not
     it is gitignored -- a secret that was never gitignored is exactly the case
     (1) cannot catch.

Structured paths are checked exactly: tool_input.file_path, .file, .path and
.notebook_path (Read, Edit, Write, NotebookEdit, Glob, Grep). A Bash command is
covered on a best-effort basis only: it is split on whitespace and each
path-shaped token is checked the same way. That is a heuristic, not a parser,
and a sufficiently indirect command evades it. It is a backstop; the
structured-path coverage is the reason the hook is worth relying on.

Overrides, inconvenient by design (see ../DATA-BOUNDARY.md):
  - one path, durably: add its path relative to the repo root to
    `.keel/data-boundary-allow`, one path per line;
  - everything, this session: a human sets KEEL_DATA_BOUNDARY_OVERRIDE=1 in the
    environment the tool calls run in. Nothing in this factory sets it.

Exit codes: 0 = allow, 2 = block.

This is the default guard: the settings templates wire it, because it is the
version that has actually been executed. Every pattern, the allowlist, the
override and the block message are the JavaScript hook's, unchanged. Two rules
differ, both decided by the framework's owner:

  - In a Bash command, a plain word (no slash, no leading dot) counts as a path
    only when a regular file by that name exists in the working directory. The
    JavaScript version treats every word matching a secret pattern as a path,
    which blocks routine commands -- `git config`, `kubectl config`,
    `grep -rn secret` -- and pushes people toward the session-wide override,
    which switches the whole guard off. (2026-10-14)
  - A shell command may use a project's own tool folders -- .venv/bin/,
    venv/bin/, node_modules/.bin/ -- even though they are gitignored. Without
    this, an operator cannot run a Python project's own tests. The Read, Edit
    and Write tools stay strict there, and secret-shaped names stay blocked
    everywhere. (2026-10-15)

Three behaviours differ as well, each closing a way the JavaScript version lets
a call through unchecked:

  - The whole of stdin is read. The JavaScript version keeps only the first
    1 MiB, so a Write or Edit whose JSON is larger fails to parse and is
    allowed without its path ever being looked at.
  - It fails closed. Input that is not empty but cannot be read as a JSON
    object is blocked, and so is any error inside the guard itself. A guard
    that cannot evaluate a call cannot vouch for it, and a hook that crashes is
    treated by the harness as a non-blocking error -- an allow.
  - Nothing is written to stdout on allow. The JavaScript version echoes its
    input for ECC's in-process chaining; a harness that reads a hook's stdout
    as a decision should get nothing from a guard that has no objection.

Standard library only. Self-test: test_data_boundary_guard.py, beside this file.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys

# Secret-shaped names that are conventionally meant to be shared -- checked
# before the denylist so a repo's own .env.example never trips it.
SAFE_BASENAME_EXCEPTIONS = re.compile(r"(\.example|\.sample|\.template|\.dist)$", re.IGNORECASE)

# Matched against the basename, case-insensitively. Deliberately broad: a false
# positive costs one override; a false negative costs a credential in the
# model's context or in a tool call's output. Each source string is the
# JavaScript hook's own, so a block reason reads the same from either runtime.
SECRET_SOURCES = [
    r"^\.env(\..+)?$",
    r"secret",
    r"credential",
    r"(^|[._-])password([._-]|$)",
    r"(^|[._-])passwd([._-]|$)",
    r"(^|[._-])api[._-]?key",
    r"\.pem$",
    r"\.key$",
    r"\.p12$",
    r"\.pfx$",
    r"\.jks$",
    r"\.keystore$",
    r"^id_(rsa|dsa|ecdsa|ed25519)$",
    r"^\.npmrc$",
    r"^\.pypirc$",
    r"^\.netrc$",
    r"^\.git-credentials$",
    r"^credentials$",  # e.g. .aws/credentials
    r"^config$",  # catches .aws/config and .kube/config alongside the directory check
    r"kubeconfig",
    r"\.tfstate(\.backup)?$",
    r"service[._-]?account.*\.json$",
    r"\.gpg$",
    r"\.asc$",
    r"wallet.*\.json$",
    r"\.keychain(-db)?$",
]

# Names too generic to denylist alone (`config`, `credentials`) are sensitive
# inside one of these directories.
SENSITIVE_DIR_SOURCES = [
    r"(^|\/)\.aws(\/|$)",
    r"(^|\/)\.kube(\/|$)",
    r"(^|\/)\.ssh(\/|$)",
    r"(^|\/)\.gnupg(\/|$)",
    r"(^|\/)\.config\/gcloud(\/|$)",
]

SECRET_PATTERNS = [(f"/{source}/i", re.compile(source, re.IGNORECASE)) for source in SECRET_SOURCES]
SENSITIVE_DIR_FRAGMENTS = [(f"/{source}/i", re.compile(source, re.IGNORECASE)) for source in SENSITIVE_DIR_SOURCES]
GIT_TIMEOUT_SECONDS = 10

# A project's own tool folders. A shell command may use what is in them even though they
# are gitignored: running .venv/bin/python is how a Python project runs its own checks.
# Only commands get this; the Read/Edit/Write tools stay strict here, and secret-shaped
# names are blocked wherever they sit.
TOOL_FOLDERS = re.compile(r"(^|/)(\.venv/bin|venv/bin|node_modules/\.bin)(/|$)")


class UnreadableInput(Exception):
    """The hook input could not be read as a JSON object."""


def is_enabled(value: object) -> bool:
    return str(value or "").lower() in ("1", "true", "yes", "on")


def basename_matches_secret_pattern(basename: str) -> str | None:
    if SAFE_BASENAME_EXCEPTIONS.search(basename):
        return None
    for literal, pattern in SECRET_PATTERNS:
        if pattern.search(basename):
            return literal
    return None


def path_matches_sensitive_dir(rel_or_abs_path: str) -> str | None:
    normalized = rel_or_abs_path.replace("\\", "/")
    for literal, pattern in SENSITIVE_DIR_FRAGMENTS:
        if pattern.search(normalized):
            return literal
    return None


def find_repo_root(start_dir: str) -> str | None:
    directory = start_dir
    for _ in range(64):
        if os.path.exists(os.path.join(directory, ".git")):
            return directory
        parent = os.path.dirname(directory)
        if parent == directory:
            return None
        directory = parent
    return None


def is_git_ignored(abs_path: str) -> bool:
    directory = os.path.dirname(abs_path.rstrip("/") or abs_path)  # as Node's path.dirname
    if not os.path.exists(directory):
        return False
    try:
        result = subprocess.run(
            ["git", "check-ignore", "-q", abs_path],
            cwd=directory,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=GIT_TIMEOUT_SECONDS,
        )
    except FileNotFoundError:  # git is not installed
        return False
    # 0 = ignored, 1 = not ignored, 128 = not a repository
    return result.returncode == 0


def is_allowlisted(abs_path: str, repo_root: str | None) -> bool:
    if not repo_root:
        return False
    allow_file = os.path.join(repo_root, ".keel", "data-boundary-allow")
    if not os.path.exists(allow_file):
        return False
    try:
        with open(allow_file, encoding="utf-8") as handle:
            lines = handle.read().split("\n")
    except (OSError, UnicodeDecodeError):
        return False
    rel_path = os.path.relpath(abs_path, repo_root).replace("\\", "/")
    entries = [line.strip() for line in lines]
    return any(entry == rel_path or entry == abs_path for entry in entries if entry and not entry.startswith("#"))


def in_tool_folder(abs_path: str) -> bool:
    # Normalized first, so `.venv/bin/../../private` cannot borrow the exemption.
    return bool(TOOL_FOLDERS.search(os.path.normpath(abs_path).replace("\\", "/")))


def evaluate_path(candidate: str, cwd: str | None, from_command: bool = False) -> str | None:
    """Return a block reason for one candidate path, or None when it is fine."""
    if not candidate:
        return None
    if os.path.isabs(candidate):
        abs_path = candidate
    else:
        abs_path = os.path.abspath(os.path.join(cwd or os.getcwd(), candidate))
    # Node's path.basename and path.dirname ignore a trailing slash; match them.
    trimmed = abs_path.rstrip("/") or abs_path
    basename = os.path.basename(trimmed)

    repo_root = find_repo_root(os.path.dirname(trimmed))
    if is_allowlisted(abs_path, repo_root):
        return None

    secret_match = basename_matches_secret_pattern(basename)
    dir_match = path_matches_sensitive_dir(abs_path)
    ignored = is_git_ignored(abs_path) and not (from_command and in_tool_folder(abs_path))

    if not secret_match and not dir_match and not ignored:
        return None

    reasons = []
    if ignored:
        reasons.append("matches this repo's .gitignore")
    if secret_match:
        reasons.append(f"filename matches secret-shaped pattern {secret_match}")
    if dir_match:
        reasons.append(f"lives inside a sensitive directory ({dir_match})")

    allow_entry = os.path.relpath(abs_path, repo_root) if repo_root else abs_path
    return (
        f"BLOCKED by data-boundary-guard: {abs_path}\n"
        f"Reason: {'; '.join(reasons)}.\n"
        "This path was not touched. If this access is genuinely needed:\n"
        f'  - Durable, this path only: add "{allow_entry}" '
        "to .keel/data-boundary-allow at the repo root.\n"
        "  - This session only, everything: a human must set "
        "KEEL_DATA_BOUNDARY_OVERRIDE=1 in the environment — never do this yourself.\n"
        "Do not retry via a different tool (cat, curl, a script) to route around this "
        "block. Stop and ask the user whether this specific access is intended."
    )


def extract_path_like_tokens(command: str, cwd: str) -> list[str]:
    """A very rough tokenizer: enough to pull path-shaped arguments out of a
    shell command for the best-effort Bash coverage. Not a substitute for the
    structured-path checks.

    A token with a slash, or a leading dot and a letter, is always a candidate.
    A plain word is one only when it matches a secret pattern *and* names a
    regular file in the directory the command runs in -- so `git config` and
    `grep secret` pass, while `cat id_rsa` beside a real id_rsa does not."""
    if not command:
        return []
    tokens = [token for token in re.split(r"\s+", command) if token]
    tokens = [re.sub(r"^['\"]|['\"]$", "", token) for token in tokens]
    path_like = [
        token
        for token in tokens
        if "/" in token
        or re.match(r"^\.[a-zA-Z]", token)
        or (any(pattern.search(token) for _, pattern in SECRET_PATTERNS) and os.path.isfile(os.path.join(cwd, token)))
    ]
    return [token for token in path_like if not token.startswith("-") and not re.match(r"^https?://", token, re.I)]


def parse_input(raw: str) -> dict:
    if not raw.strip():
        return {}
    try:
        parsed = json.loads(raw)
    except ValueError as exc:
        raise UnreadableInput(f"the hook input is not valid JSON ({exc})") from exc
    if not isinstance(parsed, dict):
        raise UnreadableInput("the hook input is JSON but not an object")
    return parsed


def run(raw: str) -> tuple[int, str]:
    """Return (exit code, stderr text) for one hook invocation."""
    if is_enabled(os.environ.get("KEEL_DATA_BOUNDARY_OVERRIDE")):
        return 0, ""

    hook_input = parse_input(raw)
    tool_input = hook_input.get("tool_input")
    if not isinstance(tool_input, dict):
        tool_input = {}
    cwd = hook_input.get("cwd")
    if not isinstance(cwd, str) or not cwd:
        cwd = os.getcwd()

    candidates = [
        (tool_input[key], False)
        for key in ("file_path", "file", "path", "notebook_path")
        if isinstance(tool_input.get(key), str)
    ]
    if isinstance(tool_input.get("command"), str):
        candidates.extend((token, True) for token in extract_path_like_tokens(tool_input["command"], cwd))

    for candidate, from_command in candidates:
        reason = evaluate_path(candidate, cwd, from_command)
        if reason:
            return 2, reason
    return 0, ""


def main() -> int:
    try:
        raw = sys.stdin.buffer.read().decode("utf-8", errors="surrogateescape")
        code, message = run(raw)
    except Exception as exc:  # fail closed: see the module docstring
        code = 2
        message = (
            f"BLOCKED by data-boundary-guard: could not evaluate this tool call ({exc}).\n"
            "A guard that cannot read what it is guarding cannot vouch for it, so the call "
            "was blocked rather than allowed. Nothing was touched. Report this to the user "
            "rather than retrying the same access another way."
        )
    if message:
        sys.stderr.write(message + "\n")
    return code


if __name__ == "__main__":
    sys.exit(main())
