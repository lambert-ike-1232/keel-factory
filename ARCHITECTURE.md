# KEEL FACTORY — the whole system, and how it ropes together

This is the map. If you read one document to understand how every piece of this
framework relates to every other, it is this one. It exists because the factory grew
by accretion — KEEL, then the harness, then Miguel's task board, then a
reverse-engineering capability — and accretion without a map becomes a pile.

The short version: **four different *kinds* of thing, plus one thin layer that decides
which to use.** They are not four competing frameworks. They answer four different
questions, and a fifth thing routes between them.

---

## 1. The four layers are not peers — they are different kinds of thing

KEEL's founding idea (`keel/framework/THE-STACK.md`) is that frameworks nest instead of
competing when they run on different *clocks* — different time scales and concerns. That
idea extends past the original four sources. The pieces now in this factory sort into
four kinds:

| Layer | The question it answers | What it is | Where it lives |
|---|---|---|---|
| **Method** | *In what order must things become true for this to be production-ready?* | KEEL — five phases, three tiers, six rules | `keel/framework/`, `keel/skills/` |
| **Execution & memory** | *How does bounded work actually get done and survive across sessions without babysitting?* | Miguel's task board, handoff/resume, focused/orchestrate, interview, spike — and CREW, for work split across more than one agent | `keel/skills-board/`; CREW at `keel/framework/CREW.md` + `keel/skills/crew/` |
| **Perception (the senses)** | *How does the agent learn what it cannot already read — a system with no source, or knowledge outside this repo?* | Two senses: REA (see opaque systems) and deep research (see external knowledge) | `keel/capabilities/reverse-engineering/`, `keel/capabilities/deep-research/` |
| **Enforcement & portability** | *How does the method travel into any project and bind at the tool call, not just on paper?* | The harness — hooks, data-boundary guard, starter prompts, the drop-in copy | `harness/`, `START-PROMPTS.md`, root docs |

Read that table as the whole thesis. **Method** is the spine. **Execution** is the
hands. **Perception** is the senses — two of them: perceiving opaque systems (REA) and
perceiving external knowledge (deep research), the second being how the system "finds out
what it doesn't know" instead of guessing. **Enforcement** is the nervous system that
makes the rules actually fire. None substitutes for another, and none is "the framework"
alone.

Underneath all four run two things that are not layers but constraints on every layer:
the **six rules** (`keel/framework/RULES.md`, the invariants), and the **doctrine**
(`keel/framework/DOCTRINE.md`, the standard of *how well* each layer is run — precise,
researched, scrutinized, altitude-aware, ever-improving). And beneath even those, one
honesty constraint the whole thing rests on: **the grounding rule**
(`keel/framework/CAPABILITIES.md`) — the framework may only ask the agent to do what some
real tool can actually do. A capability the environment lacks is named and worked around,
never faked.

The reason the layering matters: a request like "take on any project, learn its
conventions, and improve it" is not a *method* request, or an *execution* request, or a
*perception* request. It is all of them in sequence, and the thing that was missing was
anything that knew the sequence. That thing is the fifth layer.

---

## 2. The fifth layer: HELM, the thin orchestrator

> **HELM is a decision procedure, not an engine.** It reads the situation in front of
> it and routes to the right discipline. It has no method of its own: apart from
> switching KEEL on, it only routes. It does no analysis of its own and adds no new
> rules. The ship already has a keel; HELM is only where you steer.

This is deliberate, and it is the single most important design decision in this
document. The user asked whether this should become "an entire orchestrator or master
control module." The honest answer, and the one consistent with KEEL's own standing
warning against speculative generality and premature abstraction
(`keel/framework/RULES.md`), is: **the orchestrator must be thin, or it becomes the
very over-engineering the framework exists to prevent.** A heavy master-control engine
would be a second method competing with KEEL — exactly the same-clock conflict
THE-STACK.md says to avoid.

