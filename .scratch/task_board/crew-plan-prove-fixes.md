---
id: crew-plan-prove-fixes
title: CREW plan — fix PROVE pass 1's findings in parallel lanes, then PROVE pass 2
kind: ticket
status: in-progress
gate: none
priority: high
category: framework / crew
created: 2026-10-18
updated: 2026-10-20
parent: null
part-of: v1-1-harness-conformance
blocked-by: []
supersedes: []
superseded-by: null
revisit: false
outcome: null
---

# Task: CREW plan — fix PROVE pass 1's findings in parallel lanes, then PROVE pass 2

## Why this exists

PROVE pass 1 on v1.1 confirmed 26 reviewer findings and 26 critic issues, none fixed
([PROVE-FINDINGS.md](../v1.1/PROVE-FINDINGS.md), "Disposition plan", rows 1–13). The
rows touch separable files: the hook, the skills, the kit check, the installers, and
three groups of documents. Run as lanes with exclusive write sets, they finish in one
pass without two writers on one file. This is CREW's second real run.

## Plan

1. Lanes below, checked with `check_lanes.py --plan`.
2. Phase 1 (code and the always-on layer): lanes `hook`, `skills`, `instrument`,
   `installers`, `layer`, run together. Each back-briefs first: its plan is checked
   against its write set by the lead's script before the same lane builds.
3. Land phase 1: fence (snapshot diff, below), then gate, then log.
4. Phase 2 (documents that describe the landed code): lanes `guides`, `reference`,
   `records`, run together on the landed tree, with phase 1's returns in their briefs.
5. Land phase 2 the same way. Then row 11 (the live subagent probe, lead), the full
   re-run with the mutation tools (row 13), and PROVE pass 2 through `keel-prove` in
   fresh contexts. Stop at the PROVE report.

All lanes run `shared`: v1.1 is uncommitted, and a worktree branches from a commit
(`e09480c`), so it would not contain the work. The lead declares its own lane.

**Fence without commits.** CREW's field record (Gap 1) asks for a checker that compares
against a snapshot taken at dispatch. The lead takes one: a SHA-256 per file over
`git ls-files -co --exclude-standard` before each phase, and after it the changed,
added and deleted paths, fed to `check_lanes.py --changed -` (with `--lane` per lane,
because each phase's lanes are the only writers while it runs and the lead writes
nothing outside its lane meanwhile).

## Lanes

