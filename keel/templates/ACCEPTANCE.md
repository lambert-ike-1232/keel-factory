# Acceptance Gate: [Project name]

Phase 2 of KEEL. The pass/fail gate. `CONTRACT.md` is the narrative source of truth;
this file is the checklist, and every line is a runnable command or an auditable
yes/no, so "is this done?" is never a matter of interpretation.

---

## The rule that makes this file worth having

**Every command listed here must actually exist and run.**

A gate citing a lint runner, test path, or eval command that is not in the repo is
worse than no gate: it manufactures confidence while verifying nothing, and it reads
as PASS to anyone who does not try the commands.

So: add a check here at the same moment you make it runnable, never before. Aspiration
goes under **Planned Checks**. When an audit finds a Required Check that does not
execute, that is a **critical** finding, not an UNKNOWN.

The same applies to what a check *measures*. An evaluation command that runs against
zero fixtures exits 0 and proves nothing — a populated fixture set is part of the
check, not a follow-up.

---

## Toolchain

*(Rule 6a. Fill this in before writing a single check below.)*

Every Required Check names what must be installed to run it, and that is **verified now**,
not at PROVE. A `MISSING` row is a finding at this phase, not a surprise at the end.

| Check | Requires | Present? | Verified how |
|---|---|---|---|
| `[command]` | `[runtime / daemon / system binary + version]` | verified / **MISSING** | `[the command that proved it]` |

If something is `MISSING`: install it, or move every check depending on it to **Planned**
and say so in the status report. Do not write a Required Check you cannot execute.

---

## Required Checks

Each line: one check, one command, runnable from a clean checkout.

**Each also carries a negative control** (Rule 6b): the known-bad input that makes it go
red. A check never observed failing is unproven, because a silent crash and a clean pass
produce identical output.

- [ ] Static checks pass — `[command]`
- [ ] Unit and integration tests pass — `[command]`
- [ ] Security checks pass for every sensitive flow — `[command]`
- [ ] All public inputs and outputs validate against `schemas/` — enforced by contract
      tests against real payloads, not by inspection — `[command]`
- [ ] Every non-public entry point rejects unauthenticated and under-privileged
      requests, proven by a test — `[command]`
- [ ] Sensitive data named in the Production Build Contract is not logged, leaked, or
      stored outside approved locations — proven by a test asserting *absence* — `[command]`
- [ ] Cost per unit of work is at or under the contract ceiling — `[command]`
- [ ] Every row in `TRACEABILITY.md` is `PASS` or `DESCOPED`. No blanks, no `FAIL`.
- [ ] CI runs this entire gate and blocks merge on failure.

*(PLATFORM adds:)*
- [ ] Evaluation harness passes against a populated golden fixture set — `[command]`
- [ ] The demo in `DEMO.md` runs from a clean checkout.
- [ ] API behaviour matches `openapi.yaml`.

---

## Planned Checks

Aspirational checks live here until they run. **Moving a line up is the moment it
becomes binding, and it may only move once the command exists and passes.** Record the
date it moved.

- [ ] [Planned check] — blocked on: [what has to be built first]

---

## Human Review Gates

Safety made structural: high-impact output is routed to review by this gate, not by
whoever happens to be coding.

- [ ] [Category] requires human approval before it takes effect.
      *(Name the real categories: legal, financial, safety, irreversible external
      actions, anything user-visible at scale.)*
- [ ] Generated output in a regulated or high-stakes category clearly identifies its
      evidence and its limitations.
- [ ] Deviations from this gate are recorded in `DECISIONS.md` and approved by
      [whoever owns that decision].

---

## Negative controls

*(Rule 6b. Run these **before** recording any result below.)*

For each critical check: the input that must make it fail, and confirmation that it did.

| Check | Known-bad input | Reaches the thing under test? | Observed red? |
|---|---|---|---|
| `[command]` | `[the probe]` | confirmed / **unconfirmed** | yes / no |

**The probe must survive into the artifact being checked.** A known-bad string that the
build strips before output proves nothing about a scanner reading build output — the gate
passes and tells you nothing. Confirm the probe is present, *then* confirm the check
catches it.

**A check that reports nothing is not a check that passed.** Make each one state its
scope — files scanned, cases run, assertions made — so an empty run is visibly empty.

---

## Gate result — [date]

Re-run in full, even if it passed recently. A green result is evidence about a moment, not
a property (Rule 6c).

| Check | Result | Command run | Scope reported | Negative control | Evidence |
|---|---|---|---|---|---|
| | PASS / FAIL | | e.g. "72 files scanned" | armed / **unarmed** | |

**Overall:** PASS / FAIL
**If FAIL, the blocking reason:** [one sentence]
**Any check still `unarmed`:** its green result is unproven. Say so in the status report.