So HELM is one routing procedure, written once, in the `helm` skill
(`keel/skills/helm/SKILL.md`). The always-on layer (`CLAUDE.md`: injected by the session
hook, read by HELM when it switches KEEL on, or carried in the project's own `CLAUDE.md`
or `AGENTS.md`) only points at it. It classifies, then hands off. That is all.

**How it reaches the agent (v1.1).** The master folder is a Claude Code plugin and the
source of Codex's skill links (`harness/install_plugin.py`). Both harnesses list KEEL's
skills by name and description and load a skill's body only when it is used. One small
hook script (`harness/hooks/keel_hook.py`) does the two jobs prose cannot: it injects the
always-on layer at session start, and it hands every file-touching tool call to the
data-boundary guard. Both act only where KEEL is switched on: a `.keel/` folder or a
`keel-factory/`, linked or copied, in the project's folder, or in a folder above it
inside the same git repository. Outside git only the session's own folder counts. KEEL
is never on inside the kit itself or from a marker in `$HOME` or `/`, and the master's
own git checkout never switches on the folder that holds it; the exact rule is in
[`harness/README.md`](harness/README.md). What each harness really offers, row by row
with evidence, is in `keel/framework/CAPABILITIES.md`.

**Two modes, one router.** In owner mode KEEL is the project's own framework:
`.keel/keel.json` says `owner`, and HELM routes every session. The factory can also be
dropped into someone else's package to do one job. That is operator mode (`OPERATOR.md`):

- the package's own instructions are the brief;
- KEEL keeps its state in `.keel/ops/` (or `keel-factory/.ops/` with a linked kit);
- phase stops collapse to the rules of engagement;
- the package is left exactly as the mission leaves it.

HELM's first question decides which mode applies. The branches after it are the same in
both.

### The routing procedure

```
                      ┌─────────────────────────────────────────┐
                      │  A message arrives in a project.         │
                      │  What kind of situation is this?         │
                      └─────────────────────────────────────────┘
                                        │
   ┌──────────────┬──────────────┬──────┴───────┬───────────────┬──────────────┐
   ▼              ▼              ▼              ▼               ▼              ▼
Resumable?   Existing but   Greenfield /   Opaque system   A claim of     Trivial?
handoff or   unfamiliar     clear new      (binary, live   "done" to      (rename,
docs/STATE   system?        feature?       process, no     verify?        typo, one
exist        ───────────    ───────────    full source)?   ───────────    line)?
───────────  RECON first    straight to    ───────────     KEEL `audit`   ───────────
resume-      (understand +  BRIEF          PERCEPTION       + REA for      just do it,
handoff /    learn the      (keel skill)   (REA) feeds      opaque parts   say you're
keel resume  house style)                  whichever of                   skipping
             then BRIEF                     the others
```

Every branch lands in a discipline that already exists. HELM's only job is to not start
in the wrong one — not to open BRIEF on a system nobody understands yet, not to run REA
on a plain source repo, not to re-interview when a handoff already answered everything.

---

## 3. What was genuinely lacking (and is now addressed)

Three gaps, found by tracing the user's own sentence — *"take on any project and know or
learn best practices for the infrastructure that's in place, while competently providing
means toward improving it"* — against what the factory actually had. A fourth turned up
later, from the manager's framing of the work as a team's.

### Gap 1 — no orientation discipline (the biggest one)

KEEL begins at BRIEF: *what are we building and why.* That is the right start for new
work. It is the wrong start for an **existing** system, where the first job is not to
decide what to build but to **understand what is already there and what conventions it
already keeps** — before proposing a single change. The factory had an `audit` entry
point, but audit is adversarial verification of a *claim of doneness*; it is not
orientation, and it assumes there is a claim to check.

**Addressed by RECON** (`keel/framework/RECON.md`, template `keel/templates/RECON.md`, a
pre-BRIEF orientation gate wired into the `keel` and `helm` skills). RECON produces an
evidence-labeled map of the existing system and, critically, its *house style* — the
conventions, patterns, and best practices already in force — so that improvement
proposals extend the system as it is rather than imposing a foreign shape on it. This is
the literal mechanism for "learn best practices for the infrastructure in place." It is
not a sixth KEEL phase; the five phases are left intact, as every prior addition has
left them. RECON feeds BRIEF.

