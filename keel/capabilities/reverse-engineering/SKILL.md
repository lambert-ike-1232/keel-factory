---
name: reverse-engineering
description: Perceive what has no readable source (a shipped binary, a running process, a network or signal capture, firmware, an obfuscated bundle) through REA, under an authorization gate, read-only first. Use when source analysis can't answer the question. Not for ordinary source repositories.
---

# Reverse engineering — the perception capability

This is KEEL's **governance wrapper** around REA (Reverse Engineer Anything), not a
reimplementation of it. REA ships its own detailed routing skill (per target type:
native, managed, JavaScript/Electron, Android, firmware, browser, network, packet,
signal, WASM, EVM, Go, Rust, SQLite, ELF/PE, crash dumps). This file governs **when
KEEL reaches for REA, under what authorization, and how its results come back into the
framework.** For the mechanics of a given target, defer to REA's own installed skill
(`reverse-engineer-anything`) and its references.

Perception is a different kind of thing from KEEL's phases — see `../../../ARCHITECTURE.md`
§4. The phases are about time; perception is about *access*. REA is a sense the agent
can reach for from inside any phase; it is not a phase of its own.

In a copied skill (this file sits under a project's `.claude/skills/` or
`.agents/skills/`, not under `keel/`), read every `../` path under `keel-factory/keel/`,
and root files such as `CLAUDE.md` under `keel-factory/`, even when the project has a
file of that name.

## Reach for REA only when source cannot answer the question

REA's own first instruction is: skip it for ordinary source-repository analysis. Honor
that. Reach for perception only when the question genuinely depends on something you
cannot read as source:

- a shipped binary, package, or firmware image with no (or partial) source
- an obfuscated, minified, or bundled artifact where the source in the repo is not what
  actually ships
- runtime behavior that static reading cannot establish (and only when the required host
  access is authorized and available)
- a network / packet / signal capture, a crash dump, an embedded database snapshot
- a claim that a built artifact matches its source (verifying the two against each other)

If the complete source is in front of you and it is the whole truth, use normal repo
tools. Perception is for when it is not.

## The authorization gate — non-negotiable, and it runs first

REA can execute targets, attach to live processes, intercept traffic, and touch devices.
That power is exactly why it is bound to KEEL's data-boundary discipline
(`../../../CLAUDE.md` → "Data boundary"), extended here:

1. **Authorized targets only.** Adopt REA's own lawful-use boundary verbatim (see
   `../../framework/REA-CROSSREF.md` §4 and REA's `DISCLAIMER.md`): security research,
   malware/incident analysis, vulnerability research and coordinated disclosure, CTFs and
   education, interoperability, software preservation, and debugging or auditing software
   you own or are authorized to examine. The factory will not help circumvent protection
   measures, bypass access controls on systems you are not authorized to test, or any
   other use REA itself refuses. If the target's authorization is unclear, **stop and
   ask** — naming the exact target — before the first REA call.
2. **Read-only before anything that acts.** Static inspection is the default and needs
   only the authorization to examine the artifact. Any operation that **executes** a
   target, **attaches** to a live process, **mutates**, **intercepts** traffic, or
   touches a **device** is a separate, higher authorization. Name that exact action and
   get explicit approval before it — do not infer it from permission to inspect a file.
   This mirrors REA's own separation (static vs. runtime) and the data-boundary rule's
   "ask before invasive or hard-to-reverse actions."
3. **One discipline, not a new one.** The rule is the same *ask-before, name-the-exact-
   action, no-blanket-yes, do-only-the-named-action* rule that governs reading a
   gitignored file. Pointing REA at a target is an instance of it, not an exception to it.

## REA's evidence model IS KEEL's — map it, don't stack it

REA already distinguishes **observations, inferences, and unknowns**, cites **Evidence
IDs**, and refuses to imply that static analysis observed execution. That is KEEL's
Evidence Rule in a different vocabulary. Map one-to-one:

| REA | KEEL (Rule 2) |
|---|---|
| Observation (cited Evidence ID, from static read or captured runtime) | **Evidence** — observed |
| Inference / candidate / heuristic reconstruction | **Inferred** — reasonable, unverified |
| Unknown / unresolved / out-of-coverage | **Missing evidence** — could not confirm |

So a REA finding drops straight into a KEEL status report, a RECON map's labeled claims,
or a board task's finding ledger with no translation and no second evidence system.
Carry REA's Evidence IDs through as the citation. Never upgrade a REA inference to
Evidence because it is convenient; never let "static analysis saw the bytes" become
"I observed the behavior."

## How REA results flow back into the framework

Perception serves a discipline; it does not replace one. Route the result:

- **Into RECON** — opaque regions of the system map (`docs/RECON.md` §3), with REA
  Evidence IDs preserved and unknowns kept as unknowns.
- **Into a hard bug** — when the failing surface is a binary or runtime the normal
  red-capable repro cannot reach (`../../skills/keel/SKILL.md` → "A hard bug").
- **Into SLICE** — when building interop or compatibility against an artifact whose
  behavior had to be perceived rather than read.
- **Into `audit` / `keel-prove`** — when verifying that a shipped artifact matches its
  claimed source, or that a built thing does what the contract says.

In every case the KEEL discipline owns the conclusion; REA supplies evidence to it. When
the user then asks to *build* something, switch back to normal coding tools and keep
observed behavior separate from design choices (REA's own closing instruction).

## Connecting REA

REA is a separate tool with its own install (CLI + MCP server), not bundled into this
factory — same "cited, not absorbed" posture as ECC (`../../framework/REA-CROSSREF.md`
§1). It is reached through its own `reverse-engineer-anything` skill once installed. If
REA tools are not present in the session, follow REA's own connection-and-recovery
guidance rather than improvising setup; do not install unrelated software to repair it.
If REA is not installed and the user wants perception, say so plainly and point them at
it — do not attempt opaque analysis by hand and present the guesses as if they were
REA's evidence-grade output.

## What this capability does NOT do

- It does not lower the authorization bar for anything. If anything, it raises it for
  runtime/mutation operations.
- It does not make KEEL's phases optional. Perception feeds a phase; it is not a
  shortcut around BRIEF/CONTRACT/PROVE.
- It does not turn the factory into a reverse-engineering tool. REA is the tool; this is
  the governance that lets KEEL reach for it responsibly when a project genuinely needs
  to understand something it cannot read.
