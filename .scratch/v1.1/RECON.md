# Recon: KEEL FACTORY v1.0.0, read against what Claude Code and Codex actually do

**Date:** 2026-10-18
**Authorization:** The manager's own framework, master copy at
`/Users/lambertike/Documents/KEEL-FACTORY`. Work happens on branch
`v1.1-harness-conformance`; `main` stays at the `v1.0.0` tag.

This is KEEL's own RECON, run on KEEL, before BRIEF for v1.1. It is kept in `.scratch/`
because the master has no `docs/` of its own: `link_kit.py` links every top-level item
into projects, so a `docs/` here would appear inside every project's `keel-factory/`.
`.scratch/` is skipped by `link_kit.py` and excluded by the documented `rsync`.

Evidence labels: **Evidence** = read on disk or run here today; **Inferred** = reasoned
from what was read; **Missing evidence** = could not confirm.

---

## 1. What is this system?

- **Purpose:** a framework handed to an AI coding agent so it works like a disciplined
  team: five phases (BRIEF → CONTRACT → DESIGN → SLICE → PROVE), three tiers, six rules,
  RECON before BRIEF on existing systems, HELM as the router, operator mode for other
  people's packages. *Evidence* (`ARCHITECTURE.md`, `keel/README.md`).
- **Stack:** Markdown read by the agent (about 22,200 lines outside the Codex copies,
  10,400 more in them), plus standard-library Python scripts (guard, link, install,
  release, lane checker, board validator) and three Node hooks that have never run.
  *Evidence* (`wc -l`, 2026-10-18).
- **Shape:** one master folder. Projects get it two ways: `link_kit.py` (a
  `keel-factory/` folder of symlinks plus `.ops/`) or an `rsync` copy. *Evidence.*
- **How it reaches the agent today:** *Evidence*, from the files.
  1. A project's `CLAUDE.md` (a verbatim copy of `keel-factory/CLAUDE.md`, 200 lines,
     12,856 bytes) carries HELM and the standing rules. In operator mode the kit's own
     `CLAUDE.md` loads through the link.
  2. Skills are reached by **file path** from that `CLAUDE.md`. Owner-mode setup copies
     them into `.claude/skills/`; nothing installs them machine-wide.
     `~/.claude/skills/` holds only `synced` (*Evidence*, `ls`).
  3. The guard is wired machine-wide in `~/.claude/settings.json` by `install_guard.py`
     and arms only where `$CLAUDE_PROJECT_DIR/keel-factory/` exists.

## 2. The house style — conventions already in force

From the handoff's "Non-negotiable conventions" and from reading the files. *Evidence*
unless marked.

- **Cited, not absorbed.** ECC, Miguel's skills and REA are referenced, never
  bulk-copied.
- **Reconcile, don't stack.** New mechanisms map onto old ones; two systems for one job
  is the failure.
- **The vendored `keel/skills-board/` is never edited.** Claude and Codex copies differ
  only in frontmatter and `agents/openai.yaml`. *Evidence* (`diff -rq`).
- **HELM stays thin:** a routing procedure, never an engine.
- **The grounding rule** (`CAPABILITIES.md`): never write a step no real tool can do.
- **Evidence labels everywhere;** prove a check can fail before trusting it (Rule 6b),
  applied to the factory's own scripts too.
- **The five phases are never renumbered or added to.** RECON, LOOPS and CREW sit around
  them.
- **Suggest, never ask blind;** the data-boundary question keeps its exact yes/no shape.
- **Docs are plain, short-sentenced, table-heavy.** Every claim of proof names its
  command. Releases record Evidence / Inferred / Missing separately.
- **Scripts:** standard library only, a docstring that is the usage text, exit 0 on
  success and 1 on refusal, a `test_*.py` self-test beside each, run with `python3 -B`.
- **Commits:** conventional style (`chore(release): ...`), one commit so far.

## 3. The map

| Part | Path | Reaches the agent by |
| --- | --- | --- |
| Router + standing rules | `CLAUDE.md` | always-loaded instruction file |
| Operator protocol | `OPERATOR.md` | read on the activation line |
| KEEL skills | `keel/skills/{helm,keel,keel-prove,crew}/` | path from `CLAUDE.md`, or a copy in `.claude/skills/` |
| Board, handoff, commit, docs skills (vendored) | `keel/skills-board/{claude,codex}/` | same |
| Senses | `keel/capabilities/{deep-research,reverse-engineering}/` | same |
| Framework docs | `keel/framework/*.md` | read when a skill points at them |
| Templates | `keel/templates/` | copied into `docs/` per phase |
| Guard | `harness/hooks/data-boundary-guard.py` | PreToolUse hook, machine-wide |
| ECC hooks (Node) | `harness/hooks/*.js` | never run (no Node) |
| ECC write-ups | `harness/skills/` (12) | cited reading, not installed |
| Setup scripts | `harness/{link_kit,install_guard,make_release}.py` | run by the user |

**Seams that matter for v1.1:**

