# The Five Phases

`BRIEF → CONTRACT → DESIGN → SLICE → PROVE`

The phases never change. How heavy each one is changes with the tier
(see [TIERS.md](TIERS.md)). The six standing rules run underneath all of them
(see [RULES.md](RULES.md)).

**Stop points** are marked. A stop is a real blocking approval: work does not continue
until a human says yes. How many stops you get is set by the tier, and which of them
block is set by the stop mode. The marks below are the **supervised** mode. In
**checkpoint** mode, the default below PLATFORM, the stops collapse to one approval of
BRIEF and CONTRACT together and the PROVE report; the halts every mode keeps are listed
under "Stop modes" in [TIERS.md](TIERS.md).

---

## Phase 1 — BRIEF

**Question:** What are we building, for whom, and what am I guessing?
**Produces:** `docs/BRIEF.md`
**Stop:** SPRINT no · STANDARD no · PLATFORM yes

### What happens

1. **Intake, in plain language.** Fill in `templates/BRIEF.md` by hand. "I don't know
   yet" is a legitimate answer and a better one than an invention, because it becomes
   a decision to make rather than an assumption to discover later.

2. **The rewrite.** The agent restates the brief as the brief it needed, with every
   gap it had to fill tagged `[GUESS: ...]`. This runs at every tier and costs almost
   nothing. It is the single cheapest mechanism in KEEL for making silent assumptions
   visible.

3. **Resolve the guesses.** How, depends on tier:
   - **SPRINT** — one question, the most consequential, with its options and the
     agent's pick. Proceed on the rest as written.
   - **STANDARD** — grilling rounds. Model the problem as a design tree; the
     **frontier** is every decision whose prerequisites are settled. Ask the whole
     frontier in one numbered round, **each question carrying two or three concrete
     options and a recommended pick**, then wait. Recompute and repeat until the
     frontier is empty. Run through `task-interview`, this is the same procedure: its
     dependency order is the frontier, and a question still waiting on another's answer
     waits for the next round.
   - **PLATFORM** — grilling, plus decision mapping when the work is too foggy to hold
     in one session: chart the open questions as decision tickets, each carrying its
     options and a pick, and resolve them one at a time until the way is clear. Plan,
     do not build.

   Throughout: **finding facts is the agent's job; making decisions is yours.** Any
   question the agent could answer by reading the repo or the docs is a question it
   should not be asking you. And no question reaches you blind: it arrives with the
   approaches the agent would take, researched first where they are not obvious, so you
   steer rather than author (`DOCTRINE.md` §2).

4. **Write the announcement.** Three to six sentences announcing this thing to its
   users, as if it already shipped. Not a summary of the plan: an announcement. If you
   cannot write it, you are building the wrong thing, and finding that out now costs
   five minutes.

### Done when

Every `[GUESS: ...]` is either resolved or explicitly accepted as a standing
assumption, and the announcement is written.

### Banned here

Databases, schemas, endpoints, file names, framework choices. If tech shows up, it
belongs in CONTRACT. This ban is doing real work: it is the only phase that can catch
"we are solving the wrong problem," and technical detail is the most effective way to
stop that conversation from happening.

---

## Phase 2 — CONTRACT

**Question:** What must be true for this to be done?
**Produces:** `docs/CONTRACT.md`, `docs/ACCEPTANCE.md`, `schemas/`, `docs/TRACEABILITY.md`, `docs/COST_MODEL.md` (budget section)
**Stop:** SPRINT no · STANDARD **yes** · PLATFORM **yes**

This is the phase that makes "production-ready" mean something. It is also the phase
most people skip, and skipping it is why scaffolds look finished and run nothing.

### What happens

1. **Pin the Production Build Contract.** Not categories of options: actual decisions.
   Exact runtime and version. Framework. Deploy target. Persistence. Secrets policy.
   Auth model. Data model and its state transitions. Observability signals. Real
   numeric limits taken from the actual platform, not from memory.

2. **Write the Feature List**, one line per capability, phrased as a capability rather
   than a component. These lines are load-bearing: every one of them becomes a
   traceability row.

3. **Write the acceptance gate before the feature list is even finished.** Each
   Required Check is a **runnable command**. Anything aspirational goes under Planned
   Checks and may only be promoted when the command exists and passes. A gate citing a
   command that does not exist is worse than no gate: it manufactures confidence and
   verifies nothing.

4. **Define the shapes.** `schemas/*.json` and, if there are HTTP endpoints, an OpenAPI
   document. `additionalProperties: false`. Every field typed and constrained. Size
   limits are a security control. These outrank the prose the moment they disagree.

5. **Seed the traceability matrix.** One row per Feature List line. At this point every
   row is `FAIL` — nothing is built. That is correct and it is the point: the matrix
   starts honest and gets promoted by evidence.

6. **Set the cost budget.** Cost per unit of work and a ceiling. See [COST.md](COST.md).

7. **Name the Human Review Gates.** Which categories of output require a human before
   they take effect. Legal, financial, safety, anything irreversible or externally
   visible.

