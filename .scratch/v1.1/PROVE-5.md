# PROVE pass 5, a closure check: KEEL v1.1, 2026-10-20

**Outcome: findings open, none major.** A closure check after docs round 5, as the manager
chose (the crew plan's Open question 21: "Docs round 5 (Recommended)", then a closure
check of those items only, on the current tree). Of pass 4's 27 items, 26 are fixed and
1 is partly fixed (S4-a1); the dry run's DR-2 is fixed. It found 19 new items, 0 major
and 0 fix-now; 6 were records and were closed at this report, so 14 remain open, plus
S4-a1's question to the manager. Coverage is 4 / 9. Stamp of the checked tree:
`e09480c@v1.1-harness-conformance tree:c3ae134be1fa`, snapshot
`.scratch/evidence/v1.1/closure-5.json`. Every checker found the tree unchanged at its
start and end. Since then only records changed (the board, the evidence folder,
`STATE.md`, `TRACEABILITY.md`, `PROVE-4.md` and the mutation logs), so the result
applies. Stopped for the manager's word on PROVE and the release.

## How the review was done

Four closure checkers in fresh contexts, one per cluster (skills, reference,
protocols-guides, records), each re-testing its pass-4 items against the files as they
stand, reproducing the original failure where it could (the guard probes and the
listing in scratch projects through `keel_hook.py guard`). One skeptic per cluster then
tried to refute every verdict other than fixed and every new item; none was refuted.
No Standards, Spec or Gate reviewer ran this time: the manager chose a closure check of
these items only. The gate's commands were run by the lead at the landing (below). The
full result is `.scratch/evidence/v1.1/closure5.json`; the workflow is
`.scratch/v1.1/round5/closure5.workflow.js`.

## What docs round 5 did

Five shared CREW lanes (skills5, reference5, protocols5, guides5, records5) and the lead,
back-briefed, built, audited and repaired once, under the crew plan's Open question 22.
It changed no script and no test. The tree also holds the retrofit, which the manager
will ship later as 1.2.0, so each change to a file the retrofit also touched was made in
its pre-retrofit copy under `.scratch/skills-main/base/` too (the mirror rule); the
retrofit's own review diff changed only in the size figures. Before the build, the lead
probed S3's listing through the guard in three scratch projects and chose the command
the guard blocks where `.keel/` or `keel-factory` is gitignored, over a candidate that
only passes because its words do not look like paths. During the round, another session
sent two findings from a live dry run (`.scratch/evidence/dryrun-2026-10-20/`); the
lead filed both and fixed the second (DR-2: the guard probe must follow the role file,
and "File does not exist" means not armed) in HELM and OPERATOR.

## The gate, at the landing

Run by the lead on the shared tree, 2026-10-20 (Evidence):

- R1 to R7 and R13, with the retrofit's two suites: 343 tests OK (27, 108, 9, 18, 30,
  34, 21, 19, 29, 48).
- R8 `check_kit.py`: no findings; `CLAUDE.md` 5,994 characters on the shared tree
  (5,595 in v1.1's own copy, measured by protocols5 on a temporary kit).
- R9 `claude plugin validate`: exit 0, the one expected warning (the root `CLAUDE.md`).
  Claude Code 2.1.304 adds an "Advice (does not change the verdict)" line asking for a
  marketplace install line in README.
- R10 the board: 45 tasks, no findings. R11 `keel@skills-dir` loaded. R12 17 `keel:*`
  skills (the installed Codex links predate the retrofit).
- Rule 6b, each list after an identity baseline that passed: keel_hook 93/93, check_kit
  36/36, install_guard 18/18, install_plugin 29/29, make_release 33/33 (209). Logs:
  `.scratch/v1.1/round5/mutation/`.
- The fences: this round against `round5/snap.json`, 74 paths, no findings; the
  retrofit's whole-run fence, 291 paths, no findings.

R10's and R13's counts (45 tasks, 19 tests) differ from ACCEPTANCE's (27, 14) because the
retrofit shares the tree. v1.1's own counts are re-measured at the commit split, on its
own tree (Open question 22).

## Closure of pass 4

Of the 27 items: fixed (26): D1, D2, D3, D4, D5, D6, D7, D8, D9, D11, D15, D16, D17,
D18, D19, P-C5, P-K23, P-K28, P-K32, P-K34, S4-a2, S4-b, S4-c, T4-5, T4-7, T4-rest.
Partly (1): S4-a1. The dry run's DR-2: fixed. The mirror rule, judged as a whole: holds.

S4-a1 was the lead's slip. Its reject reason said the residual was quoted in the option
text the manager answered, and that a board item carried it; neither was true. The
reason is corrected in `PROVE-4.md`: the manager approved F3-1 "as written in
.scratch/v1.1/CONTRACT.md", and that entry states the residual (a kit copy that keeps
`.git` stays dormant), but the question did not spell it out, so it goes to the manager
again below.

## New items

Nineteen, every one confirmed or partly confirmed by its skeptic: 4 minor and 15 nit.
Most come from docs round 5's own wording, as each round's have.