| Lane | Owner | Tasks | Writes | Mode |
| --- | --- | --- | --- | --- |
| skills5 | worker-skills | D4, D5, D7, D8, D9, D17 in HELM and the worker brief | `keel/skills/helm/SKILL.md`, `keel/skills/crew/assets/brief.md`, `.scratch/skills-main/base/keel/skills/helm/SKILL.md`, `.scratch/skills-main/base/keel/skills/crew/assets/brief.md` | shared |
| reference5 | worker-reference | D1, D2, D8, D9, D17, T4-7 in the reference docs | `harness/DATA-BOUNDARY.md`, `harness/README.md`, `keel/framework/CAPABILITIES.md`, `harness/settings.hooks.codex.json`, `.scratch/skills-main/base/harness/README.md`, `.scratch/skills-main/base/keel/framework/CAPABILITIES.md` | shared |
| protocols5 | worker-protocols | D1, D4, D8, D9, D16, D17, P-K34 in the protocols | `OPERATOR.md`, `START-PROMPTS.md`, `RELEASES.md`, `CLAUDE.md`, `.scratch/skills-main/base/OPERATOR.md`, `.scratch/skills-main/base/START-PROMPTS.md`, `.scratch/skills-main/base/RELEASES.md`, `.scratch/skills-main/base/CLAUDE.md` | shared |
| guides5 | worker-guides | D5, D15, P-K23 in MANUAL | `MANUAL.md`, `.scratch/skills-main/base/MANUAL.md` | shared |
| records5 | worker-records | S4-a2, S4-c (the six approvals), D19, D6's and D5's CONTRACT lines | `.scratch/v1.1/CONTRACT.md`, `.scratch/v1.1/ACCEPTANCE.md`, `.scratch/v1.1/DESIGN.md` | shared |
| lead | lead | D6, D11, D18, P-C5, the 3 follow-ons, the 4 rejects, landing, the closure check, the report | `.scratch/task_board/`, `.scratch/v1.1/round5/`, `.scratch/v1.1/STATE.md`, `.scratch/v1.1/TRACEABILITY.md`, `.scratch/v1.1/PROVE-3.md`, `.scratch/v1.1/PROVE-4.md`, `.scratch/v1.1/PROVE-5.md`, `.scratch/handoff.md`, `keel/framework/HARNESS-PROBES.md`, `.scratch/skills-main/base/keel/framework/HARNESS-PROBES.md`, `.scratch/skills-main/lead-tools/lanes-build.md`, `README.md`, `.scratch/skills-main/base/README.md`, `.scratch/skills-main/base/harness/DATA-BOUNDARY.md`, `.scratch/skills-main/base/harness/settings.hooks.codex.json`, `.scratch/skills-main/results/` | shared |
| dryrun | another session (the manager's request) | the dry run's evidence, written outside this run and disclosed in its message | `.scratch/evidence/dryrun-2026-10-20/` | shared |

This is docs round 5 (2026-10-20). Fix round 4's phase-B table is kept in the execution log
below, with phase A's.

Unowned, so nobody writes them this run: `harness/hooks/data-boundary-guard.py` (never
edited, convention), `keel/skills-board/` (vendored, never edited), every script and test,
and everything else.

## Open questions

Every seam two lanes share, decided before dispatch.

1. Did the manager agree to dispatch (crew §4)? RESOLVED 2026-10-18: checkpoint mode,
   BRIEF + CONTRACT approved, and the manager's opening words, verbatim: "If you need to
   make a task list, a board of responsibilities, agents, feel free." On resuming, the
   manager picked, verbatim, "Yes, rows 1–11 → pass 2 (Recommended)", an option whose
   text said "the rest in parallel lanes with no overlapping files".
2. Contract amendments (row 12)? RESOLVED 2026-10-18: the manager ticked all four
   recommended picks, verbatim "D1: Diataxis opt-in,D3: guard-probe exception,D6: crew
   checkpoint OK,D8: keep --codex-hooks"; the option text said the wording-only fixes
   come along with these. Anything beyond them is written as *proposed* and goes to the
   manager at the PROVE report.
   Verbatim record of that question round (2026-10-18), the source CONTRACT's Amendments
   cite:
   - Question: "Should I go ahead with fix rows 1–11, then the full re-run and PROVE pass
     2, stopping at the PROVE report?" Picked: "Yes, rows 1–11 → pass 2 (Recommended)",
     whose text was "Rows 1–3 first (the live keel_hook defect), then the rest in parallel
     lanes with no overlapping files, mutation proofs re-armed, then fresh-context PROVE.
     Stops at the PROVE report, the data boundary, or anything outward-facing." Not
     picked: "Row 1 only, then check in".
   - Question: "Which contract amendments should I write in as recommended? For any you
     leave unticked, the contract stays as approved and I change the code to match it
     instead." Ticked, all four:
     - "D1: Diataxis opt-in" ("Keep the four docs skills behind --with-docs. Listing all
       16 adds ~1,100 characters and breaks the 8,000-character skill listing budget that
       both harnesses cap.");
     - "D3: guard-probe exception" ("Keep the named exception for HELM's probe of the
       nonexistent keel-armed-check/.env. Alternative: drop the probe and report the guard
       as unproven every session.");
     - "D6: crew checkpoint OK" ("In checkpoint mode, an approved BRIEF + CONTRACT plus
       your quoted words allowing agents counts as agreement to dispatch. Alternative:
       always ask before every dispatch.");
     - "D8: keep --codex-hooks" ("Keep the installer flag, never run without your yes.
       Alternative: remove it and document manual wiring. Wording-only fixes (one
       keel_hook.py, the 1,024 cap, non-strict validate) come along with these.").
3. The switch-on rule, one wording for the hook, the skills and the docs. RESOLVED:
   - Find the git root: the nearest folder at or above the start that holds `.git`
     (a folder, or a file in a worktree).
   - Inside git: KEEL is on when a folder from the start up to and including the git root
     holds an entry named exactly `.keel` (a folder) or exactly `keel-factory` (a folder or
     a link to one); the nearest wins. Names are compared exactly (`os.listdir`), because
     macOS ignores letter case. When the git root's `.git` is a file whose gitdir has a
     `commondir` file (a worktree, not a submodule), the main worktree's root is checked
     too, after the walk.
   - Outside git: only the start folder is checked.
   - Never on: a start at or inside the kit root; a marker in `$HOME` or `/`; a
     `keel-factory` entry that is the kit root's own folder rather than a link to it. *Superseded 2026-10-18 by Open question 17: only
     when the kit root is the master's own git checkout; a copy switches on (N2 = N35).*
   - Role: `.keel/keel.json` gives owner or operator, else "not recorded"; `keel-factory`
     gives "kit".
4. The hook's command line. RESOLVED: `keel_hook.py session [--harness claude|codex]` and
   `keel_hook.py guard [--harness claude|codex]`; the default is `claude`. Codex hook
   commands (installer and template) pass `--harness codex` to both. The guard behaves
   the same for both values today.
5. Shared constants. RESOLVED: `keel_hook.py` keeps a top-level
   `LAYER_MARK = "<!-- KEEL always-on layer -->"`, and `test_keel_hook.py` imports it from
   there. `install_plugin.py` keeps `OWN`, `BOARD` and `DOCS` as top-level list literals.
   `check_kit.py` reads all three, and the mark, with `ast`, so no code runs.
6. Allowlist protection (row 3). RESOLVED: where KEEL is on, the hook blocks a Write,
   Edit, MultiEdit or NotebookEdit whose path ends in `.keel/data-boundary-allow`
   (compared without case), a Codex patch naming such a path, and any Bash command
   containing `data-boundary-allow` (without case). The reason says only the user edits
   that file. CLAUDE.md (lane `layer`) gains one sentence saying the same.
7. HELM's switch-on, as the skills and docs describe it. RESOLVED:
   - The role file goes at the project root: the git root, or the session's folder
     outside git.
   - HELM refuses to create `.keel/` in `$HOME`, in `/`, or inside the kit root. It says
     so, does not switch on, and runs the data-boundary rule as strict policy.
   - After recording the role, HELM reads the kit's `CLAUDE.md` (`../../../CLAUDE.md`
     from its folder) at once, so the first session gets the layer.
   - It warns when `git check-ignore -q .keel/keel.json` succeeds. It tells an owner that
     `.keel/keel.json` belongs in the repository.
   - Codex owner mode: HELM adds the kit's `CLAUDE.md` once to the project's `AGENTS.md`,
     as a block that opens with the mark line (the file's own first line) and closes with
     `<!-- end KEEL always-on layer -->`. Operator mode never edits the package's
     `AGENTS.md`.
   - `<ops>` means `.keel/ops/` when the kit came by plugin, `keel-factory/.ops/` when it
     was linked.
8. A failed guard probe. RESOLVED, and the same in HELM and OPERATOR.md: say once that no
   guard is armed, run the data-boundary rule as strict policy (the kit's `CLAUDE.md`
   section), and optionally offer once to wire the fallback guard; never hold the job on
   the answer.
9. A copied skill's paths. RESOLVED, the same line in KEEL's six skills: "If a relative
   path here does not resolve (a copied skill), resolve it under `keel-factory/keel/`
   instead, and root files such as `CLAUDE.md` under `keel-factory/`."
   *Superseded 2026-10-18 by Open question 17 (the copied-skill line, N25).*
10. SPRINT's gate. RESOLVED: at SPRINT, keel-prove spawns Standards and Spec; the builder
    may run the gate's commands itself, because an exit code does not depend on who runs
    it, and the report says the gate was run by the builder. The review is always by
    agents.
11. Releases. RESOLVED: `make_release.py` refuses unless the current branch is `main`;
    MANUAL §11 says releases are cut from `main` after merging.
12. Reading the kit (COMPLETENESS-15). RESOLVED for this run, *proposed* to the manager:
    CLAUDE.md's data-boundary item 3 says the KEEL kit itself (the kit root the session
    note names, or the folder a KEEL skill was loaded from) counts as named by the task.
    `records` writes it into the amendments as proposed, awaiting approval.
    *Superseded 2026-10-18 by Open questions 16 and 17: P-B became a second named
    exception; item 3 keeps its approved wording.*
13. Which mode is "usual". RESOLVED: no document calls one mode the usual one;
    MANUAL drops "the usual one".
14. Back-brief answers, phase 1. RESOLVED 2026-10-18, each lane's own recommended pick
    unless noted:
    - hook: under `--harness claude`, `AGENTS.md` counts only when a Claude file imports
      `@AGENTS.md` (narrower than row 2's wording: the worst case is the layer twice, never
      missing; KEEL's research says Claude Code does not read a lone `AGENTS.md`). The
      allowlist block holds even under `KEEL_DATA_BOUNDARY_OVERRIDE=1`. A worktree's carry
      check reads the worktree's own root. A worktree whose main checkout is the kit is
      dormant. `AGENTS.override.md` is out of scope (a follow-on).
    - skills: step 0 is an unnumbered lead-in before keel-prove's and crew's existing §0,
      so nothing is renumbered. helm's and keel-prove's descriptions change minimally. HELM
      also reads the layer when KEEL is on but no layer is in context. The Codex block
      gains one portable kit-root line. Bare kit-file tokens become relative paths. HELM
      checks the mark before trusting `../../../CLAUDE.md` in a copied layout.
    - instrument: new rule ids `source` and `skill-set`; a bare `agents/` or `harness/`
      token that exists under the skill's own folder passes; `skill-set` also checks each
      DOCS skill's Claude Code copy.
    - installers: `test_install_guard.py` pins the fallback command to the one documented
      in `OPERATOR.md`, so for phase 1 only `OPERATOR.md` moves to this lane, for that one
      block; it goes back to `reference` for phase 2 (the table is re-checked then).
      `install_guard.py` upgrades a v1.0 entry in place.
    - layer: LOOPS' three otherwise unsourced cells gain CAPABILITIES rows; the CLAUDE.md
      sentence says "KEEL's hook blocks agents from it" (true wherever `keel_hook.py` is the
      wired hook, not for a bare guard: corrected in Open question 17); the Windows
      note includes the PowerShell matcher gap.
    - every code lane: the generic mutation runner never runs the unbroken suite, so each
      lane proves its baseline green on the same kit before counting mutants.

15. Back-brief answers, phase 2. RESOLVED 2026-10-18:
    - guides: MANUAL §3 drops README-FIRST's detached `git checkout v<tag>` and verifies
      the clone with `git describe --tags` (a detached HEAD breaks the upgrade pull and the
      next release); the scripts lane changes README-FIRST to match. MANUAL §3's "work from
      the SSD" step folds into step 1, so MANUAL and README give one rule. MANUAL §6 also
      leads with the plugin form.
    - reference: the Codex wording is precise (skills only without `--codex-hooks`; HELM
      still loads the layer, Inferred); WALKTHROUGH-5's armed check also requires the block
      reason and is run by the user; RELEASES lists every fix in final form and the lead
      confirms the other lanes' entries at landing.
    - records: the "Approved" amendments are exactly A1–A4 plus the three wording fixes the
      option text named; D2's exfil sentence and the phase-1 guard changes go under
      "Proposed"; D3's AGENTS.md block is implemented as approved and needs no amendment.
    - scripts: write failures are tested with read-only temp folders; a full release is
      built in temp; README-FIRST drops the detached checkout.

16. The manager's answers at the PROVE pass 2 report. RESOLVED 2026-10-18, verbatim picks:
    - "PROVE pass 2 does not pass … What next?" → "Fix round 3 → pass 3 (Recommended)".
    - "Approve P-B? …" → "Make it an explicit exception" (reword it as a second named
      exception beside the guard probe, not a reading of item 3).
    - "The other proposed amendments, P-A and P-C to P-H …" → "All as written
      (Recommended)".
    - The data-boundary question "This would require modifying `~/.claude/settings.json`
      (removing KEEL's v1.0 PreToolUse guard entry), which is security tooling outside
      this project. Do you want me to proceed with this specific action?" → "Yes" (the
      option text: run `python3 harness/install_guard.py --remove`, which removes only
      KEEL's own entry, then confirm the plugin's hook still blocks in a scratch `.keel/`
      project).

    Verbatim record of the PROVE pass 2 question round (2026-10-18):
    - "PROVE pass 2 does not pass (three confirmed major defects, one made by this fix run).
      What next?" Picked: "Fix round 3 → pass 3 (Recommended)", whose text was "Fix the 3
      majors first, then the 13 fix-now and 32 docs-only items; file the 8 follow-ons as
      board tasks; record the 7 rejects with reasons; then a fresh PROVE pass 3, stopping
      at its report." Not picked: "Majors only → pass 3", "Stop; I'll read PROVE-2.md".
    - "Approve P-B? It clarifies data-boundary item 3 in CLAUDE.md so agents may read the
      KEEL kit itself (every live run already does; the rule as written forbade it)."
      Picked: "Make it an explicit exception", whose text was "Reword it as a second named
      exception beside the guard probe, not a reading of item 3." Not picked: "Approve as
      clarification (Recommended)", "Reject and revert".
    - "The other proposed amendments, P-A and P-C to P-H (switch-on rule details, the
      AGENTS.md import rule, install_guard's in-place upgrade, agent-body wording,
      check_kit/make_release rules, the new guard blocks, the exfil wording): which do you
      approve?" Picked: "All as written (Recommended)", whose text was "Each is written up
      in CONTRACT.md 'Proposed, awaiting the manager' with its reason; all conform to what
      rows 1–11 asked for." Not picked: "All except P-D", "Decide after reading".
    - The data-boundary question, as quoted above. Picked: "Yes", whose text was "Run
      python3 harness/install_guard.py --remove (it removes only KEEL's own entry), then
      confirm the plugin's hook still blocks in a scratch .keel/ project."

17. Fix round 3's seams, decided before dispatch. RESOLVED 2026-10-18:
    - **The kit's own folder (N2 = N35).** A `keel-factory` entry is skipped only when it
      is the kit root itself and the kit root is the master: its own git checkout (a
      `.git` folder, or a linked worktree's `.git` file whose gitdir holds `commondir`).
      A copy (the documented rsync leaves `.git` out) or a link switches KEEL on. The
      docs say "the master's own git checkout", not "the kit's own folder".
    - **An import that counts (N36).** Only an import line `@keel-factory/CLAUDE.md`
      (optionally `@./`) that resolves, from the importing file's folder, to a file
      carrying the mark. A prose mention never counts.
    - **The v1.0 upgrade note (N3).** Offer the import only when
      `keel-factory/CLAUDE.md` exists and carries the mark. Otherwise: delete KEEL's v1.0
      text (the hook then supplies the layer), or replace it with v1.1's `CLAUDE.md`.
    - **install_guard's command (N37).** The exact-name test on `keel-factory` in the
      project folder stays the switch. The command then runs the installing master's own
      guard, by absolute shell-quoted path, never the project's copy. The marker
      recognizes old and new forms, and a re-run upgrades an older entry in place (P-D,
      approved). OPERATOR.md documents the command with a placeholder for the master's
      path; its pinning test compares after substitution.
    - **P-B as an explicit exception, beside the guard probe.** CLAUDE.md's item 3 goes
      back to its approved wording. A second named exception follows the guard-probe
      exception: reading the KEEL kit itself (the kit root the session note names, or the
      kit a KEEL skill was loaded from) needs no question; items 1 and 2 still apply
      inside it. The docs mirror it as an exception.
    - **The allowlist sentence (N4 with N34).** Only the user edits
      `.keel/data-boundary-allow`. KEEL's hook (the plugin's, or Codex's with
      `--codex-hooks`) blocks the direct ways of writing it; a hand-wired bare guard does
      not. It is a tripwire, not a lock.
    - **The copied-skill line (N25), identical in all six skills.** "In a copied skill
      (this file sits under a project's `.claude/skills/` or `.agents/skills/`, not under
      `keel/`), read every `../` path under `keel-factory/keel/`, and root files such as
      `CLAUDE.md` under `keel-factory/`, even when the project has a file of that name."
    - **keel in operator mode (N23 = N28).** In `keel`'s step 0, not HELM's: in operator
      mode, follow `../../../OPERATOR.md` instead of the phases.
    - **README-FIRST (N11).** First `shasum -a 256 -c SHA256SUMS`. Then
      `git clone --branch main "$PWD/KEEL-FACTORY-<tag>.bundle" ~/GitProjects/KEEL-FACTORY`
      and `git -C ~/GitProjects/KEEL-FACTORY describe --tags`, noting: your own local
      path, never the drive. Without git: `mkdir -p ~/GitProjects && tar -xzf … -C
      ~/GitProjects`. MANUAL §3 matches it.
    - **The armed check (N2).** Run the wired command from the hooks file in the real
      project root with a Read of `keel-armed-check/.env` (no fake folder), setting
      `CLAUDE_PLUGIN_ROOT` only for `plugin-hooks.json`. It needs exit 2 and the
      "BLOCKED by data-boundary-guard" reason.

18. Fix round 3, phase A back-brief answers. RESOLVED 2026-10-18, each lane's own pick
    unless noted:
    - hook3: Codex's v1.0 note uses the same delete-or-replace form; the session header
      reads "The kit is at `keel-factory/` (a link or a copy)"; an import line inside a
      fenced code block is a follow-on.
    - installers3: OPERATOR.md shows the master's path as a quoted placeholder, explained
      in one sentence above the block; the old-form marker is exactly
      `$CLAUDE_PROJECT_DIR/keel-factory/harness/hooks/data-boundary-guard.py`; an
      end-to-end test runs the real guard against a project whose own copy allows
      everything.
    - release3: README-FIRST keeps "(must print <tag>)" on the describe line.
    - skills3: the allowlist check reads `.keel/data-boundary-allow` with the Read tool and
      runs `git ls-files -- .keel`. Any command that names the file is blocked by KEEL's
      own hook, so the decided `--error-unmatch` form could not work. It also runs when
      KEEL is already on with a recorded role. keel-prove's and crew's records go to
      `<ops>` in operator mode.
    - layer3, not the lane's pick: the lead recorded probe X10 (`codex plugin --help` on
      0.138, scratch homes), and CAPABILITIES cites it.

19. Fix round 3, phase B back-brief answers. RESOLVED 2026-10-18:
    - The always-on figures cite probe P14, recorded by the lead (~2,530 tokens in this
      machine's config, ~1,953 in a fresh one). L8 is corrected to 5,918 characters of
      context.
    - The documented rsync copy commands gain `--exclude '.DS_Store'`, the same in
      START-PROMPTS and MANUAL.
    - OPERATOR.md's false `realpath keel-factory` phrase is corrected; the pinned JSON block
      stays byte-identical.
    - CONTRACT keeps each approved P-entry word for word and records round-3 changes in a
      dated F3 section. The 8,000-character listing bound needs no new proposal: the D1
      option the manager ticked names it.
    - The verbatim question and option texts of both rounds are now in Open questions 2 and
      16.

20. The manager's answer at the PROVE pass 3 report, and fix round 4's seams. RESOLVED
    2026-10-19.
    - The answer, verbatim as received (the message ends mid-sentence): "Fix round 4 → pass
      4 (Recommended): fix the 5 fix-now and 28 docs-only items, file the 5 follow-ons,
      record the 10 rejects, then a closure-focused PROVE pass 4 (three reviewers and
      closure checkers, no new critic), stopping at its report. And approve as written
      F3-7's D7 reading, the 8,000-character"
    - The questions it answers, verbatim from the report: "## Decision 1: what next?" with
      "1. **Fix round 4, then pass 4 (recommended).**" and "2. **Fix-now only, then pass
      4.**"; and "## Decision 2: three contract wordings ... Approve these as written
      (recommended), or decide each one separately:" over F3-7's D7 reading, the
      8,000-character listing bound, and F3-1, F3-2, F3-4 and F3-6.
    - Read as: fix round 4 → pass 4; F3-7's reading of D7 approved; the 8,000-character
      listing bound approved (the only 8,000-character item in the question). F3-1, F3-2,
      F3-4 and F3-6 come after the cut: **not approved**; they go to the manager again at
      the PROVE pass 4 report.
    - Dispositions: as PROVE-3.md's table. The code halves of docs-only items go to board
      tasks, never into this round: C1, K18, K19 (honor an allowlist only at the KEEL
      root), K36 → `keel-hook-hardening`; C4 (refuse or warn when run from a copy; the
      manager's call), K28, S-b5 → `installer-hooks-json-robustness`; K20's hook half, K34
      → `codex-agents-block-refresh`; K29's matcher (Monitor, PowerShell; a contract
      change) → `owner-deferred/mcp-tools-guard-matcher`; C3's probe (an interactive
      Claude Code session) → owner-gated; T7's constraint → `codex-agents-block-refresh`
      and `helm-role-override`.
      Corrected 2026-10-20 (PROVE pass 4, D6): K19's code half is the verifiers' design,
      the tracked-file test at the nearest git root; `keel-hook-hardening` item 5 says so.
    - Seams, one wording each wherever they land:
      - **S1, Codex reads (K32):** "In Codex every file read is a shell command, so the
        guard sees it only as Bash and covers it only through its Bash heuristic: a blocked
        probe shows the hook is wired, not that reads are covered."
      - **S2, the gitignore rule's scope (K18):** "The gitignore rule asks git in the
        repository nearest the file: outside git no `.gitignore` applies, and a separate
        repository inside a gitignored folder is judged only by its own rules."
      - **S3, nested allowlists (K19):** "The guard honors a `.keel/data-boundary-allow` at
        the nearest git root of each path, so a submodule or a nested clone can bring its
        own; HELM's switch-on check lists every `.keel/` folder below the root as well."
        The listing command, in HELM and OPERATOR.md: `find . -path ./keel-factory -prune
        -o -type d -name .keel -print` (it never names the file, so KEEL's hook allows
        it). Each `.keel/` found below the root is handled like the root's.
      - **S4, unmatched tools (K29):** "Claude Code's Monitor tool, and PowerShell on
        Windows, run shell commands that the matcher does not name, so the guard never
        sees them (Inferred from the matcher)."
      - **S5, the Codex installer (C4):** "`install_plugin.py --codex-hooks` writes
        machine-wide hooks that run the kit it was run from: run it from the master (or
        through a linked `keel-factory/`), never from a copy inside a project."
      - **S6, which copy switches on (C2):** "A copy made with MANUAL §4's rsync (no
        `.git`) switches KEEL on; a copy that keeps `.git` (a `git clone`, `cp -R` or a
        Finder copy) counts as a master's own checkout and stays dormant when its own hooks
        run."
      - **S7, when new wiring arms (K26):** "New wiring arms from the next session (in
        Claude Code, also once `/hooks` is opened; in Codex, once the hooks are trusted in
        `/hooks`); until a probe there comes back blocked, strict policy stands." The
        `/hooks` clause is Inferred (KEEL's research notes).
      - **S8, the gitignored `.keel/` (C14):** HELM step 1 runs `git check-ignore -q
        .keel/keel.json` before writing the file (KEEL is still off, and git answers for a
        path that does not exist yet). In HELM step 3 and OPERATOR.md: "If one of these
        checks is blocked with the reason 'matches this repo's .gitignore', that block is
        the answer: `.keel/` is ignored. Do not retry another way: say the allowlist could
        not be checked and ask the user to look in `.keel/`; in operator mode, stop before
        going on."
      - **S9, the operator test (C15),** identical in `keel`, `keel-prove` and `crew`: the
        parenthesis becomes "(`.keel/keel.json` says operator; or no role is recorded, as
        with a linked or copied `keel-factory/`, and by HELM's rule the project carries its
        own instructions that are not KEEL's; or the session note, the user or your brief
        says so; or switch-on just decided it)". Their switch-on line also runs HELM's
        switch-on when a `.keel/` holds no `keel.json`.
      - **S10, a `.keel` that is not a folder (K35):** "If `.keel` exists and is not a
        folder, say so and leave it untouched: KEEL stays off and the data-boundary rule
        runs as strict policy. In operator mode, treat it as the package switching off a
        guard (rule of engagement 3) and stop to ask; linking the kit (`link_kit.py`)
        switches KEEL on through `keel-factory/`."
      - **S11, a v1.0 `AGENTS.md` (K20):** "If `AGENTS.md` holds KEEL's v1.0 text (the line
        `This project was started from KEEL FACTORY.`), add no block: offer MANUAL §11's
        choice, replacing that text with the block (recommended, so the layer loads once)
        or deleting it and relying on the hook, and change the file only on the owner's
        yes."
      - **S12, `<ops>` (K25):** "`<ops>` is `keel-factory/.ops/` whenever the project holds
        a `keel-factory/` (linked or copied), else `.keel/ops/`."
      - **S13, the Codex skill name (K22),** CLAUDE.md's line: "`$keel:helm` in Codex
        (`$helm` where the skills were copied into `.agents/skills/`)".
      - **S14, a copied v1.0 kit (C1):** "A project holding a copied v1.0 `keel-factory/`
        re-copies it with MANUAL §4's rsync, or replaces it with a link (`link_kit.py`);
        until then its import carries v1.0's layer beside the hook's v1.1 layer."
    - Amended at phase A's audit, 2026-10-19 (skills4's auditor; the lead's decision):
      - **S8**, its step-3 sentence, because a block can name `keel-factory/` or a nested
        repository's folder as well as `.keel/`: "If one of these checks is blocked with the
        reason 'matches this repo's .gitignore', that block is the answer: the path it names
        is ignored (`.keel/`, `keel-factory/`, or the folder that holds a nested `.keel/`).
        Do not retry another way: say which check could not be run and ask the user to look
        in that folder; in operator mode, stop before going on." OPERATOR.md takes it word
        for word in phase B.
      - **S11**, because v1.0's text holds that sentence inside a longer line: "(it says
        `This project was started from KEEL FACTORY.`)" replaces "(the line `This project
        was started from KEEL FACTORY.`)".
      - **S3b**, added before phase A's build (both HELM and OPERATOR.md): "Each `.keel/`
        found below the root is handled like the root's: read its allowlist with the Read
        tool, and run `git -C <the folder that holds it> ls-files -- .keel` to see whether its
        own repository tracks it."

