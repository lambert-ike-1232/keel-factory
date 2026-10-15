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

Every tier guarantees these six. They do not scale down, and SPRINT is not permission
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
| Blocking stops | 1 | 3 | 4-5 |

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
