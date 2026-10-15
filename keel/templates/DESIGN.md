# Design: [Feature or project name]

Phase 3 of KEEL. **Stop point at STANDARD and above.**

The step everyone skips, and the cheapest bug prevention available. Read the code that
actually exists before writing any of this — never design against an imagined codebase.

---

## Files

[Every file created or changed, one line each on why it lives there.]

---

## Signatures

**No implementation bodies.** Types and signatures only. A human should read this
section in seconds and say "right" or "wrong."

```
[types and signatures here]
```

This is the highest information-per-token artifact in software: it pins down most of
the implementation and gets you the value of code review before the code exists.

---

## Seams

A **seam** is the public boundary tests observe behaviour at, without reaching inside.

| Seam | What it exposes | Why here |
|---|---|---|
| | | |

Rules:
- Prefer **existing** seams to new ones.
- Prefer the **highest** seam available.
- Fewer seams is better. The ideal number is one.
- **No test is written at an unconfirmed seam.** Agreeing them up front is how testing
  effort lands on critical paths instead of every edge case.

### Depth check

For each module: **delete it mentally.** If complexity vanishes, it was a pass-through
and should not exist. If complexity reappears across N callers, it was earning its keep.

And: do not introduce a seam unless something actually varies across it. **One adapter
means a hypothetical seam; two means a real one.**

| Module | Interface size | Deletion test | Verdict |
|---|---|---|---|
| | | | deep / shallow |

---

## Call stack

[For each main flow: what calls what, top to bottom.]

---

## Cost ladder

For every model call in this design, name its rung and why the rung below fails.
Cheapest first: deterministic code → cached result → small model → large model → human.

| Call | Rung | Why not one rung down |
|---|---|---|
| | | |

A deterministic pre-pass that handles the easy majority before any model call is
usually the largest single cost reduction available, and it makes the system faster and
more predictable at the same time.

---

## Test plan

Test names and what each one asserts, **before any of them exist**.

| Test name | Seam | Asserts |
|---|---|---|
| | | |

Expected values come from an **independent source of truth** — a known-good literal, a
worked example, the spec — never recomputed the way the code computes them.

### Round trips

For every field a consumer reads, one test crossing the **whole** path: producer →
storage → serialization → consumer, asserting the value arrives intact.

| Field | Produced by | Crosses | Consumed by | Round-trip test |
|---|---|---|---|---|
| | | | | |

*Why this has its own table:* a build shipped where the client sent a filename, the store
persisted it, and the response serializer dropped it — so every screen displayed a UUID.
Both halves were individually correct, both had passing tests, and **no test crossed the
join.** Testing at a seam is not the same as testing across one.

---

## Numbers this design commits to

*(Rule 6d.)* Any figure this design assumes — a budget, a bound, a threshold — and the
assertion that will hold it. Reasoned numbers are fine; unasserted ones are not.

| Figure | Value | Reasoned or measured | Asserted by |
|---|---|---|---|
| | | reasoned / measured | `[test name]` |

## Least confident decisions

**The most valuable section in this document.** Numbered. The calls most worth
challenging now, while changing them is free. This is the agent stating what it would
otherwise decide silently.

1. [Decision] — *options considered:* [two or three, one trade-off each] — *why I am
   unsure:* [...] — *what I will do absent an answer:* [the pick, and why]
2.
3.

*(At SPRINT tier, this section alone is the whole of Phase 3. Three bullets, thirty
seconds, still worth it.)*