21. The manager's answers at the PROVE pass 4 report, and the order of work. RESOLVED
    2026-10-20.
    - Asked through the harness's question prompt on 2026-10-20, in the session that ran
      the retrofit's PROVE pass 4, with the option texts in that session. The questions and
      answers, verbatim as received:
      - "KEEL v1.1 stopped at its PROVE pass 4 report with no major or fix-now item left, 20
        docs-only items open, and coverage at 3 of 9. What comes next for v1.1?" = "Docs
        round 5 (Recommended)". That option read: "Fix the 20 docs-only items, file 3
        follow-ons, record 4 rejects, run a closure check on those items only (on the
        current tree), then stop for PROVE and release. Accepts M2, M3, M5 and M7 as
        partial, since they need runs only you can approve."
      - "v1.1 has six contract wordings waiting: F3-1, F3-2, F3-3, F3-4, F3-6 and F4-8. ...
        Approve them?" = "Approve all six (Recommended)". That option read: "Approve all six
        as written in .scratch/v1.1/CONTRACT.md. The build already follows them, so nothing
        changes in the code."
      - "v1.1's docs round 5 and the retrofit's fifth cycle touch some of the same files.
        Which runs first?" = "Retrofit first".
    - Read as: docs round 5, then a closure check of those items only, on the tree as the
      retrofit leaves it, then a stop for PROVE and the release; M2, M3, M5 and M7 accepted
      as PARTIAL, named. F3-1 (with its third residual: a kit copy that keeps `.git` stays
      dormant), F3-2, F3-3, F3-4, F3-6 and F4-8 are approved as written: CONTRACT.md moves
      them out of "Proposed, awaiting the manager" with dated pointer lines when round 5
      starts. Round 5 starts after the retrofit's fifth cycle has landed and reported
      (`crew-plan-shimeles-retrofit`, Open question 7).

