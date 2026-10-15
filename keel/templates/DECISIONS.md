# Decisions & Implementation Notes: [Project name]

Written continuously. Two kinds of entry, kept separate.

This is where a decision gets its **one legal address**. A contract-affecting choice
that lives only in a diff is a choice nobody can find later, including you.

**Dead ends are kept, not deleted.** The wrong fix that taught you the root cause is
the most valuable line in a debugging entry, and deleting it means the next person
repeats it.

---

## Part A — Decisions

Short entries. One decision each. Numbered so `TRACEABILITY.md` can point at them.

### 0001 — [Title]
**Date:** [YYYY-MM-DD]
**Context:** [what forced a choice]
**Decision:** [what was chosen]
**Consequences:** [what this makes easy, and what it makes hard]
**Status:** active / superseded by [NNNN]

*Never rewrite an old decision. Supersede it.*

---

## Part B — Debugging sessions

Dated. One per real investigation. The shape matters: it is what makes the entry
useful to someone who was not there.

### [YYYY-MM-DD] — [Symptom in one line]

**Symptom:** [what was actually observed, in the terms the user would use]

**Feedback loop:** [the one command that went red on this bug. Deterministic, fast,
runnable unattended, asserting the exact symptom.]

**Wrong fix attempted:** [what was tried and why it seemed right. **Keep this.**]

**Root cause:** [what was actually happening]

**Fix:** [what changed]

**Regression test:** [the test that now locks it down — or, if no correct seam existed
to test it at, say so. *That is itself a finding:* the architecture is preventing the
bug from being locked down.]

---

## Part C — Deviations from the gate

Anything that departs from `ACCEPTANCE.md`, with who approved it.

| Date | Deviation | Reason | Approved by |
|---|---|---|---|
| | | | |
