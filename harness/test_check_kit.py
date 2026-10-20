#!/usr/bin/env python3
"""Self-test for check_kit.py: a clean copy of the kit passes, and each rule catches its break.

    python3 harness/test_check_kit.py

Every case copies the kit into a temporary folder, breaks one thing, and runs the check
there; the master is only read. Standard library only.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

CHECK = Path(__file__).resolve().parent / "check_kit.py"
MASTER = CHECK.parent.parent


class Kit(unittest.TestCase):
    def setUp(self):
        tmp = Path(os.path.realpath(tempfile.mkdtemp(prefix="keel-check-test-")))
        self.addCleanup(shutil.rmtree, tmp, ignore_errors=True)
        self.root = tmp / "kit"
        shutil.copytree(MASTER, self.root, symlinks=True,
                        ignore=shutil.ignore_patterns(".git", ".scratch", "__pycache__", "results", ".DS_Store"))
        version = (self.root / "VERSION").read_text().strip()
        releases = self.root / "RELEASES.md"
        if not re.search(rf"^## v{re.escape(version)}\b", releases.read_text(), re.M):
            releases.write_text(releases.read_text() + f"\n## v{version} — test\n")

    def check(self):
        result = subprocess.run([sys.executable, "-B", str(CHECK), "--root", str(self.root)],
                                capture_output=True, text=True, timeout=120)
        return result.returncode, result.stdout

    def assertCaught(self, rule: str, fragment: str = ""):
        code, out = self.check()
        self.assertEqual(code, 1, out)
        lines = [line for line in out.splitlines() if line.strip().startswith(f"[{rule}]")]
        self.assertTrue(lines, f"no [{rule}] finding in:\n{out}")
        if fragment:
            self.assertTrue(any(fragment in line for line in lines), out)

    def findings(self) -> list[str]:
        """One run that must find something; every finding line it prints."""
        code, out = self.check()
        self.assertEqual(code, 1, out)
        return [line.strip() for line in out.splitlines() if line.strip().startswith("[")]

    def assertHas(self, found: list[str], rule: str, *fragments: str):
        hits = [line for line in found if line.startswith(f"[{rule}]") and all(f in line for f in fragments)]
        self.assertTrue(hits, f"no [{rule}] finding with {fragments} in:\n" + "\n".join(found))

    def assertLacks(self, found: list[str], rule: str, fragment: str = ""):
        hits = [line for line in found if line.startswith(f"[{rule}]") and fragment in line]
        self.assertFalse(hits, "\n".join(found))

    def assertNotCaught(self, rule: str, fragment: str = ""):
        code, out = self.check()
        self.assertTrue(out.startswith("OK:") or " finding(s) on " in out, f"the check did not finish:\n{out}")
        lines = [line for line in out.splitlines() if line.strip().startswith(f"[{rule}]") and fragment in line]
        self.assertFalse(lines, out)

    def sub(self, rel: str, pattern: str, repl: str):
        """A regex edit of one file in the copy that must match exactly once."""
        path = self.root / rel
        text, n = re.subn(pattern, repl, path.read_text(), flags=re.M)
        self.assertEqual(n, 1, f"test anchor {pattern!r} matched {n} times in {rel}")
        path.write_text(text)

    def append(self, rel: str, text: str):
        path = self.root / rel
        path.write_text(path.read_text() + text)

    def edit(self, rel: str, old: str, new: str):
        path = self.root / rel
        text = path.read_text()
        self.assertIn(old, text, f"test anchor missing in {rel}")
        path.write_text(text.replace(old, new, 1))

    def manifest(self, change):
        path = self.root / ".claude-plugin" / "plugin.json"
        data = json.loads(path.read_text())
        change(data)
        path.write_text(json.dumps(data))


class Clean(Kit):
    def test_clean_copy_passes_and_states_scope(self):
        code, out = self.check()
        self.assertEqual(code, 0, out)
        self.assertIn("18 skills", out)
        self.assertIn("links", out)


class Breaks(Kit):
    def test_version_mismatch(self):
        self.manifest(lambda d: d.update(version="9.9.9"))
        self.assertCaught("manifest", "differs from VERSION")

    def test_skill_path_with_no_skill(self):
        (self.root / "empty").mkdir()
        self.manifest(lambda d: d["skills"].append("./empty/"))
        self.assertCaught("manifest", "holds no skill")

    def test_hook_script_missing(self):
        (self.root / "harness" / "hooks" / "keel_hook.py").unlink()
        self.assertCaught("hooks", "does not exist")

    def test_marketplace_source_moved(self):
        path = self.root / ".claude-plugin" / "marketplace.json"
        data = json.loads(path.read_text())
        data["plugins"][0]["source"] = "./elsewhere"
        path.write_text(json.dumps(data))
        self.assertCaught("marketplace")

    def test_skill_name_differs_from_folder(self):
        self.edit("keel/skills/crew/SKILL.md", "name: crew", "name: crewe")
        self.assertCaught("skill", "differs from its folder")

    def test_skill_description_missing(self):
        path = self.root / "keel" / "skills" / "crew" / "SKILL.md"
        text = path.read_text()
        path.write_text(re.sub(r"^description:.*$", "description:", text, count=1, flags=re.M))
        self.assertCaught("skill", "no description")

    def test_skill_description_too_long(self):
        path = self.root / "keel" / "skills" / "crew" / "SKILL.md"
        text = path.read_text()
        path.write_text(re.sub(r"^(description:.*)$", lambda m: m.group(1) + " x" * 600, text, count=1, flags=re.M))
        self.assertCaught("skill", "over 1024")

    def test_duplicate_skill_name(self):
        shutil.copytree(self.root / "keel" / "skills" / "crew", self.root / "keel" / "capabilities" / "crew")
        self.assertCaught("skill", "also used by")

    def test_listing_over_budget(self):
        extra = self.root / "keel" / "capabilities"
        for n in range(2):
            folder = extra / f"padding{n}"
            folder.mkdir()
            (folder / "SKILL.md").write_text(f"---\nname: padding{n}\ndescription: {'y' * 1000}\n---\nbody\n")
        self.assertCaught("listing-budget")

    def test_skill_path_relative_to_kit_folder(self):
        path = self.root / "keel" / "skills" / "keel" / "SKILL.md"
        path.write_text(path.read_text() + "\nSee `framework/PHASES.md`.\n")
        self.assertCaught("skill-path", "not the skill's")

    def test_skill_path_that_does_not_resolve(self):
        path = self.root / "keel" / "skills" / "helm" / "SKILL.md"
        path.write_text(path.read_text() + "\nSee `../../framework/NOPE.md`.\n")
        self.assertCaught("skill-path", "does not resolve")

    def test_codex_metadata_missing(self):
        (self.root / "keel" / "skills" / "helm" / "agents" / "openai.yaml").unlink()
        self.assertCaught("codex", "no agents/openai.yaml")

    def test_agent_with_ignored_field(self):
        self.edit("agents/prove-gate.md", "tools: Read", "permissionMode: plan\ntools: Read")
        self.assertCaught("agent", "permissionMode")

    def test_agent_name_differs_from_file(self):
        self.edit("agents/prove-spec.md", "name: prove-spec", "name: spec")
        self.assertCaught("agent", "differs from the file name")

    def test_eval_unknown_prompt_key(self):
        prompt = next((self.root / "evals").glob("*/prompt.md"))
        text = prompt.read_text()
        prompt.write_text(text.replace("---\n", "---\nbogus_key: 1\n", 1))
        self.assertCaught("eval", "unknown key 'bogus_key'")

    def test_eval_bad_grader_type(self):
        grader = next((self.root / "evals").glob("*/graders/*.md"))
        text = grader.read_text()
        grader.write_text(re.sub(r"^type:.*$", "type: vibes", text, count=1, flags=re.M))
        self.assertCaught("eval", "not a grader type")

    def test_always_on_mark_missing(self):
        path = self.root / "CLAUDE.md"
        path.write_text(path.read_text().replace("<!-- KEEL always-on layer -->\n", "", 1))
        self.assertCaught("always-on", "mark")

    def test_always_on_too_long(self):
        path = self.root / "CLAUDE.md"
        path.write_text(path.read_text() + "\npadding " * 900)
        self.assertCaught("always-on", "over 6000")

    def test_release_section_missing(self):
        (self.root / "VERSION").write_text("9.9.9\n")
        self.manifest(lambda d: d.update(version="9.9.9"))
        self.assertCaught("release", "v9.9.9")

    def test_broken_link(self):
        path = self.root / "README.md"
        path.write_text(path.read_text() + "\n[gone](no/such/file.md)\n")
        self.assertCaught("link", "no/such/file.md")


INSTALLER = "harness/install_plugin.py"
HOOK = "harness/hooks/keel_hook.py"


class Drift(Kit):
    """The skill lists and the mark come from the copy's own installer and hook, read with
    ast and never run; each drift between them and plugin.json, or a path the rules missed,
    is a finding."""

    def test_installer_lists_a_ghost_skill(self):
        self.sub(INSTALLER, r"^BOARD = \[", 'BOARD = ["ghost", ')
        found = self.findings()
        self.assertHas(found, "skill-set", "install_plugin.py lists keel/skills-board/claude/ghost", "does not load")
        self.assertHas(found, "codex", "keel/skills-board/codex/ghost: no SKILL.md")

    def test_plugin_drops_a_skill(self):
        self.manifest(lambda d: d["skills"].remove("./keel/skills-board/claude/to-task"))
        self.assertHas(self.findings(), "skill-set", "lists keel/skills-board/claude/to-task", "does not load")

    def test_installer_drops_a_skill(self):
        self.sub(INSTALLER, r'"to-task",?', "")
        self.assertHas(self.findings(), "skill-set", "loads keel/skills-board/claude/to-task", "leave out")

    def test_docs_skill_without_its_claude_copy(self):
        (self.root / "keel" / "skills-board" / "claude" / "diataxis-audit-docs" / "SKILL.md").unlink()
        self.assertHas(self.findings(), "skill-set", "DOCS lists diataxis-audit-docs",
                       "keel/skills-board/claude/diataxis-audit-docs/SKILL.md")

    def test_docs_codex_metadata_missing(self):
        (self.root / "keel" / "skills-board" / "codex" / "diataxis-audit-docs" / "agents" / "openai.yaml").unlink()
        self.assertHas(self.findings(), "codex", "keel/skills-board/codex/diataxis-audit-docs: no agents/openai.yaml")

    def test_layer_mark_comes_from_the_hook(self):
        # Annotated on purpose: an annotated top-level assignment counts as well.
        self.sub(HOOK, r"^LAYER_MARK = .*$", 'LAYER_MARK: str = "<!-- KEEL layer v2 -->"')
        self.assertHas(self.findings(), "always-on", "does not start with the always-on mark")

    def test_bare_kit_paths_name_their_fix(self):
        self.append("keel/skills/keel/SKILL.md",
                    "\nSee `agents/prove-gate.md`, `harness/check_kit.py` and `framework/PHASES.md#rules`.\n")
        found = self.findings()
        self.assertHas(found, "skill-path", "keel/skills/keel/SKILL.md: agents/prove-gate.md is relative to "
                       "the kit root, not the skill's; write ../../../agents/prove-gate.md")
        self.assertHas(found, "skill-path", "harness/check_kit.py is relative to the kit root",
                       "write ../../../harness/check_kit.py")
        self.assertHas(found, "skill-path", "framework/PHASES.md#rules is relative to the kit's keel/ folder",
                       "write ../../framework/PHASES.md#rules")

    def test_skill_own_file_passes(self):
        self.append("keel/skills/helm/SKILL.md", "\nIts Codex card is `agents/openai.yaml`.\n")
        self.assertNotCaught("skill-path", "agents/openai.yaml")

    def test_installer_missing(self):
        (self.root / INSTALLER).unlink()
        found = self.findings()
        self.assertHas(found, "source", f"{INSTALLER} is missing")
        self.assertLacks(found, "skill-set")

    def test_hook_does_not_parse(self):
        self.append(HOOK, "\ndef broken(:\n")
        self.assertHas(self.findings(), "source", f"{HOOK} does not parse")

    def test_installer_list_renamed(self):
        self.sub(INSTALLER, r"^DOCS = ", "DOCS_SKILLS = ")
        self.assertHas(self.findings(), "source", f"{INSTALLER} has no top-level DOCS")

    def test_installer_list_not_a_literal(self):
        self.sub(INSTALLER, r"^DOCS = ", "DOCS = 2 * ")
        self.assertHas(self.findings(), "source", "DOCS is not a literal list of strings")

    def test_sources_are_read_not_run(self):
        self.append(INSTALLER, '\nimport pathlib; pathlib.Path(__file__).with_name("RAN").write_text("ran")\n')
        self.assertNotCaught("source")
        self.assertFalse((self.root / "harness" / "RAN").exists(), "check_kit ran the copy's installer")


if __name__ == "__main__":
    unittest.main(verbosity=1)
