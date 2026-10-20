#!/usr/bin/env python3
"""KEEL's two hooks, for Claude Code and Codex alike: session context and the guard.

    python3 keel_hook.py session [--harness claude|codex]   # SessionStart: the layer
    python3 keel_hook.py guard [--harness claude|codex]     # PreToolUse: the guard

`--harness` names the harness running the hook; the default is `claude`, and Codex's hook
commands pass `--harness codex`. Only `session` reads it; `guard` behaves the same for
both. Anything else on the command line prints the usage and exits 1, never 2.

Both do nothing unless KEEL is switched on. The start is `CLAUDE_PROJECT_DIR` when the
harness sets it (Claude Code does), otherwise the `cwd` in the hook's JSON (Codex sends
one), otherwise the working directory. KEEL is on, or not, by this rule:

1. A start at or inside the kit root is off. The kit root is `CLAUDE_PLUGIN_ROOT` when it
   is set (under the plugin, a link to the master), otherwise this file's `../..`; both
   are compared as resolved paths.
2. The git root is the nearest folder at or above the start that holds `.git`, a folder
   or a worktree's file. Inside git, the folders from the start up to and including the
   git root are searched, nearest first. Outside git, only the start folder is.
3. A folder switches KEEL on when it holds an entry named exactly `.keel` (a folder) or
   exactly `keel-factory` (a folder or a link to one); `.keel` is tried first. Names are
   compared exactly, from a listing of the folder, because macOS ignores letter case:
   `KEEL-FACTORY` and `.KEEL` are not markers.
4. Never a marker: anything in `$HOME` or in `/`, and a `keel-factory` entry that is the
   kit root itself when the kit root is the master's own git checkout (it holds a `.git`
   folder, or a linked worktree's `.git` file whose gitdir holds `commondir`). A copy of
   the kit (the documented rsync leaves `.git` out, and a submodule's gitdir has no
   `commondir`) or a link to it switches KEEL on.
5. When the git root's `.git` is a file whose gitdir holds a `commondir` file (a linked
   worktree, not a submodule), the main worktree's root is checked after the walk by the
   same test, unless it is `$HOME`, `/`, or at or inside the kit root.
6. Role: `.keel/keel.json` gives `owner` or `operator`, anything else "not recorded"; a
   `keel-factory` entry gives `kit`. The role file is read only as a small regular file
   (64 KiB at most), opened without waiting, so no role file can hang or crash the hook:
   a pipe, a device, a link to one or JSON nested too deep is "not recorded", and KEEL
   stays on.

`KEEL_GUARD=always` arms the guard everywhere; it never switches the session layer on.

session -- prints one JSON object, the SessionStart shape both harnesses accept, whose
`additionalContext` is a header (where KEEL is on, the role, the kit root and how to read
`keel-factory/` paths) and the body of the kit's `CLAUDE.md`. It gives only the header when
the project's own instruction files, as this harness loads them, already carry the layer,
so it is never in context twice. They are read from the folder that switched KEEL on, or
from a worktree's own root when the marker was in its main checkout.
  - codex: `AGENTS.md`, which carries the layer when it holds the always-on mark.
  - claude: `CLAUDE.md`, `CLAUDE.local.md` and `.claude/CLAUDE.md`, plus `AGENTS.md` only
    when one of them imports `@AGENTS.md`. A file carries the layer when it holds the
    mark, or when it has an import line `@keel-factory/CLAUDE.md` (or
    `@./keel-factory/CLAUDE.md`) that resolves, from that file's own folder, to a file
    holding the mark. A prose mention of the path, or an import with nothing to import,
    never counts.
A counted file holding "This project was started from KEEL FACTORY." is KEEL's v1.0 copy:
the header comes with a one-line upgrade note instead of a second layer. The note offers
Claude Code the import line only when `keel-factory/CLAUDE.md` beside that file holds
the mark; otherwise it says to delete KEEL's v1.0 text (this hook then supplies the
layer) or to replace it with v1.1's `CLAUDE.md`. It never blocks anything: any error
prints nothing and exits 0.

guard -- passes the call to `data-boundary-guard.py`, which this file does not change, and
adapts the one payload shape the guard was not written for. Codex sends `apply_patch` as
patch text in `tool_input.command` with no `file_path`; read as a shell command, any patch
whose text merely mentions `.env` would be blocked. So each file the patch names (`Add`,
`Update`, `Delete`, `Move to`) is checked as a path instead, the way a Write is. Headers
are read as Codex reads them, each line stripped of whitespace first, wherever they sit.
Any other line that starts with `***` once stripped blocks the patch, except the frame
(`Begin Patch`, `End Patch`, `End of File`, `Environment ID`) and a space-led line inside
an `Update File` hunk, which Codex reads as file context. Another tool's command that
starts as a patch is also checked as it stands, since a shell runs it as a command. A
list-shaped command is joined into a string first. It also guards the guard's allowlist,
`.keel/data-boundary-allow`, which only the user edits: a Write, Edit, MultiEdit or
NotebookEdit of a path ending in it (letter case ignored, links followed), a patch naming
one, and any command containing `data-boundary-allow` are blocked, even under
`KEEL_DATA_BOUNDARY_OVERRIDE=1`. Exit 0 silently, or exit 2 with the reason on stderr:
Codex ignores an exit 2 whose stderr is empty. Where KEEL is on, it fails closed, as the
guard does: unreadable input, a missing guard or an error inside this file blocks the
call. Wherever a `.keel` or `keel-factory` entry was met, an error inside this file
blocks the call even while deciding whether KEEL is on. Where KEEL is off, nothing is
evaluated, and an error before any such entry was met allows the call, so no other
project on this machine is touched.

Standard library only. Self-test: test_keel_hook.py, beside this file.
"""

