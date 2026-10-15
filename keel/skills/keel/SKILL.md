---
name: keel
description: Drive the KEEL engineering framework - pick a tier, then run the BRIEF, CONTRACT, DESIGN, SLICE, PROVE phases with the right weight, producing the fixed artifact set. Use when starting a project or feature, resuming one after a gap, or auditing a codebase against a claim that it is done. Not for trivial tweaks.
argument-hint: "recon | brief | contract | design | slice | prove | resume | audit, or nothing to pick up where you left off"
disable-model-invocation: true
---

# KEEL

An engineering framework for going from idea to production-ready product. Five phases,
three tiers, six standing rules.

**The framework documents are the source of truth.** Read them rather than working
from this summary:

- `framework/PHASES.md` — the five phases in operational detail
- `framework/TIERS.md` — SPRINT / STANDARD / PLATFORM and how to pick
- `framework/RULES.md` — the six standing rules
- `framework/COST.md` — cost as an engineering constraint
- `framework/RECON.md` — the orientation gate that runs before BRIEF on an existing system
- `framework/DOCTRINE.md` — the standard all of this is held to (how well, not just what)
- `framework/CAPABILITIES.md` — what the agent can physically do; never ask for more
- `framework/TASK-BOARD-CROSSREF.md` — why SLICE runs on the task board, not a checklist
- `templates/` — the artifact set
- `skills-board/` — the task board, interview, and handoff skills this file delegates to
- `capabilities/reverse-engineering/` — PERCEPTION sense: reach for REA when source can't answer
- `capabilities/deep-research/` — RESEARCH sense: find out what you don't know, properly
- `../ARCHITECTURE.md` — how all of this, plus the harness, ropes together (read if lost)

Locate them relative to this repo's KEEL installation. If they are not present, tell
the user and work from this file alone.

This skill is usually reached through **HELM** (`skills/helm/SKILL.md`), the front door
that decides whether a situation even wants KEEL versus resume / recon / perception /
audit. If you arrived here directly, the orientation below does HELM's job for the KEEL
branches.

## First, orient

1. **If `docs/STATE.md` exists** for the work being discussed, read it, then every
   document in `docs/`, then the task board (run `task-board-triage` first if it looks
   stale). Continue from the first unapproved phase or first non-`completed` task.
   **Never redo an approved phase** unless the user asks or a later phase invalidated
   it. If a handoff document exists at the expected path, run `resume-handoff` instead
   of doing this by hand — it verifies the repo against it before acting.
2. **If this is an existing or unfamiliar system and no `docs/RECON.md` exists yet, run
   RECON before BRIEF** (`framework/RECON.md`). Understand the system and learn its house
   style before proposing a change. RECON hands BRIEF a grounded direction and the
   conventions it must respect. Skip recon only for genuinely greenfield work or a change
   whose shape is already obvious.
3. **Otherwise, pick the tier.** Run the ladder in `framework/TIERS.md` and state the
   result. Default to **STANDARD**. If the user picked SPRINT, say what is being given
   up.
4. **Skip KEEL entirely** for trivial work — a rename, a typo, a copy change, a
   one-line config edit — or when the user says to just do it. Say you are skipping,
   and do the task.

## The phases

Run the phase the user named, or the next unapproved one. Full detail in
`framework/PHASES.md`.

| Phase | Produces | Stop at |
|---|---|---|
| **BRIEF** | `docs/BRIEF.md` — rewrite with `[GUESS: ...]`, resolved; announcement | PLATFORM |
| **CONTRACT** | `CONTRACT.md`, `ACCEPTANCE.md`, `schemas/`, `TRACEABILITY.md` (all `FAIL`), cost budget, **verified toolchain table**, **bound-numbers table** | STANDARD, PLATFORM |
| **DESIGN** | `DESIGN.md` — signatures with no bodies, seams, depth check, cost ladder, test plan, least-confident list | STANDARD, PLATFORM |
| **SLICE** | board tasks (`task-board-init`/`to-task`) + code, tracer bullet first | every slice boundary |
| **PROVE** | **negative controls armed first**, then three-axis review, gate run, traceability promoted, cost measured against its assertion, honest status | every tier |

