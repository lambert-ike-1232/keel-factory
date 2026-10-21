# KEEL FACTORY

A portable engineering system, packaged so a new project can start from this folder
instead of re-deriving anything. **Install it once per machine**, from this folder:
`python3 harness/install_plugin.py --codex` makes this folder a Claude Code plugin
(`keel`) and links its skills into Codex. Then, in any project, say
`Use KEEL: <what you want>` ([`START-PROMPTS.md`](START-PROMPTS.md)). KEEL switches itself
on in that project, and in Claude Code every later session there starts oriented, with no
special phrasing. For Codex, `--codex` gives the skills only: Codex's guard and session
hook need `--codex --codex-hooks` and your approval of both of KEEL's hooks in Codex's
`/hooks`, and no Codex session has yet been seen blocking (Missing evidence). Linking or
copying the folder into a project as `keel-factory/` still works for a harness without
plugins or skill folders. A copy made with MANUAL §4's rsync (no `.git`) switches KEEL on;
a copy that keeps `.git` (a `git clone`, `cp -R` or a Finder copy) counts as a master's
own checkout and stays dormant when its own hooks run.

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
| [`RELEASES.md`](RELEASES.md) · `VERSION` | Which release this is (v1.1.1), and what each release changed and how it was proven. | the version record |
| [`MANUAL.md`](MANUAL.md) | **Lost track? Start here.** Everything from a blank machine to a finished job, in order, with the exact commands and prompts. | the instruction manual |
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | **The map.** How method, execution, perception, and enforcement relate; how HELM routes between them; what was lacking and how it was addressed. | the whole-system view |
| [`keel/`](keel/) | **KEEL** — five phases (BRIEF → CONTRACT → DESIGN → SLICE → PROVE), RECON before them on existing systems, three tiers, six rules, templates, and the `keel`/`keel-prove` skills. Plus `skills/helm/` (the front door), `skills/crew/` with `framework/CREW.md` (several agents on one project without collisions), and `capabilities/` (the two senses: reverse-engineering and deep-research). | **Method** — what must be true, in what order |
| [`keel/skills-board/`](keel/skills-board/) | Miguel's task board, interview, handoff/resume, focused/orchestrate, spike, diataxis. | **Execution & memory** — how work gets done and persists across sessions |
| [`keel/capabilities/`](keel/capabilities/) | The two **senses**: `reverse-engineering/` (reach **REA** to see opaque systems, under an authorization gate) and `deep-research/` (find out what you don't know from authoritative sources, wired to web search/fetch and research subagents). | **Perception** — learning what you can't already read |
| [`harness/`](harness/) | Curated **ECC** enforcement hooks, the data-boundary guard and KEEL's own hook (`hooks/keel_hook.py`), plus the scripts that install, link, check and release the kit. | **Enforcement & portability** — binding the rules at the tool call |
| [`keel/framework/DOCTRINE.md`](keel/framework/DOCTRINE.md) · [`CAPABILITIES.md`](keel/framework/CAPABILITIES.md) | The standard the work is held to, and the rule that the framework only ever asks for what a real tool can actually do. | cross-cutting — *how well*, and *what's possible* |
| [`START-PROMPTS.md`](START-PROMPTS.md) | **Start here.** The one opening line, "Use KEEL: …", and the v1.0 setup prompts for a kit without the plugin. | the entry point |
| `.claude-plugin/` · [`agents/`](agents/) · [`evals/`](evals/) | The plugin manifest and marketplace entry; the three PROVE reviewers as agents; the eval suite that scores KEEL against plain Claude Code. | packaging |
| [`OPERATOR.md`](OPERATOR.md) | **Dropped into someone else's package?** The in-and-out protocol: the package's own instructions are the mission, KEEL is the kit underneath, and nothing is left behind but the work. | the other entry point |
| [`CLAUDE.md`](CLAUDE.md) | The always-on layer, about 5,600 characters (5,595 by `harness/check_kit.py`): HELM first, how to ask, the stop mode, done means proven, the data boundary. Where KEEL is on, the plugin's session hook injects it, and HELM reads it when it switches KEEL on. In Codex it comes through the Codex hooks, or the block HELM adds once to an owner project's `AGENTS.md`. With a linked kit it is copied or imported into the project's `CLAUDE.md`/`AGENTS.md`. | — |
| [`QUICKSTART.md`](QUICKSTART.md) | The step-by-step the starter prompt automates. | — |

**What it costs in context.** The plugin's skill and agent listing is paid in every
session on a machine where the plugin is installed, KEEL project or not: about
1,950-2,530 tokens, depending on the config. `claude plugin details keel@skills-dir`
reports ~1,953 in a fresh config and ~2,530 in a configured one
([`HARNESS-PROBES.md`](keel/framework/HARNESS-PROBES.md), P14; Evidence). In a project
where KEEL is switched on, the session hook adds the always-on layer and a short header:
6,029 characters as `harness/check_kit.py` measures it on the build machine (the count
includes the kit's and the temporary project's paths, so it varies by machine), about
1,510 tokens at four characters a token (Inferred). A live run injected 5,918 characters
of context (6,132 bytes of hook output, JSON-escaped; the same file, L8). The listing
estimate does not count it ([`CAPABILITIES.md`](keel/framework/CAPABILITIES.md),
"Context cost estimate").

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
   is gitignored or shaped like a secret/credential. The gitignore rule asks git in the
   repository nearest the file: outside git no `.gitignore` applies, and a separate
   repository inside a gitignored folder is judged only by its own rules. Default-deny;
   bypassing it requires a human to deliberately add a path to an allowlist file or set
   an override environment variable. Nothing in this factory does either of those for
   you. A repository can ship an allowlist file of its own, so HELM tells you about one
   at the project root. The guard honors a `.keel/data-boundary-allow` at the nearest git
   root of each path, so a submodule or a nested clone can bring its own; HELM's
   switch-on check lists every `.keel/` folder below the root as well. Never commit your
   own. Under the plugin the guard is armed wherever KEEL is switched on, through KEEL's
   own hook (`harness/hooks/keel_hook.py`). In Codex it runs only with `--codex-hooks`
   and your approval in `/hooks`, and has not yet been seen blocking there (Missing
   evidence). In Codex every file read is a shell command, so the guard sees it only as
   Bash and covers it only through its Bash heuristic: a blocked probe shows the hook is
   wired, not that reads are covered. Only the user edits the allowlist file. KEEL's
   hook (the plugin's, or Codex's with `--codex-hooks`) blocks the direct ways of writing
   it (a Write, Edit or patch of it, or a command naming it); a hand-wired bare guard
   does not. It is a tripwire, not a lock. None of KEEL's hook wirings matches MCP tools,
   so an MCP tool that takes a local path is not checked (Inferred from the hook
   matchers). Claude Code's Monitor tool, and PowerShell on Windows, run shell commands
   that the matcher does not name, so the guard never sees them (Inferred from the
   matcher).
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

**One master, linked into each project.** Under the plugin a project holds no copy of the
kit, only its own `.keel/`. For a harness without plugins, `harness/link_kit.py` gives a
project a `keel-factory/` folder of links to this master, plus the project's own `.ops/`
for notes, so an edit here reaches every linked project at once. A full copy is still the
fallback for a project that must carry its own — committed to a shared repo, or worked on
from another machine — and a copied project keeps whatever version it was copied from.

## Carrying the master copy on removable media (USB drive, etc.)

Works the same way — the master just lives somewhere other than `~/Documents`. The rule
doesn't change: **never treat the drive itself as a working directory.** Mount it,
restore the master from the release folder onto the local disk ([`MANUAL.md`](MANUAL.md)
section 3: check the checksums, clone the bundle), install or link KEEL from there, then
you can eject — nothing after that restore needs the drive present.

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
