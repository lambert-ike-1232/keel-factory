# Cost Model: [Project name]

Budgeted in Phase 2, **measured** in Phase 5.

An estimated cost is **Inferred**. A measured cost is **Evidence**. A model built from
list prices and arithmetic is a hypothesis, and it belongs in the Estimate section
until fixtures have been run against it.

---

## Budget *(from `CONTRACT.md`)*

| | Value | Label |
|---|---|---|
| Unit of work | | |
| Unit cost ceiling | | |
| Expected volume | | Evidence / Inferred |
| Monthly ceiling at volume | | |

---

## Configuration under measurement

| | |
|---|---|
| Date measured | |
| Models and effort levels | |
| Caching | [exact-match / prompt / none] |
| Batching | |
| Fixture set | [name, and how many fixtures] |

---

## Measured — [date]

| Metric | Per unit | Source |
|---|---|---|
| Tokens in | | |
| Tokens out | | |
| Cache hit rate | | |
| Wall-clock latency (p50 / p95) | | |
| **Cost per unit** | | |

**Against ceiling:** [under / over, by how much]

---

## The escape-hatch ladder

Every model call, with the rung below it ruled out. Cheapest first.

| Call | Rung | Why not one rung down | Share of total cost |
|---|---|---|---|
| | deterministic / cached / small model / large model / human | | |

**The cheapest configuration that passes the gate wins.** If a smaller model passes
every acceptance check, it is the correct model. Where a more expensive rung was
chosen, name the acceptance check that failed one rung down — that failing check is
the written justification.

| Cheaper configuration tried | Which check failed | Verdict |
|---|---|---|
| | | rejected / adopted |

---

## The three numbers

The whole financial argument, produced by engineering and measured against fixtures.

| Number | Value | How it was arrived at |
|---|---|---|
| **Unit cost** | | measured, [date] |
| **Cost at expected volume** | | unit cost × volume |
| **Cost of the alternative** | | [the incumbent tool, the manual process, or the naive single-large-model implementation] |

The third number is the one people skip and the one that does the work. A unit cost
alone means nothing; a unit cost against what it replaces is an argument.

---

## Regression watch

At PLATFORM tier a cost regression fails CI like any other test.

| Date | Cost per unit | Change | Cause |
|---|---|---|---|
| | | | |