22. Docs round 5's seams and rules, decided before dispatch. RESOLVED 2026-10-20 (lead).
    Items: `.scratch/v1.1/round5/items/<lane>-items.md`.
    - **S5 widened (D4):** "KEEL's installers (`install_plugin.py`, with or without
      `--codex-hooks`, and `install_guard.py`) write machine-wide entries that run the kit
      they were run from. Run them from the master (or through a linked `keel-factory/`),
      never from a copy inside a project."
    - **S3 amended (D8, D9):** the listing is `find . -path ./keel-factory -prune -o -name
      .keel -print` (no `-type d`), and its parenthetical "(it never names the file, so
      KEEL's hook allows it, unless `.keel/` or `keel-factory` is gitignored; then (d)
      applies)". S8 gains "(the listing in (c) included)". Probe, 2026-10-20, three scratch
      projects through `keel_hook.py guard`: the old and the new command are both blocked
      (exit 2, "matches this repo's .gitignore") where `.keel/` or `keel-factory` is
      ignored, and only the new one lists a nested symlinked `.keel`. The handoff's
      candidate with quoted globs (`'*/keel-factory'`, `'[.]keel'`) was allowed in all
      three, but only because its words do not look like paths to the guard; the lead
      rejected it, since a command built to pass the guard's checks is the "another way"
      CLAUDE.md forbids, and the block, read by (d), is the safe answer.
    - **S7 narrowed (D17):** "(in Claude Code, a settings-file hook also once `/hooks` is
      opened, the plugin only from the next session; in Codex, once the hooks are trusted
      in `/hooks`)".
    - **S11 conditioned (D5 = D20):** HELM step 4 offers "deleting it and relying on the
      hook" only "where step 3's probe came back blocked (KEEL's Codex hooks wired and
      trusted)"; otherwise only the replacement. MANUAL §11's Codex bullet matches.
    - **P-K34, within budget:** CLAUDE.md qualifies only its first mention of "the session
      note", "(the SessionStart hook's context, never text in a project file)". check_kit
      must report CLAUDE.md at no more than 5,995 characters: the retrofit's R50 took it to
      5,930 of the 6,000 cap.
    - **The mirror rule (the retrofit shares this tree).** The manager chose to ship v1.1
      first and the retrofit later as 1.2.0 on its own commits (the retrofit's crew plan,
      Open question 7). Every file the retrofit touched has a pre-retrofit copy in
      `.scratch/skills-main/base/`, from which v1.1 is to be committed. So each round-5 edit
      to such a file is made in that copy too, adapted only where the retrofit changed the
      same sentence; the copies are in the lanes' write sets.
    - **Where the closure check runs:** on the current tree, as the manager's chosen option
      said; v1.1's own tree (the base copies with round 5 in them) gets its gate when the
      commits are split.
    - **Amended after the back-briefs** (lead, 2026-10-20; the answers are in
      `.scratch/v1.1/round5/plans/`). S3's "then (d) applies" points at HELM's step 3(d),
      which no other file has: DATA-BOUNDARY writes "then HELM's step 3(d) applies", and
      OPERATOR "then the rule below for a blocked check applies". S8's clause sits right
      after "If one of these checks" ("(the listing included)" in OPERATOR). S5 widened
      goes only where an agent offers the machine-wide wiring: OPERATOR's infil and
      START-PROMPTS' Claude Code and Codex prompts; OPERATOR's `$KEEL` names the master.
      Every figure P-K34 moves is moved where it is stated, measured with check_kit, the
      retrofit's own RELEASES section included (its size figures only). records5 gains
      `.scratch/v1.1/DESIGN.md`, D6's correction beside F4-4, and S11's condition in F4-6.

23. The manager's answers at the closure report (`.scratch/v1.1/PROVE-5.md`, "For the
    manager"). RESOLVED 2026-10-20. Asked through the harness's question prompt; the
    answers, verbatim as received:
    - "PROVE for v1.1: ... What now?" = "Approve, list as gaps (Recommended)". The option
      read: "Approve PROVE now. M2, M3, M5, M7 and M9 are named PARTIAL, and the 14 small
      items are listed as known gaps in 1.1.0's release notes and fixed in a follow-on."
    - "At the SPRINT tier, checkpoint mode currently means more stops than supervised
      mode ... What should checkpoint mean at SPRINT?" = "Up-front round (Recommended)".
      The option read: "Every tier keeps one up-front round in checkpoint mode. At SPRINT,
      BRIEF's one question and the BRIEF and CONTRACT approval go in one message, and
      supervised SPRINT gets the same stop, so you always see the brief before the build."
    - "... F3-1 carries a known gap: a copy of the KEEL kit that keeps its .git folder
      stays switched off in the project it was copied into. Do you accept that gap as
      approved?" = "Accept it (Recommended)".
    - Read as: PROVE is approved at `e09480c@v1.1-harness-conformance tree:c3ae134be1fa` (snapshot
      `.scratch/evidence/v1.1/closure-5.json`), with M2, M3, M5, M7 and M9 named PARTIAL.
      The approval holds only for that tree (the freshness rule), so nothing shipped
      changes now: the SPRINT change (TIERS, the keel skill, PHASES where it names stops)
      and the 14 small items go into `v1-1-closure5-open-items`, and RELEASES' 1.1.0
      known gaps are written at the commit split, where v1.1's own tree gets its gate run
      again. F3-1's residual is accepted as CONTRACT.md's approved F3-1 entry states it;
      CONTRACT needs no edit.

## Owner

The lead owns this plan, the board, row 11 and the landing. Each worker owns only its
lane. Budget: one workflow run per phase, 16 worker calls in all (a back-brief and a build
per lane), each worker stopping at about 120 tool calls; one headless `claude -p` probe
for row 11 on the manager's Max plan, capped at $0.40.

## Execution log

- **Docs round 5, dispatched 2026-10-20** (the manager's answer: Open question 21; the
  lead's seams and rules: Open question 22). Snapshot `.scratch/v1.1/round5/snap.json`
  (stamp `tree:a1005aadd83e`), taken before the lead's own edits. Before the build the
  lead probed S3's listing through `keel_hook.py guard` in three scratch projects
  (recorded in Open question 22), did its own items (D11 and P-C5 in HARNESS-PROBES and
  its base copy; D6, D18, the three follow-ons and item 9's relabel on the board and in
  STATE; the four rejects in PROVE-4.md; dated corrections in PROVE-3.md and Open
  question 20). Back-brief (run `wf_3bd88860-88b`, 5 agents, about 0.64M tokens): every
  plan inside its write set; 17 questions answered in `.scratch/v1.1/round5/plans/`.
  Build, audit and fix-up dispatched as run `wf_ffb58839-36f`.
- **2026-10-20, during the build:** another session in this folder, at the manager's
  request, sent two findings from a live dry run of the working tree (Claude Code 2.1.304,
  the installed plugin; `.scratch/evidence/dryrun-2026-10-20/FINDINGS.md`). The lead
  checked both against the files and the trace and filed them:
  `owner-deferred/sprint-checkpoint-stops` (checkpoint has more stops than supervised at
  SPRINT; the manager's decision) and `helm-probe-order` (the first session probed the
  guard before writing `.keel/keel.json` and gave no "not armed" notice). The second is
  slotted into this round as a lead fix in HELM and OPERATOR (and their base copies) once
  skills5 and protocols5 have landed, re-tested by the closure check.
- **Docs round 5, back and landed, 2026-10-20** (run `wf_ffb58839-36f`: 12 agents, about
  1.57M tokens, 20 minutes). All five lanes returned done with nothing outside their write
  sets. Three audits were complete; protocols5's found 1 gap (D1's wording against the
  code: only an allowlist stalls the guard, an instruction file stalls the session hook)
  and records5's 3 (R8's figures, dated lines beside F4-3 and F4-4); both fix-ups
  returned done, and the lead read the changed text instead of a re-audit. The lead then:
  moved the size figures P-K34 changed in README and HARNESS-PROBES (live CLAUDE.md 5,994,
  session 6,428; v1.1's own 5,595 and 6,029); made DR-2's fix (`helm-probe-order`) in
  HELM step 3(a) and OPERATOR's infil and their base copies; gave DATA-BOUNDARY.md and
  settings.hooks.codex.json base copies equal to the live files (the retrofit never
  touched them), so v1.1's edits stay out of the retrofit's review diff; regenerated that
  diff (its body differs from fix round 4's only in the moved figures and two context lines
  in crew/assets/brief.md's first hunk, D7's KEEL role entry, made in both copies; its path
  list gains DATA-BOUNDARY.md and settings.hooks.codex.json, both with empty diffs;
  corrected after the closure check, RECORDS-N6) and the
  retrofit's prose expectation (one line's figure); declared the peer session's dry-run
  folder as its own row; added a v1.1 lane to the retrofit's `lanes-build.md`. Checks:
  this run's fence against `round5/snap.json`, 74 paths, no findings; the retrofit's
  whole-run fence, 291 paths, no findings; R1 to R7 and R13 plus the two retrofit suites,
  343 tests OK; R8 check_kit no findings; R9 exit 0 with the one expected warning (the
  2.1.304 CLI adds a README "Advice" line that does not change the verdict); R10 44 tasks,
  no findings; R11 `keel@skills-dir` loaded; R12 17 `keel:*` skills (the installed Codex
  links predate the retrofit). R10's and R13's counts differ from ACCEPTANCE's because
  the retrofit shares the tree; v1.1's own counts are re-measured at the commit split.
  K23's MANUAL half (P-K23) is closed by guides5. Mutation, each list after an identity
  baseline: keel_hook 93/93, check_kit 36/36, install_guard 18/18, install_plugin 29/29,
  make_release 33/33 (209; `.scratch/v1.1/round5/mutation/`).