### At a stop point

1. Write the document to disk.
2. Summarise to the user: at most 5-10 bullet decisions, plus the path. Lead with the
   ones most worth challenging, each with the alternative you rejected, so "what should
   change" has something concrete to push on. **Do not paste the whole document into
   chat.**
3. Ask exactly: **"Approve <PHASE>, or what should change?"**
4. Anything short of a clear yes means revise and re-ask.
5. On approval, mark it in `docs/STATE.md` and continue. (SLICE approval marks the
   phase in `STATE.md`; the slices themselves are tracked as board tasks, not here.)
6. **Backtracking:** if a later phase shows an earlier approved decision is wrong,
   stop, update that document, set the phase back to *in progress*, and get
   re-approval.

## The six standing rules — always on

1. **Brief** — every task states a standard, points at the information, defines done.
   Tag gaps `[GUESS: ...]`, never guess silently. End non-trivial work with one line:
   `Guessed: ...` or `Full brief, nothing to guess.`
2. **Evidence** — "specified" is never "implemented." Label claims Evidence / Inferred
   / Missing evidence. Report status as *implemented and verified* (name the command) /
   *implemented, unverified* / *specified only*. A gate command that does not run is
   FAIL, not UNKNOWN.
3. **Traceability** — every feature line owns an acceptance check or is a declared
   descope. **A row with no bound check is `FAIL`, never blank.**
4. **Context** — nothing important may exist only in chat. Compact to documents at
   every phase and slice boundary. Respect the smart zone (~150k tokens); stop at a
   boundary rather than pushing on degraded. At a boundary work the tree, first yes
   wins: continue → clear → handoff → sub-agent → compact. "Handoff" means the
   `handoff` skill specifically, not an ad hoc note — it's what makes this step
   actually resumable by a session with no memory of this one.
5. **Cost** — the cheapest configuration that passes the gate wins. Budget it in the
   contract, measure it at PROVE, justify every rung on the escape-hatch ladder.
6. **Instrument** — the checks are code too.
   - **Declare the toolchain** for every Required Check at CONTRACT and **verify it is
     present**. Never write a gate you cannot run; a `MISSING` toolchain is a finding now,
     not a surprise at PROVE.
   - **Prove each critical check can fail** before trusting its green. Feed it a known-bad
     input and watch it go red, and confirm the probe actually reaches the thing under
     test. A silent crash and a clean pass produce identical output.
   - **Evidence expires.** Re-run rather than recall, especially where dependencies float
     or an external service sits in the path.
   - **Bind every stated number** to an assertion. Prose does not fail a build.

## Interviewing

Resolving the brief at STANDARD or above runs on the `task-interview` skill
(`skills-board/claude/task-interview/SKILL.md`), not a restatement of it here — see
`framework/TASK-BOARD-CROSSREF.md` §3 for why. Its operating principle is the same one
this file always stated: **finding facts is your job; making decisions is the user's.**
It explores the codebase for anything the code can answer and asks the user only what
the code genuinely cannot, walking every open question down to a recorded decision
rather than a guess. Done when nothing is left open.

KEEL adds one thing on top of `task-interview`, without editing it: **every question it
puts to the user arrives with two or three concrete options and your recommended pick**,
researched first where the options turn on knowledge you lack (`framework/DOCTRINE.md`
§2, and the standing rule in `CLAUDE.md`). Ask every question whose prerequisites are settled
together in one numbered round. That is the same dependency order `task-interview`
walks: its warning against batching every question at once is about asking dependent
questions early, and a question waiting on another's answer still waits for the next
round.

If `task-interview` is not installed for some reason, fall back to that same numbered
round by hand, then wait, rather than skipping the interview.

## Building

- **Vertical slices only.** Slice 1 is a tracer bullet: mocked, stubbed, wired end to
  end, running. Never build all of one layer then all of the next.
- **File slices as board tasks**, not a checklist. One task per slice via `to-task`;
  run each under `focused-implementation`, or several non-interfering ones together
  under `orchestrate-implementation`. Splitting that work across more than one agent
  goes through `crew` (`skills/crew/SKILL.md`) first.
