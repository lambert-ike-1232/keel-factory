# Loops in KEEL (Draft v0.1 — not yet a numbered rule)

**Status: provisional.** `CHANGELOG.md`'s own standing rule is that a KEEL rule earns its
number from a named failure, observed in the field. This document has a gap analysis
behind it, not a field failure — it was built by pulling apart a first-pass description of
Addy Osmani's "loop engineering," not by watching an unattended KEEL loop fail. It is
parked here the same way Rule 7 (Learning) was parked in `ECC-CROSSREF.md`, for the same
reason, and §5 says what would promote it.

**Source:** Addy Osmani, *Loop Engineering*, `addyosmani.com/blog/loop-engineering`. Read
in full before this document was written. Its own framing: *"You shouldn't be prompting
coding agents anymore. You should be designing loops that prompt your agents."* Six
components named there: automations, worktrees, skills, plugins/connectors, sub-agents,
state.

---

## 1. Two problems, not one

The source, and the first-pass description of it this document was built from, both use
"loop engineering" for one thing. It is actually an answer to one of two different
problems, and only one of them.

| | The problem | Does loop engineering (as coined) solve it? |
|---|---|---|
| **A. Discovery** | The agent doesn't know what it doesn't know, and has no mechanism to find out on its own | **No.** The source's own tool for this is Skills — codifying *known* conventions so the agent stops guessing. That removes a guess; it does not surface an unknown. |
| **B. Operation** | A bounded, understood, recurring task needs to keep running without a human re-prompting each cycle | **Yes.** This is what all six named components are for. |

**Evidence, not inference:** fetched and read the source directly rather than working from
a paraphrase. It does not address unknown-unknown discovery anywhere; it assumes the
agent's purpose and constraints are already defined through skills and instructions, and
automates *execution* of that already-defined work.

This split matters because it changes what "build loop engineering into KEEL" can honestly
mean. §2 below is a real, buildable answer to Problem B. §3 is not a solved answer to
Problem A — nothing available is — but it is the honest shape of an attempt, labelled as
such.

---

## 2. The Operational Loop

An Operational Loop is the six named components, plus the two pieces a from-memory
retelling of them drops most easily: an independently-checked stopping condition, and an
integration step for parallel work. Both are missing from the source too — confirmed by
direct fetch, not assumed — which is why they are stated here as requirements rather than
cited as borrowed.

**No loop may run unattended without declaring all seven fields below.** This is Rule 3's
shape (traceability: a bound check or a declared descope, never a blank) applied to
autonomy instead of to a feature line.

| Field | Requires | Why it's required |
|---|---|---|
| **Trigger** | Clock, event, or human, named explicitly | An undeclared trigger is an undeclared cost source (Rule 5) |
| **Per-iteration done condition** | A written, checkable condition — not "looks right" | The source's own mechanism: `/goal` "keeps going until a condition you wrote is actually true" |
| **Done-checker** | A process **independent of the agent doing the work** | The source's own mechanism, and the piece a paraphrase dropped: "after every turn **a separate small model** checks whether you are done." Same independence principle as KEEL's three PROVE axes and ECC's council/santa-method finding (`ECC-CROSSREF.md` §4.5) — a worker grading its own work inflates, structurally, every time. |
| **Stop-entirely condition** | Separate from the per-iteration done condition | A loop that only knows "is this cycle done" never knows "should there be another cycle." This is the actual content of the bottleneck correctly named at the start of this exploration — the fix is not agent ambition, it's a second condition nothing currently states. |
| **Escalation trigger** | Named categories: irreversible, externally visible, ambiguous | KEEL's own Human Review Gates, applied continuously instead of once at a stop point |
| **Cost ceiling** | Per iteration and per period, bound to an assertion (Rule 6d) | An unattended loop is an unbounded bill by construction unless this is a hard number, not a hope |
| **LAND step** | How concurrent worktrees reconcile before either is called done | **Confirmed missing from the source directly** ("worktrees... can not touch the other one's checkout" — and nothing past that). Same gap independently found in ECC (`ECC-CROSSREF.md` §4.6, the merge-queue-with-eviction pattern) and in CASE's diverged-branch reconciliation. Three independent sightings of the same hole is strong enough evidence to require this outright rather than note it as a nice-to-have. The procedure that fills it is `CREW.md` §9. |

**State**, the sixth named component, is not a separate row — it is what the Done-checker,
the stopping condition, and the LAND step all need to persist between iterations to avoid
re-deriving (or re-breaking) the same thing every cycle. It is scoped to *this* loop, in
*this* project. If a lesson from one loop turns out to generalise past this project, that
is no longer loop-state — it is exactly the case the parked Learning Rule
(`ECC-CROSSREF.md` §4.3) exists for. Loop-state is the small, immediate, single-project
instance of the same idea; Rule 7, if adopted, is its cross-project generalisation. They
should not be built as two separate mechanisms.

---

## 3. The Discovery Loop — still open, stated honestly

Problem A has no solved mechanism here, in the source, or anywhere else checked. Recorded
as **Missing evidence**, not dressed up as solved.

The one structural idea worth trying: KEEL's DESIGN phase already produces a
least-confident-decisions list — the numbered list of what the agent is about to guess,
surfaced once, read by a human, then frozen. A Discovery Loop is that same mechanism
**re-fired on a schedule instead of once**, writing each new entry to the same ledger the
parked Learning Rule needs (`ECC-CROSSREF.md` §4.9, the recursive decision ledger with
decaying marks).

This is speculative and is stated as speculative. It does not solve "the agent finds a
genuinely novel unknown" — it only makes the *existing, human-facing* uncertainty-surfacing
mechanism recur instead of running once. Whether that is a meaningful step toward Problem A
or just a more frequent version of something that was already only partial is an open
question, not a claim this document makes either way.

---

## 4. Where a loop sits in the stack

Not a new row in the clock table (`MCKNIGHT-CROSSREF.md` §1, extended by
`ECC-CROSSREF.md` §1). A loop is not a new speed — it is what **fires a transition between
the speeds already on that table**, without a human doing it by hand.

| Transition | What an Operational Loop does there |
|---|---|
| Session → Feature | Decides a slice is done and starts the next one, using the Done-checker instead of a human noticing |
| Feature → Project | Decides a feature is done and lands it, using the LAND step instead of a human reconciling worktrees |
| Project → Organization | Where the parked Learning Rule would fire, promoting loop-state that has proven itself across projects |

"Loop stacked on loop" is not an arbitrary nesting depth. It is *which boundary in this
table the loop is crossing.* An inner loop crossing Session→Feature and an outer loop
crossing Feature→Project are different loops because they answer to different Done-checkers
and different cost ceilings, not because one merely runs longer than the other.

---

## 5. Promotion bar

This stays a draft, not a rule, until one of these is true:

1. **A named failure**, observed running an actual unattended loop against a KEEL project
   — the same bar every existing rule cleared. Candidates to watch for, given §2's design:
   a loop whose Done-checker was not actually independent and rubber-stamped its own work;
   a cost ceiling that was prose instead of an assertion and got breached silently; a LAND
   step skipped because only one worktree was running "for now."
2. **A field test of the Discovery Loop** in §3, with an honest report of whether re-firing
   the least-confident list on a schedule surfaced anything a human wouldn't have thought
   to ask for anyway.

Until then: treat §2 as usable — it is built from confirmed gaps in a real source plus
KEEL's own already-adopted independence and traceability principles, not from guesswork —
and treat §3 as an idea worth trying once, not a mechanism to depend on.