8. **Declare the toolchain, and confirm it is present** (Rule 6a). For every Required
   Check, name what must be installed to run it — runtime, package manager, container
   daemon, system binary — and **verify it now**, not at PROVE. A gate you cannot execute
   is discovered at the end of the work, when it is most expensive and least fixable.

   ```
   | Check              | Requires            | Present? |
   |--------------------|---------------------|----------|
   | npm run build      | Node 20+            | verified |
   | pytest tests/      | Python 3.13, venv   | verified |
   | docker compose up  | Docker daemon       | MISSING  |
   ```

   A `MISSING` row is a finding at CONTRACT, not a surprise at PROVE. Either install it,
   or move every check that depends on it to Planned and say so in the status report.

9. **Bind every number** (Rule 6d). Any numeric claim in this contract — a latency
   target, a cost ceiling, a call budget, a size limit — gets a Required Check that
   asserts it. A figure with no assertion behind it is decoration, and decoration cannot
   be breached because nothing is watching.

### Done when

Every Required Check is a command that will exist, every schema field is constrained,
the traceability matrix has a row per feature line, the cost ceiling is a number **with a
check bound to it**, and every check's toolchain is confirmed present.

### Stop here at STANDARD and above

This is the highest-value approval point in KEEL. A wrong assumption is cheap to fix
in the contract and expensive to fix in code, and everything downstream inherits from
it.

---

## Phase 3 — DESIGN

**Question:** What are the shapes, and what am I least sure about?
**Produces:** `docs/DESIGN.md`
**Stop:** SPRINT no · STANDARD **yes** · PLATFORM **yes**

The step everyone skips. It is the cheapest bug prevention available.

### What happens

1. **Read the code that actually exists.** Never design against an imagined codebase.

2. **Write the signatures, with no bodies.** Types, function signatures, method
   signatures. A human should read them in seconds and say "right" or "wrong." This is
   the highest information-per-token artifact in software: you get the value of code
   review before the code exists.

3. **Name the seams.** A seam is the public boundary you test at. Prefer existing
   seams to new ones, and prefer the highest seam available. Fewer seams is better;
   the ideal number is one. Confirm them explicitly — **no test is written at an
   unconfirmed seam**, because agreeing them up front is how testing effort lands on
   critical paths instead of every edge case.

4. **Check the depth.** For each module: delete it mentally. If complexity vanishes it
   was a pass-through and should not exist. If complexity reappears across N callers,
   it was earning its keep. And do not introduce a seam unless something actually
   varies across it: one adapter is a hypothetical seam, two is a real one.

5. **Write the test plan.** Test names and what each one asserts, before any of them
   exist.

   Include the **round trip**: for every field a consumer reads, one test that crosses the
   whole path — producer, storage, serialization, consumer — and asserts the value arrives.

   *Why this earns its own line:* a build shipped where the client sent a filename, the
   store persisted it, and the response serializer silently dropped it. Every screen
   displayed a UUID instead of a document name. **Both halves were individually correct,
   both had passing tests, and no test crossed the join.** Seam discipline says test at the
   interface; this says the interface between two correct components is exactly where an
   untested gap hides.

6. **Write the least-confident decisions list.** Numbered. The calls most worth
   challenging now, while changing them is free. Each entry names the options considered
   and the one the agent will take absent an answer, so the reader can redirect with a
   word. This is the mechanism that converts a silent guess into a conversation, and it
   is why this phase pays for itself.

### Done when

Signatures exist for everything the slices will build, seams are confirmed, and the
least-confident list has been read by a human.

### At SPRINT

Collapse to the least-confident list alone. Three bullets, no signatures. Even at
maximum speed, "here are the three things I am about to guess" is worth thirty seconds.

---

## Phase 4 — SLICE

**Question:** Does a thin path through the whole thing run?
**Produces:** board tasks under `.scratch/task_board/` (via `task-board-init`/`to-task`)
plus working code. `docs/STATE.md` tracks phase approval; the board tracks the slices
themselves — see `keel/framework/TASK-BOARD-CROSSREF.md` §2 for why this split exists.
**Stop:** at every slice boundary, briefly, at every tier

### What happens

1. **File the slice plan as board tasks** — one task per slice, in build order, via
   `to-task`. A task too large or too vague to file cleanly is a sign it needs another
   pass through `task-interview` first, not a sign to skip the board.

2. **Slice 1 is the tracer bullet.** A mocked or hardcoded endpoint and a stubbed UI
   or a curl-able response, wired **end to end**. It does almost nothing. It runs, and
   you can see it.

3. **Slice 2 replaces the mocks** with real logic for the single happy path.

4. **Slice 3 onward: one capability per slice.** A business rule, an error path, an
   edge case, polish. Each ends in a working, testable state.

5. **Build test-first at the agreed seams.** Red before green: the failing test first,
   then only enough code to pass it. One seam, one test, one minimal implementation
   per cycle. Refactoring is not part of this loop; it belongs to PROVE.

6. **Run each slice under `focused-implementation`.** Several non-interfering slices
   can run together under `orchestrate-implementation`, which owns selection and
   sequencing; `focused-implementation`'s per-task entry gate and verification budget
   still apply to each one individually.

