---
name: deep-research
description: Find out what you don't know before deciding. Authoritative sources, triangulated, evidence-labeled, tied to the decision they serve. Use when a choice turns on a technique, a library's real behavior, a protocol, a standard or a best practice the repo can't answer, instead of guessing.
---

# Deep research — when you don't know, find out

The framework's promise is that the agent does not guess at things it could know. When a
real decision turns on knowledge you lack, the honest move is not to invent a plausible
answer and not to ask the user to supply what they hired you to find — it is to **go find
out, from sources that actually establish the answer**, and come back with it labeled for
what it is.

This is a **sense**, like perception (`../reverse-engineering/`). Perception sees systems
with no readable source; research sees knowledge that is not in this repo. Both feed a
decision in a discipline; neither is a phase of its own. The architecture places them
together in `../../../ARCHITECTURE.md` §1 as the perception layer.

In a copied skill (this file sits under a project's `.claude/skills/` or
`.agents/skills/`, not under `keel/`), read every `../` path under `keel-factory/keel/`,
and root files such as `CLAUDE.md` under `keel-factory/`, even when the project has a
file of that name.

## First: is this actually a research question?

Route the question to the cheapest sense that answers it. Most "I don't know" is not a
research question:

| The question is really… | Use | Not research |
|---|---|---|
| "What does *this codebase* do here?" | Read / grep / the `Explore` subagent | the answer is in the repo |
| "What does this *shipped binary / runtime* do?" | Perception (`../reverse-engineering/`) | that is a different sense |
| "What did we already decide?" | `docs/`, the task board, `DECISIONS.md` | it is recorded |
| "What does *the world* know about doing this well?" | **Deep research — this skill** | — |

Research is for the last row only: knowledge that exists outside this project and that
you cannot derive by reading what is already in front of you. Reaching for the web to
answer a question the repo already answers is the same waste as running perception on
plain source.

## The standard — what separates research from a Google search

The user's bar: *not a normal search — find the research that has actually been done on
the thing, so there is no room for doubt in the method.* Meet it:

1. **Start from the decision, not the query.** Name the specific decision this will feed —
   a DESIGN choice, a RECON unknown, a CONTRACT constraint, a hard-bug hypothesis. A
   search with no decision behind it expands forever and resolves nothing.
2. **Prefer primary and authoritative sources.** Official documentation, specifications
   and RFCs, the source or issue tracker of the actual library, peer-reviewed or primary
   technical writing, maintainers' own words. A random blog or forum answer is a lead to
   verify, not an authority to cite.
3. **Triangulate — never conclude from a single source.** A claim is solid when
   independent authoritative sources agree, or when the primary source (the spec, the
   code) states it directly. One hit is a hypothesis. Conflicting sources are a finding in
   themselves: report the disagreement rather than picking the convenient side.
4. **Date everything.** Techniques, versions, and best practices move. A source's date and
   the version it describes are part of the evidence; an answer that was true three
   versions ago can be false now. State the version/date your conclusion is bound to.
5. **Distinguish "best practice" from "common practice."** Widespread is not the same as
   correct. Say which you found. If the research shows a consensus *and* a dissent with a
   real argument, both go in the note.

## The mechanism — the actual tools this uses

This capability is grounded in tools the agent actually has (see
`../../framework/CAPABILITIES.md`). Use them, in rough escalation order:

- **A focused factual question** → `WebSearch` for authoritative sources, then `WebFetch`
  to read the specific primary source in full rather than trusting the snippet. Read the
  spec/doc page, don't paraphrase a summary of it.
- **A broad or multi-part question** (comparing approaches, surveying how a problem is
  usually solved, a literature-style sweep) → invoke the **`deep-research` skill** if this
  environment offers it, or spawn research **subagents** (the `Agent` tool) with distinct
  sub-questions, each told to return sources, conclusions, and unresolved gaps. Parallel
  subagents keep a wide sweep out of the main context. (This mirrors REA's own "decompose
  into independent questions, assign distinct scopes, point workers at evidence" pattern.)
- **A library/tool's real behavior** → prefer its official docs and its actual source or
  issue tracker over third-hand descriptions; where a quick experiment settles it faster
  and the environment allows, a `spike` (scratch prototype, `../../skills-board/claude/spike`)
  is itself primary evidence — running the thing beats reading about it.

If none of these are available in the current environment, say so plainly and tell the
user what you could not verify — do not dress an educated guess as researched fact.

## The output — a research note that feeds the decision

Research that stays in chat is lost at the next context boundary (Rule 4). Write a short
note to `docs/` (or attach it to the board task it serves), structured so the decision
can be made from it:

```
## Research: <the decision this serves>
**Question:** <the specific thing that had to be known>
**Answer:** <the conclusion, in one or two lines>
**Confidence:** Evidence (primary source confirms) / Inferred (triangulated, not
   first-hand) / Missing evidence (could not resolve — say what is still open)
**Bound to:** <version / date / platform the answer is true for>
**Sources:** <authoritative ones, with what each established>
**Dissent / open:** <any credible disagreement or unresolved part>
```

## The evidence rule still binds — research is Inferred until the system confirms it

This is the discipline that keeps research from becoming a new way to fool yourself. **A
researched answer is `Inferred`, not `Evidence`, until it is verified in the actual system
or environment.** The docs saying an API behaves a certain way is Inferred; your test
watching it behave that way in *this* project is Evidence. Carry the label honestly into
whatever artifact consumes the note — a DESIGN least-confident entry, a RECON unknown
resolved, a CONTRACT line. "The internet says so" has never once been the same as "I saw
it work here," and the framework does not let the two blur.

## Where research plugs in

- **RECON** — an unknown that a change depends on, that the system itself cannot answer.
- **DESIGN** — a least-confident decision that turns on a technique or tradeoff you do not
  yet command; research it before committing the shape.
- **CONTRACT** — a standard, protocol, or compliance constraint the contract must encode
  correctly.
- **A hard bug** — when a hypothesis needs knowledge of a library's or platform's real
  behavior to be falsifiable.
- **Before a question goes to the user** — when the options you would offer turn on
  knowledge you lack, research them first, so the question arrives with real approaches
  and a researched pick instead of a blank (`../../framework/DOCTRINE.md` §2).
- **Continuous learning** — a technique researched once, verified in use, and found to
  generalize is exactly the candidate the learning loop distills into a durable rule
  (`../../framework/DOCTRINE.md` → "Ever-evolving").

## What this capability does not do

- It does not lower the evidence bar; it raises it, by making "find out" the required move
  instead of "guess plausibly."
- It does not replace the user's decisions. It brings the facts and the options; the user
  (or the relevant phase) still decides. Finding facts is the agent's job; making the call
  is not.
- It does not turn every unknown into a web search. The routing table above sends most
  unknowns to the repo or to perception. Research is the last row, used well.
