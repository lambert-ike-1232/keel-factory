# Acceptance: KEEL v1.1 — harness conformance

Every Required Check is a command run from the master root
(`/Users/lambertike/Documents/KEEL-FACTORY`), with `PYTHONDONTWRITEBYTECODE=1`. Each
check's record of being seen failing on deliberately broken input is listed under "Where
each check was seen failing" below.
*Updated 2026-10-18 after PROVE pass 1 (G1): one citation of `RELEASES.md` became that
list, and the scope counts are the ones measured on the fixed tree (R1–R8, R10, R13).
R9, R11 and R12 were not re-run in that update.*
*Updated 2026-10-18, fix round 3 (after phase A landed): the scope counts of R1–R8, R10
and R13 are measured on that tree, during phase B, and the seen-failing rows cite phase
A's gate. R8's doc and link counts move while phase B's document lanes write (phase A's
gate measured 228 links; this lane's last run printed 213 docs, 229 links), and R10's
count moves with the lead's board tasks (26 at that run, `helm-role-override` among
them); the lead re-measured both at phase B's landing, 2026-10-19 (213 docs, 229 links;
26 tasks; the crew plan's execution log, "Fix round 3, phase B — landed"). R9,
R11 and R12 were not re-run in this update (it runs no `claude` or `codex` command);
phase A's gate recorded R9 passing with the one expected warning (the crew plan's
execution log, "Fix round 3, phase A — landed").*
*Updated 2026-10-19, fix round 4 (phase B, after phase A landed): the scope counts of
R1–R8, R10 and R13 are as each check printed them at the end of this update, on that
tree. Three moved: R2 to 108 tests (from 86); R8's line (`CLAUDE.md` 5,531 characters,
session 5,965, 236 links; from 5,469, 5,903 and 229); and R10 to 27 tasks (from 26),
which moves with the lead's board tasks. R2's seen-failing row adds fix round 4's gate.
R9, R11 and R12 were not re-run in this update (it runs no `claude` or `codex`
command); phase A's gate recorded R9 passing with the one expected warning and R11
loaded (the crew plan's execution log, "Fix round 4, phase A — landed").*

## Required Checks

| ID | Command | Passes when | Scope it reports |
| --- | --- | --- | --- |
| R1 | `python3 -B harness/hooks/test_data_boundary_guard.py` | `OK` | 27 tests |
| R2 | `python3 -B harness/hooks/test_keel_hook.py` | `OK` | 108 tests |
| R3 | `python3 -B harness/test_link_kit.py` | `OK` | 9 tests |
| R4 | `python3 -B harness/test_install_guard.py` | `OK` | 18 tests |
| R5 | `python3 -B harness/test_install_plugin.py` | `OK` | 30 tests |
| R6 | `python3 -B harness/test_check_kit.py` | `OK` | 34 tests |
| R7 | `cd keel/skills/crew && python3 -B scripts/test_check_lanes.py` | `OK` | 21 tests |
| R8 | `python3 -B harness/check_kit.py` | `OK: … no findings` | its 14 rules (`source`, `manifest`, `hooks`, `marketplace`, `skill`, `skill-set`, `skill-path`, `listing-budget`, `codex`, `agent`, `eval`, `always-on`, `release`, `link`): 14 manifest skill paths, 2 hook commands, 18 skills, 7,038 listing characters, 91 skill paths checked, 22 Codex skills, 3 agents, 3 eval cases, `CLAUDE.md` 5,595 characters, session 6,029 characters, 213 docs, 236 links |
| R9 | `claude plugin validate .claude-plugin/plugin.json` | exit 0; the only warning is the root `CLAUDE.md` one | the manifest and its paths |
| R10 | `python3 -B keel/skills-board/claude/task-board-init/scripts/validate_board.py --board .scratch/task_board` | `OK: … no findings` | 27 tasks on the board |
| R11 | `claude plugin list` | `keel@skills-dir` with status loaded | installed plugins |
| R12 | in a scratch repo holding `.keel/`: `HOME=$HOME CODEX_HOME=<scratch> /Applications/Codex.app/Contents/Resources/codex debug prompt-input hi` | 17 skills listed as `keel:<name>` | the rendered skill list (no model call) |
| R13 | `python3 -B harness/test_make_release.py` | `OK` | 14 tests |

## Where each check was seen failing

*Added 2026-10-18 after PROVE pass 1 (G1).* "Phase 1" is the first phase of the PROVE
fixes; its mutation runs are in the execution log of
[crew-plan-prove-fixes.md](../task_board/crew-plan-prove-fixes.md), each with the
unmutated baseline green on the same kit. The specs are `.scratch/v1.1/tools/mut-*.json`.
*Updated 2026-10-18, fix round 3:* they now hold `mut-hook.json` 62,
`mut-install-guard.json` 18, `mut-check.json` 36, `mut-install.json` 27 and
`mut-release.json` 25 mutants; phase 2's results are in rows R5 and R13, and every
gate's results are in the rows below.
*Updated 2026-10-19, fix round 4:* `mut-hook.json` now holds 93 (31 more, for K30's
role read and fail-closed guard, K31's patch reader and the operator note); the
other four are unchanged (`mut-install-guard.json` 18, `mut-check.json` 36,
`mut-install.json` 27, `mut-release.json` 25; counted with Python's `json`).
*Updated 2026-10-20, docs round 5 (PROVE pass 4, D19):* R9's row cites PROVE pass 3's
arming record and is Evidence. P2 stays as background. No `claude` command ran in this
update. R8's `CLAUDE.md` and session figures move with P-K34 (5,531 to 5,595; 5,965 to
6,029), measured with `check_kit.py --root` on a temp kit holding the base copies. The
session figure includes the kit's root path: a 120-character temp root gave 6,109, so
the master's 40-character root gives 6,029.

| ID | Where it was seen failing | Label |
| --- | --- | --- |
| R1 | `RELEASES.md` v1.0.0, "Proven", the Data-boundary guard row: fifteen deliberately broken copies each failed the self-test. | Evidence |
| R2 | `RELEASES.md` v1.1.0, "Proven", the Hook script row. Mutation runs at both landing gates of the fix run (the crew plan's execution log, `.scratch/task_board/crew-plan-prove-fixes.md`): 49 of 49 mutants (`mut-hook.json`) each failed the 76-test suite, the unbroken suite green first. Fix round 3, phase A's gate (the same log, "Fix round 3, phase A — landed"): 62 of 62 on the 86-test suite, the unbroken suite green first. Fix round 4, phase A's gate (the same log, "Fix round 4, phase A — landed"): 93 of 93 on the 108-test suite, the identity baseline ("MISSED baseline-identity OK") first. | Evidence |
| R3 | The v1.0 handoff, `git show e09480c:.scratch/handoff.md`, line 67: three deliberately broken copies each failed `test_link_kit.py`. `.scratch/handoff-superseded-2026-10-15.md` holds the same text. | Evidence |
| R4 | For the first time, at both landing gates of the fix run: 11 of 11 mutants (`mut-install-guard.json`) each failed the 13-test suite, the unbroken suite green first. Fix round 3, phase A's gate: 18 of 18 on the 18-test suite, the unbroken suite green first. | Evidence |
| R5 | `RELEASES.md` v1.1.0, "Proven", the Installer row. Phase 1's gate: 15 of 15 mutants on the 24-test suite; phase 2's gate: 22 of 22 (`mut-install.json`) on the 28-test suite; fix round 3, phase A's gate: 27 of 27 on the 30-test suite; each with the unbroken suite green first. | Evidence |
| R6 | `RELEASES.md` v1.1.0, "Proven", the Kit check row. Both landing gates, and fix round 3, phase A's gate: 36 of 36 mutants (`mut-check.json`) each failed the 34-test suite, the unbroken suite green first. | Evidence |
| R7 | The v1.0 handoff, `git show e09480c:.scratch/handoff.md`, line 443: five deliberately broken copies of the checker each failed the suite; the same record is in `keel/framework/CREW.md` §12, "Promotion bar". | Evidence |
| R8 | Every R6 run: `test_check_kit.py` copies the kit to a temporary folder, breaks one rule per case, and requires this command (with `--root` on the copy) to exit 1 naming that rule. Phase 1's 36 of 36 mutants, and phase A's of fix round 3, show those cases are not vacuous. | Evidence |
| R9 | Armed at PROVE pass 3: [PROVE-3.md](PROVE-3.md), "Arming (keel-prove step 0)", row R9, and "Arming I re-checked myself": the Gate reviewer's copy of the manifest in a folder with no skill paths gave exit 1 and "Validation failed". The exact command form is from PROVE pass 4's D19 verifier (`.scratch/v1.1/round4/verify4.json`, item D19): `claude plugin validate <tmp>/m/.claude-plugin/plugin.json`, with `CLAUDE_CONFIG_DIR` set to a temporary folder, gave exit 1 and "Validation failed" on that copy, and exit 0 on the real manifest. Background: `keel/framework/HARNESS-PROBES.md` P2, where validate exited 1 on a missing skill path and on a name with spaces. | Evidence |
| R10 | `RELEASES.md` v1.0.0, "Proven", the Task-board validator row: it passed a clean board and failed a broken one. | Evidence |
| R11 | Armed by hand: [PROVE-FINDINGS.md](PROVE-FINDINGS.md), "Reviewer summaries", "Arming record for G1": with an empty scratch `CLAUDE_CONFIG_DIR`, `claude plugin list` listed no `keel@` plugin. | Evidence |
| R12 | Armed by hand, the same record: with an empty scratch `HOME` and `CODEX_HOME`, `codex debug prompt-input` in a `.keel/` repo listed 0 `keel:*` skills. | Evidence |
| R13 | For the first time, at phase 2's landing gate: 18 of 18 mutants (`mut-release.json`) each failed the suite, the unbroken suite green first; the reconcile lane added a nineteenth (README-FIRST without `--branch main`), and row 13's re-run gave 19 of 19 (the crew plan's execution log, "Row 13"). Fix round 3, phase A's gate: 25 of 25 on the 14-test suite, the unbroken suite green first. | Evidence |

## Planned Checks (not yet runnable here)

| ID | Command | Why not now |
| --- | --- | --- |
| P1 | `claude plugin eval . --trust-plugin --no-publish --scaffold --json results.json --allow-tools Write Edit Bash` | needs Claude Code ≥ 2.1.269; this machine has 2.1.170 |
| P2 | a `codex exec` run in a KEEL project reading a fake `.env` | needs `--codex-hooks`, the manager's trust in `/hooks`, and a Codex model call the manager has not approved |
