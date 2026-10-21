---
name: helm
description: The front door to KEEL. Use it first whenever the user says "use KEEL", names helm, or opens a session in a project where KEEL is switched on (a .keel/ or keel-factory/ folder). Works out owner or operator and switches KEEL on, then routes to resume, RECON, BRIEF, perception, audit or just-do-it. Does no other work itself.
---

# HELM — where you steer

A keel is the spine of a ship; the helm is where you steer it. This skill is the one
place the whole framework is steered from: it classifies the situation and routes to the
discipline that fits. **It is a decision procedure, not an engine.** It does no analysis
and has no method of its own: apart from switching KEEL on (recording the role, probing
the guard, loading the always-on layer), it only routes. If you find yourself *doing
work* inside HELM, you have routed wrong — hand off to the discipline and let it work.

Why this exists and why it is deliberately thin: `../../../ARCHITECTURE.md` §2. The short
version is that a heavy "master control module" would be a second method competing with
KEEL on the same clock, which is the exact conflict the framework is built to avoid. So
HELM steers and gets out of the way.

## How you got here

- **Claude Code, KEEL installed as a plugin:** `/keel:helm`, or the model picked this
  skill because the user asked for KEEL. The plugin's session hook also names this skill
  in every session of a project where KEEL is on.
- **Codex, KEEL's skills linked into `~/.agents/skills/`:** `$keel:helm` (Codex names
  linked skills after the plugin manifest they sit under), or by description.
- **A linked or copied kit (`keel-factory/`):** the project's `CLAUDE.md` or `AGENTS.md`
  pointed here.
- **Sent by `keel`, `keel-prove` or `crew`,** because KEEL was not on, or its `.keel/`
  held no `keel.json`: switch it on below, then go back to that skill instead of routing.

Paths in KEEL's documents that start `keel-factory/` mean the kit root. Under the plugin
that is the plugin's folder, three folders above this skill's folder (`../../../`); the
session hook prints it.

In a copied skill (this file sits under a project's `.claude/skills/` or
`.agents/skills/`, not under `keel/`), read every `../` path under `keel-factory/keel/`,
and root files such as `CLAUDE.md` under `keel-factory/`, even when the project has a
file of that name.

## First — is KEEL switched on here, and in what role?

KEEL is on when the project root, or a folder above it inside the same git repository,
holds an entry named exactly `.keel/` or `keel-factory/`. Outside git only the session's
own folder counts, and a git worktree also counts its main checkout's `.keel/`. It is
never on inside the kit root, and an entry in `$HOME` or `/` does not count.

When it is on with a recorded role (`.keel/keel.json` says owner or operator), take that
role. First (step 2 below), load the layer unless its Data boundary section is in
context; the session note alone is not the layer. In Codex owner mode, also make sure the
project's `AGENTS.md` carries it (step 4). Either way, run step 3's allowlist check. Then
route; operator mode reads `../../../OPERATOR.md` first (step 5). A `.keel/` with no role
recorded still needs one: decide it below and run the steps. A `keel-factory/` (linked
or copied) is itself the switch: decide the role the same way, record nothing, and start
at step 2.

When it is not on yet, the user has just asked for it. Decide the role from what you can
see before asking anything:

- **Operator** — someone else's package: it carries its own instructions (a README,
  `CLAUDE.md` or `AGENTS.md`, contributor notes) that are not KEEL's, and the user wants
  a job done in it. Follow `../../../OPERATOR.md`. The package's instructions are the
  brief, there are no phase stops beyond its rules of engagement, and KEEL keeps its
  notes in `<ops>`. `<ops>` is `keel-factory/.ops/` whenever the project holds a
  `keel-factory/` (linked or copied), else `.keel/ops/`.
- **Owner** — the user's own project or idea: an empty or near-empty folder, a project
  whose instructions are KEEL's, or the user says it is theirs.
- **Can't tell** — ask once: both options, your pick first, and what it rests on
  (`../../framework/DOCTRINE.md` §2).

Then do these steps, in order, every time HELM switches KEEL on, however small the job
looks:

