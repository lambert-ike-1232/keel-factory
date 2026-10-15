# Demo Script: [Project name]

A fixed, runnable proof sequence **from a clean checkout**. Not a sales script: a
verification that the thing works on a machine that has never seen it.

It is a Required Check at PLATFORM tier, which means it is not decoration — if it does
not run, the gate fails.

---

## Preconditions

- [ ] Clean checkout, no local state
- [ ] [Runtime and version] installed
- [ ] `.env` created from `.env.example` with [which values]
- [ ] Nothing else

---

## Sequence

Each step: the exact command, and what you should see. If what you see differs, that
is a failure, not a variation.

### 1. [Step name]
```bash
[exact command]
```
**Expect:** [exact observable outcome]

### 2. [Step name]
```bash
[exact command]
```
**Expect:**

### 3. Show a failure path
```bash
[exact command with bad input]
```
**Expect:** [the structured error, the rejection, the review-gate routing. A demo that
only shows the happy path is a demo of the happy path.]

---

## Total runtime

[Target: under five minutes. If it takes longer, the demo is doing too much.]

## If it fails

Do not fix it live. Note the step, run `AUDIT.md`, and treat it as a gate failure.
