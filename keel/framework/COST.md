# Cost as an Engineering Constraint

The financial layer of KEEL, kept entirely inside engineering.

---

## Why this is an engineering document

A product that works and costs too much to run is a product that does not work. That
is an engineering failure, not a business one, and every lever that fixes it is an
engineering lever: which model, at which effort level, how much is cached, what is
batched, what could have been deterministic code, which infrastructure tier, whether
it runs locally at all.

So cost lives here. What falls out of it — unit cost, cost at volume, cost of the
alternative — happens to be the entire financial argument a buyer needs. Marketing
does not have to ask engineering for those numbers later, and engineering does not
have to do marketing. The numbers are a byproduct of building the thing correctly.

**The market this framework is aimed at:** people who need the product and do not want
to spend money. That constraint is not a compromise on quality. It is a design input,
and treating it as one produces better engineering, because every one of the levers
below also makes the system faster and more predictable.

---

## The cost budget is a contract line

In `CONTRACT.md`, alongside runtime and deploy target, three numbers:

| Line | Example |
|---|---|
| **Unit** | What one unit of work costs. "One 10-page document translated to 2 locales." |
| **Unit cost ceiling** | The maximum acceptable cost per unit. A number, not a hope. |
| **Volume ceiling** | Total monthly cost at expected volume, with the volume stated. |

A ceiling that was never a number is not a ceiling. If you genuinely do not know the
volume yet, write the number you are assuming and label it *Inferred* — that is what
the labels are for, and an assumption on the page gets challenged while an assumption
in your head does not.

---

## The escape-hatch ladder

**Every rung justifies why the rung below it does not work.** Climb only when forced.

| Rung | Cost | Use when |
|---|---|---|
| **1. Deterministic code** | ~0 | The rule is expressible. Regex, parser, lookup table, state machine. |
| **2. Cached result** | ~0 after first | The same input recurs. Exact-match first, then fuzzy if it earns it. |
| **3. Small model** | Low | Classification, extraction, routing, short structured output. |
| **4. Large model** | High | Genuine reasoning, long context, ambiguity, quality that is visibly worse one rung down. |
| **5. Human** | Highest | Judgement, liability, irreversibility. The Human Review Gates. |

The most common and most expensive mistake in AI products is doing rung 3 or 4 work
that rung 1 or 2 would have handled. A deterministic pre-pass that resolves 80% of
inputs before any model is called is usually the single largest cost reduction
available, and it makes the system faster and more predictable at the same time.

**Where this shows up in the phases:** the ladder is a DESIGN-phase question. For each
model call in the design, write which rung it is on and why the rung below fails. It
takes one line each and it is the highest-yield cost work you will do.

---

## The cheapest thing that passes the gate wins

Model choice and effort level are **gated decisions, not taste**.

The procedure:

1. Build the acceptance gate first (Phase 2). It defines quality.
2. Run the full gate against the cheapest plausible configuration.
3. If it passes, that is the configuration. Ship it.
4. If it fails, climb one rung and record *which check failed*. That failing check is
   now the documented justification for the more expensive configuration.

This inverts the usual order, where the biggest model is chosen first and cost
reduction is a project nobody ever gets to. Here, expense has to earn itself against a
named check, and you have written proof of why it was necessary — which is exactly
what a reviewer, a buyer, or a future you will ask for.

**Corollary:** you cannot do this without a real gate. Cost discipline is downstream of
acceptance discipline, which is another reason Phase 2 does not get skipped.

---

## Measured, not estimated

Rule 2 applies in full. An estimated cost is **Inferred**. A measured cost is
**Evidence**. A cost model built from list prices and arithmetic is a hypothesis.

**The measurement:** run the eval fixture set, record per unit — tokens in, tokens out,
wall-clock latency, cost in currency, and cache hit rate. Store the run in
`COST_MODEL.md` with a date and the configuration it was measured under. Change the
configuration, re-measure.

At PLATFORM tier, **a cost regression fails CI** exactly like a test regression. A
change that quietly triples per-unit spend is a defect, and it is a defect that no
other check in the suite will catch.

---

## The other levers, in rough order of payoff

1. **Deterministic pre-pass.** Handle the easy majority before any model call.
2. **Caching.** Exact-match caching is nearly free and often removes most repeat spend.
   Prompt caching removes most repeated-prefix cost on top of that.
3. **Batching.** Where latency is not user-facing, batch. Often a large discount.
4. **Right-sizing the model per call.** A pipeline is not one model. Classification,
   extraction, and routing steps rarely need the model the hard step needs.
5. **Right-sizing the effort level** on the calls that do need the big model.
6. **Truncation and retrieval discipline.** Stuffing context is the most common silent
   cost multiplier. Send what is needed.
7. **Self-contained and local-first packaging.** A single container the user runs
   themselves has no per-seat infrastructure cost at all, and it is a genuine
   engineering property with a genuine financial consequence.
8. **Infrastructure tier honesty.** Most projects do not need the managed tier they
   reach for. Pin the real numeric limits of the free or cheap tier in the contract
   and design inside them.

---

## What `COST_MODEL.md` produces

Three numbers, and they are the whole financial argument:

| Number | Question it answers |
|---|---|
| **Unit cost** | "What does one use of this cost?" |
| **Cost at volume** | "What will this cost me per month?" |
| **Cost of the alternative** | "Compared to what?" — the incumbent tool, the manual process, or the naive implementation |

The third is the one people skip and the one that does the work. "$0.04 per document"
means nothing alone. "$0.04 per document against $12 of a person's time, or $0.31 on
the naive single-large-model implementation" is an argument.

Every one of those numbers is produced by engineering, measured against fixtures, and
carries an evidence label. Nobody has to take them on faith, which is the point.

---

## The anti-pattern this section exists to prevent

Building the expensive version first, shipping it, and treating cost as a
post-launch optimisation project. That project does not happen. The architecture has
already hardened around the assumption of unlimited spend, the easy wins are now
refactors, and the cheapest moment to have made these decisions has passed.

Cost is like testability: nearly free if designed in, expensive to retrofit, and
invisible in a demo right up until it is the only thing anyone cares about.