1. **Record the role** at the project root: the git root
   (`git rev-parse --show-toplevel`), or the session's folder outside git. If that root
   is `$HOME`, `/`, or the kit root (`../../../`, the folder that holds
   `keel/skills/helm/`) or inside it, say so and suggest the project's own folder: do not
   create `.keel/`, KEEL stays off, and the data-boundary rule runs as strict policy (the
   Data boundary section of `../../../CLAUDE.md`). If `.keel` exists and is not a
   folder, say so and leave it untouched: KEEL stays off and the data-boundary rule runs
   as strict policy. In operator mode, treat it as the package switching off a guard
   (rule of engagement 3) and stop to ask; linking the kit (`link_kit.py`) switches KEEL
   on through `keel-factory/`. If neither applies, run
   `git check-ignore -q .keel/keel.json` before writing the file (KEEL is still off, and
   git answers for a path that does not exist yet). If it succeeds, or a `.keel/` already
   there gets it blocked as matching this repo's .gitignore, warn that this repository
   ignores `.keel/`, so the guard will block KEEL's own role file and notes: an owner
   removes that ignore (`../../../MANUAL.md` §10); in operator mode, tell the user, and
   if the debrief copy is blocked, give the debrief in the reply only. Then write one
   file, `.keel/keel.json`, holding `{"role": "owner"}` or `{"role": "operator"}`. That
   file switches KEEL on: where KEEL's hooks run (Claude Code's plugin, or Codex with
   `--codex-hooks` trusted in `/hooks`), the guard arms on the next tool call and every
   later session starts with the always-on layer. Tell an owner that `.keel/keel.json`
   belongs in the repository: commit it by name with the work, never `.keel/` as a whole.
