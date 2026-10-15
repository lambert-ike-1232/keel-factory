# Recon: [System or codebase name]

**Date:** [YYYY-MM-DD]
**Authorization:** [State it plainly. "My own project." / "Employer's repo, I'm on the
team." / "Client X, engagement scoped to Y." Recon reads a system; if any part of it is
a binary, a running service, or anything you do not own, the data-boundary rule applies
before you touch it.]

The orientation gate. Run this **before BRIEF** when taking on an existing or unfamiliar
system — before proposing a single change. Its job is not to decide what to build. Its
job is to understand what is already there and what conventions it already keeps, so that
whatever gets built next extends the system as it is rather than imposing a foreign shape
on it.

Skip recon only for a genuinely greenfield project (nothing exists yet) or a change so
small the system's shape is already obvious. When in doubt, a half-page recon is cheaper
than a change that fights the codebase.

Every claim in this document carries an evidence label, same as everywhere else in KEEL:
**Evidence** (observed — a file read, a command run, a test watched), **Inferred**
(reasonable from what was seen, not confirmed), or **Missing evidence** (could not
confirm). A guess about an existing system is more dangerous than a guess about a new
one, because the system will not warn you that you guessed wrong until the change lands.

---

## 1. What is this system?

[One paragraph, plain language. What it does, who runs it, what it is built on. Label
each claim.]

- **Purpose:**
- **Stack / runtime:**
- **Shape:** [monolith, services, library, CLI, firmware, a binary with no source, …]
- **How it is run / built / deployed:** [the actual commands, verified by running them
  where possible — not inferred from a README that may be stale]

## 2. The house style — conventions already in force

[This is the heart of recon and the literal answer to "learn the best practices of the
infrastructure in place." Do not propose your own conventions; find the system's. Read
enough real code, config, and history to state these with evidence, not taste.]

- **Code conventions:** [naming, file layout, error handling, how modules talk —
  observed in the actual code, with example file references]
- **Testing conventions:** [what kind of tests exist, where, what they assume, how they
  run]
- **Commit / PR conventions:** [from `git log` — message style, review flow, branch
  strategy]
- **What this codebase clearly values:** [inferred from repeated choices — e.g. "prefers
  explicitness over cleverness," "keeps modules small," "no new dependencies without
  strong reason." Label as Inferred; it is a read of patterns, not a documented rule.]
- **What it clearly avoids:** [the negative space is as informative as the positive]

## 3. The map

[The parts, how they connect, where the important seams are. A diagram or a short list.
For opaque parts — a shipped binary, a running service, an obfuscated bundle — this is
where PERCEPTION (REA) does the seeing; cite its Evidence IDs and keep its
observed/inferred/unknown distinctions intact.]

- **Entry points:**
- **Core modules / components and their responsibilities:**
- **External dependencies and services:**
- **The seams** [where a change would naturally cut; where contracts between parts live]:
- **Opaque regions** [parts you could not read as source, and how they were perceived if
  at all — or marked Missing evidence if not]:

## 4. Health and risk — read honestly

[Not a rewrite plan. An honest read of where this system is fragile, undocumented, or
surprising, each labeled. The point is to know the terrain before walking it.]

- **Fragile / high-churn / high-risk areas:**
- **Undocumented or surprising behavior:**
- **Tests you do NOT trust** [green that may not mean what it says — Rule 6 territory]:
- **Unknowns that matter** [things you could not determine and that a change would
  depend on — these are the first candidates for a spike or a focused REA pass]:

## 5. From map to backlog

[The bridge from "understood" to "improvable." Turn the assessment into a prioritized
list of candidate improvements — each one respecting the house style from §2, each
destined to become a board task (`to-task`) if the user agrees. This is a proposal to
the user, not a mandate to start.]

| # | Candidate improvement | Why (evidence from above) | House-style constraints it must respect | Rough size |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |

**Recommended first pick:** [the candidate you would start with, and why. The user picks
from the table, so lead with your recommendation rather than asking what they would
like.]

**Explicitly not proposing:** [improvements you considered and are ruling out, and why —
usually because they fight a convention the system deliberately keeps, or because the
evidence for them is too thin. Naming these prevents re-litigating them later.]

---

## 6. Handoff to BRIEF

[Recon does not decide what to build; it hands BRIEF a grounded starting point. State
the one or few improvements the user chose to pursue, and carry forward every relevant
house-style constraint and unknown so BRIEF and CONTRACT inherit them rather than
rediscovering them.]

**Chosen direction:**

**Constraints BRIEF/CONTRACT must honor (from §2 and §4):**

**Unknowns to resolve in BRIEF's grilling:**