- Every root document addresses the kit as `keel-factory/...` (about 150 references in
  11 files). Skills address each other by **relative** path (`../../framework/...`), so
  they work wherever the folder sits. *Evidence* (`grep`).
- The guard's arming test is the presence of `keel-factory/`.

## 4. Health and risk — read honestly

Findings, each tied to what Claude Code or Codex actually does. Harness facts are being
gathered in `research-*.md` beside this file.

1. **Skills are invisible to the harness.** Neither Claude Code nor Codex lists a skill
   it was never installed for, so the model never sees HELM's or keel's description and
   cannot pick them by itself. It reaches them only because `CLAUDE.md` names their
   paths. *Evidence* (`ls ~/.claude/skills`).
2. **`keel` has `disable-model-invocation: true`.** In Claude Code that removes it from
   the model's skill list entirely, so HELM (a model) cannot route to it through the
   Skill tool. The vendored `commit` is the same, by its author's design. *Evidence*
   (frontmatter).
3. **The always-loaded file is large.** `CLAUDE.md` is about 3,200 tokens in context for
   the whole session, most of it detail that only matters at one branch (operator gate,
   CREW tripwire, loops, hooks). *Inferred* token count (bytes / 4).
4. **Three opening lines** (owner prompt, operator line, test-drive line). The manager's
   trial run 2 showed one ambiguous word sending a fresh agent to test the wrong thing.
   *Evidence* (the manager's report).
5. **Copies drift.** Owner setup copies skills into each project; those copies never
   follow the master. *Evidence* (`QUICKSTART.md` §0).
6. **No setting for how often it stops.** STANDARD stops at CONTRACT, DESIGN, every
   slice boundary and PROVE. "Run without me between check-ins" exists only as
   `LOOPS.md`, a never-run draft. *Evidence* (`TIERS.md`, `keel/SKILL.md`).
7. **The independent review depends on memory.** `keel-prove` asks for three parallel
   sub-agents with pasted prompts; nothing ships them as agent definitions, and nothing
   stops a "done" claim with no PROVE report. *Evidence.*
8. **Owner mode has never had a fresh-agent trial;** the question-with-options posture is
   wording only. *Evidence* (`RELEASES.md`).
9. **Small contradictions found while reading:**
   - `TIERS.md` says "Every tier guarantees these six" and lists seven items.
   - `RULES.md` is titled "The Five Standing Rules" and defines six.
   *Evidence* (lines 42 and 1).
10. **The Codex instructions assume Claude Code's names.** `settings.hooks.codex.json`
    matches `Read|Edit|Write|Bash`, which START-PROMPTS itself says is unverified for
    Codex. *Evidence* (the file); whether Codex uses those names is in research.
11. **`claude plugin eval` is not in this machine's CLI** (2.1.170). `validate`,
    `details`, `install`, `marketplace`, `tag` and `--plugin-dir` are. *Evidence*
    (`claude plugin --help`, `claude --help`).

**Tests not to trust:** none of the Node hooks (never run). The guard, link, install,
lane and board tests are trusted: each was proven to fail on broken copies.

## 5. From map to backlog

The manager's feedback already ranked six changes. RECON confirms each one against the
files, and adds the contradictions in item 9.

| # | Candidate | Why | House-style constraint |
| --- | --- | --- | --- |
| 1 | Ship KEEL as a Claude Code plugin from the master folder | Findings 1, 2, 5 | Don't edit the vendored bundle; plugin points at it |
| 2 | One front door: HELM decides owner vs operator, one opening line | Finding 4 | HELM stays a router |
| 3 | A stop-mode setting (supervised / checkpoint / unattended) | Finding 6 | Five phases unchanged; mode changes stops, not phases |
| 4 | `keel-prove` reviewers as shipped agent definitions | Finding 7 | Same three axes, same prompts |
| 5 | An eval suite with a no-plugin baseline | Finding 8 | Rubric fixed before the run; grader is not the worker |
| 6 | A short always-loaded file, detail in skills | Finding 3 | Data-boundary rule stays always-on |
| 7 | The same for Codex, as far as Codex really allows | Finding 10 | Name each gap instead of faking it |
| 8 | Fix the two contradictions | Finding 9 | — |

**Recommended first pick:** 1, because 2, 4 and 6 all depend on the plugin existing, and
it is the one change with a real validator here (`claude plugin validate`).

**Explicitly not proposing:** rewriting the five phases; editing the vendored skills;
a heavy orchestrator; porting the three Node hooks (no Node to prove them on).

## 6. Handoff to BRIEF

**Chosen direction:** the manager asked for all of it, for both harnesses, built with
KEEL itself. BRIEF settles scope and the decisions only the manager can make.

**Constraints BRIEF/CONTRACT must honor:** §2 in full; the guard's proven behavior must
not regress (its 27-test self-test stays green); `link_kit.py` operator flow keeps
working for machines without the plugin.

**Unknowns to resolve:** how plugin installs update (copied cache or live); whether a
plugin can point its skill list at `keel/skills-board/claude/` without moving it; what
Codex supports for skills, hooks, subagents and plugins today.
