---
name: keel-prove
description: The KEEL PROVE phase - a three-axis review (Standards, Spec, Gate) in parallel sub-agents, the acceptance gate actually run, the traceability matrix promoted on evidence, cost measured, and an honest status report. Use when finishing a feature or project, before committing, or when asked whether something is done.
---

# KEEL — Prove

Turn a claim of "done" into a fact, or find out it is not one.

Run this in a **fresh context**. An agent that just wrote code is the worst possible
reviewer of it.

## 0. Arm the gate before you trust it

**Do this first, before recording any result.** A check never observed failing is
unproven: a silent crash and a clean pass produce identical output.

For each critical check in `docs/ACCEPTANCE.md`:

1. Feed it a **known-bad input** and confirm it exits non-zero.
2. **Confirm the probe reaches the thing under test.** A bad string the build strips
   before output proves nothing about a scanner reading build output. Verify the probe is
   present in the artifact, *then* verify the check catches it.
3. Note whether the check **reports its scope** — files scanned, cases run. A check that
   examined nothing and a check that found nothing look the same from the outside.

Record each as armed or unarmed. **An unarmed check's green result is `PARTIAL`, not
`PASS`**, and the status report says so.

Also confirm the toolchain each check needs is actually present. If it is not, that check
cannot produce evidence and its rows stay `PARTIAL` — say which command would close them.

## 1. Pin the fixed point

Whatever the user names — a commit, branch, tag, or merge-base. If they name nothing,
ask. Confirm it resolves and the diff is non-empty **before** spawning anything:

```
git diff <fixed-point>...HEAD
git log <fixed-point>..HEAD --oneline
```

A bad ref should fail here, not inside three parallel sub-agents.

## 2. Find the sources

- **Spec:** `docs/CONTRACT.md`, plus any issue referenced in the commit messages.
- **Standards:** whatever the repo documents — `CONTRIBUTING.md`, a standards file,
  `CONTEXT.md` for vocabulary.
- **Gate:** `docs/ACCEPTANCE.md` and `docs/TRACEABILITY.md`.

## 3. Spawn three sub-agents in parallel

They must not share context. Each reports under 400 words.

**Standards.** *"Report, per file or hunk: (a) every place the diff violates a
documented standard, citing the file and the rule; (b) any code smell from this
baseline, naming it and quoting the hunk. A documented repo standard always overrides
the baseline. Distinguish hard violations from judgement calls; baseline smells are
always judgement calls. Skip anything tooling already enforces."*

Paste this baseline in full — the sub-agent has no other access to it:
Mysterious Name · Duplicated Code · Feature Envy · Data Clumps · Primitive Obsession ·
Repeated Switches · Shotgun Surgery · Divergent Change · Speculative Generality ·
Message Chains · Middle Man · Refused Bequest.

**Spec.** *"Report: (a) requirements the contract asked for that are missing or
partial; (b) behaviour in the diff nobody asked for (scope creep); (c) requirements
that look implemented but where the implementation looks wrong. Quote the contract line
for each finding."*

**Gate.** *"For every Required Check in `docs/ACCEPTANCE.md`: run the command and
report the exit code, the output, and **the scope it reports** (files scanned, cases run,
assertions made). Do not reason about whether it would pass. A check whose command does
not exist is a CRITICAL finding, not an UNKNOWN. A check that exits 0 having examined
nothing is also a CRITICAL finding — flag any check that cannot state its scope. Then, for
every row in `docs/TRACEABILITY.md`, report whether its bound check exists, is armed, and
passes."*

## 4. Aggregate

Report under `## Standards`, `## Spec`, and `## Gate`, verbatim or lightly cleaned.

**Do not merge or rerank across axes.** A change can pass one and fail another — code
that follows every convention while implementing the wrong feature, or code that does
exactly what was asked while breaking every convention. Separation is what stops one
axis masking another. End with the worst issue *within each axis*, never a single
winner across them.

## 5. Promote the traceability matrix

Every row becomes `PASS` (with a named check that ran **and has been observed failing**),
`PARTIAL` (say what is missing, including "check unarmed"), `FAIL`, or `DESCOPED` (with a
pointer to the decision in `DECISIONS.md`).

**No blanks.** A blank row is how a sixty-percent-built feature reads as finished, and
it is the specific failure this whole file exists to prevent.

Compute the roll-up: coverage = (`PASS` + `DESCOPED`) / total. An external reviewer
computes this whether or not you do.

## 6. Measure cost

Run the fixture set. Record tokens in and out, cache hit rate, latency, and cost per
unit into `docs/COST_MODEL.md` with the date and configuration.

An estimate is **Inferred**. A measurement is **Evidence**. If it was not measured, say
so rather than reporting arithmetic as a result.

Check it against the contract ceiling. If a cheaper configuration was never tried, try
one: **the cheapest configuration that passes the gate wins**, and expense has to earn
itself against a named failing check.

## 7. The honest status report

Three categories, never blurred:

- **Implemented and verified** — the code exists and *this named command* proves it
- **Implemented, unverified** — the code exists, nothing tests it
- **Specified only** — a schema, contract, doc, or plan exists; no runtime behaviour does

If asked whether something is done, **answer by running the checks, not by recalling
what was written.** When a check cannot run, say so plainly rather than describing what
it would have proven.

## 8. Log it

`docs/DECISIONS.md` for contract-affecting decisions and any debugging entries (keep
the wrong fixes). `docs/AI_WORKFLOW.md` for what this phase caught — **and if it caught
nothing, record that too.** A phase that never catches anything should be questioned.
