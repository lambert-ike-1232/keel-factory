#!/usr/bin/env python3
"""Check that the KEEL kit is well formed for both harnesses it ships to.

    python3 "$KEEL/harness/check_kit.py"            # the master this file sits in
    python3 "$KEEL/harness/check_kit.py" --root DIR # another copy

What `claude plugin validate` does not check, or checks differently on 2.1.170, plus the
numbers KEEL's v1.1 contract binds. The skill lists (OWN, BOARD, DOCS) come from the
kit's own harness/install_plugin.py and the always-on mark (LAYER_MARK) from its
harness/hooks/keel_hook.py, read with ast as top-level literals: no code in them runs,
and --root checks a copy against its own installer and hook. Each rule reports findings
under its own id:

  source            install_plugin.py holds OWN, BOARD and DOCS as top-level literal lists
                    of strings, and keel_hook.py holds LAYER_MARK as a literal string; a
                    file that is missing or does not parse is a finding, and the rules
                    that need its value are skipped
  manifest          .claude-plugin/plugin.json parses, is named keel, its version equals
                    VERSION, and every skills path holds skills
  hooks             the plugin's hooks file parses and every script it runs exists
  marketplace       .claude-plugin/marketplace.json offers the plugin from "./"
  skill             every skill on the plugin's paths: frontmatter parses, name equals
                    the folder, a description is present and at most 1,024 characters
                    (Codex's cap, stricter than Claude Code's 1,536); no name twice
  skill-set         the skill folders plugin.json loads are exactly the installer's OWN
                    plus keel/skills-board/claude/<name> for each BOARD name, and each
                    DOCS name has a Claude Code copy there (what --with-docs links)
  skill-path        in KEEL's own skills (the installer's OWN), a path into the kit is
                    written relative to the skill's folder (`../../framework/...`,
                    `../../../agents/...`) and resolves; a bare `framework/...` or
                    `agents/...` is a finding that names the fix, because a loaded skill
                    resolves paths from its own folder; a bare path to a file in the
                    skill's own folder (`agents/openai.yaml`) is fine
  listing-budget    names plus descriptions of the plugin's skills fit in 8,000
                    characters, Codex's default catalog budget
  codex             every skill install_plugin.py --codex links (OWN, plus
                    keel/skills-board/codex/<name> for BOARD and DOCS) exists and carries
                    agents/openai.yaml with a display name and an invocation policy
  agent             agents/*.md: name equals the file, description and tools present, no
                    field Claude Code ignores for plugin agents (hooks, mcpServers,
                    permissionMode)
  eval              evals/<case>/: a prompt.md or case.yaml, only documented prompt.md
                    keys, at least one grader of a documented type
  always-on         CLAUDE.md starts with the hook's LAYER_MARK and is at most 6,000
                    characters; the session hook's output for a KEEL project carries the
                    mark and is at most 7,000
  release           RELEASES.md has a section for the version in VERSION
  link              every relative Markdown link resolves (fences and code spans skipped;
                    .git/, .scratch/ and evals/results/ not walked)

States its scope, then every finding. Exits 0 when clean, 1 with findings. Reads files
and runs the session hook on a temporary folder; writes nothing in the kit. Standard
library only. Self-test: test_check_kit.py, beside this file.
"""

from __future__ import annotations

import argparse
import ast
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath

SOURCES = {"harness/install_plugin.py": ("OWN", "BOARD", "DOCS"),
           "harness/hooks/keel_hook.py": ("LAYER_MARK",)}
CLAUDE_MD_MAX = 6000
SESSION_MAX = 7000
DESC_MAX = 1024
LISTING_MAX = 8000
AGENT_IGNORED = {"hooks", "mcpServers", "permissionMode"}
PROMPT_KEYS = {"name", "description", "tags", "plugins", "runs", "expected_outcome", "model", "max_turns",
               "timeout_seconds", "allowed_tools", "append_system_prompt", "env", "schema_version"}
GRADER_TYPES = {"regex", "tool_used", "tool_order", "file_exists", "llm", "baseline"}
SKIP_WALK = {".git", ".scratch", "__pycache__", "node_modules"}
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")