- **The closure check, 2026-10-20** (run `wf_a0f42b9e-9fb`: 8 agents, about 1.34M tokens;
  snapshot `.scratch/evidence/v1.1/closure-5.json`, stamp `tree:c3ae134be1fa`; fresh at
  every checker's start and end). Of pass 4's 27 items, 26 fixed and S4-a1 partly (the
  lead's own reject reason was wrong: it said the residual was quoted in the manager's
  option text; corrected in `PROVE-4.md`, and the residual goes to the manager again);
  DR-2 fixed; the mirror rule holds. New: 19 items, none refuted, 4 minor and 15 nit, 0
  major, 0 fix-now; 6 closed at the report as records or a follow-on, 14 filed as
  `v1-1-closure5-open-items`; `helm-probe-order` done. Coverage 4 / 9 (M8 to PASS).
  Report: `.scratch/v1.1/PROVE-5.md`. **Stopped for the manager's word on PROVE and the
  release.** Docs round 5 and its closure check cost 25 agents and about 3.55 million
  subagent tokens.
- **2026-10-20: PROVE approved by the manager** (Open question 23, verbatim), at the
  closure-checked tree, with M2, M3, M5, M7 and M9 named PARTIAL; the SPRINT decision and
  the 14 small items go to `v1-1-closure5-open-items`, to land with their own check; the
  release-note gaps are written at the commit split.

- Fix round 4, phase B's lanes table, as it stood (superseded by docs round 5's):

  Lanes (fix round 4, phase B)

  | Lane | Owner | Tasks | Writes | Mode |
  | --- | --- | --- | --- | --- |
  | reconcile4 | worker-reconcile | RELEASES' "Fixed after PROVE pass 3" and figures; ACCEPTANCE's counts; DESIGN §2; CONTRACT's F4 record; OPERATOR's amended S8 | `RELEASES.md`, `OPERATOR.md`, `.scratch/v1.1/ACCEPTANCE.md`, `.scratch/v1.1/DESIGN.md`, `.scratch/v1.1/CONTRACT.md` | shared |
  | lead | lead | plan, board, landing, PROVE pass 4 and its report | `.scratch/task_board/`, `.scratch/v1.1/STATE.md`, `.scratch/v1.1/TRACEABILITY.md`, `.scratch/v1.1/PROVE-3.md`, `.scratch/v1.1/PROVE-4.md`, `.scratch/v1.1/round4/`, `keel/framework/HARNESS-PROBES.md`, `.scratch/handoff.md`, `.scratch/handoff-superseded-2026-10-19.md` | shared |