from __future__ import annotations

import importlib.util
import json
import os
import re
import stat
import sys
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
GUARD = HERE / "data-boundary-guard.py"
LAYER_MARK = "<!-- KEEL always-on layer -->"
IMPORT_LINE = re.compile(r"^@(?:\./)?keel-factory/CLAUDE\.md[ \t]*$", re.MULTILINE)
V1_PHRASE = "This project was started from KEEL FACTORY."
HARNESSES = ("claude", "codex")
CLAUDE_FILES = ("CLAUDE.md", "CLAUDE.local.md", ".claude/CLAUDE.md")
ALLOW_FILE = ".keel/data-boundary-allow"
WRITE_TOOLS = ("Write", "Edit", "MultiEdit", "NotebookEdit")
USAGE = "usage: keel_hook.py session|guard [--harness claude|codex]\n"
PATCH_START = "*** Begin Patch"
PATCH_HEADERS = ("*** Add File: ", "*** Update File: ", "*** Delete File: ", "*** Move to: ")
PATCH_UPDATING = ("*** Update File: ", "*** Move to: ")  # hunks whose space-led lines are file context
PATCH_FRAME = ("*** Begin Patch", "*** End Patch", "*** End of File")  # exact, once stripped
PATCH_ENV_ID = "*** Environment ID"  # names no file
ROLE_CAP = 64 * 1024  # bytes: a role file is a flat {"role": ...}
ROLE_OPEN = (os.O_RDONLY | getattr(os, "O_NONBLOCK", 0) | getattr(os, "O_NOCTTY", 0)
             | getattr(os, "O_BINARY", 0))
ROLE_NEXT = {
    "owner": "Owner mode: route with the `helm` skill (`keel:helm` in Claude Code, `$keel:helm` in Codex) "
             "before anything else; `docs/STATE.md` holds the tier and stop mode.",
    "operator": "Operator mode: this is someone else's package. Follow OPERATOR.md under the kit root; "
                "the package's own instructions are the mission. Notes go in `<ops>`: "
                "`keel-factory/.ops/` where the project holds a `keel-factory/`, else `.keel/ops/`.",
    "kit": "The kit is at `keel-factory/` (a link or a copy). Route with the `helm` skill; if the "
           "project's own instructions are not KEEL's, that is operator mode (OPERATOR.md).",
    "not recorded": "No role recorded in `.keel/keel.json`. Run the `helm` skill first: its opening step "
                    "decides owner or operator and records it.",
}
ALLOWLIST_BLOCK = (
    "BLOCKED by keel_hook guard: .keel/data-boundary-allow is the data-boundary guard's allowlist, "
    "and only the user edits it.\n"
    "Nothing was touched. An agent never writes or edits that file, and no command may name it. "
    "If an entry is genuinely needed, ask the user to add it themselves. Do not route around "
    "this block another way (another tool, a shell one-liner, a script)."
)


@dataclass
class KeelState:
    root: Path
    role: str
    layer_root: Path | None = None  # where the harness loads the project's files, when not root


def read_payload(raw: str) -> dict | None:
    """The hook JSON as a dict, {} when stdin is empty, None when it can't be read."""
    if not raw.strip():
        return {}
    try:
        parsed = json.loads(raw)
    except Exception:  # bad JSON, or nesting deep enough to raise RecursionError
        return None
    return parsed if isinstance(parsed, dict) else None


