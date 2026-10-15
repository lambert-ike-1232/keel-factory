# The Five Standing Rules

These run underneath every phase, at every tier. Phases are what you do; rules are
what stays true while you do it.

Each rule exists because a specific failure keeps happening. The failure is named.

---

## Rule 1 — The Brief Rule

> Every non-trivial task states a **standard**, points at the **information**, and
> defines **done**. Gaps are tagged `[GUESS: ...]`, never guessed silently.

**The failure it prevents:** the agent fills a hole in your instructions with a
plausible invention, does not mention it, and you discover it three hours of work
later.

**In practice:**

- **Standard** — point at a reference to match. "Match how the existing PDF export
  works." An obvious existing pattern in the codebase counts.
- **Information** — point at where the knowledge lives, or confirm the agent can find
  it. Missing information that cannot be looked up is the one hard failure.
- **Done** — what finished looks like, and how it gets verified.

The test: **could this message be sent, as written, to a senior engineer colleague and
produce the right result?** Or does it only make sense alongside information still in
your head?

When a brief falls short, the response is not a list of questions. It is **the
rewrite**: the request restated as the brief it needed, every filled gap tagged, one
question asked, then work proceeds. You see the delta between what you wrote and what
was needed, which is the only thing that actually teaches.

Every non-trivial task ends with one line: `Guessed: ...` or `Full brief, nothing to
guess.` The goal is to make the second line the normal one.

**This rule is designed to go quiet.** As briefs improve, it disappears. That is
success.

---

## Rule 2 — The Evidence Rule

> "Specified" is never "implemented." Every claim carries a label.

**The failure it prevents:** a scaffold that looks finished and runs nothing.
Contracts, rubrics, runbooks, and plans accumulate; each one describes a working
system; none of them is one.

**The three labels:**

| Label | Means |
|---|---|
| **Evidence** | Directly observed. A file exists and contains X. A command runs and exits 0. A test asserts Y. |
| **Inferred** | A reasonable conclusion from docs or architecture, not verified in code. **Never graduates to Evidence without checking.** |
| **Missing evidence** | Required, and could not be confirmed either way. **Do not round this up to "implemented."** |

**The three status categories** for any progress report:

- **Implemented and verified** — the code exists and a *named* command proves it
- **Implemented, unverified** — the code exists, nothing tests it
- **Specified only** — a schema, contract, doc, or plan exists; no runtime behaviour does

**Two corollaries that catch most self-deception:**

1. A schema file, an OpenAPI path, or a runbook section describing a feature is
   evidence the feature was **designed**, not that it exists.
2. **If a gate command does not run, the gate is FAIL** — not UNKNOWN, and not "PASS
   once we add tests." A gate referencing a command that does not exist is itself a
   critical finding.

When asked whether something is done: **run the checks, do not recall what was
written.** If a check cannot run, say so plainly rather than describing what it would
have proven.

### An unrun check is not weak evidence. It is no evidence.

The first version of this rule said an unrun gate was "not much better" than a gate whose
command does not exist. That was too generous, and running the gates proved it. On the
first build to test this properly, **four defects survived typecheck, lint, a passing
unit suite, and a successful production build** — every one of them invisible to reading.

So the line is harder than it was: **code that has only been read has not been checked.**
"Looks correct" is not a label in the table above, and there is no honest place to put it.

The corollary is Rule 6: if the claim depends on a check, the check itself has to be
trustworthy, and that is a separate problem from the code.

---

## Rule 3 — The Traceability Rule

> Every feature line owns an acceptance check, or is a declared descope. A feature
> line with no bound check is a `FAIL` row, never a blank.

**The failure it prevents:** a feature that is 60% built and reads as done. This is
the rule that exists because of a measured, specific loss: 78% on specification
completion against 90% and 96% on the other two axes, where four of five gaps were
spec lines no check was ever bound to.

**In practice:**

- Each Feature List line in `CONTRACT.md` gets a row in `TRACEABILITY.md`.
- A row has: the feature line, its acceptance check, its test, and a status.
- Statuses are `PASS` (implemented and verified), `PARTIAL` (exists but incomplete,
  unenforced, or untested), `FAIL` (required and absent), or `DESCOPED` (a decision,
  with a pointer to where it was made).
- **The matrix is regenerated at PROVE**, not hand-maintained between times.

**Why `DESCOPED` is a first-class state:** "Persistent translation memory: descoped
for v1, see `DECISIONS.md#0007`" is a judgement call, and a reviewer reads it as one.
The same feature half-built and unmentioned reads as a failure of follow-through.
Identical code, very different score, and the reviewer is right both times. Declaring a
gap is cheap. Hiding one is expensive.

---

## Rule 4 — The Context Rule

> Nothing important may exist only in chat.

**The failure it prevents:** losing the *why* behind what you built. The diff survives;
the reasoning does not, and no amount of reading the code back returns it.

**In practice:**

- **Compact to documents at every phase boundary and every slice boundary.** After
  each, the documents must contain everything decided.
- **Respect the smart zone** — roughly 150k tokens before attention degrades and the
  model starts being confidently wrong. Treat it as a budget. Stop at a boundary
  rather than pushing on degraded.
- **Keep BRIEF through DESIGN in one unbroken window** where you can. Implementation
  wants the reasoning verbatim, not a summary of it.
- **Clear between slices** once each slice is self-contained.

**At a phase boundary, work this tree. First yes wins:**

1. **Can you continue?** Yes if the next phase needs this one as a primary source, or
   there is smart zone left. Costs nothing, loses nothing. Rule it out first.
2. **Is this context irrelevant to what comes next?** → clear. Cheapest move available.
3. **Do you need portability** — a new harness, a new directory, a colleague, or
   forking a side task? → write a handoff file.
