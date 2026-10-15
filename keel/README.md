# KEEL

**A general engineering framework for getting software from ideation to production, fast.**

A keel is the spine of a ship. Everything attaches to it, and it is what keeps the
thing upright when the weather turns. That is the job of this framework: give every
kind of decision a fixed place to live, so that speed comes from not re-deciding
rather than from cutting corners.

KEEL is built by stacking four existing frameworks that each solve a different
problem at a different time scale, then adding the two things none of them have:
**traceability** and **cost discipline**.

---

## The one-sentence version

> Fixed artifacts, composable process, and nothing is "done" until a command proves it.

## The one-paragraph version

Decisions are cheap while they are still sentences and expensive once they are code,
so KEEL front-loads every decision that can be written down: the brief, the contract,
the schemas, the acceptance checks, the type signatures. It front-loads *contracts*
only, never implementations, because implementations have to be learned from running
code. It then builds in thin vertical slices that each run end to end, reviews along
three independent axes, and refuses to call anything complete on the basis of a plan,
a schema, or a scaffold. Every feature line owns an acceptance check or is a declared
descope. Every run has a measured cost. Every claim carries an evidence label.

---

## The five phases

```
 (RECON)  →  BRIEF  →  CONTRACT  →  DESIGN  →  SLICE  →  PROVE
    │          │          │           │          │         │
 what's      what &    what must    what the   thin, end-  did it
 already &    why      be true      shapes are  to-end     actually
 its rules                                      slices     work
```

RECON is in parentheses because it is not one of the five phases — it is an orientation
gate that runs *before* BRIEF when the work targets an existing system, so changes
extend what's there instead of fighting it (`framework/RECON.md`). The five phases
themselves never change.

> **New here, or not sure how the parts relate?** Read `../ARCHITECTURE.md` — it maps
> KEEL (method), the task board (execution), REA/perception (seeing opaque systems), and
> the harness (enforcement) into one picture, with HELM (`skills/helm/SKILL.md`) as the
> front door that routes between them.

| Phase | Question it answers | Produces |
|---|---|---|
| **1. BRIEF** | What are we building, for whom, and what am I guessing? | `BRIEF.md` with every gap tagged `[GUESS: ...]` and resolved |
| **2. CONTRACT** | What must be true for this to be done? | `CONTRACT.md`, `ACCEPTANCE.md`, `schemas/`, `TRACEABILITY.md` seeded, `COST_MODEL.md` budget |
| **3. DESIGN** | What are the shapes, and what am I least sure about? | `DESIGN.md` — signatures with no bodies, seams, call stack, test plan, least-confident list |
| **4. SLICE** | Does a thin path through the whole thing run? | Board tasks (one per slice) + working code, one vertical slice at a time |
| **5. PROVE** | Is the claim of "done" true? | Three-axis review, the gate run, an honest status report |

The loop is not one-way. A later phase invalidating an earlier one sends that phase
back to "in progress" and requires re-approval. That is a normal event, not a failure.

## The three tiers

The phases never change. **How heavy each phase is** changes with the tier.

| | **SPRINT** | **STANDARD** *(default)* | **PLATFORM** |
|---|---|---|---|
| Scale | Hours | Days | Weeks, multi-session |
| Promise | Presentable | Production-ready | Full product |
| BRIEF | Rewrite + one question | Grilling rounds to empty frontier | Grilling, plus decision mapping when foggy |
| CONTRACT | Types on boundaries, 1 real check | Full contract, gate, schemas, traceability | + ops contract, eval harness, cost model |
| DESIGN | Least-confident list only | Signatures + seams + test plan | + ADRs, module-depth pass |
| SLICE | Tracer bullet, then ship | Vertical slices, TDD at agreed seams | + tickets, one per context window |
| PROVE | Gate + honest status | Three-axis review + full gate | + adversarial audit + demo from cold |

**The Floor** is what even SPRINT guarantees. It never bends:

1. A README a stranger can run from cold
2. A brief whose `[GUESS: ...]` list has been resolved
3. A contract on every boundary — a schema, or types
4. At least one acceptance check that runs, **and that you have watched fail once**
5. The toolchain for that check, named and confirmed present
6. No secrets on disk
7. An honest status report using the three evidence labels

## The six standing rules

These run underneath all five phases, at every tier.

1. **The Brief Rule** — every non-trivial task states a *standard*, points at the *information*, and defines *done*. Gaps are tagged `[GUESS: ...]`, never guessed silently.
2. **The Evidence Rule** — "specified" is never "implemented." Every claim is **Evidence** (observed), **Inferred** (reasonable, unverified), or **Missing evidence** (could not confirm). Code that has only been read has not been checked.
3. **The Traceability Rule** — every feature line owns an acceptance check, or is a declared descope. A feature line with no bound check is a `FAIL` row, never a blank.
4. **The Context Rule** — nothing important may exist only in chat. Compact to documents at every phase and slice boundary. Respect the smart zone (~150k tokens).
5. **The Cost Rule** — the cheapest thing that passes the gate wins. Cost is measured, budgeted in the contract, and checked in CI like a test.
6. **The Instrument Rule** — the checks are code too. Declare the toolchain before writing the gate, prove each critical check can fail before trusting it, treat evidence as expiring, and bind every stated number to an assertion.