- **Test at confirmed seams only.** Red before green. One seam, one test, one minimal
  implementation per cycle. Refactoring belongs to PROVE, not to the loop.
- **Never write a test that cannot fail** — one that passes against pre-change code,
  or whose assertion recomputes the expected value the way the code does. Never
  weaken, skip, or comment out a test to reach green.
- **Cross every join.** For each field a consumer reads, one test spanning producer,
  storage, serialization, and consumer. Two individually correct components with
  individually passing tests still drop data between them.
- **After every slice**, prove it works by running it and showing the result, close
  the task on the board, and propose the next step: the next slice, or the re-steer you
  would recommend if this slice taught you something. Let the user confirm or redirect.
- **Running short on context mid-slice?** Use `handoff` rather than compacting blind —
  it's a self-contained document a fresh session can resume from with no memory of this
  conversation; the next session runs `resume-handoff` against it.

## Other entry points

- **`recon`** — orient to an existing or unfamiliar system before proposing changes:
  understand what's there, learn its house style, map it, and turn the assessment into a
  prioritized, convention-respecting improvement backlog. Fill in `docs/RECON.md`;
  full discipline in `framework/RECON.md`. Runs before BRIEF, feeds it. This is the
  entry point for "take on this project and learn how it does things."
- **perception** — when a question depends on something you cannot read as source (a
  shipped binary, a running process, a capture, firmware, an obfuscated bundle), reach
  for REA through `capabilities/reverse-engineering/SKILL.md`, under its authorization
  gate. It serves recon, a hard bug, SLICE interop, or an audit — it is a sense, not a
  phase. Skip it entirely for ordinary source work.
- **deep research** — when a decision turns on knowledge you lack and cannot derive from
  the repo (a technique, a protocol, a best practice, a tradeoff), reach for
  `capabilities/deep-research/SKILL.md`: authoritative sources, triangulated,
  evidence-labeled, tied to the decision. The required alternative to guessing. A
  researched claim stays `Inferred` until the system confirms it. The other sense beside
  perception — skip it for what the repo already answers.
- **`resume`** — read `docs/STATE.md`, then all of `docs/`, then the task board,
  continue from the first unapproved phase or non-`completed` task. If a handoff
  document exists, run `resume-handoff` instead.
- **`audit`** — fill in `docs/AUDIT.md` adversarially. Cite a file for every claim,
  label each one, run every acceptance check rather than reasoning about it, walk the
  failure-mode list explicitly, and finish with a dependency-ordered task list where
  every task has a Verify command. **Run this before writing more code** on inherited
  work or against a claim of "basically done." `task-board-triage` does the board-state
  half of this same job when the question is narrower — "is the board honest" rather
  than "is the whole claim of done true."
- **A hard bug** — build a red-capable feedback loop *before* any hypothesis: one
  command, deterministic, fast, agent-runnable, asserting the exact symptom. Minimise
  the repro. Generate 3-5 falsifiable hypotheses before testing any. Instrument one
  variable at a time with a tagged prefix. Regression test before the fix. If no
  correct seam exists to test at, **that is the finding** — record it. If the failing
  surface is a binary or runtime the repro cannot reach as source, reach for perception
  (above) to see it.
- **A design question you cannot settle on paper** — run the `spike` skill: a
  throwaway prototype in scratch space, built to answer one stated question, then
  explicitly discarded or promoted. No tests or abstractions, kept out of main as a
  primary source. Fold only the answer into the real code.
- **Ending a session, or handing work to a fresh one** — run `handoff` before clearing
  or compacting. Don't rely on a document that only describes *what* was decided;
  `handoff` also captures the exact commands, the dead ends, and what's still
  undecided, which `resume-handoff` checks the repo against before acting.
- **Tidying up after a block of work lands** — `post-creation-audit` for hygiene
  (tests at the right level, docs updated, scratch artifacts removed); `commit` to
  split the result into clean, revertible commits. Neither substitutes for `keel-prove`
  when the actual question is whether the work is done.
