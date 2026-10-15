# KEEL Changelog

Every rule here has a named failure behind it. This file records which failure, and when.

---

## v1.1 — 2026-08-25

**Added Rule 6, the Instrument Rule.** The first five rules all assumed the checks work.
Nothing examined that assumption, and the first serious field test broke it four times in
one afternoon.

### What happened

Building a web UI for an existing translation engine, v1 caught four things before any
frontend code existed — the largest being that the engine could never have deployed to the
platform its config targeted, because it depends on a system binary that platform cannot
install.

Then the gates ran. **Four more defects turned up that had survived a completely green
build**: passing typecheck, passing lint, passing unit suite, successful production build.

| Defect | Why reading could not catch it | Rule added |
|---|---|---|
| Build had stopped being reproducible — a transitive caret range moved to a version with an incompatible options type | No source changed. It worked the day it was written and broke on its own | **6c** evidence expires |
| A field was dropped at a serialization boundary; every screen showed a UUID instead of a filename | Both sides individually correct, both individually tested. No test crossed the join | **round-trip** rule in DESIGN |
| A stated cost ceiling of 20 was actually 23 | The number lived in prose. Prose does not fail a build | **6d** numbers are bound |
| The lint gate had never once executed — it crashed on import before linting anything | A silent crash and a clean pass produce identical output | **6b** prove the check can fail |

And separately: the build ended its first pass at 35% coverage with thirteen rows
`PARTIAL`, because the machine had no Node toolchain and Docker was down. Honest, but
avoidable — hence **6a**, declare and verify the toolchain before writing the gate.

### The shape worth naming

**Three of those four defects were in the gate apparatus, not the product.** v1 was better
at catching bad software than at catching bad evidence about software — which is the more
dangerous of the two, because bad software fails loudly and bad evidence reports success.

### Changes

**Rules**
- **New Rule 6 — Instrument**, in four clauses: 6a declare the toolchain, 6b prove the
  check can fail, 6c evidence expires, 6d bind every number.
- **Rule 2 sharpened.** "An unrun gate is not much better than a gate whose command does
  not exist" became **"an unrun check is not weak evidence, it is no evidence"**, plus
  *code that has only been read has not been checked.* The original phrasing was too
  generous, and four defects out of four proved it.

**The Floor** — grew from six items to seven.
- Item 4 now reads "at least one acceptance check that runs, **and that you have seen
  fail**."
- New item 5: the toolchain for that check, named and confirmed present.

**Phases**
- **CONTRACT** — two new steps: declare and verify the toolchain (with a `MISSING` row
  treated as a finding at this phase), and bind every stated number to an assertion.
- **DESIGN** — new *round trips* requirement: for every field a consumer reads, one test
  crossing producer → storage → serialization → consumer. Testing at a seam is not the
  same as testing across one.
- **PROVE** — new step 2, *arm the gate before you trust it*, ahead of running it. Two
  sub-rules: the probe must reach the thing under test, and a check that prints nothing is
  not a check that passed. New closing rule: **a gate never observed failing is unproven.**

**Templates**
- `ACCEPTANCE.md` — new Toolchain table, new Negative controls table, gate result gains
  *scope reported* and *negative control* columns.
- `CONTRACT.md` — new Toolchain and Bound numbers sections.
- `TRACEABILITY.md` — new **Armed?** column; a row may only reach `PASS` on an armed check.
- `DESIGN.md` — new Round trips table and Numbers this design commits to table.

**Skills**
- `keel` — Rule 6 added to the standing rules; phase outputs updated; *cross every join*
  added to the building rules.
- `keel-prove` — new step 0, arm the gate first. The Gate sub-agent now reports each
  check's scope, and a check that exits 0 having examined nothing is a CRITICAL finding.

**Docs**
- `THE-STACK.md` — the Measure layer gains **instruments** as a third concern, with the
  reasoning for why instrument decay belongs on the slowest layer: a dependency range
  drifts over weeks, and only the across-projects layer has a long enough baseline to see
  it. Five rows added to the failure-mode table.
- `EXPLAINING-KEEL.md` — "how do you know it works" now answers with the field test
  including its failures; new hard question, *"four defects got past your gates, doesn't
  that undermine it?"*; the negative-control demo added to the show-don't-tell list.
- `HOW-TO-USE.md` — six new common mistakes, arming added to the PROVE walkthrough.

### The self-referential bit

A framework that has never been observed failing is in exactly the position of a gate that
has never been observed failing. v1.1 exists because v1 was watched failing, which is the
only reason to trust either of them slightly more today than yesterday.

---

## v1.0 — 2026-08-22

Initial version. Five phases (BRIEF · CONTRACT · DESIGN · SLICE · PROVE), three tiers
(SPRINT · STANDARD · PLATFORM), five standing rules, a six-item Floor.

Built by stacking four existing frameworks that run on different clocks — the Thorsten
Prompt (per message), Matt Pocock's skills (per session), the Software Factory (per
feature), and a project template of my own (per project) — then adding the two things none
of them had: a **traceability matrix** and **cost discipline**.

**The failure behind it:** a project scored 88%, with 90% on professional standards and
96% on template completeness but **78% on specification coverage**. Four of the five gaps
had the identical shape — a spec line that no acceptance check was ever bound to. The
engineering was not the problem; the bookkeeping was. Rule 3 exists because of that.
