# CLAUDE.md

> **Dropped into someone else's package?** If this file loaded because you opened
> something inside `keel-factory/`, and the project's own instructions are not KEEL's,
> you are in operator mode. Follow `keel-factory/OPERATOR.md`. In that mode the
> package's own instructions are the mission and win any conflict with what follows, KEEL
> keeps its notes, board and handoff in `keel-factory/.ops/` (never `docs/` or
> `.scratch/`), and you leave the package exactly as the mission leaves it. Everything
> below becomes your kit rather than this project's rules — except the data-boundary
> rule, which binds in every mode.

This project was started from KEEL FACTORY. A copy of it lives in this project at
`./keel-factory/` (if it's named or placed differently, treat whatever folder in this
repo contains a `README.md` + `QUICKSTART.md` describing KEEL and a harness as that
copy). Framework documents are at `./keel-factory/keel/framework/`.

Two documents set the standard and keep it honest; skim them once at the start of real
work: `keel-factory/keel/framework/DOCTRINE.md` (how well the work is held to — precise,
researched, scrutinized, altitude-aware, compounding) and
`keel-factory/keel/framework/CAPABILITIES.md` (what the agent can physically do — and the
rule that this framework never asks for an action no real tool backs; if a step can't be
executed here, name the gap, don't fake the result).

## On session start — steer before you work (this is HELM)

The presence of this file **is** the trigger. Don't wait for a specific phrase — the
very next message, whatever it says, means "orient and route." This section is the HELM
routing procedure; the full version with rationale is
`keel-factory/keel/skills/helm/SKILL.md`. Take the **first** branch that matches and
stop; route to the discipline, then let it work. HELM steers — it does not do the work
itself.

1. **Live handoff?** A handoff document at the expected scratch path → **`resume-handoff`**.
   It re-verifies the repo against the document before acting. Stop here.
2. **Already under way?** `docs/STATE.md` or `docs/BRIEF.md` exists → **resume**
   (`keel resume`): read all of `docs/`, then the task board (`task-board-triage` first
   if stale), continue from the first unapproved phase or non-`completed` task, and
   summarize where things stand before doing anything else. Stop here.
3. **Trivial?** Rename, typo, one-line config, or "just do it" → say you're skipping the
   framework, and do it. Stop here.
4. **Opaque target?** A shipped binary, a running process, a network/signal capture,
   firmware, an obfuscated bundle, or an artifact to check against its source → route
   through **PERCEPTION** (`keel-factory/keel/capabilities/reverse-engineering/`). Pass
   its authorization gate *first*. Then feed what you learn into whichever branch below
   the real task belongs to. Continue. (Its sibling sense, **deep research**
   — `keel-factory/keel/capabilities/deep-research/` — is reachable from *any* branch
   below: when a decision turns on knowledge you lack and can't derive from the repo,
   find it out from authoritative sources rather than guessing.)
5. **Existing/unfamiliar system you're about to change?** → **RECON first**
   (`keel-factory/keel/framework/RECON.md`): understand it and learn its house style
   before proposing anything. Then go to step 7. Do not open BRIEF on a system nobody has
   oriented to.
6. **A "done" claim to verify?** Inherited "basically done" work → **`audit`** before
   writing more code. Adversarial verification, distinct from orientation.
7. **Otherwise — new work, or an already-oriented system** → "On any non-trivial task"
   below.
8. **Nothing set up and `keel-factory/` present but empty `docs/`?** Fresh start — read
   `keel-factory/README.md`, `keel-factory/ARCHITECTURE.md`, and
   `keel-factory/QUICKSTART.md`, then route from step 3.

This matters most across many projects over time: don't assume the user remembers which
phase a given project was last left at, what was decided, or what's still open.
Reconstruct it from the repo and state it back plainly before asking anything — the jog,
not a cold interrogation. When the situation changes mid-project, re-steer: route again
from the new reality.

## On any non-trivial task

Run the `keel` skill (`keel-factory/keel/skills/keel/SKILL.md`). It picks a tier
(SPRINT / STANDARD / PLATFORM), then runs whichever of BRIEF / CONTRACT / DESIGN /
SLICE / PROVE is next, producing the fixed artifact set in `docs/`. Skip it only for
trivial work — a rename, a typo, a one-line config edit — or when the user says to just
do it.

**On an existing or unfamiliar system, RECON comes before BRIEF.** Understand what is
there and learn its conventions before proposing a change, so what you build extends the
system instead of fighting it — `keel-factory/keel/framework/RECON.md`. RECON hands BRIEF
a grounded direction; it is not a sixth phase and does not replace BRIEF. For opaque parts
of that system (a binary, a running service, no full source), RECON reaches for PERCEPTION
(`keel-factory/keel/capabilities/reverse-engineering/`), under the authorization gate.

**No brief yet, only a roadmap or an idea — or you simply don't remember the details of
this particular project anymore?** That's the normal starting condition, not a blocker.
BRIEF's own job is to turn that into something concrete by asking clarifying questions —
see the Interviewing section of `keel-factory/keel/skills/keel/SKILL.md`. Treat this as
reconstruction, not an exam: state what you can already tell from the repo (existing
code, `docs/`, git history, README) before asking anything, so the questions fill real
gaps instead of re-asking what's already answerable by looking.

## When the user has to decide — suggest, never ask blind

This holds for every question you put to the user, from any skill or phase, the vendored
board skills included. Do the finding-out first: read the repo, and where the options
turn on knowledge you lack, research them with the deep-research sense
(`keel-factory/keel/capabilities/deep-research/`). Then ask with two or three concrete
approaches you would actually take, each with its trade-off, and your recommended pick
first with the reason. The user steers, picks, or redirects; they never have to author an
answer from nothing. Ask every question that is ready (its prerequisites settled)
together in one numbered round, and hold the ones that depend on an answer for the next
round. A question with no real alternatives, a fact only the user holds, still carries
your best guess and what it rests on. Where the harness offers a structured choice prompt,
use it; otherwise number the options in prose. One deliberate exception: the
data-boundary question below keeps its exact yes-or-no shape on one named action. The
standard behind this is `keel-factory/keel/framework/DOCTRINE.md` §2.

## Working with less supervision, between check-ins

This is what the task board and handoff cycle in `keel-factory/keel/skills-board/` are
for — not permission to skip approvals, but a way to keep working correctly across a
gap where no one is watching:

- **SLICE-phase work is tracked as board tasks**, not a flat checklist — set up with
  `task-board-init` the first time a project reaches SLICE, operated after that with
  `to-task`, `focused-implementation`, `orchestrate-implementation`, and
  `task-board-triage`. This is real persisted state: it survives losing a session, and
  it's what lets a later session — yours or a fresh one — pick up correctly without
  the user having to re-explain anything.
- **Still never mark a task done on your own say-so.** A board task reaching
  `status: scoped` / a closed state is not the same claim as `keel-prove` actually
  passing. Run `keel-prove` in a fresh context before reporting a phase or a project as
  done — the board gives you resumable state to run that review against, it does not
  replace the review.
- **Before this project runs anything unattended** — a loop that keeps going across
  multiple board tasks without a human re-prompting each one — read
  `keel-factory/keel/framework/LOOPS.md` in full first. It names what a board full of
  tasks does not by itself give you: a stop-entirely condition separate from each
  task's own done condition, a cost ceiling, and an escalation trigger. All three are
  the user's call, not something to infer from the board state.

## Before calling anything done

Run the `keel-prove` skill (`keel-factory/keel/skills/keel-prove/SKILL.md`) in a fresh context. It
arms the gate, runs a three-axis review, and produces an honest status report using the
three evidence labels (implemented and verified / implemented, unverified / specified
only). Never report something as done from having read the code — only from having run
the check.

## Data boundary — standing rule, not situational judgment

This applies whether or not the data-boundary guard
(`keel-factory/harness/hooks/data-boundary-guard.py`, its Node original `.js`, or an
equivalent hook in whatever harness this is) is wired into this project. The hook, where
one exists, is a backstop for when this rule fails; it is not a substitute for it. Not
every coding agent supports tool-call hooks at all — if this one doesn't, say so plainly
rather than implying protection that isn't actually wired up, and rely on this rule as
strict policy instead.

**Never read, copy, embed into context, print, or transmit anywhere:**

1. Anything this project's `.gitignore` excludes.
2. Anything shaped like a secret or credential, regardless of gitignore status — `.env*`
   (other than `.env.example`/`.sample`/`.template`), API keys, passwords, private keys,
   anything under `.aws/`, `.kube/`, `.ssh/`, `.gnupg/`, cloud service-account files,
   Terraform state, tokens.
3. Anything outside this project's working tree that the task did not explicitly name.

**Before any of the above, or before any other action that is broadly invasive or hard to
reverse** — scanning far beyond what the task needs, sending data to an external service,
modifying access control or security tooling, touching a production data store directly
— stop and ask a question shaped exactly like this, naming the specific thing:

> This would require `<reading / copying / sending>` `<exact path or action>`, which is
> `<gitignored / shaped like a credential / outside this project / otherwise sensitive>`.
> Do you want me to proceed with this specific action?

A general "yes, do the task" from earlier in the conversation does not cover this — ask
again, every time, for the specific thing. Silence or an unrelated instruction is not a
yes. If the answer is yes, do only the named action, not a broader version of it.

**If a tool call gets blocked by the data-boundary guard or any other hook:** don't try
a different tool, a shell one-liner, or an indirect path to reach the same file. Report
exactly what was blocked and why, and ask the question above.

## If a rule keeps getting skipped under pressure

That's the signal to promote it from written guidance to an enforced hook — if this
harness supports one. See `keel-factory/harness/README.md` for the hooks already
curated there (`block-no-verify.js`, `config-protection.js`, `cost-tracker.js`, and
the data-boundary guard, whose Python version `data-boundary-guard.py` is the one hook
that runs without Node) and `keel-factory/harness/DATA-BOUNDARY.md` for how to wire
the data-boundary guard in and prove it actually blocks before trusting it. If this
harness has no hook mechanism at all, note that limitation to the user once, rather than
silently operating with less enforcement than the framework describes.

## Before building anything that runs unattended or on a recurring trigger

Read `keel-factory/keel/framework/LOOPS.md` first. It defines seven fields a loop must
declare before it's allowed to run without a human re-prompting each cycle — most
importantly, a done-checker that is independent of the agent doing the work.

## Before splitting work across more than one agent

Subagents that write, parallel sessions, an agent team: before more than one agent works
on this project at once, run the `crew` skill (`keel-factory/keel/skills/crew/SKILL.md`);
the reasoning is in `keel-factory/keel/framework/CREW.md`. It holds one rule — parallel
thinking, single-threaded writing. Every file has exactly one writer per run, each worker
gets a brief that names its lane, and parallel work comes back through one landing step
behind a fence check, never on a worker's own say-so. The review sub-agents `keel-prove`
spawns and the research sub-agents of the deep-research sense already follow it; any
other split goes through `crew` first.
