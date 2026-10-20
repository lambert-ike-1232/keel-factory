# State: [Feature or project name]

The **state file** — the first thing a resuming session reads. Carries phase
approvals and anything that must survive a context boundary. Slice-level work
itself is tracked on the task board (`task-board-init`), not here — see
`keel/framework/TASK-BOARD-CROSSREF.md` §2 for why that split exists.

---

## Phase state

| Phase | Status |
|---|---|
| 1 — BRIEF | pending / in progress / **APPROVED** [date] |
| 2 — CONTRACT | pending / in progress / **APPROVED** [date] |
| 3 — DESIGN | pending / in progress / **APPROVED** [date] |
| 4 — SLICE | pending / in progress / **APPROVED** [date] |
| 5 — PROVE | pending / in progress / **APPROVED** [date] |

**Tier:** SPRINT / STANDARD / PLATFORM

**Stop mode:** supervised / checkpoint / unattended — default checkpoint, supervised at
PLATFORM (`keel/framework/TIERS.md`, "Stop modes"). In checkpoint and unattended mode,
DESIGN and SLICE show "done [date], no stop" rather than APPROVED.

**Unattended only** — the seven fields `keel/framework/LOOPS.md` §2 requires, filled in
before the run starts, or the run does not start:

| Field | Value |
|---|---|
| Trigger | |
| Per-iteration done condition | |
| Done-checker (independent of the worker) | |
| Stop-entirely condition | |
| Escalation trigger | |
| Cost ceiling (per iteration, per period) | |
| LAND step | |

**Resume rule:** read this file, then every document in `docs/`, then the task board
(`.scratch/task_board/`, via `task-board-triage` if it looks stale), then continue
from the first unapproved phase or the first non-`completed` task. Never redo an
approved phase unless a later phase invalidated it.

**Backtracking:** if a later phase reveals an earlier approved decision is wrong, stop,
update that phase's document, set it back to *in progress* here, and get re-approval
before continuing. This is a normal event, not a failure.

**Handing off mid-task?** Use the `handoff` skill rather than leaving this file as the
only record of in-progress reasoning — it's built for exactly that context boundary,
and `resume-handoff` re-verifies the repo against it before acting, which this file's
own "Resume rule" above does not do on its own.

---

## Notes for a fresh session

[Anything decided in conversation that a new session must know. Nothing important may
exist only in chat — if it matters and it is not in a document, it goes here.]

---

## Blocked / open

[Anything waiting on a human, an external service, or a decision.]
