# KEEL cross-referenced against REA

**Source:** *REA — Reverse Engineer Anything*, MIT licensed, a local-only
reverse-engineering tool exposing shared CLI and MCP workflows (`morluto/rea`). Read at
the state of the `rea-main` download, 2026-10-14: its `DISCLAIMER.md`, `AGENTS.md`, and
the `reverse-engineer-anything` agent skill with its routing table and investigation
workflow.

Cited, not absorbed — the strongest form of it in this factory. REA is ~3,800 files of
tool. None of it is copied in. What is adopted is a *posture* and a *mapping*; the tool
stays where it is and is reached through its own skill.

---

## 1. The headline: REA is on a different axis, not a different clock

Every prior cross-reference placed its source on the *clock* model — McKnight one layer
above KEEL (organization, months–years), ECC one layer below (the harness, per tool
call). REA does not fit that line at all, and that is the finding.

The clocks are about **time**: per message, per session, per feature, per project,
per organization. REA is about **access** — what the agent can see. A shipped binary is
exactly as opaque whether you study it for one second or one month; opacity is not a
duration. So REA cannot sit on the clock stack, because it is not answering a
time-scale question. It is a **perception** capability, orthogonal to all of the clocks.

| | Clock stack (method/process/session/message/harness) | REA |
|---|---|---|
| Governs | *when* things must become true | *what the agent can perceive* |
| Varies with | time scale of the work | source availability of the target |
| Competes with a KEEL layer? | a new one would, if same-clock | no — different axis entirely |

**Consequence:** the question "does REA conflict with KEEL" is malformed in the same way
"is ECC better than KEEL" was. REA is a sense the phases reach for, not a rival to them.
This is why it ropes in without a single phase changing. Full placement in
`../../ARCHITECTURE.md` §1 and §4.

## 2. The convergence that makes integration almost free: REA already keeps KEEL's evidence discipline

This is the most important finding and the reason REA was safe to adopt at all. REA was
built, independently, on the same evidence doctrine KEEL's Rule 2 encodes:

- It distinguishes **observations, inferences, and unknowns** and will not blur them.
- It cites **Evidence IDs** and preserves provenance across every boundary and adapter.
- It **refuses to imply that static analysis observed execution** — the exact distinction
  KEEL Rule 2 draws between *implemented and verified* and *specified only*.
- Its `AGENTS.md` carries a **fail-closed integration rule**: do not integrate a
  capability while scope, authority, side-effect, or verification questions are
  unresolved. That is KEEL's "nothing is done until a command proves it," turned on the
  act of integration itself.

Two systems arriving independently at the same evidence doctrine is strong evidence the
doctrine is right — the same argument KEEL already made when ECC and McKnight
independently restated its layers. The practical payoff: REA's evidence model is **mapped
one-to-one** onto KEEL's labels (observation→Evidence, inference→Inferred,
unknown→Missing evidence; table in `../capabilities/reverse-engineering/SKILL.md`), so no
second evidence system is stacked. We reconcile, as always.

## 3. What is adopted (posture and mapping), and what is deliberately not

**Adopted:**

- **The evidence mapping** (§2) — so REA findings flow into KEEL artifacts untranslated.
- **REA's lawful-use boundary**, verbatim, as the authorization gate on the capability
  (§4). This is the one place REA's *prose* is taken directly into the factory, because
  it is exactly the boundary the data-boundary discipline needed for this capability.
- **The reach-for-it-only-when-source-cannot-answer rule** — REA's own first instruction,
  which keeps perception from being run on plain source repos.
- **The read-only-before-runtime separation** — REA's static/runtime authority split
  maps onto the data-boundary rule's invasive-action escalation.

**Deliberately not absorbed:**

- **The tool itself.** 3,800 files stay in their own repo, reached through REA's own
  skill. Copying them in would be the opposite of the "cited, not absorbed" posture every
  other cross-ref holds, and would rot instantly against REA's release cadence.
- **REA's own "Plan broader investigations" workflow** overlaps KEEL phases + the task
  board. We do **not** adopt it as a second planning system. A multi-question REA
  investigation is run as board tasks with REA supplying evidence to each — the investigation
  ledger is the board, not a parallel REA-specific ledger. Reconcile, don't stack.
- **REA's provider/engine setup, CLI, and MCP mechanics.** Those are REA's to own; the
  factory's wrapper governs *when and under what authority*, never *how* a given engine
  runs.

## 4. The safety posture, stated plainly

Reverse engineering is dual-use, and the factory treats it as such without flinching and
without refusing legitimate work. The boundary is REA's own, adopted verbatim because it
is well-drawn:

> Lawful analysis: security research, malware and incident analysis, vulnerability
> research and coordinated disclosure, CTFs and education, interoperability, software
> preservation, and debugging or auditing software you own or are authorized to examine.
> **Not** for circumventing protection measures, bypassing access controls on systems you
> are not authorized to test, reproducing protected code and assets, or evading provider
> policies.

Three mechanisms enforce it, all of them already part of the factory rather than new
invention:

1. **The data-boundary rule** (`../../CLAUDE.md`) governs pointing REA at a target the
   same way it governs reading a sensitive file: name the exact target, ask first, no
   blanket yes, do only the named action.
2. **Read-only is the default; runtime/mutation is a separate, named, approved
   authorization.** Inspecting an artifact never implies permission to execute it, attach
   to it, or intercept its traffic.
3. **The authorization gate runs before the first REA call**, not after findings exist.
   If authorization is unclear, the capability stops and asks.

This is why integrating a reverse-engineering tool does not make the factory a
reverse-engineering weapon: the capability is bound, read-only-first, and gated on
explicit authorization, inside a framework whose whole ethos is already "don't do the
invasive thing without being told to, specifically."

## 5. What KEEL has that REA does not, and vice versa

**KEEL brings what REA has no reason to have:** a method (phases), a persistence/execution
layer (the task board), an improvement discipline (RECON→backlog), and enforcement at the
tool call (the harness). REA is a sense; it does not drive a project to production. It was
never trying to.

**REA brings the one thing KEEL structurally could not:** sight into systems with no
readable source. Before REA, "take on any project" quietly meant "any project whose
source is complete and honest." Much of production reality — shipped binaries, running
services, obfuscated bundles, firmware, captures — is not that. REA removes the silent
qualifier. That is the whole reason it earns a place here.

## 6. Provenance

Integrated 2026-10-14. Placement decided as **perception axis, orthogonal to the clock
stack** (§1); evidence models mapped rather than stacked (§2); tool cited, not copied
(§3); bound to the existing data-boundary discipline with REA's own lawful-use boundary
adopted verbatim (§4). No KEEL phase changed. The capability wrapper lives at
`../capabilities/reverse-engineering/SKILL.md`; REA itself stays in its own install.
