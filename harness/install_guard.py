#!/usr/bin/env python3
"""Install KEEL's data-boundary guard machine-wide, once per computer.

    python3 "$KEEL/harness/install_guard.py"            # add the guard
    python3 "$KEEL/harness/install_guard.py" --remove   # take it out again

Merges one PreToolUse hook into ~/.claude/settings.json, keeping every other setting and
hook. The hook is self-disarming. It does nothing in any project without a
keel-factory/ folder, arms itself in every project that has one, and disarms when that
folder is gone (see ../OPERATOR.md). It matches the name keel-factory exactly, letter
case included: macOS ignores case in names by default, so [ -f ] alone would also arm in
a folder that holds only KEEL-FACTORY. The folder is only the switch. The hook then runs
this master's guard, by its absolute, shell-quoted path, never the project's own copy,
so a package cannot ship a guard that lets everything through. Run this script from the
master, or through a link to it: the hook runs the guard of the copy it was run from. If
the master moves, the hook disarms until this script is run again. Running it twice
changes nothing. An entry an older version wrote (v1.0's and the early v1.1 build's ran
the project's copy) or one from a master elsewhere is updated in place, and the script
says so.

Before writing, it saves the original file once as settings.json.before-keel-guard. It
prints only key names, never values, because a settings file can hold private values
such as API keys. If the file is not JSON shaped the way Claude Code writes it, it is
left untouched and the script exits 1. --settings points it at another file, which the
self-test uses.

Standard library only. Self-test: test_install_guard.py, beside this file.
"""

from __future__ import annotations

import argparse
import json
import shlex
import shutil
import sys
from pathlib import Path

MASTER = Path(__file__).resolve().parent.parent
GUARD = MASTER / "harness" / "hooks" / "data-boundary-guard.py"
COMMAND = ('ls -1 "$CLAUDE_PROJECT_DIR" 2>/dev/null | grep -qxF keel-factory || exit 0; '
           f'g={shlex.quote(str(GUARD))}; [ -f "$g" ] || exit 0; exec python3 "$g"')
MATCHER = "Read|Edit|Write|NotebookEdit|Glob|Grep|Bash"
# What every command KEEL wrote before this one held: it ran the project's copy.
OLD_MARKER = "$CLAUDE_PROJECT_DIR/keel-factory/harness/hooks/data-boundary-guard.py"
# What the current command holds, from any master: the exact-name switch and a guard path.
SWITCH = "grep -qxF keel-factory"
GUARD_END = "harness/hooks/data-boundary-guard.py"


def is_keel_command(command: object) -> bool:
    """A command this script, or an older version of it, wrote. A hand-wired guard is not."""
    command = str(command)
    return OLD_MARKER in command or (SWITCH in command and GUARD_END in command)


def is_keel(entry: dict) -> bool:
    return any(is_keel_command(hook.get("command", "")) for hook in entry.get("hooks", [])
               if isinstance(hook, dict))


def load(path: Path) -> dict | None:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return None
    if not isinstance(data, dict) or not isinstance(data.get("hooks", {}), dict) \
            or not isinstance(data.get("hooks", {}).get("PreToolUse", []), list):
        return None
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--remove", action="store_true", help="take KEEL's guard out again")
    parser.add_argument("--settings", type=Path, default=Path.home() / ".claude" / "settings.json")
    args = parser.parse_args()
    path = args.settings.expanduser()

    data = load(path)
    if data is None:
        print(f"refused: {path} is not shaped the way Claude Code writes it; left untouched")
        return 1
    pre = data.setdefault("hooks", {}).setdefault("PreToolUse", [])
    present = any(is_keel(entry) for entry in pre if isinstance(entry, dict))

    if args.remove:
        if not present:
            print(f"nothing to remove: KEEL's guard is not in {path}")
            return 0
        data["hooks"]["PreToolUse"] = [e for e in pre if not (isinstance(e, dict) and is_keel(e))]
        if not data["hooks"]["PreToolUse"]:
            del data["hooks"]["PreToolUse"]
        if not data["hooks"]:
            del data["hooks"]
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        print(f"removed KEEL's guard from {path}; every other setting kept")
        return 0

    if present:
        stale = [hook for entry in pre if isinstance(entry, dict) and is_keel(entry)
                 for hook in entry.get("hooks", []) if isinstance(hook, dict)
                 and is_keel_command(hook.get("command", "")) and hook.get("command") != COMMAND]
        if not stale:
            print(f"already installed in {path}; nothing changed")
            return 0
        for hook in stale:
            hook["command"] = COMMAND
        done = "updated KEEL's guard to the current command"
    else:
        pre.append({"matcher": MATCHER, "hooks": [{"type": "command", "command": COMMAND}]})
        done = "installed KEEL's guard"
    backup = path.with_name(path.name + ".before-keel-guard")
    if path.exists() and not backup.exists():
        shutil.copy2(path, backup)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"{done} in {path} (top-level keys: {', '.join(sorted(data))})")
    print(f"original saved as {backup}" if backup.exists() else "no earlier settings file to save")
    return 0


if __name__ == "__main__":
    sys.exit(main())