4. **Can the next task run unattended?** → send it to a sub-agent, leave this session
   untouched. Automated review is the standard case.
5. **Otherwise, compact,** with an instruction about what comes next.

Every move except *continue* converts a **primary source** (the session as it actually
happened) into a **secondary source** (a summary). Primary is full information and
lots of noise; secondary is lossy and leaves room to move. You pay the lossiness only
when staying costs more than it saves. Make the call **at** a boundary; mid-phase,
continue or split the remainder into sub-agents.

---

## Rule 5 — The Cost Rule

> The cheapest thing that passes the gate wins. Cost is budgeted, measured, and
> checked like a test.

**The failure it prevents:** a product that works and costs too much to run, which is
the same as a product that does not work.

**In practice:**

- A **cost ceiling is a contract line**, pinned in `CONTRACT.md` next to runtime and
  deploy target: cost per unit of work, and a monthly ceiling at expected volume.
- **The escape-hatch ladder**, cheapest rung first: deterministic code → cached result
  → small model → large model → human. Every call justifies why the rung below it does
  not work.
- **Measured, not estimated.** An estimate is *Inferred*; a measurement is *Evidence*.
  Rule 2 applies here exactly as it does everywhere else.
- **Model and effort selection are gated decisions, not taste.** If a smaller model
  passes every acceptance check, it is the correct model. The gate decides, not the
  vibe.
- **A cost regression fails CI** at PLATFORM tier, like any other test.

Full treatment in [COST.md](COST.md).

---

---

## Rule 6 — The Instrument Rule

> The checks are code too. An instrument you have not verified produces readings you
> cannot trust.

**The failure it prevents:** a green result that means nothing. Rules 2 and 3 govern
claims *about the code*. Nothing governed whether the apparatus producing those claims
actually worked, and on the first serious field test that gap produced four separate
defects.

Four clauses, each with a named failure behind it.

### 6a — Declare the toolchain before writing the gate

Every acceptance check names what must be installed to run it, and that is **confirmed
present** during CONTRACT, before the gate is written.

*Named failure:* a build ended at 35% coverage with thirteen rows recorded `PARTIAL`,
because the machine had no Node toolchain and the Docker daemon was down. The code was
written, the tests were written, and not one of them could be executed. The honest label
was available and correct, but the cost was avoidable: "what must be installed to run
this?" belongs beside "what's the hard part," and its absence is discovered at the worst
possible moment, at the end.

### 6b — Prove the check can fail

**Before recording what a check accepts, show it rejecting something.** A gate that has
never been observed going red is indistinguishable from a gate that is broken.

*Named failure:* `npm run lint` reported no problems for the entire build. It was not
linting cleanly. `eslint-config-next` applies a legacy patch on import that throws under
ESLint 9 flat config, so the command **crashed before linting anything** — and a crash
that prints nothing reads exactly like success.

And the negative control is itself a check, so it gets the same scrutiny. The known-bad
input must be one you have confirmed **survives into the artifact under test**.

*Named failure:* the first negative control for a credential scanner used a string the
build strips before output. The gate passed, and proved nothing. Only the second probe —
a string confirmed present in the built bundle — actually demonstrated the scanner could
go red.

### 6c — Evidence expires

A green result is evidence about **a moment**, not a property of the system. Wherever
inputs can drift beneath you — unpinned transitive dependencies, external services, model
versions, remote fixtures — the check must be re-run, and the drift pinned or watched.

*Named failure:* a CSS build that worked the day it was written failed weeks later with
**no source change at all**. A direct dependency was pinned exactly; its own native
scanner was declared with a caret range and had since resolved to a version whose options
type gained a required field. The defect arrived entirely from someone else's version
range.

The practical form: commit the lockfile, and treat "it built once" as a dated
observation rather than a standing fact.

### 6d — A number in prose is not a commitment

Any numeric claim in the contract is **bound to an assertion, or it is decoration.**
This is Rule 3 applied to figures rather than features.

*Named failure:* the contract promised at most 20 engine calls per watched job. The
decision record said "roughly 20." Nobody had counted. Measured against the real backoff
schedule through the full ceiling, the actual number was **23** — the stated ceiling was
being breached, in writing, by a document nobody could fail. The bound moved, and the
number now has a test that fails above 20.

Prose does not fail a build.

### Where the clauses run

| Clause | Phase | Cost |
|---|---|---|
| 6a — declare the toolchain | CONTRACT | one line per check |
| 6b — prove the check can fail | PROVE | one deliberate red per critical check |
| 6c — evidence expires | PROVE, and on every resume | re-run, don't recall |
| 6d — numbers are bound | CONTRACT, asserted at PROVE | one test per stated figure |

---

## Why exactly six

Each rule guards a different thing, and dropping any one of them opens a hole nothing
else covers:

| Rule | Guards | Added |
|---|---|---|
| 1. Brief | The input | v1 |
| 2. Evidence | The claim | v1 |
| 3. Traceability | The coverage | v1 |
| 4. Context | The reasoning | v1 |
| 5. Cost | The viability | v1 |
| 6. Instrument | **The measuring apparatus** | v1.1 |

Rule 6 was added because the first five all assume the checks work. Rules 2 and 3 ask
whether a reading is right; Rule 6 asks whether the thermometer does. That is a different
question, and it went unasked until a field test answered it four times in one afternoon.

The pattern to notice: **three of those four defects were in the gate apparatus or in
claims about the code, not in the code itself.** The framework was better at catching bad
software than at catching bad evidence about software, which is the more dangerous of the
two — bad software fails loudly, and bad evidence reports success.