class Findings:
    def __init__(self) -> None:
        self.items: list[tuple[str, str]] = []
        self.scope: dict[str, int] = {}

    def add(self, rule: str, message: str) -> None:
        self.items.append((rule, message))

    def count(self, what: str, n: int = 1) -> None:
        self.scope[what] = self.scope.get(what, 0) + n


def frontmatter(text: str) -> dict[str, str] | None:
    """Top-level keys of a Markdown file's YAML frontmatter, values joined onto one line."""
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    fields: dict[str, str] = {}
    key = None
    for line in text[3:end].splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if match:
            key = match.group(1)
            fields[key] = match.group(2).strip()
        elif key and line[:1] in (" ", "\t"):
            fields[key] = (fields[key] + " " + line.strip()).strip()
        else:
            return None
    for name, value in fields.items():
        if value[:1] in ("'", '"') and value[-1:] == value[:1] and len(value) > 1:
            fields[name] = value[1:-1]
        elif value in (">", ">-", "|", "|-"):
            fields[name] = ""
    return fields


def load_json(path: Path, rule: str, found: Findings):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        found.add(rule, f"{path.name} is missing")
    except ValueError as exc:
        found.add(rule, f"{path.name} is not valid JSON ({exc})")
    return None


def read_sources(root: Path, found: Findings) -> dict[str, object]:
    """OWN, BOARD, DOCS and LAYER_MARK from the kit's own files, read with ast: no code runs.

    The last top-level assignment of each name wins. A value that cannot be read stays None,
    and the rules that need it skip it; the source finding says why."""
    src: dict[str, object] = {name: None for names in SOURCES.values() for name in names}
    for rel, names in SOURCES.items():
        try:
            tree = ast.parse((root / rel).read_text(encoding="utf-8"), filename=rel)
        except OSError:
            found.add("source", f"{rel} is missing or unreadable")
            continue
        except (SyntaxError, ValueError) as exc:
            found.add("source", f"{rel} does not parse ({type(exc).__name__}: {exc})")
            continue
        nodes: dict[str, ast.expr] = {}
        for node in tree.body:
            if isinstance(node, ast.Assign):
                targets, value = node.targets, node.value
            elif isinstance(node, ast.AnnAssign) and node.value is not None:
                targets, value = [node.target], node.value
            else:
                continue
            for target in targets:
                if isinstance(target, ast.Name) and target.id in names:
                    nodes[target.id] = value
        for name in names:
            if name not in nodes:
                found.add("source", f"{rel} has no top-level {name}")
                continue
            try:
                value = ast.literal_eval(nodes[name])
            except (ValueError, TypeError, SyntaxError, RecursionError):
                value = None
            if name == "LAYER_MARK":
                kind, good = "non-empty string", isinstance(value, str) and bool(value)
            else:
                kind, good = "list of strings", isinstance(value, list) and all(isinstance(v, str) for v in value)
            if not good:
                found.add("source", f"{rel}: {name} is not a literal {kind}")
                continue
            src[name] = value
    return src


def skill_dirs(root: Path, rel: str) -> list[Path]:
    path = (root / rel).resolve()
    if (path / "SKILL.md").is_file():
        return [path]
    return sorted(p for p in path.iterdir() if (p / "SKILL.md").is_file()) if path.is_dir() else []


def check_manifest(root: Path, found: Findings) -> list[Path]:
    data = load_json(root / ".claude-plugin" / "plugin.json", "manifest", found)
    if not isinstance(data, dict):
        return []
    if data.get("name") != "keel":
        found.add("manifest", f"plugin name is {data.get('name')!r}, not 'keel'")
    try:
        version = (root / "VERSION").read_text(encoding="utf-8").strip()
    except OSError:
        version = None
        found.add("manifest", "VERSION is missing")
    if version is not None and data.get("version") != version:
        found.add("manifest", f"plugin.json version {data.get('version')!r} differs from VERSION {version!r}")
    skills: list[Path] = []
    paths = data.get("skills", [])
    for rel in [paths] if isinstance(paths, str) else paths:
        found.count("skill paths")
        dirs = skill_dirs(root, rel)
        if not dirs:
            found.add("manifest", f"skills path {rel} holds no skill")
        skills.extend(dirs)
    hooks_rel = data.get("hooks")
    if hooks_rel:
        hooks = load_json(root / hooks_rel, "hooks", found)
        for event, entries in (hooks or {}).get("hooks", {}).items() if isinstance(hooks, dict) else []:
            for entry in entries:
                for hook in entry.get("hooks", []):
                    found.count("hook commands")
                    for script in re.findall(r"\$\{CLAUDE_PLUGIN_ROOT\}/([\w./-]+\.py)", hook.get("command", "")):
                        if not (root / script).is_file():
                            found.add("hooks", f"{event} runs {script}, which does not exist")
    return skills


