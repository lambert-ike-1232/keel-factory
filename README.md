# KEEL FACTORY

A portable engineering system, packaged so a new project can start from this folder
instead of re-deriving anything. **Copy this whole folder into a project's root
directory** (conventionally renamed `keel-factory/`), paste the prompt in
[`START-PROMPTS.md`](START-PROMPTS.md) as your first message to whichever coding agent
you're using, and it sets the project up from there — including writing a project-local
instruction file that makes every session after the first one self-orienting, with no
special phrasing required.

It is built to take on **any** project — greenfield or inherited, source you can read or
systems you can only observe — learn the conventions already in force, and improve them
without fighting them. How the parts cohere is the subject of
[`ARCHITECTURE.md`](ARCHITECTURE.md); read that if the folder ever feels like a pile
rather than a system.

## What's inside

Four kinds of thing, plus one thin layer that routes between them. The full model is in
[`ARCHITECTURE.md`](ARCHITECTURE.md) §1.

| Folder | What it is | The kind of thing it is |
| --- | --- | --- |
| [`RELEASES.md`](RELEASES.md) · `VERSION` | Which release this is (v1.0.0), and what each release changed and how it was proven. | the version record |
| [`MANUAL.md`](MANUAL.md) | **Lost track? Start here.** Everything from a blank machine to a finished job, in order, with the exact commands and prompts. | the instruction manual |
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | **The map.** How method, execution, perception, and enforcement relate; how HELM routes between them; what was lacking and how it was addressed. | the whole-system view |
| [`keel/`](keel/) | **KEEL** — five phases (BRIEF → CONTRACT → DESIGN → SLICE → PROVE), RECON before them on existing systems, three tiers, six rules, templates, and the `keel`/`keel-prove` skills. Plus `skills/helm/` (the front door), `skills/crew/` with `framework/CREW.md` (several agents on one project without collisions), and `capabilities/` (the two senses: reverse-engineering and deep-research). | **Method** — what must be true, in what order |
| [`keel/skills-board/`](keel/skills-board/) | Miguel's task board, interview, handoff/resume, focused/orchestrate, spike, diataxis. | **Execution & memory** — how work gets done and persists across sessions |
| [`keel/capabilities/`](keel/capabilities/) | The two **senses**: `reverse-engineering/` (reach **REA** to see opaque systems, under an authorization gate) and `deep-research/` (find out what you don't know from authoritative sources, wired to web search/fetch and research subagents). | **Perception** — learning what you can't already read |
| [`harness/`](harness/) | Curated **ECC** enforcement hooks + the data-boundary guard. | **Enforcement & portability** — binding the rules at the tool call |
| [`keel/framework/DOCTRINE.md`](keel/framework/DOCTRINE.md) · [`CAPABILITIES.md`](keel/framework/CAPABILITIES.md) | The standard the work is held to, and the rule that the framework only ever asks for what a real tool can actually do. | cross-cutting — *how well*, and *what's possible* |
| [`START-PROMPTS.md`](START-PROMPTS.md) | **Start here.** One starter prompt for any coding agent, plus precise Claude Code / Codex CLI variants. | the entry point |
| [`OPERATOR.md`](OPERATOR.md) | **Dropped into someone else's package?** The in-and-out protocol: the package's own instructions are the mission, KEEL is the kit underneath, and nothing is left behind but the work. | the other entry point |
| [`CLAUDE.md`](CLAUDE.md) | The project-local instruction file the starter prompt installs — it carries HELM's routing. Tool-agnostic; copied as-is into `AGENTS.md`, `.cursorrules`, etc. | — |
| [`QUICKSTART.md`](QUICKSTART.md) | The step-by-step the starter prompt automates. | — |

## Why two folders, not one merged framework

They run on different clocks, and merging them would hide that. KEEL is mostly prose —
rules you follow. ECC is mostly enforced — hooks that fail a tool call if you don't. The
full reasoning, including what each has that the other doesn't, is in
[`keel/framework/ECC-CROSSREF.md`](keel/framework/ECC-CROSSREF.md). The loop-engineering
material specifically — how to run an unattended, recurring task safely — is in
[`keel/framework/LOOPS.md`](keel/framework/LOOPS.md).

**`harness/` is deliberately partial.** It holds only the mechanisms KEEL's cross-reference
already evaluated and named — three hook scripts and twelve cited `SKILL.md` files — not
the full 3,500-file ECC download. That is the framework's own stated adoption posture
("cited, not absorbed") applied to this folder. The full ECC repo, if you want to browse
past what's curated here, was downloaded to `~/Downloads/ECC-main`
(`github.com/affaan-m/ECC`).

## Data privacy and security — read before using this against a real system

This factory is meant to be safe to point at a production project without a human having
to remember to protect anything by hand. Two layers, both required, neither one alone
sufficient — full detail in [`harness/DATA-BOUNDARY.md`](harness/DATA-BOUNDARY.md):

1. **The data-boundary guard** (`harness/hooks/data-boundary-guard.py`, with its Node
   original `data-boundary-guard.js`) — blocks, by default, any file access that
   is gitignored or shaped like a secret/credential. Default-deny; bypassing it requires
   a human to deliberately add a path to an allowlist file or set an override environment
   variable. Nothing in this factory does either of those for you.
2. **A standing rule in [`CLAUDE.md`](CLAUDE.md)** requiring the agent to name the exact
   sensitive path or invasive action and ask before attempting it — not a one-time
   blanket "yes" at the start of a session, a fresh, specific question every time.

**Honesty check on this claim, per KEEL's own Evidence Rule:** the Python guard,
`harness/hooks/data-boundary-guard.py`, has actually run. As of 2026-10-15 its 27-test
self-test passed, fifteen deliberately broken copies of it each failed that suite, and the
armed check blocked and allowed as required. The Node original has **not** been executed,
because the machine this factory was built on has no Node.js, so treat the `.js` as
`PARTIAL`. Either way, a hook proven on one machine is not proven on yours: run the armed
check in `harness/DATA-BOUNDARY.md` and watch it block before relying on it.

## Provenance

Copied from `~/Documents/FRAMEWORK/00 Engineering` (KEEL v1.1), `~/Downloads/ECC-main`
on 2026-09-28, and `~/Downloads/skills-main 2` (*Skills*, Miguel Hernandez, MIT) on
2026-10-14 — the last one now `keel/skills-board/`, cross-referenced in
[`keel/framework/TASK-BOARD-CROSSREF.md`](keel/framework/TASK-BOARD-CROSSREF.md)
because two of its pieces replace, rather than merely sit alongside, something KEEL
already had. Also on 2026-10-14, **REA** (*Reverse Engineer Anything*, MIT,
`~/Downloads/rea-main`) was integrated as the perception capability — *cited, not
copied*: the tool stays in its own install, reached through a governed wrapper at
`keel/capabilities/reverse-engineering/`, placed and bounded in
[`keel/framework/REA-CROSSREF.md`](keel/framework/REA-CROSSREF.md). The same date added
RECON (the orientation gate) and HELM (the routing front door), written for this factory
rather than copied from anywhere. **From v1.0.0 on, KEEL is developed here, in this
master,** and moves between machines as versioned releases (`RELEASES.md`, and section 11
of `MANUAL.md`). The original `FRAMEWORK/` folder is provenance only. It also holds the `Planning/` source material (the four frameworks
KEEL is built from) and the reflection docs behind KEEL's own design decisions — worth
keeping around for provenance, but not needed to run a project, so it isn't duplicated
here.

**One master, linked into each project.** `harness/link_kit.py` gives a project a
`keel-factory/` folder of links to this master, plus the project's own `.ops/` for notes,
so an edit here reaches every linked project at once. A full copy is still the fallback
for a project that must carry its own — committed to a shared repo, or worked on from
another machine — and a copied project keeps whatever version it was copied from.

## Carrying the master copy on removable media (USB drive, etc.)

Works the same way — the master just lives somewhere other than `~/Documents`. The rule
doesn't change: **never treat the drive itself as a working directory.** Mount it, copy
it into the project's local disk as `keel-factory/`, then you can eject — nothing after
that copy step needs the drive present.

Three things that are genuinely different when the master travels between machines,
rather than staying put on one:

1. **Node.js is a per-machine dependency the drive doesn't carry.** Every laptop the
   harness hooks run on needs its own `node` on `PATH`. Without it, KEEL's prose-only
   half still works; the enforced backstop doesn't. A standalone Node binary could be
   bundled onto the drive itself for true zero-install use, with hook commands pointed
   at that instead of a system install — not done by default, ask if you want it. The
   data-boundary guard does not need Node: its Python port runs on Python 3 alone.
2. **A hook proven armed on one machine is not proven on another.** Re-run the
   armed-check in `harness/DATA-BOUNDARY.md` after every wiring, on every new machine —
   different OS, different Node version, different `git` all count as untested
   conditions. "It worked on my other laptop" is exactly the kind of claim Rule 6b
   exists to refuse.
3. **None of this is a sandbox against the laptop itself.** The data-boundary guard
   stops the agent from reading something it shouldn't; it assumes the machine running
   it is reasonably trustworthy to begin with. Plugging into your own second laptop is
   one thing. Plugging into a machine you don't control — a client site, a shared or
   managed machine — is a different, harder problem this framework was never built to
   solve, and no hook added here changes that.
