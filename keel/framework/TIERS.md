# Tiers

The phases never change. The weight of each phase does.

Three tiers, because three is the fewest that covers "I need it today," "this is real
work," and "this is a product." **STANDARD is the default.** Reaching for SPRINT is a
decision you make on purpose and say out loud, not a place you drift into.

---

## Picking one

Answer in order. The first yes wins.

1. **Is this throwaway code whose only job is to answer a question?**
   → Not a tier. That is a **prototype**: build it, learn from it, fold the answer into
   the real work, keep the prototype as a primary source out of the main branch. No
   tests, no error handling, no abstractions, clearly named as a prototype. KEEL does
   not govern it.

2. **Will anyone other than me depend on this within a week?**
   → No, and it is under a day of work → **SPRINT**
   → Yes → keep going

3. **Will this outlive one working session?**
   → No → **STANDARD**
   → Yes → keep going

4. **Does it need ops — deployment, incidents, on-call, an SLA, real users?**
   → No → **STANDARD**
   → Yes → **PLATFORM**

Tiers are per-effort, not per-repo. A PLATFORM product absorbs SPRINT-tier fixes all
the time. What must not happen is a SPRINT effort quietly becoming the foundation of a
product without being re-tiered, because the artifacts it skipped are exactly the ones
a product needs.

---

## The Floor

Every tier guarantees these seven. They do not scale down, and SPRINT is not permission
to skip them. This is what makes "in a pinch" mean *fast*, never *embarrassing*.

1. **A README a stranger can run from cold.** Not a description: instructions that work.
2. **A brief whose `[GUESS: ...]` list has been resolved.** Assumptions are stated, not buried.
3. **A contract on every boundary.** A schema, or types. Something that rejects malformed input.
4. **At least one acceptance check that runs, and that you have seen fail.** One real
   command beats ten described ones — but a command you have only ever seen pass is a
   command you have not tested. Break something on purpose once and watch it go red.
5. **The toolchain for that check, confirmed present.** Named and verified, not assumed.
6. **No secrets on disk.** Placeholder `.env.example` only. Verified, not assumed.
7. **An honest status report** using the three evidence labels.

The floor costs perhaps twenty-five minutes. It is the difference between work you can
show someone and work you have to apologise for.

Items 4 and 5 grew in v1.1. The original said only "a check that actually runs," and a
field test found a lint gate that had run on every build of an entire project while
**crashing before it linted anything.** A silent crash and a clean pass produce the same
output. Watching a check go red once is what separates them, and it costs a minute.

---

## SPRINT

**Hours. Presentable.**

For a fix, a small feature, a spike that has to survive contact with another person, a
demo tomorrow. The promise is *presentable*, not *production*, and the difference is
stated rather than hidden.

| Phase | What runs |
|---|---|
| BRIEF | The rewrite with `[GUESS: ...]`, one question, the announcement in one line. No grilling. |
| CONTRACT | Types on the boundaries. One Required Check. Cost ceiling if it calls a metered API. No schemas file, no full contract. |
| DESIGN | The least-confident list only. Three bullets. No signatures. |
| SLICE | Tracer bullet, then finish. Tests at one seam. |
| PROVE | **Stop.** Arm the one floor check (watch it fail once), run the gate, two-axis review (Standards + Spec), honest status report. |

**Artifacts:** `README.md`, `docs/BRIEF.md` (short form), `docs/ACCEPTANCE.md` (a
handful of lines), `docs/DECISIONS.md`.

**Blocking stops:** one, at PROVE.

**What you are explicitly giving up:** traceability, ops, audit, eval harness,
schemas. Say so in the status report. A declared limitation reads as judgement; an
undeclared one reads as an oversight.

---

## STANDARD

**Days. Production-ready. The default.**

For a real feature, a service, a tool other people will use. This is what "I built
this properly" means, and it is where KEEL is tuned to sit.

| Phase | What runs |
|---|---|
| BRIEF | Grilling rounds until the frontier is empty. Announcement. Intake filled in. |
| CONTRACT | **Stop.** Full Production Build Contract, feature list, acceptance gate with Required and Planned Checks, constrained schemas, traceability seeded, cost budget, human review gates. |
| DESIGN | **Stop.** Signatures with no bodies, confirmed seams, depth check, test plan, least-confident list. |
| SLICE | Vertical slices, tracer bullet first, TDD at the agreed seams, compact at each boundary. |
| PROVE | **Stop.** Negative control on every Required Check, then the full gate. Three-axis review (Standards + Spec + Gate). Traceability promoted on evidence. Cost measured against its bound assertion. Honest status report. |

**Artifacts:** the floor, plus `CONTRACT.md`, `TRACEABILITY.md`, `DESIGN.md`,
`STATE.md` + the task board, `COST_MODEL.md`, `CONTEXT.md`, `schemas/`, `CHANGELOG.md`,
`AI_WORKFLOW.md`, CI running the gate.

**Blocking stops:** three — CONTRACT, DESIGN, PROVE.

---

## PLATFORM

**Weeks. Multi-session. A full product.**

For something with users, deployment, and a lifespan. Everything in STANDARD, plus the
machinery for work that cannot fit in one head or one context window.

