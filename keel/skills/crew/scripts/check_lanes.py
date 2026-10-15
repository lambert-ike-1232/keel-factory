#!/usr/bin/env python3
"""Check a CREW lane plan: one writer per file, and every change inside its lane.

The lane plan is the `## Lanes` table in a plan task (see the crew skill). Two
checks; the second runs only when changed paths are given.

    scripts/check_lanes.py --plan <plan.md>
    <changed paths> | scripts/check_lanes.py --plan <plan.md> --lane <id> --changed -
    <changed paths> | scripts/check_lanes.py --plan <plan.md> --changed -

1. Plan check (always). Write sets must be pairwise disjoint: per file, per
   run, exactly one writer. A write entry is a repository-relative file, or a
   directory written with a trailing slash. Globs are refused, because overlap
   between globs cannot be decided by inspection, and a fence nobody can check
   is not a fence.
2. Fence check (--changed). With --lane, every changed path must sit inside
   that lane's write set; a path inside another lane's write set is reported
   with its owner. Without --lane, every changed path must sit inside some
   lane's write set. Feed it the real diff, never a worker's own account of
   what it touched -- with git, for example (-z keeps unusual paths unquoted):

       { git diff --name-only -z --no-renames <base>;
         git ls-files -z --others --exclude-standard; }

Exits 0 when clean, 1 when any finding is reported, and 2 when an input cannot
be read. States its scope -- lanes parsed, paths checked -- because a check that
examined nothing and a check that found nothing look the same from outside.
Reports findings; never edits a file. Standard library only.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

MODES = ("worktree", "shared", "read-only")
WRITE_MODES = ("worktree", "shared")
EMPTY_CELLS = {"", "-", "—", "–", "none", "n/a"}
GLOB_CHARS = set("*?[]{}")
HEADING = re.compile(r"^##\s+Lanes\s*$", re.IGNORECASE)
FENCE = re.compile(r"^\s*(```|~~~)")
SEPARATOR_CELL = re.compile(r"^:?-{3,}:?$")


class Lane:
    """One row of the lane table."""

    def __init__(self, lane_id: str, mode: str, writes: list[str], line: int) -> None:
        self.id = lane_id
        self.mode = mode
        self.writes = writes
        self.line = line

    def owns(self, path: str) -> bool:
        return any(covers(entry, path) for entry in self.writes)


def split_row(line: str) -> list[str]:
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|"):
        body = body[:-1]
    return [cell.strip() for cell in body.split("|")]


def unwrap(cell: str) -> str:
    return cell.strip().strip("`").strip()


def normalize(entry: str) -> tuple[str | None, str | None]:
    """Return (normalized entry, None), or (None, the problem with it)."""
    path = unwrap(entry)
    if path.startswith(("/", "~")) or re.match(r"^[A-Za-z]:", path):
        return None, "absolute path; write it relative to the repository root"
    if "\\" in path:
        return None, "backslash; use forward slashes"
    if GLOB_CHARS & set(path):
        return None, "glob; list the files, or a directory with a trailing slash"
    is_dir = path.endswith("/")
    while path.startswith("./"):
        path = path[2:]
    parts = path.rstrip("/").split("/")
    if any(part in ("", ".", "..") for part in parts):
        return None, "empty, '.' or '..' path segment"
    return "/".join(parts) + ("/" if is_dir else ""), None


def covers(entry: str, path: str) -> bool:
    """Whether a changed path falls inside one write entry."""
    if entry.endswith("/"):
        return path.startswith(entry) or path == entry[:-1]
    return path == entry


def overlaps(a: str, b: str) -> bool:
    """Whether two write entries could name the same file."""
    a_path, b_path = a.rstrip("/"), b.rstrip("/")
    if a_path == b_path:
        return True
    if a.endswith("/") and b_path.startswith(a):
        return True
    if b.endswith("/") and a_path.startswith(b):
        return True
    return False


def parse_plan(text: str, name: str) -> tuple[list[Lane], list[tuple[str, str, str]]]:
    """Parse the lane table and run the plan check."""
    lines = text.splitlines()
    start = None
    in_fence = False
    for index, line in enumerate(lines):
        if FENCE.match(line):
            in_fence = not in_fence
        elif not in_fence and HEADING.match(line):
            start = index
            break
    if start is None:
        return [], [(name, "lanes-missing", "no '## Lanes' section; the lane table lives in the plan task")]

    index = start + 1
    while index < len(lines) and not lines[index].strip():
        index += 1
    table = []
    while index < len(lines) and lines[index].lstrip().startswith("|"):
        table.append((index + 1, lines[index]))
        index += 1
    if len(table) < 2 or not all(SEPARATOR_CELL.match(cell) for cell in split_row(table[1][1])):
        return [], [(name, "lanes-missing",
                     "'## Lanes' has no table under it: a header row, a separator row, then one row per lane")]

    header = [unwrap(cell).lower() for cell in split_row(table[0][1])]
    absent = [column for column in ("lane", "writes", "mode") if column not in header]
    if absent:
        return [], [(name, "lanes-columns",
                     f"the lane table has no {', '.join(absent)} column; required: Lane, Writes, Mode")]
    position = {column: header.index(column) for column in ("lane", "writes", "mode")}

    lanes: list[Lane] = []
    findings: list[tuple[str, str, str]] = []
    first_seen: dict[str, int] = {}
    for line_no, raw in table[2:]:
        cells = split_row(raw)
        cell = {column: cells[k] if k < len(cells) else "" for column, k in position.items()}
        where = f"{name}:{line_no}"

        lane_id = unwrap(cell["lane"])
        if not lane_id:
            findings.append((where, "lane-id-missing", "a lane row has no Lane id"))
            continue
        if lane_id in first_seen:
            findings.append((where, "lane-id-duplicate",
                             f"lane '{lane_id}' is already declared on line {first_seen[lane_id]}"))
            continue
        first_seen[lane_id] = line_no

        mode = unwrap(cell["mode"]).lower()
        if mode not in MODES:
            findings.append((where, "mode-invalid",
                             f"lane '{lane_id}' has mode '{mode}'; use one of: {', '.join(MODES)}"))

        writes: list[str] = []
        invalid = False
        if unwrap(cell["writes"]).lower() not in EMPTY_CELLS:
            for entry in cell["writes"].split(","):
                if not unwrap(entry):
                    continue
                normalized, problem = normalize(entry)
                if problem:
                    invalid = True
                    findings.append((where, "write-path-invalid",
                                     f"lane '{lane_id}' write entry {unwrap(entry)!r}: {problem}"))
                else:
                    writes.append(normalized)

        if mode == "read-only" and writes:
            findings.append((where, "read-only-writes",
                             f"lane '{lane_id}' is read-only but lists writes: {', '.join(writes)}"))
        if mode in WRITE_MODES and not writes and not invalid:
            findings.append((where, "write-lane-empty",
                             f"lane '{lane_id}' is a {mode} lane that owns no paths; "
                             "give it a write set or make it read-only"))
        lanes.append(Lane(lane_id, mode, writes, line_no))

    if not lanes and not findings:
        findings.append((name, "lanes-missing", "the lane table has no rows"))

    for i, first in enumerate(lanes):
        for second in lanes[i + 1:]:
            for a in first.writes:
                for b in second.writes:
                    if overlaps(a, b):
                        findings.append((f"{name}:{second.line}", "lane-overlap",
                                         f"lanes '{first.id}' ({a}) and '{second.id}' ({b}) overlap; "
                                         "one writer per file -- put the work in one lane, or split the path"))
    return lanes, findings


def parse_changed(data: str) -> list[str]:
    """Changed paths, NUL-separated (git -z) or one per line; deduplicated."""
    items = data.split("\0") if "\0" in data else [item.strip() for item in data.splitlines()]
    paths: list[str] = []
    seen: set[str] = set()
    for item in items:
        path = item
        while path.startswith("./"):
            path = path[2:]
        if path and path not in seen:
            seen.add(path)
            paths.append(path)
    return paths


def fence(lanes: list[Lane], changed: list[str], lane_id: str | None) -> list[tuple[str, str, str]]:
    """Run the fence check over the changed paths."""
    findings: list[tuple[str, str, str]] = []
    if lane_id is None:
        for path in changed:
            if not any(lane.owns(path) for lane in lanes):
                findings.append((path, "unowned-write", "changed, but no lane owns this path"))
        return findings

    lane = next((candidate for candidate in lanes if candidate.id == lane_id), None)
    if lane is None:
        known = ", ".join(candidate.id for candidate in lanes)
        return [("--lane", "lane-unknown", f"no lane '{lane_id}' in the plan (lanes: {known})")]
    for path in changed:
        if lane.owns(path):
            continue
        owner = next((other.id for other in lanes if other is not lane and other.owns(path)), None)
        if owner is not None:
            findings.append((path, "foreign-lane-write", f"lane '{lane.id}' changed a path that lane '{owner}' owns"))
        else:
            findings.append((path, "out-of-lane-write", f"lane '{lane.id}' changed a path outside its write set"))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--plan", type=Path, required=True, help="the plan task holding the ## Lanes table")
    parser.add_argument("--changed", metavar="FILE",
                        help="changed paths, one per line or NUL-separated; '-' reads stdin")
    parser.add_argument("--lane", help="check the changed paths against this one lane")
    args = parser.parse_args()
    if args.lane is not None and args.changed is None:
        parser.error("--lane needs --changed")

    try:
        text = args.plan.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        print(f"cannot read the plan: {exc}", file=sys.stderr)
        return 2
    lanes, findings = parse_plan(text, args.plan.name)

    scope = f"{len(lanes)} lane(s)"
    notes: list[str] = []
    if args.changed is not None:
        try:
            data = sys.stdin.read() if args.changed == "-" else Path(args.changed).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            print(f"cannot read the changed paths: {exc}", file=sys.stderr)
            return 2
        changed = parse_changed(data)
        if findings:
            notes.append("fence check skipped: a fence drawn from a plan with findings proves nothing")
        else:
            findings.extend(fence(lanes, changed, args.lane))
            target = f"lane '{args.lane}'" if args.lane is not None else "every lane"
            scope += f", {len(changed)} changed path(s) checked against {target}"
            if not changed:
                notes.append("no changed paths were given, so the fence had nothing to check; "
                             "if changes were expected, check the diff base")

    if findings:
        print(f"{len(findings)} finding(s) on {args.plan} ({scope}):\n")
        for where, rule, message in findings:
            print(f"  {where}: [{rule}] {message}")
        for note in notes:
            print(f"\n{note}")
        print("\nOne writer per file. Fix the plan, or send the change back to the lane that owns it.")
        return 1
    print(f"OK: {args.plan} -- {scope}, no findings")
    for note in notes:
        print(f"note: {note}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