def check_marketplace(root: Path, found: Findings) -> None:
    data = load_json(root / ".claude-plugin" / "marketplace.json", "marketplace", found)
    if not isinstance(data, dict):
        return
    entries = [p for p in data.get("plugins", []) if isinstance(p, dict) and p.get("name") == "keel"]
    if not entries:
        found.add("marketplace", "no plugin entry named keel")
    elif entries[0].get("source") != "./":
        found.add("marketplace", f"keel's source is {entries[0].get('source')!r}, not './'")
    if not isinstance(data.get("owner"), dict) or not data["owner"].get("name"):
        found.add("marketplace", "owner.name is missing")


def check_skills(root: Path, skills: list[Path], found: Findings) -> None:
    seen: dict[str, Path] = {}
    listing = 0
    for folder in skills:
        found.count("skills")
        rel = folder.relative_to(root.resolve()) if root.resolve() in folder.parents else folder
        fields = frontmatter((folder / "SKILL.md").read_text(encoding="utf-8"))
        if fields is None:
            found.add("skill", f"{rel}/SKILL.md: frontmatter does not parse")
            continue
        name, desc = fields.get("name", ""), fields.get("description", "")
        if name != folder.name:
            found.add("skill", f"{rel}: name {name!r} differs from its folder {folder.name!r}")
        if not desc:
            found.add("skill", f"{rel}: no description")
        elif len(desc) > DESC_MAX:
            found.add("skill", f"{rel}: description is {len(desc)} characters, over {DESC_MAX}")
        if name in seen:
            found.add("skill", f"{rel}: name {name!r} is also used by {seen[name]}")
        seen[name] = rel
        listing += len(name) + len(desc) + 4
    found.scope["listing characters"] = listing
    if listing > LISTING_MAX:
        found.add("listing-budget", f"skill names and descriptions total {listing} characters, over {LISTING_MAX}")


def check_skill_set(root: Path, skills: list[Path], src: dict, found: Findings) -> None:
    """plugin.json and install_plugin.py name the same skills; each DOCS skill has its copy."""
    own, board, docs = src["OWN"], src["BOARD"], src["DOCS"]
    if own is None or board is None:
        return
    base = root.resolve()
    loaded = {f.relative_to(base).as_posix() if base in f.parents else str(f) for f in skills}
    listed = {PurePosixPath(rel).as_posix() for rel in own} | {f"keel/skills-board/claude/{b}" for b in board}
    for rel in sorted(loaded - listed):
        found.add("skill-set", f"plugin.json loads {rel}, which install_plugin.py's OWN and BOARD leave out")
    for rel in sorted(listed - loaded):
        found.add("skill-set", f"install_plugin.py lists {rel}, which plugin.json does not load")
    for name in docs or []:
        if not (root / "keel" / "skills-board" / "claude" / name / "SKILL.md").is_file():
            found.add("skill-set", f"install_plugin.py's DOCS lists {name}, which has no "
                                   f"keel/skills-board/claude/{name}/SKILL.md for --with-docs to link")


KEEL_PREFIXES = ("framework/", "templates/", "skills-board/", "capabilities/", "skills/")
ROOT_PREFIXES = ("agents/", "harness/")
KIT_PREFIXES = KEEL_PREFIXES + ROOT_PREFIXES