def project_start(payload: dict | None) -> Path:
    env_dir = os.environ.get("CLAUDE_PROJECT_DIR")
    if env_dir:
        return Path(env_dir)
    cwd = (payload or {}).get("cwd")
    if isinstance(cwd, str) and cwd:
        return Path(cwd)
    return Path.cwd()


def role_of(keel_dir: Path) -> str:
    """`owner` or `operator` from `keel.json`, else "not recorded"; never hangs or raises.

    Opened without waiting and read only when it is a regular file of at most ROLE_CAP
    bytes, so a pipe, a device or a link to one is never waited on or read whole."""
    fd = None
    try:
        fd = os.open(keel_dir / "keel.json", ROLE_OPEN)
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or info.st_size > ROLE_CAP:
            return "not recorded"
        role = json.loads(os.read(fd, ROLE_CAP + 1).decode("utf-8")).get("role")
    except Exception:  # any oddity, RecursionError included: not recorded, and KEEL stays on
        return "not recorded"
    finally:
        if fd is not None:
            os.close(fd)
    return role if role in ("owner", "operator") else "not recorded"


def kit_root() -> Path:
    env_root = os.environ.get("CLAUDE_PLUGIN_ROOT")
    return Path(env_root) if env_root else HERE.parent.parent


def home_dir() -> Path | None:
    """$HOME resolved, or None when it can't be found (then no folder is treated as home)."""
    try:
        return Path.home().resolve()
    except (OSError, RuntimeError, KeyError):
        return None


def inside(path: Path, root: Path) -> bool:
    return path == root or root in path.parents


def has_entry(folder: Path, name: str) -> bool:
    """An entry called exactly `name` that is a folder or a link to one.

    is_dir() alone is no name test: APFS ignores case, so `KEEL-FACTORY` answers to
    `keel-factory`. The stat comes first, so a folder is listed only when it may match."""
    try:
        return (folder / name).is_dir() and name in os.listdir(folder)
    except OSError:
        return False


def marker(folder: Path, kit: Path, seen: list[Path]) -> KeelState | None:
    """What a `.keel` or `keel-factory` entry in `folder` gives. Each entry found goes into
    `seen` before anything else is read, so the guard can fail closed past that point."""
    if has_entry(folder, ".keel"):
        seen.append(folder / ".keel")
        return KeelState(folder, role_of(folder / ".keel"))
    if has_entry(folder, "keel-factory"):
        entry = folder / "keel-factory"
        seen.append(entry)
        try:
            # Only the master's own checkout is skipped; a copy of the kit or a link switches on.
            linked = entry.is_symlink() or entry.resolve() != kit or not master_checkout(kit)
        except (OSError, RuntimeError):
            linked = True
        if linked:
            return KeelState(folder, "kit")
    return None


def git_root(start: Path) -> Path | None:
    for folder in (start, *start.parents):
        if os.path.exists(folder / ".git"):  # a folder, or a worktree's or submodule's file
            return folder
    return None


def main_worktree(top: Path) -> Path | None:
    """The main checkout's root when `top` is a linked worktree; None otherwise.

    A worktree's `.git` file points at a gitdir holding `commondir`; a submodule's gitdir
    has none, so a submodule never reaches its superproject."""
    dot_git = top / ".git"
    try:
        if not dot_git.is_file():
            return None
        line = dot_git.read_text(encoding="utf-8").strip()
        if not line.startswith("gitdir:"):
            return None
        gitdir = (top / line[len("gitdir:"):].strip()).resolve()
        common = (gitdir / (gitdir / "commondir").read_text(encoding="utf-8").strip()).resolve()
    except (OSError, RuntimeError, ValueError):
        return None
    return common.parent if common.name == ".git" else None


def master_checkout(kit: Path) -> bool:
    """True when the kit root is the master's own git checkout: a `.git` folder, or a linked
    worktree. The documented copy leaves `.git` out, and a submodule's gitdir has no
    `commondir`, so both are copies that belong to the project holding them."""
    return (kit / ".git").is_dir() or main_worktree(kit) is not None


def keel_state(start: Path, seen: list[Path] | None = None) -> KeelState | None:
    """Where KEEL is switched on for `start`, by the rule in the module docstring. Every
    `.keel` or `keel-factory` entry met on the way is added to `seen` when it is given."""
    seen = [] if seen is None else seen
    try:
        folder = start.resolve()
        kit = kit_root().resolve()
    except (OSError, RuntimeError):
        return None
    if inside(folder, kit):
        return None
    home = home_dir()
    top = git_root(folder)
    chain = [folder] if top is None else [f for f in (folder, *folder.parents) if inside(f, top)]
    for candidate in chain:
        if candidate == home or candidate.parent == candidate:
            continue
        found = marker(candidate, kit, seen)
        if found is not None:
            return found
    main = main_worktree(top) if top is not None else None
    if main is not None and main != home and main.parent != main and not inside(main, kit):
        found = marker(main, kit, seen)
        if found is not None:
            return KeelState(found.root, found.role, layer_root=top)
    return None


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, ValueError):
        return ""