| Phase | What runs on top of STANDARD |
|---|---|
| BRIEF | **Stop.** Decision mapping when the work is foggy: chart the open questions, resolve one per session, plan rather than build. |
| CONTRACT | + ops contract (deployment, runbook), eval harness against golden fixtures, full cost model with volume projections. |
| DESIGN | + ADRs for decisions that outlive this feature, an explicit module-depth pass, `CONTEXT.md` as a maintained glossary. |
| SLICE | + tickets with blocking edges, each sized to one fresh context window, cleared between. |
| PROVE | + adversarial audit, demo from a clean checkout, cost regression in CI. |

**Artifacts:** everything, plus `ops/DEPLOYMENT.md`, `ops/RUNBOOK.md`, `DEMO.md`,
`AUDIT.md`, `docs/adr/`, `eval/`, `fixtures/`.

**Blocking stops:** four or five — BRIEF, CONTRACT, DESIGN, PROVE, and each ticket
boundary.

---

## Reading the tier table quickly

| | SPRINT | STANDARD | PLATFORM |
|---|---|---|---|
| The Floor | yes | yes | yes |
| `[GUESS: ...]` rewrite + debrief | yes | yes | yes |
| Grilling to empty frontier | no | yes | yes |
| Production Build Contract | no | yes | yes |
| Constrained schemas | no | yes | yes |
| Traceability matrix | no | yes | yes |
| Signatures with no bodies | no | yes | yes |
| Least-confident list | yes | yes | yes |
| TDD at confirmed seams | one seam | yes | yes |
| Three-axis review | two axes | yes | yes |
| Toolchain declared + verified | yes | yes | yes |
| Negative control on critical checks | the one floor check | every Required Check | + re-armed on every resume |
| Every stated number bound to a check | if any | yes | yes |
| Round-trip test across each join | no | yes | yes |
| Cost budget | if metered | yes | yes |
| Cost measured + in CI | no | measured | + CI |
| ADRs / `CONTEXT.md` | no | `CONTEXT.md` | both |
| Ops docs, eval harness, audit, demo | no | no | yes |
| Blocking stops (supervised mode) | 1 | 3 | 4-5 |

---

## Stop modes

The tier sets how heavy each phase is. The **stop mode** is a second dial: it sets which
of the tier's stops wait for a person. It never adds, removes or reorders a phase, and
it never lightens what a phase must produce.

| Mode | Waits for a person at | Runs on its own |
|---|---|---|
| **supervised** | every blocking stop the tier lists above | nothing between stops |
| **checkpoint** | one up-front round, one approval of BRIEF and CONTRACT together, and the PROVE report | DESIGN, SLICE, and the PROVE review itself |
| **unattended** | the same up-front approval, then nothing until the PROVE report | everything after the approval, inside `LOOPS.md` |

**Defaults:** checkpoint at SPRINT and STANDARD; supervised at PLATFORM, whose decisions
outlive the project and reach real users. The user can pick any mode; record it in
`docs/STATE.md` beside the tier. *(Chosen by the framework's owner, 2026-10-18.)*

**The up-front round** asks BRIEF's whole frontier and CONTRACT's production questions
together: who uses it and how they sign in, what data it holds and how long it keeps it,
where secrets live, where it runs and how anyone will know it is healthy (logs,
monitoring), which outside services it calls, the toolchain the checks need, and the
cost ceiling. Each question carries options and a recommended pick (`DOCTRINE.md` §2).
A question that depends on another's answer waits for a second round, still before the
approval.

**In Codex** the round depends on the mode (`CAPABILITIES.md`, Codex table; Inferred: no
Codex trial has run one). In Plan mode `request_user_input` takes options, so run the
round there. In Default mode there is no choice prompt, and KEEL's question rule asks one
question per turn, as a sentence that names the pick and the alternatives (`DOCTRINE.md`
§2, and the question rule in the always-on `CLAUDE.md`). The round then takes several
turns, one per question, all still before the approval.

**Why checkpoint is safe:** not because a person approves every phase, but because the
approved CONTRACT fixes what "done" means as runnable checks, every slice is proven by
running it, and PROVE is an independent review in a fresh context. A phase boundary in
checkpoint mode is a progress note (what was decided, what is next), not a question.

**Every mode still halts for:**

1. the data boundary, and any action that is irreversible or outward-facing (push,
   deploy, publish, migrate, delete what it did not create, send to an outside service);
2. a decision BRIEF and CONTRACT don't settle and that changes the outcome — asked with
   options and a pick;
3. a check still failing after three honest attempts — named, with what was tried;
4. a finding that breaks the approved CONTRACT — backtracking needs re-approval;
5. the cost ceiling.

**Unattended has nobody to ask.** There, a halt means: file it as a board task with
`gate: owner` or `gate: manual`, carry on with work that does not depend on it, and stop
at the PROVE report. Unattended needs `LOOPS.md`'s seven fields written into
`docs/STATE.md` before it starts, and a harness that can run without a person (a
headless run with a cost cap; `LOOPS.md` §6 says what each harness offers).

---

## Upgrading mid-effort

You will be wrong about the tier sometimes. The recovery is cheap **if you do it at a
phase boundary**, which is why the boundaries exist.

- **SPRINT → STANDARD:** go back and write CONTRACT properly, then seed the
  traceability matrix from the code that already exists, marking every row honestly.
  Rows without a check are `FAIL`, including ones already built. That is the point.
- **STANDARD → PLATFORM:** run the audit first. Do not add ops documents on top of
  unverified claims.

Downgrading is not a thing. You cannot un-promise production readiness once someone
depends on it.
