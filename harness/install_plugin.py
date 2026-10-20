#!/usr/bin/env python3
"""Install KEEL once per machine, for Claude Code and Codex, as links to this master.

    python3 "$KEEL/harness/install_plugin.py"                  # Claude Code
    python3 "$KEEL/harness/install_plugin.py" --codex          # + Codex skills
    python3 "$KEEL/harness/install_plugin.py" --codex-hooks    # + Codex hooks (see below)
    python3 "$KEEL/harness/install_plugin.py" --with-docs      # + the four Diataxis skills
    python3 "$KEEL/harness/install_plugin.py" --remove [same flags]

Claude Code: makes ~/.claude/skills/keel a link to this master. Claude Code loads a
folder there that holds .claude-plugin/plugin.json as the plugin keel@skills-dir, in
place: an edit to the master reaches every project at the next session, with no copy and
no version bump. Its skills appear as keel:helm, keel:keel, ...; its hooks inject KEEL's
always-on layer and arm the data-boundary guard, but only in projects that hold .keel/ or
keel-factory/. An installed marketplace plugin of the same name (claude plugin install
keel@keel-factory) takes precedence over this link, so use one or the other.

Codex (--codex): links each KEEL skill into ~/.agents/skills/<name>, which Codex lists by
name and description and follows through the link. The vendored skills come from their
Codex copies (keel/skills-board/codex/). A name already taken there is skipped, never
overwritten. When it is one of KEEL's own six skills (helm above all), the script also
prints a warning: $keel:<name> will not work in Codex until that name is free.

Codex hooks (--codex-hooks): merges KEEL's two hooks into hooks.json in the Codex home
($CODEX_HOME when it is set, else ~/.codex), keeping every other hook. It saves the file
as it was before KEEL's hooks first went in, once, as hooks.json.before-keel; a re-run
that finds KEEL's hooks already there saves nothing. It prints the hooks.json path it
wrote. The commands pass --harness codex and use this master's absolute path,
shell-quoted so a path with spaces or a $ still reaches the hook; they disarm themselves
if the master moves. Codex runs a hook only after the user trusts it in /hooks; until
then KEEL's rule runs as policy alone.

--with-docs adds diataxis-{audit,manage,migrate,update}-docs, left out by default to keep
the skill list short (both harnesses cap it).

--remove takes out only what this script made: links that point into this master, and
hook entries that name keel_hook.py. It never deletes a folder or a file it did not make.
--claude-home, --agents-home and --codex-home retarget it, which the self-test uses.

A link the system will not make (on Windows, links need Developer Mode or an
administrator shell) is reported as refused, with the reason, and nothing more is linked.
A hooks.json, or its backup, that cannot be written is reported as refused, naming the
path. Exits 0 on success, 1 when it refuses. Standard library only. Self-test:
test_install_plugin.py, beside this file.
"""

from __future__ import annotations

import argparse
import json
import os
import shlex
import shutil
import sys
from pathlib import Path

MASTER = Path(__file__).resolve().parent.parent
HOOK = MASTER / "harness" / "hooks" / "keel_hook.py"
OWN = ["keel/skills/helm", "keel/skills/keel", "keel/skills/keel-prove", "keel/skills/crew",
       "keel/capabilities/deep-research", "keel/capabilities/reverse-engineering"]
BOARD = ["commit", "focused-implementation", "handoff", "orchestrate-implementation",
         "post-creation-audit", "resume-handoff", "spike", "task-board-init", "task-board-triage",
         "task-interview", "to-follow-on", "to-task"]
DOCS = ["diataxis-audit-docs", "diataxis-manage-docs", "diataxis-migrate-docs", "diataxis-update-docs"]
CODEX_MATCHER = "Bash|apply_patch"


def ours(path: Path) -> bool:
    """A link this script could have made: it points into the master."""
    if not path.is_symlink():
        return False
    target = path.resolve()
    return target == MASTER or MASTER in target.parents


def link(path: Path, target: Path, report: list[str], skip_taken: bool) -> bool:
    """Make path a link to target. False means refused."""
    if path.is_symlink() and path.resolve() == target.resolve():
        report.append(f"already linked: {path}")
        return True
    if path.exists() or path.is_symlink():
        if skip_taken:
            report.append(f"skipped {path.name}: the name is taken at {path}; left untouched")
            return True
        report.append(f"refused: {path} exists and is not this script's link to {target}; left untouched")
        return False
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.symlink_to(target)
    except OSError as err:
        report.append(f"refused: could not make the link {path} -> {target} ({err.strerror or err}). "
                      "On Windows, links need Developer Mode or an administrator shell.")
        return False
    report.append(f"linked {path} -> {target}")
    return True


def unlink(path: Path, report: list[str], strict: bool) -> bool:
    if ours(path):
        path.unlink()
        report.append(f"removed the link {path}; the master was not touched")
        return True
    if path.exists() or path.is_symlink():
        if strict:
            report.append(f"refused: {path} is not a link this script made; left untouched")
            return False
        report.append(f"left {path}: not this script's link")
    return True


def codex_skills(with_docs: bool) -> list[tuple[str, Path]]:
    skills = [(Path(rel).name, MASTER / rel) for rel in OWN]
    names = BOARD + (DOCS if with_docs else [])
    skills += [(name, MASTER / "keel" / "skills-board" / "codex" / name) for name in names]
    return skills


def default_codex_home() -> Path:
    """Where Codex keeps hooks.json: $CODEX_HOME when it is set, else ~/.codex."""
    env = os.environ.get("CODEX_HOME")
    return Path(env) if env else Path.home() / ".codex"


