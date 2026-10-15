#!/usr/bin/env python3
"""Link the KEEL kit into a project instead of copying it.

    python3 "$KEEL/harness/link_kit.py" /path/to/project
    python3 "$KEEL/harness/link_kit.py" /path/to/project --remove

Linking creates <project>/keel-factory/ as a real folder. It holds one symbolic link
for each item in this master folder (keel/, harness/, OPERATOR.md, CLAUDE.md, ...), and
a real, empty .ops/ folder for that project's own notes. Every path the framework names,
such as keel-factory/keel/..., resolves through the links, so the master stays the only
copy and an edit to it reaches every linked project at once. A project's notes stay in
the project, never in the shared master.

Removing deletes the links, never what they point at, and then keel-factory/ itself once
nothing else is in it. A non-empty .ops/ is left in place and named, because it holds
the mission's notes and debrief.

Both commands refuse rather than touch anything they did not make: a keel-factory/
that holds real files, such as an old full copy, is reported and left alone.
Standard library only. Exits 0 on success and 1 when it refuses.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

MASTER = Path(__file__).resolve().parent.parent
# .gitignore stays out: the kit must never bring its own ignore rules into a project, where
# they could make the guard treat keel-factory/.ops/ as gitignored and block the notes.
SKIP = {".git", ".gitignore", ".scratch", ".ops", "__pycache__", ".DS_Store"}
KIT = "keel-factory"
OPS = ".ops"


def is_ours(kit: Path) -> bool:
    """True when every entry in kit/ is a link into the master, or the .ops/ folder."""
    for entry in kit.iterdir():
        if entry.name == OPS and entry.is_dir() and not entry.is_symlink():
            continue
        if not entry.is_symlink() or MASTER not in entry.resolve().parents:
            return False
    return True


def link(project: Path) -> int:
    if not project.is_dir():
        print(f"refused: {project} is not a folder")
        return 1
    if project == MASTER or MASTER in project.parents or project in MASTER.parents:
        print(f"refused: {project} is the master folder, inside it, or above it")
        return 1
    kit = project / KIT
    if kit.is_symlink():
        print(f"refused: {kit} is itself a link; remove that link first (rm, no -r, no trailing slash)")
        return 1
    if kit.exists() and not is_ours(kit):
        print(f"refused: {kit} already exists and holds real files (an old full copy?); left untouched")
        return 1
    kit.mkdir(exist_ok=True)
    made = kept = 0
    for item in sorted(MASTER.iterdir()):
        if item.name in SKIP:
            continue
        dest = kit / item.name
        if dest.is_symlink() and dest.resolve() == item.resolve():
            kept += 1
            continue
        if dest.exists() or dest.is_symlink():
            print(f"refused: {dest} exists and is not a link to {item}; left untouched")
            return 1
        dest.symlink_to(item)
        made += 1
    (kit / OPS).mkdir(exist_ok=True)
    print(f"linked: {kit} -> {MASTER} ({made} new link(s), {kept} already in place, notes folder {kit / OPS})")
    return 0


def remove(project: Path) -> int:
    kit = project / KIT
    if kit.is_symlink():
        kit.unlink()
        print(f"removed the link {kit}; nothing it pointed at was touched")
        return 0
    if not kit.exists():
        print(f"nothing to remove: {kit} does not exist")
        return 0
    if not is_ours(kit):
        print(f"refused: {kit} holds real files besides {OPS}/ (an old full copy?); left untouched")
        return 1
    links = 0
    for entry in kit.iterdir():
        if entry.is_symlink():
            entry.unlink()
            links += 1
    ops = kit / OPS
    if ops.is_dir() and any(ops.iterdir()):
        print(f"removed {links} link(s); kept {ops} because it holds this project's notes and debrief")
        return 0
    if ops.is_dir():
        ops.rmdir()
    kit.rmdir()
    print(f"removed {links} link(s) and {kit}; the master was not touched")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("project", type=Path, help="the project or package folder")
    parser.add_argument("--remove", action="store_true", help="take the links out again")
    args = parser.parse_args()
    project = args.project.expanduser().resolve()
    return remove(project) if args.remove else link(project)


if __name__ == "__main__":
    sys.exit(main())