def instruction_files(root: Path, harness: str) -> list[tuple[str, str]]:
    """The project's own instruction files this harness loads at the start, as (name, text)."""
    if harness == "codex":
        return [("AGENTS.md", read_text(root / "AGENTS.md"))]
    files = [(name, read_text(root / name)) for name in CLAUDE_FILES]
    if any("@AGENTS.md" in text for _, text in files):
        files.append(("AGENTS.md", read_text(root / "AGENTS.md")))
    return files


def layer_import(folder: Path) -> bool:
    """True when `@keel-factory/CLAUDE.md`, imported from a file in `folder`, brings the layer."""
    return LAYER_MARK in read_text(folder / "keel-factory" / "CLAUDE.md")


def carries_layer(text: str, harness: str, folder: Path) -> bool:
    """The mark, or (Claude Code only) an import line that resolves from `folder` to the layer."""
    return LAYER_MARK in text or (harness != "codex" and IMPORT_LINE.search(text) is not None
                                  and layer_import(folder))


def layer_status(root: Path, harness: str) -> tuple[str, str]:
    """("v1.0", file) for KEEL's v1.0 copy, ("carries", "") when the layer is loaded, else ("", "")."""
    files = instruction_files(root, harness)
    for name, text in files:
        if V1_PHRASE in text:
            return "v1.0", name
    if any(carries_layer(text, harness, root / Path(name).parent) for name, text in files):
        return "carries", ""
    return "", ""


def upgrade_note(name: str, harness: str, root: Path) -> str:
    if harness != "codex" and layer_import(root / Path(name).parent):
        fix = "replace that copy with `@keel-factory/CLAUDE.md` or the v1.1 layer."
    else:
        layer = ("the v1.1 layer: the kit's CLAUDE.md, as one block that opens with its mark line"
                 if harness == "codex" else "v1.1's `CLAUDE.md`")
        fix = (f"delete KEEL's v1.0 text from that file (this hook then supplies the layer), "
               f"or replace it with {layer}.")
    return (f"This project's {name} is KEEL's v1.0 copy of the layer, so the v1.1 layer was not "
            f"added on top of it. Upgrade: {fix}")


def session_text(state: KeelState, kit: Path, harness: str = "claude") -> str:
    header = (
        f"KEEL is switched on in this project ({state.root}); role: {state.role}.\n"
        f"KEEL kit root for this session: {kit}. Wherever KEEL's documents say `keel-factory/`, "
        f"read it as that folder.\n"
        f"{ROLE_NEXT[state.role]}"
    )
    loads_from = state.layer_root or state.root
    status, name = layer_status(loads_from, harness)
    if status == "carries":
        return header
    if status == "v1.0":
        return f"{header}\n{upgrade_note(name, harness, loads_from)}"
    try:
        body = (kit / "CLAUDE.md").read_text(encoding="utf-8")
    except OSError:
        return header
    return f"{header}\n\n{body.strip()}"


def session(raw: str, harness: str = "claude") -> int:
    try:
        state = keel_state(project_start(read_payload(raw)))
        if state is None:
            return 0
        context = session_text(state, kit_root(), harness)
        sys.stdout.write(json.dumps({"hookSpecificOutput": {
            "hookEventName": "SessionStart", "additionalContext": context}}) + "\n")
    except Exception:  # context is a convenience; never break a session start over it
        return 0
    return 0


def patch_paths(text: str) -> list[str]:
    """Every path a patch's headers name, each line stripped first as Codex's parser does
    (str.strip removes at least what Rust's trim does). A header is caught wherever it
    sits, even where Codex would read the line as context, so the check is a superset.

    Raises ValueError on any other line that starts with `***` once stripped, so the guard
    blocks a patch it cannot read; the frame and a space-led line inside an Update File
    hunk, which Codex reads as file context, pass."""
    paths: list[str] = []
    updating = False
    for line in text.split("\n"):
        stripped = line.strip()
        header = next((h for h in PATCH_HEADERS if stripped.startswith(h)), None)
        if header is not None:
            paths.append(stripped[len(header):].strip())
            updating = header in PATCH_UPDATING
        elif (stripped.startswith("***") and stripped not in PATCH_FRAME
              and not stripped.startswith(PATCH_ENV_ID) and not (updating and line[:1] == " ")):
            raise ValueError(f"a patch line this hook cannot read: {stripped[:80]!r}")
    return paths


