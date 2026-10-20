# State: KEEL v1.1 — harness conformance

## Phase state

| Phase | Status |
|---|---|
| 0 — RECON | done 2026-10-18 (`RECON.md`, `keel/framework/HARNESS-PROBES.md`) |
| 1 — BRIEF | **APPROVED** 2026-10-18 |
| 2 — CONTRACT | **APPROVED** 2026-10-18 |
| 3 — DESIGN | written 2026-10-18 (`DESIGN.md`); checkpoint mode, not a blocking stop |
| 4 — SLICE | done 2026-10-18, no stop (checkpoint); 13 slices closed on `.scratch/task_board/` |
| 5 — PROVE | **in progress**: pass 1 (52 findings) → fix run → pass 2 (`PROVE-2.md`, did not pass: 3 majors) → the manager picked fix round 3 → pass 3. Fix round 3: phase A (code, skills, layer) landed and gated 2026-10-18; phase B (docs, records) landed 2026-10-19 after reference3 and records3 were re-dispatched (a usage limit had cut off their first builds), each lane audited by a fresh reader and repaired (the crew plan's execution log). PROVE pass 3 run 2026-10-19 (`PROVE-3.md`): does not pass yet; 0 majors after verification, 5 fix-now items open (two fail-open paths in `keel_hook.py`); coverage 3 / 9. The manager picked fix round 4 → pass 4 (crew plan Open question 20, verbatim). Fix round 4 landed 2026-10-19 (phases A and B, each fenced and gated; the full re-run's mutation proofs 199/199). PROVE pass 4 ran 2026-10-19 (`PROVE-4.md`): no major and no fix-now item; 20 docs-only, 3 follow-ons, 4 rejects; coverage 3 / 9. The manager approved docs round 5 and all six contract wordings on 2026-10-20 (crew plan Open question 21, verbatim), after the retrofit's fifth cycle. Docs round 5 landed 2026-10-20 (run `wf_ffb58839-36f`, fenced and gated; the crew plan's "Docs round 5, back and landed"; the five mutation proofs 209/209 after identity baselines). The closure check of pass 4's items on the current tree (`PROVE-5.md`): 26 of 27 fixed, S4-a1 partly; the dry run's DR-2 fixed; 19 new small items, none major or fix-now (6 records closed at the report, 14 in `v1-1-closure5-open-items`); coverage 4 / 9. **APPROVED** 2026-10-20 at `e09480c@v1.1-harness-conformance tree:c3ae134be1fa`, snapshot `.scratch/evidence/v1.1/closure-5.json` (the manager's answer, crew plan Open question 23), with M2, M3, M5, M7 and M9 named PARTIAL and 14 small items as known gaps. Next, only on the manager's word: the release steps. |

**Tier:** STANDARD
**Stop mode:** checkpoint — the manager approved BRIEF and CONTRACT together by answering
the one question round; the next blocking stop is the PROVE report.
**Branch:** `v1.1-harness-conformance` (from `main` at `v1.0.0`). Nothing committed yet;
committing waits for the manager's word. **Resume from `.scratch/handoff.md` (2026-10-19).**

## Notes for a fresh session

The manager's answers, 2026-10-18, verbatim picks:

- Stop mode default: "Checkpoint; PLATFORM supervised (Recommended)".
- Guard scope: "KEEL projects only (Recommended)".
- Install now: "Yes, Claude Code and Codex (Recommended)" — the links
  `~/.claude/skills/keel` and one per skill in `~/.agents/skills/`. Writing
  `~/.codex/hooks.json` was not part of what was offered, so it needs its own yes.
- Trial budget: "i have the claude max plan, so as long as I'm not spending any more
  from my plan, have fun". `ANTHROPIC_API_KEY` is unset (checked), so `claude -p` runs on
  the plan. This covers Claude runs only; a Codex model call needs its own yes.

Research behind every decision: `research-*.md` in the session scratchpad, summarized in
`CONTRACT.md` §2 and `keel/framework/HARNESS-PROBES.md`. The scratchpad does not survive the session; anything
load-bearing is copied into these files.

## Blocked / open

- `claude plugin eval` needs Claude Code ≥ 2.1.269 (this machine: 2.1.170). Evals stay a
  manual gate.
- A live Codex probe of the hooks needs a Codex model call (not yet approved).

- **Contract amendments:** all answered by the manager 2026-10-18 (A1–A4 + three wording
  fixes; then P-A, P-C–P-H "All as written", P-B as an explicit exception). Recorded in
  `CONTRACT.md` "Amendments" (with fix round 3's F3 changes); verbatim picks in the crew
  plan's Open questions 2 and 16.
- **Answered at the PROVE pass 4 report, 2026-10-20** (crew plan Open question 21,
  verbatim): docs round 5, then a closure check; F3-1 (with its third residual), F3-2,
  F3-3, F3-4, F3-6 and F4-8 approved as written. F3-7's reading of D7 and the
  8,000-character listing bound were approved 2026-10-19.
- **The retrofit shares this tree** (its crew plan, `crew-plan-shimeles-retrofit`): v1.1
  ships first as 1.1.0, committed from the pre-retrofit copies in
  `.scratch/skills-main/base/`, which round 5 edits too (Open question 22's mirror rule).
- **The v1.0 machine-wide guard hook:** removed 2026-10-18 on the manager's yes.
- **At commit time (the manager's call):** whether `.scratch/v1.1/` (records, `round3/`,
  `round4/`) is committed, and how much of it (PROVE pass 3, T9).
