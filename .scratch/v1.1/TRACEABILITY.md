# Traceability: KEEL v1.1 — must-haves to checks

Must-haves from `BRIEF.md`; checks from `ACCEPTANCE.md`; live runs L1–L8 from
`keel/framework/HARNESS-PROBES.md` (traces for L3–L8 in `trials/`). Status here is the
lead's claim before PROVE; PROVE promotes or demotes each row.

| # | Must-have | Bound checks | Status before PROVE | After PROVE pass 2 | After PROVE pass 3 | After PROVE pass 4 | After the closure check (docs round 5) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| M1 | Install once; every skill visible in every project, from one master | R5, R11; L1, L3 | claimed PASS | **PASS**: R5, R11 armed | **PASS**: R5 (27/27), R11 armed | **PASS**: R5 (27/27), R11 armed | **PASS**: R5 (29/29), R11 loaded |
| M2 | One front door; HELM tells owner from operator | L3, L4 (owner, live); L7 (operator, live); R2 (role handling in the hook) | claimed PASS | **PARTIAL**: new HELM text not re-run live; keel in operator mode (N23, N28) | **PARTIAL**: HELM text not re-run live; C14, C15 fix-now | **PARTIAL**: no live HELM run since L7; D4, D5, D8, D9 docs-only | **PARTIAL**: a live dry run (another session, Claude Code 2.1.304) ran HELM's switch-on and routing end to end; it found DR-2, now fixed in text and not yet re-run live |
| M3 | Stop modes: supervised, checkpoint, unattended | L4 (checkpoint, live) | claimed PARTIAL: supervised and unattended not exercised | **PARTIAL**: as claimed | **PARTIAL**: as claimed; no runnable check | **PARTIAL**: no runnable check | **PARTIAL**: the dry run's SPRINT run in checkpoint mode showed the stop-mode docs disagree (`owner-deferred/sprint-checkpoint-stops`) |
| M4 | PROVE reviewers shipped as agents | R8 (agent rule); L5 | claimed PASS | **PASS**: R8 armed; run in pass 2 | **PASS**: R8 armed; run in pass 3 | **PASS**: R8 armed; run in pass 4 | **PASS**: R8 armed; the dry run spawned prove-standards and prove-spec live |
| M5 | Eval suite with a no-plugin baseline | R8 (eval rule); P1 | claimed PARTIAL: written and checked, never run | **PARTIAL**: as claimed | **PARTIAL**: P1 needs Claude Code ≥ 2.1.269 | **PARTIAL**: P1 needs Claude Code ≥ 2.1.269 | **PARTIAL**: P1 is runnable now (CLI 2.1.304) but has not run (`eval-run`, before release) |
| M6 | Less always-on context | R8 (sizes); R9; `claude plugin details` | claimed PASS | **PASS**: R8 sizes armed (R9 armed only by inference) | **PASS**: R8 sizes armed; R9 armed (Evidence) | **PASS**: R8 sizes, R9 armed | **PASS**: R8 sizes armed (`CLAUDE.md` 5,595 in v1.1's own tree, 5,994 on the shared tree), R9 armed |
| M7 | Codex, as far as Codex allows, gaps named | R8 (codex rule); R12; P2 | claimed PARTIAL: skills proven, hooks not | **PARTIAL**: Codex hooks unproven; copied-kit route dormant (N2) | **PARTIAL**: Codex hooks unproven (P2); Codex reads unnamed (K32); C4 | **PARTIAL**: Codex hooks unproven live (P2) | **PARTIAL**: R12 lists 17 skills; Codex hooks unproven live (`codex-hook-live-probe` approved, not run) |
| M8 | Guard keeps working and arms in KEEL projects | R1, R2; L1, L2, L3, L8 | claimed PASS | **FAIL**: copied-kit route does not arm (N2 = N35); plugin route PASS (R1, R2, L1, L8) | **PARTIAL**: copied-kit route arms (N2 fixed); K30, K31 fail open (fix-now); K18, K19, K29 unnamed | **PARTIAL**: K30, K31 fixed (93/93); D1 misstated in two docs | **PASS**: D1 fixed in both docs; K30, K31 armed (93/93 at this landing); the dry run's guard blocked Read and `cat .env` on 2.1.304 |
| M9 | CAPABILITIES says what each harness can and can't do, dated | R8 (links); reviewer reading | claimed PASS | **PARTIAL**: N13 and N15 rows stale or unsourced | **PARTIAL**: C5, K27 stale; no Codex-reads row (K32); C3 unprobed | **PARTIAL**: P-C5 preamble; no row for D17 | **PARTIAL**: P-C5 and D17's row landed; one claim in that row has no source (REFERENCE-N2) |

Coverage claimed: 6 PASS of 9 (67%); the rest PARTIAL with the reason stated.

After PROVE pass 2 (2026-10-18, `PROVE-2.md`): 3 PASS, 5 PARTIAL, 1 FAIL, so coverage is
3 / 9 (33%). Each row's evidence and the findings behind it are in `PROVE-2.md`.

After PROVE pass 3 (2026-10-19, `PROVE-3.md`): 3 PASS, 6 PARTIAL, 0 FAIL, so coverage is
3 / 9 (33%); M8 moved from FAIL to PARTIAL. Each row's evidence is in `PROVE-3.md`.

After PROVE pass 4 (2026-10-19, `PROVE-4.md`): 3 PASS, 6 PARTIAL, 0 FAIL, so coverage is
3 / 9 (33%). M2, M3, M5 and M7 need runs the manager gates; M8 and M9 need only pass 4's
docs-only fixes.

After the closure check (2026-10-20, `PROVE-5.md`), which followed docs round 5: 4 PASS,
5 PARTIAL, 0 FAIL, so coverage is 4 / 9 (44%). M8 moved to PASS. M2, M3, M5 and M7 need
runs the manager gates (a live HELM run after DR-2, a stop-mode decision, P1, P2); M9 needs
one source line. The tree is shared with the retrofit; these rows judge v1.1's text,
which is the same in its pre-retrofit copies.

PROVE approved by the manager on 2026-10-20 (the crew plan's Open question 23) at the
closure-checked tree, with M2, M3, M5, M7 and M9 accepted as PARTIAL and named: they
need the live HELM run, the SPRINT stop-mode change (decided: one up-front round), the
eval run (P1) and the Codex probe (P2), and M9 one source line.
