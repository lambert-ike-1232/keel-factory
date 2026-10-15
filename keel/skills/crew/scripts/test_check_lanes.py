#!/usr/bin/env python3
"""Self-test for check_lanes.py -- proves each check can fail, not only pass.

    python3 scripts/test_check_lanes.py

Standard library only. The round trip through a real git diff is skipped when
git is absent, and unittest reports it as skipped -- a skipped test is not a
passed one.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import check_lanes  # noqa: E402

SCRIPT = HERE / "check_lanes.py"
HEADER = "| Lane | Owner | Tasks | Writes | Mode |\n| --- | --- | --- | --- | --- |\n"


def plan(*rows: str) -> str:
    return "# Task: plan\n\n## Lanes\n\n" + HEADER + "".join(row + "\n" for row in rows)


def rules(findings) -> list[str]:
    return [rule for _, rule, _ in findings]


CLEAN = plan(
    "| api | worker-api | add-endpoint | `src/api/`, `tests/api/` | worktree |",
    "| docs | worker-docs | update-guide | `docs/guide.md` | shared |",
    "| survey | researcher | — | — | read-only |",
)


class PlanCheck(unittest.TestCase):
    def check(self, *rows: str) -> list[str]:
        return rules(check_lanes.parse_plan(plan(*rows), "plan.md")[1])

    def test_disjoint_lanes_are_clean(self):
        lanes, findings = check_lanes.parse_plan(CLEAN, "plan.md")
        self.assertEqual(findings, [])
        self.assertEqual([lane.id for lane in lanes], ["api", "docs", "survey"])

    def test_directory_overlapping_a_file_is_caught(self):
        self.assertEqual(self.check("| a | w | t | `src/` | worktree |",
                                    "| b | w | t | `src/api/handler.py` | shared |"), ["lane-overlap"])

    def test_same_file_in_two_lanes_is_caught(self):
        self.assertEqual(self.check("| a | w | t | `config.py` | shared |",
                                    "| b | w | t | `./config.py` | shared |"), ["lane-overlap"])

    def test_nested_directories_are_caught(self):
        self.assertEqual(self.check("| a | w | t | `src/api/` | shared |",
                                    "| b | w | t | `src/` | shared |"), ["lane-overlap"])

    def test_lookalike_paths_do_not_overlap(self):
        self.assertEqual(self.check("| a | w | t | `src/a.py`, `src/ap/` | shared |",
                                    "| b | w | t | `src/a.py.bak`, `src/api.py` | shared |"), [])

    def test_globs_absolute_and_parent_paths_are_refused(self):
        self.assertEqual(self.check("| a | w | t | `src/*.py`, `/etc/hosts`, `../x` | shared |"),
                         ["write-path-invalid"] * 3)

    def test_read_only_lane_with_writes(self):
        self.assertEqual(self.check("| a | w | t | `notes.md` | read-only |"), ["read-only-writes"])

    def test_write_lane_with_no_writes(self):
        self.assertEqual(self.check("| a | w | t | — | worktree |"), ["write-lane-empty"])

    def test_invalid_mode(self):
        self.assertEqual(self.check("| a | w | t | `x.py` | parallel |"), ["mode-invalid"])

    def test_duplicate_lane_id(self):
        self.assertEqual(self.check("| a | w | t | `x.py` | shared |",
                                    "| a | w | t | `y.py` | shared |"), ["lane-id-duplicate"])

    def test_missing_section_ignores_a_heading_inside_a_fence(self):
        text = "# Task: plan\n\n```\n## Lanes\n\n" + HEADER + "| a | w | t | `x.py` | shared |\n```\n"
        self.assertEqual(rules(check_lanes.parse_plan(text, "plan.md")[1]), ["lanes-missing"])

    def test_missing_column(self):
        text = "## Lanes\n\n| Lane | Writes |\n| --- | --- |\n| a | `x.py` |\n"
        self.assertEqual(rules(check_lanes.parse_plan(text, "plan.md")[1]), ["lanes-columns"])


class FenceCheck(unittest.TestCase):
    def setUp(self):
        self.lanes, findings = check_lanes.parse_plan(CLEAN, "plan.md")
        self.assertEqual(findings, [])

    def fence(self, changed: list[str], lane: str | None) -> list[str]:
        return rules(check_lanes.fence(self.lanes, changed, lane))

    def test_changes_inside_the_lane_pass(self):
        self.assertEqual(self.fence(["src/api/routes.py", "tests/api/test_routes.py"], "api"), [])

    def test_change_in_another_lanes_path_names_the_owner(self):
        findings = check_lanes.fence(self.lanes, ["docs/guide.md"], "api")
        self.assertEqual(rules(findings), ["foreign-lane-write"])
        self.assertIn("'docs'", findings[0][2])

    def test_change_outside_every_lane(self):
        self.assertEqual(self.fence(["README.md"], "api"), ["out-of-lane-write"])

    def test_read_only_lane_may_not_change_anything(self):
        self.assertEqual(self.fence(["notes.md"], "survey"), ["out-of-lane-write"])

    def test_shared_tree_unowned_change(self):
        self.assertEqual(self.fence(["src/api/x.py", "docs/guide.md", "setup.cfg"], None), ["unowned-write"])

    def test_unknown_lane(self):
        self.assertEqual(self.fence(["src/api/x.py"], "nope"), ["lane-unknown"])

    def test_changed_list_parsing(self):
        self.assertEqual(check_lanes.parse_changed("./a.py\n\nb.py\na.py\n"), ["a.py", "b.py"])
        self.assertEqual(check_lanes.parse_changed("a b.py\0c.py\0"), ["a b.py", "c.py"])


class CommandLine(unittest.TestCase):
    def run_cli(self, *args: str, stdin: str = "") -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, str(SCRIPT), *args], input=stdin, capture_output=True, text=True)

    def test_exit_codes_and_reported_scope(self):
        with tempfile.TemporaryDirectory() as tmp:
            good = Path(tmp, "good.md")
            good.write_text(CLEAN, encoding="utf-8")
            bad = Path(tmp, "bad.md")
            bad.write_text(plan("| a | w | t | `src/` | shared |", "| b | w | t | `src/x.py` | shared |"),
                           encoding="utf-8")

            self.assertEqual(self.run_cli("--plan", str(good)).returncode, 0)

            result = self.run_cli("--plan", str(bad))
            self.assertEqual(result.returncode, 1)
            self.assertIn("[lane-overlap]", result.stdout)

            self.assertEqual(self.run_cli("--plan", str(Path(tmp, "missing.md"))).returncode, 2)

            result = self.run_cli("--plan", str(good), "--lane", "api", "--changed", "-", stdin="docs/guide.md\n")
            self.assertEqual(result.returncode, 1)
            self.assertIn("[foreign-lane-write]", result.stdout)

            result = self.run_cli("--plan", str(bad), "--lane", "a", "--changed", "-", stdin="src/x.py\n")
            self.assertEqual(result.returncode, 1)
            self.assertIn("fence check skipped", result.stdout)

            result = self.run_cli("--plan", str(good), "--lane", "api", "--changed", "-", stdin="")
            self.assertEqual(result.returncode, 0)
            self.assertIn("0 changed path(s)", result.stdout)
            self.assertIn("nothing to check", result.stdout)


@unittest.skipUnless(shutil.which("git"), "git is not installed, so the round trip through a real diff did not run")
class GitRoundTrip(unittest.TestCase):
    """The probe must reach the thing under test: a real repository, a real diff."""

    def git(self, repo: Path, *args: str) -> str:
        return subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, text=True).stdout

    def land(self, repo: Path, base: str, plan_file: Path) -> subprocess.CompletedProcess:
        recipe = (f"{{ git -C '{repo}' diff --name-only -z --no-renames {base}; "
                  f"git -C '{repo}' ls-files -z --others --exclude-standard; }} "
                  f"| '{sys.executable}' '{SCRIPT}' --plan '{plan_file}' --lane api --changed -")
        return subprocess.run(["sh", "-c", recipe], capture_output=True, text=True)

    def test_the_recipe_in_the_skill(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp, "repo")
            (repo / "src" / "api").mkdir(parents=True)
            (repo / "docs").mkdir()
            self.git(repo, "init", "-q")
            self.git(repo, "config", "user.email", "crew-self-test@example.invalid")
            self.git(repo, "config", "user.name", "crew self-test")
            (repo / "src/api/routes.py").write_text("v1\n")
            (repo / "docs/guide.md").write_text("v1\n")
            self.git(repo, "add", "-A")
            self.git(repo, "commit", "-q", "-m", "base")
            base = self.git(repo, "rev-parse", "HEAD").strip()
            plan_file = Path(tmp, "plan.md")
            plan_file.write_text(CLEAN, encoding="utf-8")

            # In lane: one committed edit, one uncommitted edit, one untracked new file.
            (repo / "src/api/routes.py").write_text("v2\n")
            self.git(repo, "commit", "-q", "-am", "lane work")
            (repo / "src/api/routes.py").write_text("v3\n")
            (repo / "tests" / "api").mkdir(parents=True)
            (repo / "tests/api/test_routes.py").write_text("t\n")
            result = self.land(repo, base, plan_file)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("2 changed path(s)", result.stdout)

            # Now the api lane steps on the docs lane's file.
            (repo / "docs/guide.md").write_text("v2\n")
            result = self.land(repo, base, plan_file)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("docs/guide.md: [foreign-lane-write]", result.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