def hook_command(sub: str) -> str:
    """A Codex hook command: the path is shell-quoted, so $ or a space in it stays literal."""
    return f'g={shlex.quote(str(HOOK))}; [ -f "$g" ] || exit 0; exec python3 "$g" {sub} --harness codex'


def is_keel_entry(entry: object) -> bool:
    return isinstance(entry, dict) and any(
        "keel_hook.py" in str(h.get("command", "")) for h in entry.get("hooks", []) if isinstance(h, dict))


def write_refused(err: OSError, path: Path, report: list[str]) -> bool:
    """A write codex_hooks could not make: one line naming the file or folder that failed."""
    report.append(f"refused: could not write {err.filename or path} ({err.strerror or err})")
    return False


def codex_hooks(path: Path, remove: bool, report: list[str]) -> bool:
    data: dict = {}
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            data = None  # type: ignore[assignment]
        if not isinstance(data, dict) or not isinstance(data.get("hooks", {}), dict):
            report.append(f"refused: {path} is not hooks JSON this script can merge into; left untouched")
            return False
    hooks = data.setdefault("hooks", {})
    had_keel = False  # KEEL's hooks are already in: the file is not the user's original
    for event in ("SessionStart", "PreToolUse"):
        if not isinstance(hooks.get(event, []), list):
            report.append(f"refused: {path} has a {event} that is not a list; left untouched")
            return False
        had_keel = had_keel or any(is_keel_entry(e) for e in hooks.get(event, []))
        hooks[event] = [e for e in hooks.get(event, []) if not is_keel_entry(e)]
        if not hooks[event]:
            del hooks[event]
    if remove:
        if not hooks:
            del data["hooks"]
        try:
            if data:
                path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
            elif path.exists():
                path.write_text("{}\n", encoding="utf-8")
        except OSError as err:
            return write_refused(err, path, report)
        report.append(f"removed KEEL's hooks from {path}; every other hook kept")
        return True
    hooks.setdefault("SessionStart", []).append(
        {"hooks": [{"type": "command", "command": hook_command("session"),
                    "statusMessage": "KEEL: loading the always-on layer"}]})
    hooks.setdefault("PreToolUse", []).append(
        {"matcher": CODEX_MATCHER, "hooks": [{"type": "command", "command": hook_command("guard"),
                                               "statusMessage": "KEEL: checking the data boundary"}]})
    backup = path.with_name(path.name + ".before-keel")
    try:
        if path.exists() and not backup.exists() and not had_keel:
            shutil.copy2(path, backup)
            report.append(f"saved the original as {backup}")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    except OSError as err:
        return write_refused(err, path, report)
    report.append(f"wrote KEEL's SessionStart and PreToolUse hooks into {path}. Codex runs them only "
                  "after you trust them: open Codex, run /hooks, and approve both.")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--codex", action="store_true", help="also link the skills for Codex")
    parser.add_argument("--codex-hooks", action="store_true", help="also merge KEEL's hooks into Codex")
    parser.add_argument("--with-docs", action="store_true", help="also the four Diataxis docs skills")
    parser.add_argument("--remove", action="store_true", help="take out what this script made")
    parser.add_argument("--claude-home", type=Path, default=Path.home() / ".claude")
    parser.add_argument("--agents-home", type=Path, default=Path.home() / ".agents")
    parser.add_argument("--codex-home", type=Path, default=None,
                        help="default: $CODEX_HOME when it is set, else ~/.codex")
    args = parser.parse_args()
    claude_skills = args.claude_home.expanduser() / "skills"
    agents_skills = args.agents_home.expanduser() / "skills"
    report: list[str] = []
    ok = True

    only_codex_hooks = args.codex_hooks and not args.codex and not args.with_docs
    if not only_codex_hooks:
        if args.remove:
            ok &= unlink(claude_skills / "keel", report, strict=True)
            for name in DOCS:
                ok &= unlink(claude_skills / name, report, strict=False)
        else:
            ok &= link(claude_skills / "keel", MASTER, report, skip_taken=False)
            if ok and args.with_docs:
                for name in DOCS:
                    ok &= link(claude_skills / name, MASTER / "keel" / "skills-board" / "claude" / name,
                               report, skip_taken=True)
                    if not ok:
                        break
            installed = args.claude_home.expanduser() / "plugins" / "installed_plugins.json"
            if installed.is_file() and '"keel@' in installed.read_text(encoding="utf-8", errors="replace"):
                report.append("note: a marketplace install of keel is also present; it takes precedence "
                              "over the link. Keep one (claude plugin uninstall keel@keel-factory).")
    if ok and args.codex:
        own = {Path(rel).name for rel in OWN}
        for name, target in codex_skills(with_docs=True if args.remove else args.with_docs):
            if args.remove:
                ok &= unlink(agents_skills / name, report, strict=False)
            else:
                ok &= link(agents_skills / name, target, report, skip_taken=True)
                if name in own and report[-1].startswith("skipped "):
                    report.append(f"warning: KEEL's own skill {name} is not installed for Codex because "
                                  f"{agents_skills / name} is taken; $keel:{name} will not work until "
                                  "you move it aside and re-run.")
                if not ok:
                    break
    if ok and args.codex_hooks:
        codex_home = (args.codex_home or default_codex_home()).expanduser().resolve()
        ok &= codex_hooks(codex_home / "hooks.json", args.remove, report)

    print("\n".join(report))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