2. **Load the always-on layer now:** read `../../../CLAUDE.md`, the kit's own file, so
   this first session runs under it in any harness. If it does not open with the line
   `<!-- KEEL always-on layer -->` (a copied skill can reach the project's own file),
   read `keel-factory/CLAUDE.md` instead.
3. **Prove the guard is live,** then look for an allowlist that came with the repository:
   - (a) Once KEEL is switched on (step 1's `.keel/keel.json` written, or a
     `keel-factory/` in place; probe again if you probed before that), a Read of
     `keel-armed-check/.env` (a path that does not exist) must come back blocked. If it
     is attempted instead ("File does not exist", or a shell's
     "No such file or directory", means it was), say once that no guard is armed here,
     run the data-boundary rule as strict policy (the Data boundary section of
     `../../../CLAUDE.md`), and you may offer once to wire the fallback guard. In Claude
     Code that is the plugin's hook (`../../../harness/install_plugin.py`; the older
     `../../../harness/install_guard.py` covers only `keel-factory/` projects); in Codex,
     the same installer with `--codex-hooks`. KEEL's installers (`install_plugin.py`,
     with or without `--codex-hooks`, and `install_guard.py`) write machine-wide entries
     that run the kit they were run from. Run them from the master (or through a linked
     `keel-factory/`), never from a copy inside a project. With only a copy here, ask the
     user for the master's path; if there is no master, leave the wiring out and keep
     strict policy. New wiring arms from the next session (in Claude Code, a settings-file
     hook also once `/hooks` is opened, the plugin only from the next session; in Codex,
     once the hooks are trusted in `/hooks`); until a probe there comes back blocked,
     strict policy stands. Never hold the job on the answer.
   - (b) Read `.keel/data-boundary-allow` with the Read tool, and run
     `git ls-files -- .keel` (KEEL's hook blocks any command that names that file). If
     the file exists, show its entries to the user; where the only way to read is a
     shell command (Codex, usually), `ls -a .keel` shows whether it exists, and the user
     opens it. If git lists it, say it came with the repository and was not made by this
     user. In operator mode, treat it as the package switching off a guard
     (`../../../OPERATOR.md`, rule of engagement 3) and stop to ask.
   - (c) A submodule or a nested clone can bring its own, so also run
     `find . -path ./keel-factory -prune -o -name .keel -print` (it never names the file,
     so KEEL's hook allows it, unless `.keel/` or `keel-factory` is gitignored; then (d)
     applies). Each `.keel/` found below the root is handled like the root's: for one
     that is a link, say where it points, and if that is outside the project, ask the
     data-boundary question before reading through it; read its allowlist with the Read
     tool, and run `git -C <the folder that holds it> ls-files -- .keel` to see whether
     its own repository tracks it.
   - (d) If one of these checks (the listing in (c) included) is blocked with the reason
     'matches this repo's .gitignore', that block is the answer: the path it names is
     ignored (`.keel/`, `keel-factory/`, or the folder that holds a nested `.keel/`). Do
     not retry another way: say which check could not be run and ask the user to look in
     that folder (when the blocked check is the listing in (c), ask the user to look for
     `.keel` entries in submodules and nested clones instead); in operator mode, stop
     before going on.
4. **Codex, owner mode.** If `AGENTS.md` holds KEEL's v1.0 text (it says
   `This project was started from KEEL FACTORY.`), add no block: offer MANUAL §11's
   choice, replacing that text with the block (recommended, so the layer loads once) or,
   only where step 3's probe came back blocked (the guard wired and trusted; ask the
   owner to confirm `/hooks` also trusts KEEL's session hook), deleting it and relying on
   the hook. Where the probe was not blocked, offer only the replacement. Change the file
   only on the owner's yes.
   Otherwise (no v1.0 text), if the project's `AGENTS.md` has no line
   `<!-- KEEL always-on layer -->`, add the kit's `CLAUDE.md` to it once, creating the
   file if needed, so later Codex sessions get the layer without hooks. The block is the
   file as it stands, opening with that mark line (the file's own first line) and closing
   with `<!-- end KEEL always-on layer -->`. Just before the closing line, add: "Kit root
   for this block: the project's `keel-factory/` if it has one, else three folders above
   the real folder of the `keel:helm` skill (resolve its link first)." Operator mode never
   edits the package's `AGENTS.md`.
5. **Operator mode: read `../../../OPERATOR.md` before touching the package.** It is
   short, and it is the protocol: the package's rules win, `.keel/` or a linked or copied
   `keel-factory/` is KEEL's whole footprint (notes in `<ops>`), and the job ends with a
   debrief at `<ops>/debrief.md` whose claims carry Evidence / Inferred / Missing labels.
   A one-line fix still gets its debrief; "trivial" (§2 below) skips KEEL's phases, never
   the operator protocol.
6. **Owner mode: go to the routing procedure below.**

In owner mode the tier and the **stop mode** go in `docs/STATE.md` when BRIEF starts.
The stop mode is checkpoint by default and supervised at PLATFORM
(`../../framework/TIERS.md`, "Stop modes"). If the user's message doesn't settle it, it
is one question in BRIEF's first round, not a separate one.

## The routing procedure

Work top to bottom. Take the **first** branch that matches; do not keep going once one
fits.

### 0. Is there a live handoff to resume?

If a handoff document exists at the expected scratch path (`.scratch/handoff.md`, or
`<ops>/handoff.md` in operator mode) → **run `resume-handoff`**
(`../../skills-board/claude/resume-handoff`). It re-verifies the repo against what the
handoff claims before acting. Do not re-orient from scratch when a previous session
already left a verified baseline. Stop here.

### 1. Is this project already under way?

If `docs/STATE.md` or `docs/BRIEF.md` exists → **resume** (`keel resume`). Read every
document in `docs/`, then the task board (run `task-board-triage` first if it looks
stale), and continue from the first unapproved phase or first non-`completed` task.
Summarize where things stand — plainly, assuming the user may not remember this project's
exact state — before doing anything else. Stop here.

### 2. Is the task trivial?

A rename, a typo, a copy change, a one-line config edit, or the user says "just do it" →
**skip the framework.** Say you are skipping, and do the task. In operator mode the
debrief still follows (`../../../OPERATOR.md` §4). Stop here.

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
proceed through CONTRACT → DESIGN → SLICE → PROVE, stopping where the stop mode says:
every gate when supervised; once up front and at the PROVE report when checkpoint.

## After routing

- The discipline you routed to owns the work and the conclusion. HELM does not supervise
  it.
- The six standing rules (`../../framework/RULES.md`) run underneath whatever you routed
  to — brief, evidence, traceability, context, cost, instrument — and so does the
  data-boundary rule, which stands on its own in `../../../CLAUDE.md`. HELM does not
  enforce them; it does not get to turn them off either.
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
it serves, a strategy against what `../../framework/CAPABILITIES.md` says can actually be
built here — and name the altitude when you change it so the user can follow. A
business-strategy question and "why is this tool not loading right" are the same session
at different altitudes, not different tools.

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
