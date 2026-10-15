# Traceability Matrix: [Project name]

Seeded in Phase 2, regenerated and re-checked at Phase 5.

**This file exists because of a measured failure.** A previous build scored 90% on
professional standards and 96% on template completeness, but 78% on specification
coverage — and four of five gaps had the same shape: a spec line no acceptance check
was ever bound to. Nothing forced the binding, so partially-built features read as
finished.

---

## The rules

1. **One row per Feature List line in `CONTRACT.md`.** Same wording, same grain.
2. **A row with no bound check is `FAIL`, never a blank.** Blanks are the failure this
   file prevents.
3. **`DESCOPED` is a legitimate terminal state** — but only with a pointer to where
   the decision was made. A declared gap is a judgement call; an undeclared one is a
   failure of follow-through, and a reviewer is right to score them differently.
4. **Regenerated at PROVE**, not hand-maintained in between. Hand-maintained matrices
   drift toward optimism.
5. **Seeded all-`FAIL`.** At the end of Phase 2 nothing is built, so every row is
   `FAIL`. That is correct: the matrix starts honest and gets promoted by evidence.
6. **A row may only reach `PASS` on an armed check** (Rule 6b). A check nobody has watched
   fail cannot distinguish working code from a broken check.
7. **A `PASS` is dated** (Rule 6c). Where the check depends on anything that can drift
   underneath it, re-run before carrying the row forward.

## Status values

| Status | Means |
|---|---|
| `PASS` | Implemented **and** verified by something automated. Name the check. |
| `PARTIAL` | Exists but incomplete, unenforced, or untested. Say which. |
| `FAIL` | Required by the contract and absent. |
| `DESCOPED` | Deliberately not built for this version. Link the decision. |

---

## Matrix

| # | Feature line (from `CONTRACT.md`) | Acceptance check | Test | Armed? | Status | Evidence / note |
|---|---|---|---|---|---|---|
| 1 | | | | no | `FAIL` | |
| 2 | | | | no | `FAIL` | |
| 3 | | | | no | `FAIL` | |

**Armed** (Rule 6b) means the bound check has been observed *failing* on a known-bad
input. A `PASS` on an unarmed check is a claim about the check, not about the code — mark
it `PARTIAL` until the check has been seen to go red at least once.

---

## Descope register

Every `DESCOPED` row, restated with its reasoning. This section is read by reviewers
and is worth writing well — it is where deliberate scoping is distinguished from
things that quietly did not get done.

| # | Feature line | Why descoped | Decided in | Revisit when |
|---|---|---|---|---|
| | | | `DECISIONS.md#NNNN` | |

---

## Roll-up — [date]

| Status | Count | % |
|---|---|---|
| `PASS` | | |
| `PARTIAL` | | |
| `FAIL` | | |
| `DESCOPED` | | |

**Coverage** = (`PASS` + `DESCOPED`) / total. This is the number an external reviewer
computes whether or not you do, so compute it yourself first.