Rule 6 is the newest and was added the hard way: on the first field test, **four defects
survived a green build** — a passing typecheck, a passing lint, a passing unit suite, and
a successful production build. Three of the four were in the gate apparatus rather than in
the code. The framework was better at catching bad software than bad evidence about
software, which is the more dangerous of the two, because bad software fails loudly and
bad evidence reports success.

---

## What KEEL is made of

KEEL is not original. It is an opinionated stack of four frameworks that operate at
different frequencies, plus two additions.

| Layer | Frequency | Source |
|---|---|---|
| **Measure** — traceability, evidence, cost, instruments | Across projects | **New in KEEL** |
| **Artifact** — the fixed document set | Per project | The Project Starter Template (`Planning/`) |
| **Process** — phases and gates | Per feature | The Software Factory, Dex Horthy / HumanLayer |
| **Session** — grilling, slices, context hygiene | Per session | The skills repo, Matt Pocock |
| **Brief** — prompt quality | Per message | The Thorsten Prompt, Thorsten Ball / Amp |

They stack rather than compete **because they run on different clocks.** Two
frameworks only conflict when they try to govern the same time scale. See
[framework/THE-STACK.md](framework/THE-STACK.md) — that idea is the whole design, and
it is the thing worth understanding before anything else here.

---

## File map

| File | What it is |
|---|---|
| [../ARCHITECTURE.md](../ARCHITECTURE.md) | **The whole-system map.** How method, execution, perception, and enforcement rope together, and how HELM routes between them. Read first if the parts feel disconnected. |
| [HOW-TO-USE.md](HOW-TO-USE.md) | The operational playbook. Start a project, run a session, resume after a gap. |
| [EXPLAINING-KEEL.md](EXPLAINING-KEEL.md) | How to teach, pitch, and defend this framework, including the hard questions. |
| [framework/THE-STACK.md](framework/THE-STACK.md) | How four frameworks combine into one, layer by layer, with every conflict resolved. |
| [framework/PHASES.md](framework/PHASES.md) | The five phases in operational detail. |
| [framework/RECON.md](framework/RECON.md) | The orientation gate before BRIEF: understand an existing system and learn its house style before changing it. |
| [framework/TIERS.md](framework/TIERS.md) | SPRINT / STANDARD / PLATFORM, and how to pick. |
| [framework/RULES.md](framework/RULES.md) | The six standing rules and why each exists. |
| [framework/COST.md](framework/COST.md) | Cost as an engineering constraint. The financial layer. |
| [framework/LOOPS.md](framework/LOOPS.md) | Running a loop unattended, safely — the seven required fields. |
| [framework/CREW.md](framework/CREW.md) | Several agents on one project without stepping on each other — lanes, briefs, and the LAND step. |
| [framework/TASK-BOARD-CROSSREF.md](framework/TASK-BOARD-CROSSREF.md) | Why the task board replaced `SLICES.md` and `task-interview` replaced BRIEF's own interview mechanism. |
| [framework/REA-CROSSREF.md](framework/REA-CROSSREF.md) | How REA (perception) ropes in — a different *axis*, not a clock — and the safety posture around it. |
| [framework/ECC-CROSSREF.md](framework/ECC-CROSSREF.md) · [MCKNIGHT-CROSSREF.md](framework/MCKNIGHT-CROSSREF.md) | The earlier placements: the harness layer, and the organization layer above the stack. |
| [templates/](templates/) | The artifact set to copy into a new project. |
| [skills/](skills/) | `helm` (the front door that routes), `keel` and `keel-prove` (the five phases), `crew` (splitting work across agents). |
| [skills-board/](skills-board/) | The task board, interview, handoff, and daily-workflow skills SLICE now runs on — see the task-board cross-ref before changing how these interact. |
| [capabilities/reverse-engineering/](capabilities/reverse-engineering/) | PERCEPTION: KEEL's governed wrapper for reaching REA when source can't answer, under the authorization gate. |
| [capabilities/deep-research/](capabilities/deep-research/) | The second sense: find out what you don't know from authoritative sources, triangulated and evidence-labeled, instead of guessing. |

## Provenance

**Version 1.1.** KEEL exists because a real project scored **88%** and the 12 points it
lost were not engineering points. Rule 6 and the sharpened Floor came later, from putting
v1 to work and watching what it still let through — see [CHANGELOG.md](CHANGELOG.md). Specification Feature Completion came in at 78% while Professional
Standards hit 90% and Template Representation hit 96%. Four of the five gaps had the
same shape: **a spec line that no acceptance check was ever bound to.** The work was
good; the bookkeeping was not. Rules 3 and 5 exist because of that, and the full
account is in [EXPLAINING-KEEL.md](EXPLAINING-KEEL.md).