def guard_payloads(raw: str, payload: dict) -> list[str]:
    """What to hand the guard: one payload per patched file, or the call as it came.

    The call itself goes too when the patch names no file, or when a tool other than
    apply_patch sent text that starts as a patch: a shell runs that text as a command."""
    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict):
        return [raw]
    command = tool_input.get("command")
    if isinstance(command, list):
        command = " ".join(str(part) for part in command)
        payload = dict(payload, tool_input=dict(tool_input, command=command))
        raw = json.dumps(payload)
    if isinstance(command, str) and (payload.get("tool_name") == "apply_patch"
                                     or command.lstrip().startswith(PATCH_START)):
        paths = patch_paths(command)
        payloads = [json.dumps({"tool_name": "Write", "cwd": payload.get("cwd"),
                                "tool_input": {"file_path": path}}) for path in paths]
        if not paths or payload.get("tool_name") != "apply_patch":
            payloads.append(raw)
        return payloads
    return [raw]


def names_allowlist(path: str, cwd: str) -> bool:
    for candidate in (path, os.path.realpath(os.path.join(cwd, path))):
        p = candidate.replace("\\", "/").lower()
        if p == ALLOW_FILE or p.endswith("/" + ALLOW_FILE):
            return True
    return False


def touches_allowlist(one: str) -> bool:
    """True when one payload writes the guard's allowlist or runs a command naming it."""
    try:
        payload = json.loads(one)
    except ValueError:
        return False  # the guard fails closed on it
    if not isinstance(payload, dict) or not isinstance(payload.get("tool_input"), dict):
        return False
    tool_input = payload["tool_input"]
    cwd = payload.get("cwd") if isinstance(payload.get("cwd"), str) and payload.get("cwd") else os.getcwd()
    if payload.get("tool_name") in WRITE_TOOLS:
        for key in ("file_path", "notebook_path"):
            path = tool_input.get(key)
            if isinstance(path, str) and path and names_allowlist(path, cwd):
                return True
    command = tool_input.get("command")
    return isinstance(command, str) and "data-boundary-allow" in command.lower()


def load_guard():
    spec = importlib.util.spec_from_file_location("keel_data_boundary_guard", GUARD)
    if spec is None or spec.loader is None or not GUARD.is_file():
        raise FileNotFoundError(f"the data-boundary guard is missing at {GUARD}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def guard(raw: str, harness: str = "claude") -> int:
    always = os.environ.get("KEEL_GUARD", "").lower() == "always"
    seen: list[Path] = []  # the .keel or keel-factory entries met while deciding
    try:
        payload = read_payload(raw)
        if not always and keel_state(project_start(payload), seen) is None:
            return 0
        module = load_guard()
        for one in guard_payloads(raw, payload) if payload is not None else [raw]:
            if touches_allowlist(one):
                return block(ALLOWLIST_BLOCK)
            code, message = module.run(one)
            if code != 0:
                return block(message or "BLOCKED by data-boundary-guard (no reason given).")
        return 0
    except Exception as exc:  # fail closed past any marker, as the guard itself does
        if not always and not seen:
            return 0  # no .keel or keel-factory entry was met: KEEL is off here
        return block(
            f"BLOCKED by keel_hook guard: could not evaluate this tool call ({exc}).\n"
            "A guard that cannot read what it is guarding cannot vouch for it, so the call was "
            "blocked rather than allowed. Nothing was touched. Report this to the user rather "
            "than retrying the same access another way."
        )


def block(message: str) -> int:
    sys.stderr.write(message.rstrip("\n") + "\n")
    return 2


def parse_args(argv: list[str]) -> tuple[str, str] | None:
    """(command, harness) from `session|guard [--harness claude|codex]`; None for anything else."""
    args = argv[1:]
    harness = "claude"
    if len(args) == 3 and args[1] == "--harness" and args[2] in HARNESSES:
        harness = args[2]
    elif len(args) != 1:
        return None
    return (args[0], harness) if args[0] in ("session", "guard") else None


def main(argv: list[str]) -> int:
    parsed = parse_args(argv)
    if parsed is None:
        sys.stderr.write(USAGE)
        return 1
    command, harness = parsed
    raw = sys.stdin.buffer.read().decode("utf-8", errors="surrogateescape")
    return session(raw, harness) if command == "session" else guard(raw, harness)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