def check_skill_paths(root: Path, src: dict, found: Findings) -> None:
    for rel in src["OWN"] or []:
        folder = root / rel
        try:
            text = (folder / "SKILL.md").read_text(encoding="utf-8")
        except OSError:
            continue
        for token in re.findall(r"`([^`\s]+)`", text):
            path = token.split("#", 1)[0]
            if token.startswith("../"):
                found.count("skill paths checked")
                if not (folder / path).exists():
                    found.add("skill-path", f"{rel}/SKILL.md: {token} does not resolve from the skill's folder")
            elif token.startswith(KIT_PREFIXES):
                found.count("skill paths checked")
                if (folder / path).is_file():
                    continue  # the skill's own file, such as agents/openai.yaml
                if token.startswith(ROOT_PREFIXES):
                    base, where = root, "the kit root"
                else:
                    base, where = root / "keel", "the kit's keel/ folder"
                fix = os.path.relpath(base / path, folder) + token[len(path):]
                found.add("skill-path", f"{rel}/SKILL.md: {token} is relative to {where}, not the skill's; write {fix}")


def check_codex(root: Path, src: dict, found: Findings) -> None:
    codex = root / "keel" / "skills-board" / "codex"
    folders = [root / rel for rel in src["OWN"] or []]
    folders += [codex / name for name in src["BOARD"] or []]
    folders += [codex / name for name in src["DOCS"] or []]
    for folder in folders:
        found.count("codex skills")
        if not (folder / "SKILL.md").is_file():
            found.add("codex", f"{folder.relative_to(root)}: no SKILL.md")
            continue
        meta = folder / "agents" / "openai.yaml"
        try:
            text = meta.read_text(encoding="utf-8")
        except OSError:
            found.add("codex", f"{folder.relative_to(root)}: no agents/openai.yaml")
            continue
        if not re.search(r"^\s+display_name:\s*\S", text, re.M):
            found.add("codex", f"{meta.relative_to(root)}: no interface.display_name")
        if not re.search(r"^\s+allow_implicit_invocation:\s*(true|false)\s*$", text, re.M):
            found.add("codex", f"{meta.relative_to(root)}: no policy.allow_implicit_invocation")


def check_agents(root: Path, found: Findings) -> None:
    for path in sorted((root / "agents").glob("*.md")):
        found.count("agents")
        fields = frontmatter(path.read_text(encoding="utf-8"))
        rel = path.relative_to(root)
        if fields is None:
            found.add("agent", f"{rel}: frontmatter does not parse")
            continue
        if fields.get("name") != path.stem:
            found.add("agent", f"{rel}: name {fields.get('name')!r} differs from the file name")
        for key in ("description", "tools"):
            if not fields.get(key):
                found.add("agent", f"{rel}: no {key}")
        for key in sorted(AGENT_IGNORED & fields.keys()):
            found.add("agent", f"{rel}: {key} is ignored for plugin agents; enforce it another way")


def check_evals(root: Path, found: Findings) -> None:
    base = root / "evals"
    if not base.is_dir():
        found.add("eval", "evals/ is missing")
        return
    for case in sorted(p for p in base.iterdir() if p.is_dir() and p.name not in ("results", "mocks")):
        found.count("eval cases")
        prompt, yaml = case / "prompt.md", case / "case.yaml"
        if not prompt.is_file() and not yaml.is_file():
            found.add("eval", f"{case.name}: neither prompt.md nor case.yaml")
        if prompt.is_file():
            fields = frontmatter(prompt.read_text(encoding="utf-8"))
            if fields is None:
                found.add("eval", f"{case.name}/prompt.md: frontmatter does not parse")
            else:
                for key in sorted(fields.keys() - PROMPT_KEYS):
                    found.add("eval", f"{case.name}/prompt.md: unknown key {key!r}")
        graders = sorted((case / "graders").glob("*.md")) if (case / "graders").is_dir() else []
        if not graders and not (yaml.is_file() and "graders:" in yaml.read_text(encoding="utf-8")):
            found.add("eval", f"{case.name}: no grader")
        for grader in graders:
            fields = frontmatter(grader.read_text(encoding="utf-8")) or {}
            if fields.get("type") not in GRADER_TYPES:
                found.add("eval", f"{case.name}/graders/{grader.name}: type {fields.get('type')!r} is not a grader type")