### Gap 2 — no bridge from "understood" to "prioritized improvement"

Once a system is understood, KEEL can drive any single improvement through its phases,
and the task board can run many. What was missing was the step between: turning an
assessment into a *prioritized, convention-respecting improvement backlog* rather than a
pile of ad-hoc ideas. RECON's output feeds this directly: its findings become board
tasks (`to-task`), ordered by the assessment, each carrying the house-style constraints
it must respect. The bridge is now explicit in RECON.md's "From map to backlog" section.

### Gap 3 — perception was absent entirely

The agent could read source. It could not perceive a shipped binary, a running process,
a network capture, obfuscated bundles, firmware, or anything where source is absent or
not the whole truth. For "take on *any* project" that is a real blind spot — much
production reality is exactly these opaque surfaces.

**Addressed by integrating REA as a governed perception capability**
(`keel/capabilities/reverse-engineering/`), reached for only when source cannot answer
the question, and bound to the authorization discipline below.

### Gap 4 — the agent was written as a solo developer

*"You are a team, and I am the manager."* Nothing in the factory said how several agents
share one project without stepping on each other. `orchestrate-implementation` already
kept interfering streams apart, but it never said who runs each stream, what each worker
is told, or how parallel work comes back. `LOOPS.md` required a LAND step and gave it no
procedure.

**Addressed by CREW** (`keel/framework/CREW.md`; the `crew` skill at `keel/skills/crew/`;
triggered from `CLAUDE.md` whenever work is split across agents). It holds one rule:
parallel thinking, single-threaded writing. Lanes with exclusive write sets enforce it,
along with a self-contained brief for every worker and a LAND step behind a mechanical
fence check (`check_lanes.py`, proven to fail on bad input). It wraps the vendored
`orchestrate-implementation` without editing it, and it adds no phase.

---

## 4. How REA ropes in without conflict — and safely

Full treatment in `keel/framework/REA-CROSSREF.md`. The essentials:

**It sits on a different axis, not a different clock.** The other layers are about
*time* (per message, per session, per feature, per project). Perception is about
*access* — what the agent can see. A binary is equally opaque whether you look at it for
a second or a week, so REA does not compete with any phase; it is a tool any phase can
reach for. That orthogonality is why it ropes in cleanly.

**Its evidence model is already KEEL's.** REA distinguishes observations, inferences, and
unknowns, cites Evidence IDs, and refuses to imply that static analysis observed
execution. That is KEEL's Evidence Rule (Rule 2: Evidence / Inferred / Missing evidence)
in a different vocabulary. They are mapped one-to-one in the cross-ref, so a REA finding
drops straight into a KEEL status report or a board task's finding ledger without
translation. We reconcile; we do not stack a second evidence system.

**It is governed by the data-boundary discipline, extended.** This is the safety spine,
and it is non-negotiable:

- REA runs only against targets the user is **authorized** to analyze, and REA's own
  disclaimer (lawful analysis: security research, malware/incident analysis, coordinated
  disclosure, interoperability, software preservation, debugging software you own or are
  authorized to examine) is adopted verbatim as the boundary. The factory will not help
  circumvent protection measures, evade controls on systems you do not own, or any of the
  other uses REA itself refuses.
- **Read-only before anything that acts.** Static inspection is the default. Any
  operation that executes a target, attaches to a live process, mutates, intercepts
  traffic, or touches a device is a distinct, higher authorization that must be named and
  approved per the data-boundary rule — not inferred from permission to inspect a file.
  This mirrors REA's own separation (Ghidra ephemeral, IDA read-only) and the harness's
  own "ask before invasive or hard-to-reverse actions."
- The same *ask-before, name-the-exact-action, no-blanket-yes* rule that governs reading
  a gitignored file governs pointing REA at a target. One discipline, extended to a new
  capability — not a new discipline.

