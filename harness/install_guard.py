#!/usr/bin/env python3
"""Install KEEL's data-boundary guard machine-wide, once per computer.

    python3 "$KEEL/harness/install_guard.py"            # add the guard
    python3 "$KEEL/harness/install_guard.py" --remove   # take it out again

Merges one PreToolUse hook into ~/.claude/settings.json, keeping every other setting and
hook. The hook is self-disarming. It does nothing in any project without a
keel-factory/ folder, arms itself in every project that has one, and disarms when that
folder is gone (see ../OPERATOR.md). Running it twice changes nothing.

Before writing, it saves the original file once as settings.json.before-keel-guard. It
prints only key names, never values, because a settings file can hold private values
such as API keys. If the file is not JSON shaped the way Claude Code writes it, it is
left untouched and the script exits 1. --settings points it at another file, which the
self-test uses.

Standard library only.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

COMMAND = ('g="$CLAUDE_PROJECT_DIR/keel-factory/harness/hooks/data-boundary-guard.py"; '
           '[ -f "$g" ] || exit 0; exec python3 "$g"')
MATCHER = "Read|Edit|Write|NotebookEdit|Glob|Grep|Bash"
MARKER = "keel-factory/harness/hooks/data-boundary-guard.py"


def is_keel(entry: dict) -> bool:
    return any(MARKER in str(hook.get("command", "")) for hook in entry.get("hooks", []) if isinstance(hook, dict))


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
        print(f"already installed in {path}; nothing changed")
        return 0
    backup = path.with_name(path.name + ".before-keel-guard")
    if path.exists() and not backup.exists():
        shutil.copy2(path, backup)
    pre.append({"matcher": MATCHER, "hooks": [{"type": "command", "command": COMMAND}]})
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"installed KEEL's guard in {path} (top-level keys: {', '.join(sorted(data))})")
    print(f"original saved as {backup}" if backup.exists() else "no earlier settings file to save")
    return 0


if __name__ == "__main__":
    sys.exit(main())