def check_always_on(root: Path, src: dict, found: Findings) -> None:
    mark = src["LAYER_MARK"]
    try:
        text = (root / "CLAUDE.md").read_text(encoding="utf-8")
    except OSError:
        found.add("always-on", "CLAUDE.md is missing")
        return
    found.scope["CLAUDE.md characters"] = len(text)
    if mark is not None and not text.startswith(mark):
        found.add("always-on", f"CLAUDE.md does not start with the always-on mark keel_hook.py defines ({mark})")
    if len(text) > CLAUDE_MD_MAX:
        found.add("always-on", f"CLAUDE.md is {len(text)} characters, over {CLAUDE_MD_MAX}")
    hook = root / "harness" / "hooks" / "keel_hook.py"
    if not hook.is_file():
        found.add("always-on", "harness/hooks/keel_hook.py is missing")
        return
    with tempfile.TemporaryDirectory(prefix="keel-check-") as tmp:
        (Path(tmp) / ".keel").mkdir()
        (Path(tmp) / ".keel" / "keel.json").write_text('{"role": "owner"}', encoding="utf-8")
        env = {"PATH": "/usr/bin:/bin", "CLAUDE_PLUGIN_ROOT": str(root), "CLAUDE_PROJECT_DIR": tmp}
        result = subprocess.run([sys.executable, "-B", str(hook), "session"], input=b"{}",
                                capture_output=True, env=env, timeout=60)
    try:
        context = json.loads(result.stdout)["hookSpecificOutput"]["additionalContext"]
    except (ValueError, KeyError, TypeError):
        found.add("always-on", f"the session hook printed no context for a KEEL project (exit {result.returncode})")
        return
    found.scope["session characters"] = len(context)
    if len(context) > SESSION_MAX:
        found.add("always-on", f"the session hook injects {len(context)} characters, over {SESSION_MAX}")
    if mark is not None and mark not in context:
        found.add("always-on", "the session hook did not inject the always-on layer (no mark in its output)")


def check_release(root: Path, found: Findings) -> None:
    try:
        version = (root / "VERSION").read_text(encoding="utf-8").strip()
        releases = (root / "RELEASES.md").read_text(encoding="utf-8")
    except OSError as exc:
        found.add("release", f"cannot read VERSION or RELEASES.md ({exc})")
        return
    if not re.search(rf"^## v{re.escape(version)}\b", releases, re.M):
        found.add("release", f"RELEASES.md has no '## v{version}' section")


def check_links(root: Path, found: Findings) -> None:
    for md in sorted(root.rglob("*.md")):
        rel = md.relative_to(root)
        if any(part in SKIP_WALK for part in rel.parts) or rel.parts[:2] == ("evals", "results"):
            continue
        found.count("docs")
        fenced = False
        for number, line in enumerate(md.read_text(encoding="utf-8").splitlines(), 1):
            if line.lstrip().startswith(("```", "~~~")):
                fenced = not fenced
                continue
            if fenced:
                continue
            for target in LINK.findall(re.sub(r"`[^`]*`", "", line)):
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                path = target.split("#", 1)[0]
                if not path:
                    continue
                found.count("links")
                if not (md.parent / path).exists():
                    found.add("link", f"{rel}:{number} -> {target}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args()
    root = args.root.resolve()
    found = Findings()
    src = read_sources(root, found)
    skills = check_manifest(root, found)
    check_marketplace(root, found)
    check_skills(root, skills, found)
    check_skill_set(root, skills, src, found)
    check_skill_paths(root, src, found)
    check_codex(root, src, found)
    check_agents(root, found)
    check_evals(root, found)
    check_always_on(root, src, found)
    check_release(root, found)
    check_links(root, found)
    scope = ", ".join(f"{n} {what}" for what, n in found.scope.items())
    if not found.items:
        print(f"OK: {root} -- {scope}; no findings")
        return 0
    print(f"{len(found.items)} finding(s) on {root} ({scope}):\n")
    for rule, message in found.items:
        print(f"  [{rule}] {message}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
