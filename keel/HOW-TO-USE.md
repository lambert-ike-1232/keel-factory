# How to Use KEEL

The operational playbook. What to actually type, in what order, and what to do when it
goes sideways.

If you have not read [framework/THE-STACK.md](framework/THE-STACK.md), read it first.
This document assumes you know why the pieces are there.

---

## Setup, once

```bash
# 1. Copy the artifact templates into your new project
cp -r "00 Engineering/templates/" /path/to/new-project/docs-seed/

# 2. Copy the skills so they are invocable
cp -r "00 Engineering/skills/keel"       ~/.claude/skills/
cp -r "00 Engineering/skills/keel-prove" ~/.claude/skills/
```

Restart your agent. `/keel` and `/keel-prove` are now available.

You do not need the skills to use KEEL. They are packaging: they make the framework
invocable and consistent between runs instead of depending on you remembering the
sequence. The framework is the documents.

---

## Starting a new project

### Step 0 — Pick the tier, out loud

Run the decision ladder in [framework/TIERS.md](framework/TIERS.md). Write the answer
in the brief. **STANDARD unless you have a reason.** Choosing SPRINT is a decision you
state, not a place you drift into.

### Step 1 — BRIEF

Fill in `docs/BRIEF.md` **by hand**. Plain language. This is the only writing you do
before an agent is involved, and "I don't know yet" is a better answer than an
invention, because it becomes a decision to make rather than an assumption to discover.

Then, in a fresh session:

```
/keel brief
```

Or without the skill:

> Read `docs/BRIEF.md`. Before writing anything, rewrite it as the brief you would
> have needed, tagging every gap you had to fill with `[GUESS: ...]`. Then grill me:
> work the design tree in rounds, ask the whole frontier at once, number the questions,
> and attach your recommended answer to each. Find facts yourself; only ask me for
> decisions. Do not start until the frontier is empty.

Answer the rounds. Expect somewhere between six and twenty questions at STANDARD tier.
Finish by writing the announcement: three to six sentences, as if it already shipped.

**Do not clear the context after this.** BRIEF, CONTRACT, and DESIGN want the same
window.

### Step 2 — CONTRACT · *stop point*

```
/keel contract
```

Produces `CONTRACT.md`, `ACCEPTANCE.md`, `schemas/`, `TRACEABILITY.md` (all rows
`FAIL`), and the cost budget.

**Read this output properly.** It is the highest-value review point in the whole
framework — a wrong assumption costs a sentence here and a rewrite later. Check
specifically:

- [ ] Is the Production Build Contract made of *decisions*, not categories of options?
- [ ] Is every Required Check a command that will actually exist? Anything aspirational under Planned?
- [ ] Do the schemas have `additionalProperties: false` and constrained fields, or are they permissive placeholders?
- [ ] Is there one traceability row per feature line?
- [ ] Is the cost ceiling a number, **with a check bound to it**?
- [ ] Does every Required Check name the toolchain it needs, and has that been verified present?

Approve, or say what changes.

### Step 3 — DESIGN · *stop point*

```
/keel design
```

Produces signatures with no bodies, confirmed seams, the depth check, the test plan,
and the least-confident decisions list.

**Read the signatures and the least-confident list.** Skip everything else if you are
short on time — those two are where the value is. The list is the agent telling you
what it is about to guess. Answering three bullets here routinely saves half a day.

### Step 4 — SLICE

```
/keel slice
```

Slice 1 is the tracer bullet: mocked, stubbed, wired end to end, running. It should
appear fast and do almost nothing. That is correct.

After every slice you get a demonstration — a run, a curl, a screenshot — and a
question: continue, or re-steer? **Re-steering is cheap here and expensive later.**

At PLATFORM, clear context between slices. At any tier, compact at each boundary.

### Step 5 — PROVE · *stop point, every tier*

```
/keel-prove
```

**Arm the gate first.** Before recording what any critical check accepts, feed it a
known-bad input and watch it go red. Confirm the probe actually reaches the thing under
test — a bad string the build strips before output proves nothing about a scanner reading
build output.

Then: three parallel axes (Standards, Spec, Gate), the gate actually run, the traceability
matrix promoted on evidence, the cost measured against its bound assertion, and an honest
status report in three categories.

**Do not accept a status report that blurs the categories.** "Implemented and
verified" requires a *named command*. If the report cannot name one, the correct
category is "implemented, unverified," and that is fine — it is just not the same
thing.

---

## Working an existing project

### Resuming after a gap

```
/keel resume
```

Reads `docs/STATE.md` for the phase-approval state, then every document in `docs/`,
then the task board (`task-board-triage` first if it looks stale), then continues from
the first unapproved phase or first non-`completed` task. Never redoes an approved
phase unless something invalidated it. If a handoff document exists at the expected
path, run `resume-handoff` instead — it verifies the repo against it first.

### Inheriting a codebase, or checking a claim of "basically done"

**Audit before writing any more code.**

```
/keel audit
```

Or:

> Audit this repository against `docs/CONTRACT.md` and `docs/ACCEPTANCE.md`, and fill
> in `docs/AUDIT.md`. Be adversarial. Cite a file for every claim and label each one
> Evidence / Inferred / Missing evidence. Do not count a contract, schema, or plan as
> an implemented feature. Run every acceptance check rather than reasoning about it; a
> check that does not run is a FAIL and a critical finding. Finish with a
> dependency-ordered task list where every task has a Verify command.

This is the mechanism that catches the failure mode KEEL is most built against: a
scaffold that looks finished and runs nothing.

### A hard bug

Do not let the agent theorise. **Demand the loop first:**

> Before any hypothesis, build me one command that goes red on this specific bug. It
> must be deterministic, fast, and runnable unattended, and it must assert the exact
> symptom rather than "did not crash." Show me the invocation and its output. No
> red-capable command, no hypotheses.

Then: minimise the repro until every remaining element is load-bearing, generate three
to five *falsifiable* hypotheses before testing any of them, instrument one variable at
a time with tagged log prefixes, write the regression test before the fix, and grep the
tags out at the end.

If no correct seam exists to lock the bug down, **that is itself the finding** — the
architecture is preventing the bug from being regression-tested, and that goes in
`DECISIONS.md`.

---

## The session rhythm

```
┌─ Session 1 ─────────────────────────────┐
│  BRIEF → CONTRACT → DESIGN              │   one unbroken window
│  (compact at each boundary,             │   they share reasoning
│   never clear)                          │
└─────────────────────────────────────────┘
              ↓  clear
┌─ Session 2..n ──────────────────────────┐
│  One slice (or one ticket) per session  │   each self-contained
│  Prove it runs. Check it off.           │
└─────────────────────────────────────────┘
              ↓  clear
┌─ Final session ─────────────────────────┐
│  PROVE — three axes in parallel         │   fresh window on purpose:
│  sub-agents, gate run, status report    │   an agent reviewing its own
└─────────────────────────────────────────┘   fresh work reviews it badly
```

**At every boundary, work the tree** (Rule 4). First yes wins: continue → clear →
handoff → sub-agent → compact. Continue is first because it costs nothing and loses
nothing, and every other option converts the session from a primary source into a
summary of one.

**Watch the smart zone.** Around 150k tokens the model gets confidently wrong. Stop at
a boundary rather than pushing on degraded — pushing on is how a good session produces
a bad decision at the very end and nobody notices.

---

## Common mistakes

**Skipping CONTRACT because the project seems obvious.**
The obvious ones are where undeclared assumptions hide best. Twenty minutes.

**Letting the traceability matrix have blanks.**
A blank row is how a 60%-built feature reads as done. It is `FAIL` or it is `DESCOPED`
with a pointer. Those are the only options.

**Promoting a Planned Check without running it.**
The promotion *is* the moment the check becomes binding. Run it first, then move it.

**Accepting "implemented" without a command.**
Ask: "which command proves that?" If there is no answer, the status is
"implemented, unverified."

**Building horizontally because it feels more organised.**
All the models, then all the services, then all the API. It feels tidy and it means
nothing is testable until everything is done, which is exactly when it is most
expensive to be wrong.

**Reviewing in the same context that wrote the code.**
An agent that just wrote something is the worst possible reviewer of it. Parallel
sub-agents with clean windows, every time.

**Reaching for the big model first.**
Run the gate against the cheap configuration. Let expense earn itself against a named
failing check.

**Trusting a check you have never seen fail.**
A silent crash and a clean pass produce identical output. Break something on purpose,
watch it go red, then trust the green. Fifteen seconds.

**Writing a gate before checking you can run it.**
Name the toolchain each check needs during CONTRACT and verify it then. Discovering at
PROVE that the machine cannot execute half the gate is the most expensive possible moment
to find out.

**Treating a green result as permanent.**
It is a dated observation. Where dependencies float or an external service sits in the
path, last week's pass says nothing about today. Re-run, don't recall.

**Putting a number in a document and calling it a commitment.**
Prose does not fail a build. Every stated figure gets an assertion or it is decoration.

**Testing both sides of a boundary and neither the crossing.**
Two individually correct components with individually passing tests still drop data
between them. For every field a consumer reads, one test that crosses the whole path.

**Drifting into SPRINT.**
SPRINT is a decision you announce, with the giving-ups stated in the status report. It
is not what happens when you are tired.

---

## Quick reference

| Situation | Do this |
|---|---|
| New project | Tier → BRIEF → CONTRACT → DESIGN → SLICE → PROVE |
| New feature in an existing project | Same five phases, tier it separately |
| Resuming after a gap | `/keel resume` |
| Inherited code, or "it's basically done" | `/keel audit` **first** |
| Hard bug | Red-capable loop first, hypotheses second |
| Design question you cannot settle on paper | Prototype it. Throwaway, out of main, fold the answer back |
| Work too foggy to hold in one session | PLATFORM tier, decision mapping in BRIEF |
| "Is it done?" | Arm the gate, run it, report in three categories |
| A check that always passes | Break something on purpose. If it stays green, the check is broken |
| Resuming after weeks away | Re-run the gate before trusting it. Evidence expires |
