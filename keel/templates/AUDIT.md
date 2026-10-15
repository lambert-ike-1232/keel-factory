# Audit: [Project name]

**Date:** [YYYY-MM-DD]

A point-in-time audit of what is *actually true* versus what is *claimed*. Where
`CONTRACT.md` and `ACCEPTANCE.md` define what done means going forward, this is the
adversarial look backward.

**Run this before writing more code** whenever you are: picking work back up after a
gap, inheriting a codebase, or checking a claim that something is "basically done."

---

## How to write this honestly

The way this document fails is optimism: counting a contract as a feature, a described
command as a working command, or a plan as an implementation.

**Every claim cites a file, and every claim carries a label.**

| Label | Means |
|---|---|
| **Evidence** | Directly observed. A file exists and contains X; a command runs and exits 0; a test asserts Y. |
| **Inferred** | A reasonable conclusion from docs or architecture, not verified in code. Never graduates without checking. |
| **Missing evidence** | Required, could not be confirmed either way. **Do not round up to "implemented."** |

Two rules that catch most self-deception:

1. **"Specified" is not "implemented."** A schema file, an OpenAPI path, or a runbook
   section describing a feature is evidence the feature was *designed*.
2. **If a gate command does not run, the gate is FAIL** — not UNKNOWN, not "PASS once
   we add tests." A gate citing a command that does not exist is itself a CRITICAL
   finding.

**Severity:** CRITICAL (blocks any production claim) · HIGH (will cause incidents or
breaking changes) · MED (real problem with a workaround) · LOW (cleanup, docs).

**Status:** PASS (implemented *and* verified) · PARTIAL (exists but incomplete,
unenforced, or untested) · FAIL (required and absent) · UNKNOWN (a finding, not a pass).

**Complexity:** S under a day · M 1-3 days · L about a week · XL multi-week, split it.

---

## 1. System overview

**Purpose:** [one paragraph, sourced from `CONTRACT.md`] — *Evidence:* `docs/CONTRACT.md`

**What is actually built:**
- Implemented, with evidence:
- Specified only, not implemented:
- Missing evidence:

**Data flow as it exists today:** [trace an actual request or job through the system as
it stands, not as designed. Mark every spec-only stage.]

**Entry points:** [every HTTP route, CLI command, scheduled process, script — each
marked **exists** or **described only**]

**External dependencies:** [explicit, from lockfile or config / inferred / missing]

---

## 2. Skeptical audit

Adversarial staff-engineer stance. Find what is wrong before a reviewer, an attacker,
or production does.

**Verdict:** production readiness PASS / FAIL — [one sentence]

### Findings

**[N]. [Title]**
- **Why it matters:** [concrete consequence — what breaks, for whom, when]
- **Severity:** CRITICAL / HIGH / MED / LOW
- **Evidence:** [exact paths and what they show, or the absence that proves the gap]

### Failure modes — check each explicitly

- [ ] A gate command that does not exist or does not run
- [ ] A permissive schema (`additionalProperties: true`, unconstrained domain fields)
- [ ] A test that cannot fail — passes against pre-change code, or recomputes the
      expected value the way the code does
- [ ] An eval or fixture command running against zero fixtures
- [ ] Secrets on disk, in the image, or in logs
- [ ] A traceability row that is blank rather than `FAIL` or `DESCOPED`
- [ ] A feature reported "done" whose proving command cannot be named
- [ ] Horizontal building — a layer with no vertical path through it
- [ ] Cost never measured, only estimated
- [ ] A decision that exists only in a diff or only in chat

---

## 3. Gap analysis

| Contract requirement | Status | Evidence | Severity |
|---|---|---|---|
| | PASS / PARTIAL / FAIL / UNKNOWN | | |

---

## 4. Plan to close the gap

Dependency-ordered. **Every task has a Verify command** — a task that cannot be
verified is not a task, it is a hope.

### Epic 1 — [name]
| # | Task | Blocked by | Complexity | Verify |
|---|---|---|---|---|
| 1.1 | | | S/M/L/XL | `[command]` |
