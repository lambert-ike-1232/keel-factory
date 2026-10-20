---
name: keel-prove
description: Prove a claim of done. Arms the checks, runs fresh-context reviewers (standards, spec, and gate above SPRINT), promotes the traceability matrix on evidence, measures cost and writes an honest status report. Use before calling a feature or project done, or when asked whether it is.
---

# KEEL — Prove

Turn a claim of "done" into a fact, or find out it is not one.

Run this in a **fresh context**. An agent that just wrote code is the worst possible
reviewer of it. If you are that agent, you still run this skill: you orchestrate, and the
reviewer agents in step 3 do the reviewing. At SPRINT, spawn two of them (Standards and
Spec); you may run the gate's commands yourself, because an exit code does not depend on
who runs it, and the report says the gate was run by the builder. Above SPRINT, spawn all
three. The review is always by agents.

In a copied skill (this file sits under a project's `.claude/skills/` or
`.agents/skills/`, not under `keel/`), read every `../` path under `keel-factory/keel/`,
and root files such as `CLAUDE.md` under `keel-factory/`, even when the project has a
file of that name.

## First, is KEEL switched on here?

If KEEL is not switched on here (no `.keel/` or `keel-factory/` by HELM's rule), or a
`.keel/` holds no `keel.json`, run HELM's switch-on first (`../helm/SKILL.md`, its
"First — is KEEL switched on here" section), then come back.

In operator mode (`.keel/keel.json` says operator; or no role is recorded, as with a
linked or copied `keel-factory/`, and by HELM's rule the project carries its own
instructions that are not KEEL's; or the session note, the user or your brief says so; or
switch-on just decided it), `../../../OPERATOR.md` governs: every record this skill would
keep under `docs/` or on the task board goes in `<ops>`, KEEL's notes folder defined
there, never in the package's own tree.

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
propose one (the commit the work started from, from `docs/STATE.md` or `git log`) and
say which. Confirm it resolves and the diff is non-empty **before** spawning anything:

```
git diff <fixed-point>...HEAD          # committed work
git log <fixed-point>..HEAD --oneline
git diff <fixed-point>                 # uncommitted work: the working tree
git ls-files --others --exclude-standard
```

KEEL does not commit without the user's word, so the work under review is often
uncommitted: then the review covers the working tree against the fixed point, plus the
untracked files. Tell each reviewer which of the two it is reviewing.

A bad ref should fail here, not inside the parallel sub-agents.

## 2. Find the sources

- **Spec:** `docs/CONTRACT.md`, plus any issue referenced in the commit messages.
- **Standards:** whatever the repo documents — `CONTRIBUTING.md`, a standards file,
  `CONTEXT.md` for vocabulary.
- **Gate:** `docs/ACCEPTANCE.md` and `docs/TRACEABILITY.md`.

## 3. Spawn the reviewers in parallel

Three of them, or two at SPRINT (Standards and Spec, with the gate's commands run by you).
They must not share context with each other or with whoever wrote the code. Each reports
under 400 words. Their instructions live in one place each, the agent files at the kit
root (`../../../agents/`):

| Reviewer | File | In Claude Code (KEEL plugin) |
| --- | --- | --- |
| **Standards** — documented standards and a code-smell baseline | `../../../agents/prove-standards.md` | subagent type `keel:prove-standards` |
| **Spec** — missing, wrong and unrequested behavior against the contract | `../../../agents/prove-spec.md` | `keel:prove-spec` |
| **Gate** — every Required Check run, scope reported, traceability rows checked | `../../../agents/prove-gate.md` | `keel:prove-gate` |

Hand each one the fixed point from step 1 and the paths from step 2; in operator mode,
each fresh-context run is also told the mode and `<ops>` in its brief. Nothing else: the
less of this session it sees, the more independent it is.

- **Claude Code with the plugin:** spawn the subagent types in one message, so they run
  at once.
- **Any other harness, or a linked kit:** spawn one fresh-context sub-agent per reviewer
  and give each the body of its file, after the frontmatter, as its instructions. In
  Codex, use `spawn_agent` without forking this conversation's history; the user asking
  for `keel-prove` is the explicit request Codex needs before it spawns agents.
- **No sub-agents at all:** say so, and run the reviews one after another in a fresh
  session, starting each from its file. Same-context review is not independent, and the
  status report says which way it was done.

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

Say first how the review was done: by which reviewer agents, in fresh contexts, or, if
none could be spawned, that it was not independent. At SPRINT, also say that the gate was
run by the builder. Then three categories, never blurred:

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