---

## 5. The overlap gradient — five ways to "understand existing state," placed so none is redundant

Adding RECON and REA created a cluster of "understand what's there" tools alongside what
the factory already had. They are not redundant; they sit on a gradient from broadest and
earliest to narrowest and most specific. Reach for the leftmost that fits.

| Tool | The question it answers | When |
|---|---|---|
| **RECON** | *What is this system, and what conventions does it already keep?* | First contact with an existing/unfamiliar system, before proposing anything |
| **REA** | *What is this opaque artifact actually doing?* | Any time the target is a binary / runtime / capture and source can't answer — serves RECON, SLICE, or a hard bug |
| **diataxis-audit / manage-docs** | *Is the documentation honest and well-shaped?* | When the question is specifically about docs health |
| **task-board-triage** | *Does the recorded plan still match the repo?* | When the board may have drifted from reality |
| **KEEL `audit`** | *Is this claim of "done" actually true?* | Adversarially verifying a doneness claim, before trusting inherited "basically done" work |

RECON orients; REA senses; the middle three are narrow health checks; audit is
adversarial verification. A single investigation may use several — RECON on first
contact, reaching for REA on the opaque parts, ending in audit before trusting a prior
claim — but each is invoked for its own distinct question.

---

## 6. The standing rules still run underneath everything

Nothing above weakens the six rules (`keel/framework/RULES.md`). They are the invariant
the whole stack preserves:

- **Evidence** — RECON findings, REA results, board tasks, and prove reports all carry
  the same three labels. A perceived fact and a verified fact are never blurred.
- **Traceability** — every improvement RECON proposes becomes a tracked task or a
  declared non-goal; nothing improves "in general."
- **Cost** — REA analysis, like model choice, is a cost; broad investigation is budgeted
  and bounded, not run open-endedly.
- **Context** — RECON maps and REA finding ledgers are written to disk, not held in chat;
  handoff carries them across boundaries.
- **Instrument & the data boundary** — the harness enforces what it can at the tool call;
  REA's higher-authority operations fall under exactly that enforcement.

HELM routes; the rules bind; the doctrine sets the standard; the grounding rule keeps it
all honest about what can actually be done. That is the whole architecture.

---

## 7. The two senses, and "find out what you don't know"

Perception is two senses, not one, and the second is the direct answer to "when the team
doesn't know how, it finds out."

- **See opaque systems** — REA (`keel/capabilities/reverse-engineering/`): binaries,
  runtime, captures, firmware. Placed and bounded in `keel/framework/REA-CROSSREF.md`.
- **See external knowledge** — deep research (`keel/capabilities/deep-research/`): when a
  decision turns on a technique, protocol, or best practice the repo cannot answer, find
  it from authoritative sources, triangulated, evidence-labeled — not a guess, and not a
  single search hit. Wired to real tools (web search/fetch, research subagents, a spike
  when running it settles the question).

Both obey the same evidence discipline: a perceived or researched fact is `Inferred`
until the actual system confirms it. "The docs say so" and "the binary appears to" are
never upgraded to `Evidence` without running the thing here.

---

## 8. Reading order for someone new to this

1. This file — the map.
2. `keel/README.md` — the method in one page.
3. `keel/framework/DOCTRINE.md` — the standard the whole system holds itself to.
4. `keel/framework/CAPABILITIES.md` — what the agent can physically do, and the rule that
   the framework never asks for more. (Short; read it before trusting any claim of a
   capability.)
5. `keel/skills/helm/SKILL.md` — the front door that routes to everything else.
6. `keel/framework/RECON.md` — how an existing system gets understood before it gets
   changed.
7. `keel/framework/CREW.md` — how more than one agent works on one project without
   collisions. Read it before splitting work.
8. The cross-refs (`ECC-`, `MCKNIGHT-`, `TASK-BOARD-`, `REA-CROSSREF.md`) — how each
   outside source was placed, and what was deliberately *not* absorbed from each.