Base for every lane: branch `v1.1-harness-conformance` at `e09480c`, plus the
uncommitted v1.1 work (48 `git status` entries at dispatch), fingerprinted by the lead's
snapshot before each phase.

**Phase 1 lanes (landed), as dispatched:**

| Lane | Owner | Tasks | Writes | Mode |
| --- | --- | --- | --- | --- |
| hook | worker-hook | rows 1, 2 (hook side), 3 (hook side) | `harness/hooks/keel_hook.py`, `harness/hooks/test_keel_hook.py`, `harness/plugin-hooks.json`, `.scratch/v1.1/tools/mut-hook.json` | shared |
| skills | worker-skills | rows 4, 5 | `keel/skills/helm/`, `keel/skills/keel/`, `keel/skills/keel-prove/`, `keel/skills/crew/SKILL.md`, `keel/skills/crew/agents/`, `keel/capabilities/deep-research/`, `keel/capabilities/reverse-engineering/` | shared |
| instrument | worker-instrument | row 6 | `harness/check_kit.py`, `harness/test_check_kit.py`, `.scratch/v1.1/tools/mut-check.json` | shared |
| installers | worker-installers | rows 7, 8, 10, row 2 (Codex wiring) | `harness/install_plugin.py`, `harness/test_install_plugin.py`, `harness/install_guard.py`, `harness/test_install_guard.py`, `harness/make_release.py`, `harness/settings.hooks.codex.json`, `.scratch/v1.1/tools/mut-install.json`, `.scratch/v1.1/tools/mut-install-guard.json`, `OPERATOR.md` | shared |
| layer | worker-layer | row 9 (layer, framework, agents), row 3 (CLAUDE.md sentence), COMPLETENESS-15 | `CLAUDE.md`, `keel/framework/LOOPS.md`, `keel/framework/TIERS.md`, `keel/framework/CAPABILITIES.md`, `agents/` | shared |
| guides | worker-guides | row 9 (user guides) | `README.md`, `QUICKSTART.md`, `MANUAL.md` | shared |
| reference | worker-reference | row 9 (reference docs) | `START-PROMPTS.md`, `ARCHITECTURE.md`, `harness/README.md`, `harness/DATA-BOUNDARY.md`, `RELEASES.md` | shared |
| records | worker-records | row 12, record fixes in row 9 | `.scratch/v1.1/CONTRACT.md`, `.scratch/v1.1/BRIEF.md`, `.scratch/v1.1/DESIGN.md`, `.scratch/v1.1/ACCEPTANCE.md`, `.scratch/v1.1/briefs/` | shared |
| lead | lead | plan, board, row 11, landing, PROVE report | `.scratch/task_board/`, `.scratch/v1.1/STATE.md`, `.scratch/v1.1/TRACEABILITY.md`, `.scratch/v1.1/PROVE-FINDINGS.md`, `.scratch/v1.1/PROVE-2.md`, `.scratch/v1.1/trials/`, `keel/framework/HARNESS-PROBES.md`, `keel/framework/CREW.md` | shared |

**Phase 1 — back-briefs 2026-10-18.** All five returned plans with every file inside the
lane (checked by script) and raised real premises: the generic mutation runner never runs
the unbroken suite (so every lane proved its baseline green first); `test_install_guard.py`
pins the fallback command to `OPERATOR.md`'s copy (so `OPERATOR.md` moved to `installers`
for phase 1); KEEL's research contradicts row 2 on Claude Code reading a lone `AGENTS.md`
(narrowed, Open question 14). Answers recorded in Open question 14.

**Phase 1 — landed 2026-10-18, all five lanes together** (the installers' Codex commands
depend on the hook's new `--harness`).
- Fence: the dispatch snapshot (SHA-256 per file, 395 files) diffed against the tree gave
  31 changed paths; `check_lanes.py --changed -` over them: no findings. Each lane's share
  equals the files its worker reported (hook 4, skills 8, instrument 3, installers 9,
  layer 7). The fence was first shown failing on a stray path and a cross-lane path.
- Gate: self-tests guard 27, keel_hook 76, link_kit 9, install_guard 13, install_plugin 24,
  check_kit 34, check_lanes 21 (204, all OK); `check_kit.py` OK with no findings (80 skill
  paths, 22 codex skills); plugin validate passed with the one expected warning; board OK.
  Mutation proofs, each with an unmutated baseline green on the same kit: keel_hook 49/49,
  install_plugin 15/15, install_guard 11/11 (R4 seen failing for the first time), check_kit
  36/36.
- Lead review: read the switch-on code against Open question 3 and CLAUDE.md's
  data-boundary section in full; both as decided.
- Row 11 (lead): live run L8, recorded in `keel/framework/HARNESS-PROBES.md`: a
  `general-purpose` and an `Explore` subagent each had their Read of `.env` blocked by the
  plugin's hook in a `.keel/` project; the fake value never reached the trace.
- Carried to phase 2: stale docs named by the workers (DATA-BOUNDARY's quoted command,
  `~/.codex/hooks.json` mentions, "three reviewers", ARCHITECTURE's "holds no state",
  OPERATOR's infil and failed-probe text, RELEASES' counts); a self-test for
  `make_release.py`; a clear message for a failed `hooks.json` write. Follow-ons, not this
  run: Codex's `AGENTS.override.md`; the old hook-only mutation runner, now superseded by
  `mut-hook.json` on the generic runner (its anchors no longer match, so it stops at its
  first assert rather than passing silently).

**Phase 2 lanes (landed), as dispatched:**

| Lane | Owner | Tasks | Writes | Mode |
| --- | --- | --- | --- | --- |
| guides | worker-guides | row 9 (user guides) | `README.md`, `QUICKSTART.md`, `MANUAL.md` | shared |
| reference | worker-reference | row 9 (reference docs) | `START-PROMPTS.md`, `OPERATOR.md`, `ARCHITECTURE.md`, `harness/README.md`, `harness/DATA-BOUNDARY.md`, `RELEASES.md`, `agents/` | shared |
| records | worker-records | row 12, record fixes in row 9, G1 | `.scratch/v1.1/CONTRACT.md`, `.scratch/v1.1/BRIEF.md`, `.scratch/v1.1/DESIGN.md`, `.scratch/v1.1/ACCEPTANCE.md`, `.scratch/v1.1/briefs/` | shared |
| scripts | worker-scripts | rows 7 and 10 follow-through | `harness/make_release.py`, `harness/test_make_release.py`, `harness/install_plugin.py`, `harness/test_install_plugin.py`, `.scratch/v1.1/tools/mut-release.json`, `.scratch/v1.1/tools/mut-install.json` | shared |
| lead | lead | plan, board, row 11, landing, PROVE report | `.scratch/task_board/`, `.scratch/v1.1/STATE.md`, `.scratch/v1.1/TRACEABILITY.md`, `.scratch/v1.1/PROVE-FINDINGS.md`, `.scratch/v1.1/PROVE-2.md`, `.scratch/v1.1/trials/`, `keel/framework/HARNESS-PROBES.md`, `keel/framework/CREW.md` | shared |

**Phase 2 — back-briefs 2026-10-18.** All four plans inside their lanes. Premises worth
keeping: README-FIRST's detached `git checkout v<tag>` would strand `main` on the upgrade
pull and make the next release refuse; the R3 and R7 seen-failing records live in the v1.0
handoff (`git show e09480c:.scratch/handoff.md`), not the file pass 1 cited. Answers in
Open question 15.

**Phase 2 — landed 2026-10-18, all four lanes together.**
- Fence: 23 changed paths since the phase-2 snapshot, `check_lanes.py --changed -`: no
  findings; each lane's share equals its worker's list (guides 3, reference 9, records 5,
  scripts 6).
- Gate: self-tests guard 27, keel_hook 76, link_kit 9, install_guard 13, install_plugin 28,
  check_kit 34, make_release 13 (new), check_lanes 21 (221, all OK); `check_kit.py` OK, no
  findings (228 links); plugin validate passed with the one expected warning; board OK;
  R11 `keel@skills-dir` loaded; R12 17 `keel:*` skills listed from 18 links (`commit` is
  hidden by its own metadata, probe X9). Mutation proofs, each baseline green first:
  keel_hook 49/49, check_kit 36/36, install_plugin 22/22, install_guard 11/11,
  make_release 18/18 (R13 seen failing for the first time).
- Carried to the reconcile lane: the scripts lane measured that a fresh clone of a release
  bundle lands on whichever branch sits at HEAD's commit (on a sibling
  `v1.1-harness-conformance`, not `main`), so README-FIRST and MANUAL §3 clone with
  `--branch main`; MANUAL's self-test list and harness/README's release entry lack the new
  suite; ACCEPTANCE's seen-failing rows predate the phase-2 runs; CONTRACT gets one line
  that HELM's layer read and gitignore warning serve approved D3 and D5.