Closed at this report (records only): RECORDS-N1 (`STATE.md` updated), RECORDS-N2 (with
S4-a1, the reason corrected), RECORDS-N5 (a dated line in `mcp-tools-guard-matcher`),
RECORDS-N6 (the execution log's mirror line), PROTOCOLS-GUIDES-N2 (filed:
`installer-hooks-json-robustness` item 3 now names every installer mode and
`install_guard.py`). The last is a follow-on.

Open, in `.scratch/task_board/v1-1-closure5-open-items.md`: SKILLS-N1 (HELM's copied-kit
fallback names no alternative), SKILLS-N2 (3(d) points at the wrong folder when the
listing is the blocked check), SKILLS-N3, SKILLS-N4, REFERENCE-N1, REFERENCE-N2 (the new
CAPABILITIES row states one fact without a source), PROTOCOLS-GUIDES-N1 and N3 to N7,
RECORDS-N3 and N4. Each skeptic's fix is in `closure5.json`.

## Traceability, promoted

| # | Must-have | After pass 4 | After this check |
| --- | --- | --- | --- |
| M1 | Install once | PASS | **PASS**: R5 (29/29), R11 loaded |
| M2 | One front door | PARTIAL | **PARTIAL**: a live dry run ran HELM end to end on 2.1.304; DR-2 fixed in text, not re-run live |
| M3 | Stop modes | PARTIAL | **PARTIAL**: the dry run showed checkpoint at SPRINT disagrees with the docs (`sprint-checkpoint-stops`) |
| M4 | PROVE reviewers as agents | PASS | **PASS**: R8 armed; run live in the dry run |
| M5 | Eval suite | PARTIAL | **PARTIAL**: runnable now (CLI 2.1.304), not run (`eval-run`) |
| M6 | Less always-on context | PASS | **PASS**: R8 sizes and R9 armed |
| M7 | Codex | PARTIAL | **PARTIAL**: R12 17 skills; hooks unproven live (probe approved, not run) |
| M8 | Guard arms in KEEL projects | PARTIAL | **PASS**: D1 fixed; K30, K31 armed (93/93); the dry run's guard blocked on 2.1.304 |
| M9 | CAPABILITIES honest, dated | PARTIAL | **PARTIAL**: one unsourced claim in the new row (REFERENCE-N2) |

Coverage = (PASS + DESCOPED) / total = **4 / 9 (44%)**.

## Cost

Measured from the workflow runs (Evidence: the harness's own counts): the back-brief, 5
agents and about 0.64M tokens; the build, audits and fix-ups, 12 agents and about 1.57M;
the closure check, 8 agents and about 1.34M. That is 25 agents and about 3.55 million
subagent tokens, on the manager's plan, with `ANTHROPIC_API_KEY` unset. No model call
was made by the lead; the gate's `claude` and Codex commands make none.

## Honest status

- **Implemented and verified:** everything pass 4 listed, plus this round's docs, each
  checked against the files and, where it can be, reproduced (the listing and the guard
  in scratch projects).
- **Implemented, unverified:** HELM's switch-on with DR-2's fix (no live run since);
  supervised and unattended stop modes; the Codex hooks (P2).
- **Specified only:** the eval suite's run (P1), now runnable.
- **Known open items:** 14 small docs and record items (none major or fix-now), the
  SPRINT stop-mode decision, and S4-a1's question.

## For the manager

This check found what it was for: pass 4's items are closed, one record of the lead's was
wrong and is corrected, and the new items are small. What is left for PROVE: M2, M3, M5
and M7 need runs or a decision only you can give (a live HELM run, the SPRINT stop-mode
answer, the eval run, the Codex probe); M9 needs one source line. The decisions:

1. **PROVE for v1.1.** Approve it now, with M2, M3, M5, M7 and M9 named as PARTIAL and
   the 14 small items listed as known gaps in 1.1.0's release notes and fixed in a
   follow-on (recommended: each round's own wording has drawn about 20 new small items,
   and none of these changes what KEEL does); or run one more small docs round over the 14
   items and a closure check of them first, then decide.
2. **SPRINT's checkpoint stops** (`sprint-checkpoint-stops`): one up-front
   round at every tier (recommended), SPRINT stays one stop in every mode, or document the
   difference.
3. **F3-1's residual:** a kit copy that keeps `.git` stays dormant. Acknowledge it as
   approved (recommended), or file it to be closed in `keel-hook-hardening`.

## The manager's answers (2026-10-20)

Recorded verbatim in the crew plan's Open question 23: "Approve, list as gaps
(Recommended)"; "Up-front round (Recommended)"; "Accept it (Recommended)". PROVE is
approved at `e09480c@v1.1-harness-conformance tree:c3ae134be1fa`. Because an approval holds only for the tree it reviewed, the SPRINT
change and the 14 small items land later, with their own check, in
`v1-1-closure5-open-items`, and 1.1.0's known-gap lines are written at the commit split.