7. **After every slice:** prove it works (run it, curl it, browser-test it) and show
   the result. Close the task on the board — a status update there, not a checkbox in
   `docs/`. Propose the next step — the next slice, or a re-steer if this slice taught
   something — and let the user confirm or redirect.

### Banned here

**Horizontal building** — all of the database, then all of the services, then all of
the API, then all of the frontend, with nothing testable until the end. This is the
default an agent falls into and it is the reason 2,000-line diffs land in your lap.

**Tests that cannot fail.** Never write a test that passes against the pre-change
code. Never comment out, skip, or weaken a test to reach green. Never write a test
whose assertion recomputes the expected value the way the code does: expected values
come from an independent source of truth.

### Context discipline

At PLATFORM, each slice is a ticket sized to one fresh context window, and you clear
between them. At every tier, compact to the documents at each slice boundary, and stop
before the smart zone runs out rather than pushing on degraded.

---

## Phase 5 — PROVE

**Question:** Is the claim of "done" true?
**Produces:** the review, the gate result, an honest status report
**Stop:** SPRINT **yes** · STANDARD **yes** · PLATFORM **yes**

Every tier stops here. This is the one non-negotiable approval in KEEL, because it is
the phase where a claim becomes a fact or fails to.

### What happens

1. **Run the three-axis review.** Parallel sub-agents, so no axis pollutes another.
   Reported side by side, never merged, never reranked across axes.

   | Axis | Asks | Fails when |
   |---|---|---|
   | **Standards** | Does this follow the repo's documented conventions, plus a code-smell baseline? | Right thing, built badly |
   | **Spec** | Does this faithfully implement what the contract asked for? Anything missing, anything extra? | Built well, wrong thing |
   | **Gate** | Does every Required Check actually run and pass? Does every traceability row have evidence? | Claimed, not proven |

   Two axes is Matt's design and the reasoning is that a change can pass one and fail
   the other, so merging them lets one mask the other. The third axis is KEEL's
   addition and it is what makes "production-ready" a verified claim rather than an
   asserted one.

2. **Arm the gate before you trust it** (Rule 6b). Before recording what any critical
   check *accepts*, show it **rejecting** something. Feed it a known-bad input and watch
   it go red.

   Two rules make this real rather than ceremonial:

   - **The probe must reach the thing under test.** A known-bad string that the build
     strips before output proves nothing about a scanner that reads build output. Confirm
     the probe survives into the artifact being checked, then confirm the check catches it.
   - **A check that prints nothing is not a check that passed.** Distinguish "exited 0
     having examined N things" from "exited 0 having examined nothing." Make the check
     report its scope — files scanned, cases run, assertions made — so an empty run is
     visibly empty.

   *Named failure:* a lint command reported no problems across an entire build. It was not
   linting cleanly; a config incompatibility made it **crash before linting anything**, and
   a silent crash is indistinguishable from a clean pass.

3. **Run the gate.** Actually run it. Not "reason about whether it would pass."

   Re-run it, even if it passed recently (Rule 6c). A green result is evidence about a
   moment, not a property. Where dependencies float, where an external service sits in the
   path, where a model version can move underneath you, the previous run tells you about
   the previous day.

4. **Update the traceability matrix.** Every row gets promoted on evidence, or stays
   `FAIL`, or becomes a **declared descope** with a pointer to the decision. No blanks.

5. **Measure the cost.** Run the fixture set, record the numbers. An estimate is
   *Inferred*; a measurement is *Evidence*.

6. **Write the honest status report.** Three categories, never blurred:
   - **Implemented and verified** — the code exists and a named command proves it
   - **Implemented, unverified** — the code exists, nothing tests it
   - **Specified only** — a schema, contract, doc, or plan exists; no runtime behaviour does

7. **Log it.** Contract-affecting decisions and dead ends into `DECISIONS.md`; the
   tool-and-workflow record into `AI_WORKFLOW.md`.

### The two rules that make this phase real

**If asked whether something is done, answer by running the checks, not by recalling
what was written.** When a check cannot run, say so plainly rather than describing
what it would have proven.

**A gate never observed failing is unproven.** Running a check tells you it exited zero.
It does not tell you the check was capable of any other outcome. Until you have watched it
go red on purpose, a green result is a claim about the check, not about the code.

---

## Resuming

Any session starting cold: read `docs/STATE.md` (which carries the phase-approval
state), then every document in `docs/`, then the task board (`task-board-triage` if it
looks stale), then continue from the first unapproved phase or the first non-`completed`
task. Never redo an approved phase unless it was invalidated. If a handoff document
exists, use `resume-handoff` instead of doing this by hand — it re-verifies the repo
against what the document claims before acting on it.

Picking work back up after a real gap, inheriting a codebase, or checking a claim that
something is "basically done": run the **audit** first (`templates/AUDIT.md`) before
writing more code. Cite a file for every claim, label each Evidence / Inferred /
Missing evidence, and do not count a contract, schema, or plan as an implemented
feature.
