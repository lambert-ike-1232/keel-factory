---
name: helm
description: The front door for any project using KEEL FACTORY. Reads the situation in front of you and routes to the right discipline — resume, recon, brief, perception, audit, or just-do-it — rather than guessing. Run it first when picking up any project, new or existing, familiar or not. It routes and hands off; it holds no state and does no work of its own.
---

# HELM — where you steer

A keel is the spine of a ship; the helm is where you steer it. This skill is the one
place the whole framework is steered from: it classifies the situation and routes to the
discipline that fits. **It is a decision procedure, not an engine.** It does no analysis,
holds no state, and adds no rules. If you find yourself *doing work* inside HELM, you
have routed wrong — hand off to the discipline and let it work.

Why this exists and why it is deliberately thin: `../../../ARCHITECTURE.md` §2. The short
version is that a heavy "master control module" would be a second method competing with
KEEL on the same clock, which is the exact conflict the framework is built to avoid. So
HELM steers and gets out of the way.

## First, whose project is this?

If you were dropped into someone else's package — its own instructions exist and are not
KEEL's — you are in operator mode: follow `../../../OPERATOR.md`. The branches below still
route the work, but with the package's instructions as the brief, KEEL's state kept in
`keel-factory/.ops/`, and no phase stops beyond its rules of engagement.

## The routing procedure

Work top to bottom. Take the **first** branch that matches; do not keep going once one
fits.

### 0. Is there a live handoff to resume?

If a handoff document exists at the expected scratch path → **run `resume-handoff`**
(`../../skills-board/*/resume-handoff`). It re-verifies the repo against what the handoff
claims before acting. Do not re-orient from scratch when a previous session already left
a verified baseline. Stop here.

### 1. Is this project already under way?

If `docs/STATE.md` or `docs/BRIEF.md` exists → **resume** (`keel resume`). Read every
document in `docs/`, then the task board (run `task-board-triage` first if it looks
stale), and continue from the first unapproved phase or first non-`completed` task.
Summarize where things stand — plainly, assuming the user may not remember this project's
exact state — before doing anything else. Stop here.

### 2. Is the task trivial?

A rename, a typo, a copy change, a one-line config edit, or the user says "just do it" →
**skip the framework.** Say you are skipping, and do the task. Stop here.

### 3. Is the target opaque — a system you cannot fully read as source?

A shipped binary, a running process you must observe, a network/packet/signal capture,
firmware, an obfuscated or packaged bundle, or a built artifact you must check against
its source → **route through PERCEPTION** (`../../capabilities/reverse-engineering/`).
Pass the authorization gate *first* — name the exact target, confirm it is yours or
authorized, keep runtime/mutation as a separate approval. Perception does not replace the
rest of routing: once you can see the thing, feed what you learn into whichever branch
below the real task belongs to (usually RECON or a hard bug). Continue.

**Either sense is reachable from any branch, not just here.** Perception has a sibling:
when a decision in *any* branch turns on knowledge you lack and cannot derive from the
repo — an unfamiliar technique, a protocol, a best practice — reach for the **deep-research**
sense (`../../capabilities/deep-research/`): authoritative sources, triangulated,
evidence-labeled. Finding out is a required move, not an optional one; guessing where you
could have known is the failure the doctrine forbids (`../../framework/DOCTRINE.md` §2).

### 4. Is this an existing or unfamiliar system you are about to change?

If the project exists and you do not already know its shape and conventions cold →
**run RECON first** (`../../framework/RECON.md`, template `../../templates/RECON.md`).
Understand what is there and learn its house style *before* proposing anything. RECON
hands BRIEF a grounded direction. Do not open BRIEF on a system nobody has oriented to
yet. Then go to §6.

### 5. Is there a claim of "done" to verify?

Inheriting work described as "basically done," or checking a doneness claim before
trusting it → **run `audit`** (`keel audit`, `../../templates/AUDIT.md`) before writing
more code. Audit is adversarial verification; it is not orientation. If you also need to
understand the system to improve it, that is RECON (§4), and often you do recon first and
audit later. Route by the actual question — see the gradient in `../../../ARCHITECTURE.md`
§5.

### 6. Otherwise: new work with a clear-enough shape.

Greenfield, or an existing system you have already oriented to → **run the `keel` skill**
from BRIEF. Pick the tier, grill the brief into decisions (via `task-interview`), and
proceed through CONTRACT → DESIGN → SLICE → PROVE, stopping for approval at each gate.

## After routing

- The discipline you routed to owns the work and the conclusion. HELM does not supervise
  it.
- The six standing rules (`../../framework/RULES.md`) run underneath whatever you routed
  to — evidence labels, traceability, cost, context, the data boundary, the instrument
  rule. HELM does not enforce them; it does not get to turn them off either.
- The doctrine (`../../framework/DOCTRINE.md`) is the standard the routed-to work is held
  to: precise not bloated, researched not guessed, scrutinized not asserted,
  altitude-aware, compounding. HELM routes to the discipline; the doctrine says how well
  it must be run.
- When the situation changes mid-project (a greenfield feature turns out to depend on an
  opaque third-party binary; a resume reveals the system is nothing like the stale docs
  claimed), re-steer: come back to this procedure and route again from the new reality.

## Altitude — the one behavior HELM keeps across every branch

Whatever you routed to, hold both the high level and the low level at once, and move
between them on demand — the systems-design-interview stance (`../../framework/DOCTRINE.md`
§4). The artifacts make the switch cheap and lossless: zoom out by reading the artifact at
that altitude (BRIEF/CONTRACT/RECON/ARCHITECTURE), drill down with grep/read/run on the
specific file or failing command. Check each against the other — a slice against the brief
it serves, a strategy against what `CAPABILITIES.md` says can actually be built here — and
name the altitude when you change it so the user can follow. A business-strategy question
and "why is this tool not loading right" are the same session at different altitudes, not
different tools.

## What HELM must never do

- **Do the work itself.** It routes. The moment it starts analyzing, briefing, or
  building, it has become the over-engineered master-control engine the architecture
  exists to prevent.
- **Skip the authorization gate** when routing to perception. That gate runs before the
  first REA call, every time.
- **Open BRIEF on an unoriented existing system.** That is the specific mistake RECON was
  added to prevent; routing past it defeats the point.
- **Re-interrogate the user** for what a handoff, `docs/`, or the repo itself already
  answers. Reconstruct first, ask only for the genuine gaps — the jog, not the exam.
- **Ask cold.** When routing genuinely needs the user, say which branch you think this
  is and why, name the alternative, and let them pick (`../../framework/DOCTRINE.md` §2).