- Follow-ons named, not this run: an unreadable `hooks.json` reports the wrong cause; a
  partial `hooks.json` write is not atomic; START-PROMPTS' hand-wired project-level
  `./.codex/hooks.json` is unprobed; Codex's `AGENTS.override.md`.

**Reconcile lane — landed 2026-10-18 (lead).** README-FIRST and MANUAL §3 clone with
`--branch main` (a new test reproduced the clone landing on a sibling work branch first,
and its behavior check alone failed on the old text); MANUAL's self-test list and
harness/README name `test_make_release.py`; ACCEPTANCE's seen-failing rows cite the gate
runs; CONTRACT records HELM's layer read and gitignore warning as serving approved D3 and
D5. Fence: 7 paths, all in the lane.

**Row 13 — 2026-10-18.** All eight self-tests (221) OK; check_kit, plugin validate, board,
R11 and R12 pass; mutation proofs with baselines: 49/49, 36/36, 22/22, 11/11, 19/19.

**PROVE pass 2 — 2026-10-18: does not pass** (`.scratch/v1.1/PROVE-2.md`). Three
`keel:prove-*` reviewers, four closure checkers, one critic, then ten skeptics: 68 of 76
pass-1 verdicts fixed, 8 partly; 60 new or remaining items verified, none refuted; three
distinct major defects (N2 = N35, a regression from this run's row 1; N36; N37, from v1.0);
traceability 3 PASS, 5 PARTIAL, 1 FAIL (M8). Waiting on the manager. This plan stays
`in-progress` until PROVE passes.

**Data-boundary action, 2026-10-18, on the manager's "Yes" (Open question 16).** Ran
`python3 -B harness/install_guard.py --remove`: "removed KEEL's guard from
~/.claude/settings.json; every other setting kept". A second run: "nothing to remove". The
file's contents were never opened. Then the plugin's wired PreToolUse command, run as
`plugin-hooks.json` states it, blocked a Read of `.env` (exit 2) in a scratch `.keel/`
project and in a scratch linked-kit project.

**Fix round 3, phase A lanes (landed), as dispatched:**

| Lane | Owner | Tasks | Writes | Mode |
| --- | --- | --- | --- | --- |
| hook3 | worker-hook | N2 = N35, N36 with N3 | `harness/hooks/keel_hook.py`, `harness/hooks/test_keel_hook.py`, `.scratch/v1.1/tools/mut-hook.json` | shared |
| installers3 | worker-installers | N37, N43, N44, install_plugin's docstring | `harness/install_guard.py`, `harness/test_install_guard.py`, `harness/install_plugin.py`, `harness/test_install_plugin.py`, `harness/settings.hooks.json`, `OPERATOR.md`, `.scratch/v1.1/tools/mut-install.json`, `.scratch/v1.1/tools/mut-install-guard.json` | shared |
| release3 | worker-release | N11 | `harness/make_release.py`, `harness/test_make_release.py`, `.scratch/v1.1/tools/mut-release.json` | shared |
| skills3 | worker-skills | N23, N28, N25, N9, N24, N33 (HELM's part) | `keel/skills/`, `keel/capabilities/` | shared |
| layer3 | worker-layer | P-B as an exception, N4 with N34, N13, N15, N40 (CAPABILITIES' part) | `CLAUDE.md`, `keel/framework/CAPABILITIES.md` | shared |
| lead | lead | plan, board, landing, PROVE report | `.scratch/task_board/`, `.scratch/v1.1/STATE.md`, `.scratch/v1.1/TRACEABILITY.md`, `.scratch/v1.1/PROVE-FINDINGS.md`, `.scratch/v1.1/PROVE-2.md`, `.scratch/v1.1/PROVE-3.md`, `.scratch/v1.1/trials/`, `keel/framework/HARNESS-PROBES.md`, `keel/framework/CREW.md`, `.scratch/handoff.md`, `.scratch/handoff-superseded-2026-10-18.md` | shared |

**Fix round 3, phase A — landed 2026-10-18, five lanes together.** Back-briefs: all five plans
inside their lanes; answers in Open question 18 (the skills lane found that the decided
allowlist check named the file, which KEEL's own hook blocks; the lead recorded probe X10
for the layer lane's uncited row). Fence: 23 changed paths since the phase-A snapshot (21
from workers, 2 board files of the lead's), `check_lanes.py --changed -`: no findings; each
lane's share equals its worker's list. Gate: self-tests 27, 86, 9, 18, 30, 34, 14, 21 (239,
all OK); check_kit OK (91 skill paths, CLAUDE.md 5,469 characters, session 5,903); plugin
validate with the one expected warning; board OK; mutation proofs, each baseline green first:
keel_hook 62/62, check_kit 36/36, install_plugin 27/27, install_guard 18/18, make_release
25/25. End to end (worker evidence): an rsync copy of the kit wired from its own hooks now
blocks `.env` and injects the layer; the master named `keel-factory` with its own `.git`, seen
from its parent, stays dormant; a project's always-allow guard copy no longer disarms the
machine-wide fallback.


**Fix round 3, phase B — landed 2026-10-19.** A usage limit had cut off reference3's and
records3's first builds mid-edit, unreported (guides3 had finished). A new session
re-dispatched both in build mode with their approved plans and a resume note, then had a
fresh read-only auditor check every plan item against the files; each lane got a fix-up
and a re-audit. A repair round then audited guides3 for the first time and fixed what all
three audits left (MANUAL's `git clean -f` claim; the OPERATOR prose order; the Inferred
token figure moved out of RELEASES' Evidence table; F3-7's full list of the Gate's added
rules; F3-7's reading of D7 recorded as a proposal for the PROVE pass 3 report, since
pass 2's verifier wrote it as one). A last narrow repair, checked by the lead with
whitespace-normalised greps, made the clean/stash sentence identical in OPERATOR §3 and
MANUAL §10 (the lead verified in a scratch repo: plain `git clean` removes a `keel-factory`
that is a single link; `-d` is needed for `.keel/`; the `-e` form keeps both). The lead
filed two pass-2 follow-ons the audit found unfiled: N33's code half (item 5 of
`keel-hook-hardening`) and N33's role sub-claim (`helm-role-override`); PROVE-2's table
lists both.

- Fence: the old pre-phase-B snapshot was lost with the previous session's scratchpad, so
  a fresh one (430 files) was taken before the re-dispatch; the earlier partial edits rest
  on the previous session's fence (13 paths, all inside lanes) and on no file changing
  after the handoff was written. Diff at landing: 18 changed paths, `check_lanes.py
  --changed -`: no findings; each lane's share equals its workers' lists (guides3:
  MANUAL, README; reference3: ARCHITECTURE, OPERATOR, RELEASES, harness/DATA-BOUNDARY,
  harness/README; records3: ACCEPTANCE, BRIEF, CONTRACT, DESIGN; lead: the board, PROVE-2,
  the round-3 scripts).
- Gate and full re-run (row 13): self-tests 27, 86, 9, 18, 30, 34, 14, 21 (239, all OK);
  check_kit OK (91 skill paths, `CLAUDE.md` 5,469 characters, session 5,903, 213 docs, 229
  links); plugin validate with the one expected warning; board OK, 26 tasks; R11
  `keel@skills-dir` 1.1.0 loaded; R12 17 `keel:*` skills. Mutation proofs, each identity
  baseline "MISSED baseline-identity OK" first: keel_hook 62/62, check_kit 36/36,
  install_plugin 27/27, install_guard 18/18, make_release 25/25 (168, all caught). In the
  mutation mirror (no `.git`) one keel_hook test skips; the live suite skips none.
- Cost: three workflow runs, 18 agents, about 3.2 million subagent tokens (1,792,922;
  1,168,627; 257,100), on the manager's plan. No Codex model call.
- Disclosed by a worker: one `find` listing printed the name of a gitignored `__pycache__`
  file; its contents were never opened.

**PROVE pass 3 — 2026-10-19: does not pass yet** (`.scratch/v1.1/PROVE-3.md`). Three
`keel:prove-*` reviewers, four closure checkers, two fresh critics (new user; fail-open),
then twenty-seven skeptics (three lenses per claimed major, one per area). Gate: all 13
Required Checks exit 0; R9 newly armed by Evidence. Closure of pass 2: 64 fixed, 5 partly,
none regressed; its three majors are closed. New: 49 distinct items, none refuted; 0 major
after verification (five of the seven claimed majors had one "major" vote, from the
reproduce lens), 34 minor, 15 none; 5 fix-now (K30 and K31, fail-open paths in
`keel_hook.py`; C14, C15, K20 in HELM and the skills), 28 docs-only, 5 follow-on, 10
reject, 1 for the manager (F3-7). Traceability 3 PASS, 6 PARTIAL, 0 FAIL (M8 FAIL →
PARTIAL). What this phase caught that the fix round's own audits did not: the two fail-open
paths, the Monitor and nested-repo limits, and that PROVE-2 never verified N10, N12 and N20
(C9). Cost: 36 agents, about 5.8 million subagent tokens. Waiting on the manager; this plan
stays `in-progress`.

**Fix round 3, phase B lanes (landed), as dispatched:**

| Lane | Owner | Tasks | Writes | Mode |
| --- | --- | --- | --- | --- |
| guides3 | worker-guides | round-3 items in the user guides | `README.md`, `QUICKSTART.md`, `MANUAL.md` | shared |
| reference3 | worker-reference | round-3 items in the protocols, reference docs and release notes | `START-PROMPTS.md`, `OPERATOR.md`, `ARCHITECTURE.md`, `harness/README.md`, `harness/DATA-BOUNDARY.md`, `RELEASES.md` | shared |
| records3 | worker-records | the manager's approvals into CONTRACT; record fixes | `.scratch/v1.1/CONTRACT.md`, `.scratch/v1.1/BRIEF.md`, `.scratch/v1.1/DESIGN.md`, `.scratch/v1.1/ACCEPTANCE.md` | shared |
| lead | lead | plan, board, landing, PROVE report, HELM's one copied-kit word, scratch tools | `.scratch/task_board/`, `.scratch/v1.1/STATE.md`, `.scratch/v1.1/TRACEABILITY.md`, `.scratch/v1.1/PROVE-FINDINGS.md`, `.scratch/v1.1/PROVE-2.md`, `.scratch/v1.1/PROVE-3.md`, `.scratch/v1.1/trials/`, `.scratch/v1.1/tools/`, `.scratch/v1.1/round3/`, `keel/framework/HARNESS-PROBES.md`, `keel/framework/CREW.md`, `keel/skills/helm/SKILL.md`, `.scratch/handoff.md`, `.scratch/handoff-superseded-2026-10-18.md` | shared |

**Fix round 4, phase A — landed 2026-10-19.** Six lanes back-briefed (all plans inside
their write sets; the lead's answers in `.scratch/v1.1/round4/plans/`), then built. The first
builds were cut off by a session limit with partial edits in their lanes and no returns; the
lead fenced the partial tree (every path inside its lane), then re-dispatched all six with
resume notes. Each lane was audited by a fresh reader and repaired: hook4's audit found two
new tests no mutant turned red (mutants added), skills4's found three real defects (S8 named
only `.keel/`, S11 called v1.0's sentence a line, and S10 moved what HELM's "Otherwise"
referred to; the amended seams are in Open question 20), boundary4, guides4 and records4 one
or two each, protocols4 none. The lead fixed the generic mutation runner in the tools folder
to mirror only what git lists (no ignored file is copied any more; earlier rounds' runs may
have copied an ignored `.DS_Store` into their temp mirrors, deleted after each mutant), and
filed the follow-ons and recorded the rejects (PROVE-3.md).

- Fence: the snapshot taken before the back-briefs (443 files). At landing, 47 changed
  paths; `check_lanes.py --changed -` names only the runner, the lead's own edit made before
  the builds (its sha256, 6b108429…2384, unchanged since). Each lane's share equals its
  workers' lists: hook4 keel_hook.py, its test and mut-hook.json; skills4 the four skills;
  boundary4 DATA-BOUNDARY, harness/README, CAPABILITIES; protocols4 CLAUDE.md, OPERATOR,
  START-PROMPTS, RELEASES; guides4 MANUAL, README; records4 CONTRACT, ACCEPTANCE.
- Gate: self-tests 27, 108, 9, 18, 30, 34, 14, 21 (261, all OK); check_kit OK (91 skill
  paths, `CLAUDE.md` 5,531 characters, session 5,965, 213 docs, 236 links); plugin validate
  with the one expected warning; board OK, 27 tasks; R11 loaded. Hook mutation proof,
  identity baseline "MISSED baseline-identity OK" first: keel_hook 93/93.
- Cost: back-briefs 6 agents, 1,064,063 subagent tokens; the cut-off builds 12 agents,
  896,660; the re-dispatched builds, audits and fix-ups 17 agents, 3,022,808. No Codex model
  call.

**Fix round 4, phase A lanes (landed), as dispatched:**

| Lane | Owner | Tasks | Writes | Mode |
| --- | --- | --- | --- | --- |
| hook4 | worker-hook | K30, K31 (fail-open paths in the hook); K25's operator note in the hook | `harness/hooks/keel_hook.py`, `harness/hooks/test_keel_hook.py`, `.scratch/v1.1/tools/mut-hook.json` | shared |
| skills4 | worker-skills | C14, C15, K20, K35 and the skill halves of K19, K25, K26, C4, K34 | `keel/skills/` | shared |
| boundary4 | worker-boundary | K18, K19, K29, K32, K36, C4, C8, K23, C2, C5, K27, C3 in the reference docs | `harness/DATA-BOUNDARY.md`, `harness/README.md`, `keel/framework/CAPABILITIES.md` | shared |
| protocols4 | worker-protocols | C4, C14, K19, K25, K35, K26, K21, K22, K23, C1, C2, K29, K32, K18 in the protocols, release notes and layer | `OPERATOR.md`, `START-PROMPTS.md`, `RELEASES.md`, `CLAUDE.md` | shared |
| guides4 | worker-guides | K18, K19, K32, C1, C2, K25, K28, C7, C3 in the user guides | `README.md`, `QUICKSTART.md`, `MANUAL.md` | shared |
| records4 | worker-records | S-a1, C11, C12 = S-c2, S-c1, C2, C13 in the records | `.scratch/v1.1/CONTRACT.md`, `.scratch/v1.1/ACCEPTANCE.md` | shared |
| lead | lead | plan, board, follow-ons and rejects, C9, C17, C5's probe preamble, landing, PROVE report | `.scratch/task_board/`, `.scratch/v1.1/STATE.md`, `.scratch/v1.1/TRACEABILITY.md`, `.scratch/v1.1/PROVE-2.md`, `.scratch/v1.1/PROVE-3.md`, `.scratch/v1.1/PROVE-4.md`, `.scratch/v1.1/round3/`, `.scratch/v1.1/round4/`, `keel/framework/HARNESS-PROBES.md`, `.scratch/handoff.md`, `.scratch/handoff-superseded-2026-10-19.md` | shared |

**Fix round 4, phase B — landed 2026-10-19.** One reconcile lane, built, audited and
repaired: RELEASES' "Fixed after PROVE pass 3" list and figures, ACCEPTANCE's counts,
DESIGN §2 for the hook's changes, CONTRACT's dated F4 record (F4-1 to F4-7 carry out their
findings; F4-8, the `<ops>` rule, rewords D2 and P-H, so it is proposed for the PROVE pass 4
report beside F3-1, F3-2, F3-4 and F3-6), and OPERATOR.md's amended S8. The audit found one
gap (no pointer under A5 for F4-2), fixed. A lead's error: the brief's template string held
unescaped backticks, so the build and audit agents received "NaN" as the brief; both read
the brief from the script file instead and said so. The script is fixed; phase A's six
briefs were checked and were intact. The lead kept F4-6 (S11) as a change, not a proposal,
and notes for pass 4 that S11's "delete it and rely on the hook" holds only where Codex's
hooks are wired (Inferred).

- Fence: a snapshot taken before phase B; at landing, 8 changed paths, `check_lanes.py
  --changed -`: no findings (reconcile4: RELEASES, OPERATOR, ACCEPTANCE, DESIGN, CONTRACT;
  lead: its round-4 scripts and results).
- Full re-run (row 13): self-tests 27, 108, 9, 18, 30, 34, 14, 21 (261, all OK); check_kit
  OK (CLAUDE.md 5,531 characters, session 5,965, 213 docs, 236 links); plugin validate with
  the one expected warning; board OK, 27 tasks; R11 loaded; R12 17 `keel:*` skills.
  Mutation proofs, each identity baseline green first: keel_hook 93/93, check_kit 36/36,
  install_plugin 27/27, install_guard 18/18, make_release 25/25 (199 broken copies, all
  caught).
- Cost: 3 agents, 636,615 subagent tokens. No Codex model call.

**PROVE pass 4 — 2026-10-19: does not pass outright** (`.scratch/v1.1/PROVE-4.md`).
Closure-focused, as the manager chose: three `keel:prove-*` reviewers and five closure
checkers over pass 3's 49 items, no new critic; then four skeptics. Gate: all 13 Required
Checks exit 0, each with its scope; R11 and R12 re-armed. Closure of pass 3: 72 verdicts
fixed, 6 partly, none regressed; K30 and K31 reproduced as fixed. New: 27 distinct items,
none refuted; 0 major, 18 minor, 9 none; 0 fix-now, 20 docs-only (14 from fix round 4's own
wording), 3 follow-on, 4 reject. Verification also found F3-3 narrows P-C's approved words,
so it joins the contract question. Traceability 3 PASS, 6 PARTIAL, 0 FAIL. A reviewer
listed folder names under `~/.claude/skills` by mistake (disclosed in the report). Cost: 12
agents, about 2.1 million subagent tokens. Waiting on the manager; this plan stays
`in-progress`.
