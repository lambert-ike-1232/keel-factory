# The Stack

How four frameworks combine into one without any of them losing what made it good.

Read this first. The rest of KEEL is mechanics; this is the idea.

---

## 1. The insight: frameworks conflict only when they share a clock

Put the four side by side and they look like rivals. Dex Horthy stops for human
approval four times per feature. Thorsten Ball says stop tweaking, stop ceremony,
ship. Matt Pocock's repo opens by arguing *against* frameworks that own the process.
Your own template demands twelve living documents before anyone writes code.

Pick any two and you can construct an argument. Which is exactly why most people pick
one and discard the rest.

They are not actually in conflict. **They operate at different frequencies.**

| Framework | Governs | Clock |
|---|---|---|
| The Thorsten Prompt | A single message you send | **Seconds** |
| Matt Pocock's skills | A working session | **Hours** |
| The Software Factory | A feature | **Days** |
| Your Project Template | A project | **Weeks** |

A rule about how to phrase one message cannot contradict a rule about which documents
a project must contain. They never touch. The apparent contradictions all come from
reading a fast-clock rule as if it were a slow-clock rule, or the reverse.

Once you sort them by clock speed, they stop competing and start **nesting**: each
slower layer sets the frame that the faster layer runs inside.

```
   ┌─ PROJECT ── weeks ─ Artifacts: what must exist on disk
   │  ┌─ FEATURE ── days ─ Process: which gates, in what order
   │  │  ┌─ SESSION ── hours ─ Context: what is in the window, when to clear
   │  │  │  ┌─ MESSAGE ── seconds ─ Brief: standard, information, done
   │  │  │  │
   │  │  │  └─ Thorsten
   │  │  └──── Matt
   │  └─────── Dex
   └────────── Your template

   ┌─ ACROSS PROJECTS ── the Measure layer: what compounds
```

Everything below follows from that picture.

---

## 2. Layer 1 — Brief (per message, from Thorsten Ball)

**What it contributes:** the quality of every individual instruction.

The agent is a senior engineer with a hood over its head: brilliant, and holding only
what you put in front of it. Two information sources exist, training data and the
context window, and you control exactly one.

**What KEEL takes:**

- **The Slack test** — could this message go, as written, to a senior colleague and
  produce the right result?
- **The three checks** — *Standard* (points at a reference to match), *Information*
  (points at where the knowledge lives), *Done* (what finished looks like and how to
  verify it).
- **The `[GUESS: ...]` rewrite** — a weak prompt is not interrogated with a list of
  questions. It is rewritten as the brief it needed, every filled gap tagged, one
  question asked, then work proceeds.
- **The one-line debrief** — `Guessed: ...` or `Full brief, nothing to guess.`
- **Demand proof** — screenshots, test runs, benchmarks. You are async anyway.

**Why this layer has to be the fastest one:** it is the only layer with *negative*
overhead over time. It is explicitly designed to go quiet as you improve. Every other
layer adds permanent structure; this one amortizes to nothing, which is why it is safe
to run it at every tier including SPRINT.

**What KEEL does not take:** "kill the backlog" and the general anti-process posture.
Those are slow-clock claims made from a fast-clock framework, and they lose to the
layers above. Rule 5 in that cheat sheet ("stop tweaking, start shipping") is kept, in
the specific form: *do not spend engineering effort on tool configuration; spend it on
what to build.*

---

## 3. Layer 2 — Session (per session, from Matt Pocock)

**What it contributes:** everything about work that outlives a single context window.
This is the only layer that takes context death seriously.

**What KEEL takes:**

- **`/grilling`** as the universal interview. Model the problem as a **design tree**.
  The **frontier** is every decision whose prerequisites are settled. Ask the whole
  frontier in one numbered round, **with a recommended answer attached to every
  question**, then wait. Recompute and repeat. Done when the frontier is empty.
  Crucially: *finding facts is the agent's job; making decisions is yours.*
- **`to-spec` → `to-tickets`** for work larger than one window. Tickets are
  tracer-bullet vertical slices, each declaring its blocking edges, each sized to fit
  one fresh context window.
- **The phase-boundary tree.** At every gap between phases, first yes wins: Can you
  continue? → Is the context irrelevant (`/clear`)? → Do you need portability
  (`/handoff`)? → Can it run AFK (subagent)? → otherwise `/compact`. The reasoning
  underneath: every move except Continue converts a **primary source** (the session as
  it happened) into a **secondary source** (a summary of it). You only pay that
  lossiness when staying costs more than it saves.
- **The smart zone** — roughly 150k tokens before attention degrades. A hard budget,
  not a soft warning.
- **Deep modules.** *Depth* is leverage at the interface: how much behaviour a caller
  exercises per unit of interface they must learn. Two sharp tests: the **deletion
  test** (delete the module; if complexity vanishes it was a pass-through, if it
  reappears across N callers it was earning its keep) and **one adapter means a
  hypothetical seam, two means a real one.** And the line that matters most for
  agent-driven work: **the interface is the test surface.**
- **`CONTEXT.md`** — the project's ubiquitous language. Fewer tokens, consistent
  naming, easier navigation, and it compounds across every future session.
- **Two-axis review** — Standards and Spec, run as parallel sub-agents that cannot
  pollute each other, reported side by side and deliberately never merged or reranked.
- **The red-capable loop rule** from `/diagnosing-bugs`: no hypothesising until one
  command exists that is red-capable, deterministic, fast, and agent-runnable.

**What KEEL does not take:** the full 38-skill surface, the issue-tracker dependency,
and `/wayfinder` except at PLATFORM tier on genuinely foggy work.

---

## 4. Layer 3 — Process (per feature, from Dex Horthy)

**What it contributes:** the discipline of making every consequential decision before
the code that would make it expensive exists.

**What KEEL takes, and where it lands:**

| Dex's gate | Where it goes in KEEL | Why |
|---|---|---|
| Gate 1 — Product | Folded into **BRIEF** | The template's intake already does this, with more structure. The one thing carried over verbatim is *the announcement*: 3-6 sentences announcing the feature. If you cannot write it, you are building the wrong thing. |
| Gate 2 — Architecture | Folded into **CONTRACT** | The Production Build Contract covers everything Gate 2 does and adds auth model, persistence, observability, and real numeric platform limits. |
| Gate 3 — Program Design | Kept whole as **DESIGN** | See below. This is the crown jewel. |
| Gate 4 — Vertical Slices | Kept whole as **SLICE** | Tracer bullet first, real happy path second, one capability per slice after. |

**Gate 3 is the highest-leverage artifact in the entire corpus and it survives
untouched.** Type signatures with no bodies are the best information-per-token
document in software: a human reads them in seconds and says "right" or "wrong," but
they pin down most of the implementation. You get the value of code review before the
code exists. Paired with the **least-confident decisions list**, which forces the
agent to surface what it would otherwise decide silently, it kills the exact failure
mode that produces a 2,000-line diff pointed the wrong way.

**Also taken:** `00-status.md` and the **resume rule** (any fresh session reads the
folder and continues from the first unapproved phase), and the **backtracking
protocol** (a later phase invalidating an earlier one sends it back to "in progress"
and requires re-approval).

**What KEEL does not take:** four separate blocking ceremonies per feature. Gates 1
and 2 duplicate artifacts the template produces better, and on a two-week deadline
four human approvals per feature is the single largest time cost in the corpus.

---

## 5. Layer 4 — Artifact (per project, from your own template)

**What it contributes:** the only layer that knows what "production" means, and the
only one with an epistemics.

**What KEEL takes — nearly all of it:**

- **Every decision has one legal address.** No reconstructing intent from a diff.
- **"Specified" is never "implemented."** The strongest single idea in the corpus.
- **The three evidence labels** — Evidence / Inferred / Missing evidence — plus the
  honest-status trichotomy: *implemented and verified* / *implemented but unverified*
  / *specified only*.
- **Required Checks vs Planned Checks.** Aspiration is allowed to exist without
  contaminating the gate, and promoting a line is a real, dated event that requires
  the command to actually run.
- **Schemas outrank prose.** `additionalProperties: false`, constrained domain fields,
  size limits as a security control. A permissive schema is the most dangerous state
  a project can be in, because it looks like a contract while validating nothing.
- **Human Review Gates.** Safety made structural: high-impact output is routed to
  review by the gate itself, not by whoever happens to be coding that day.
- **The Production Build Contract.** Forces the decisions normally deferred into
  implementation: exact runtime, deploy target, auth model, persistence and state
  transitions, observability signals, secrets policy, real numeric limits.
- **The audit** (`EXECUTION_PLAN.md`, renamed `AUDIT.md`). Adversarial by
  construction. Nothing in layers 1-3 audits a claim of "basically done."
- **Job-shaped from day one**, so scaling swaps an implementation, never the API shape.

**What KEEL fixes:** no traceability, no tiers, no session layer, no interview
mechanism, no module vocabulary, and its phase prompts were copy-paste text rather
than invocable skills. The first of those cost real points; the rest cost consistency.

---

## 6. Layer 5 — Measure (across projects, new in KEEL)

The three things none of the four have. Traceability and cost were there from v1;
**instruments** arrived in v1.1, after a field test showed the other two were resting on
an unexamined assumption.

### Traceability

Every line in the Feature List gets a row in `TRACEABILITY.md`:

```
| Feature line | Acceptance check | Test | Status |
```

Three rules make it work:

1. **A feature line with no bound check is a `FAIL` row, never a blank.** Blanks are
   how partial work reads as done.
2. **A declared descope is a legitimate terminal state.** "TM persistence: descoped,
   see DECISIONS.md#0007" is a decision. TM half-built and unmentioned is a failure of
   follow-through. Reviewers score those very differently, and correctly so.
3. **The matrix is regenerated and re-checked at PROVE**, never hand-maintained
   between times.

This exists because it is precisely and provably the thing that cost 22 points.

### Cost

Cost is treated as an engineering constraint with a budget, a measurement, and a gate
check. The full treatment is in [COST.md](COST.md). The short version:

- A cost ceiling is a **contract line**, pinned alongside runtime and deploy target.
- **The cheapest thing that passes the gate wins.** Model, effort level, caching, and
  batching are gated decisions, not taste.
- **Measured, not estimated.** An estimated cost is *Inferred*; a measured one is
  *Evidence*. The labels apply here exactly as they do everywhere else.
- **The escape-hatch ladder**, cheapest rung first: deterministic code → cached result
  → small model → large model → human. Every call justifies why the rung below fails.
- **A cost regression fails CI**, like a test.

Why this belongs in the engineering layer and not the business layer: every lever in
it is an engineering decision. The business value falls out for free.

### Instruments

Traceability and cost both assume the same thing: **that the checks doing the measuring
work.** Nothing in v1 examined that assumption, and the first serious field test broke it
four times in one afternoon.

Four defects survived a passing typecheck, a passing lint, a passing unit suite, and a
successful production build:

| Defect | Why reading it could never have caught it |
|---|---|
| The build had stopped being reproducible | No source changed. A caret range in a transitive dependency moved beneath it |
| A field was dropped at a serialization boundary | Both sides individually correct and individually tested. No test crossed the join |
| A stated cost ceiling was being breached | The number lived in prose. Prose does not fail a build |
| The lint gate had never executed | It crashed before linting. A silent crash reads exactly like a clean pass |

Three of those four are defects in **the apparatus**, not the product. That is the shape
worth naming: the measure layer was measuring the code and nothing was measuring the
instruments.

Rule 6 closes it with four clauses — declare the toolchain, prove the check can fail,
treat evidence as expiring, bind every number — and the reason it belongs on this layer
rather than any faster one is that instrument decay is **slower than a project**. A
dependency range drifts over weeks. A gate rots quietly across many builds. Only the
layer that runs across projects is looking at a long enough baseline to see it.

---

## 7. The conflicts, resolved

Each one dissolves the same way: identify which clock each side is on.

**1. Approval gates (Dex) vs. flow (Thorsten).**
Gates are per-feature; "stop the ceremony" is per-message. Different clocks, no
contradiction. Resolution: **the number of blocking stops is a function of the tier,
not of the framework.** SPRINT stops once. STANDARD stops at CONTRACT and DESIGN.
PLATFORM stops at every phase.

**2. Front-load everything vs. learn from slice 1.**
You cannot both decide everything up front and learn from running code. Resolution:
**front-load contracts, learn implementations.** Contracts are cheap to write and
expensive to change; implementations are the exact reverse. Schemas, acceptance
checks, and signatures go first. How the thing is actually built is discovered one
slice at a time. Dex's own framework already does this — Gates 1-3 front-load, Gate 4
learns — KEEL just names the principle.

**3. One legal address per decision vs. compact-and-clear.**
These read as opposites and are actually complements. The compact rule only works
*because* the documents exist; without them, compacting is data loss. Resolution:
**nothing important may exist only in chat.** That single sentence is the bridge
between the artifact layer and the session layer, and it is Rule 4.

**4. Composable and hackable vs. fixed and auditable.**
Matt's entire pitch is against frameworks that own the process. Your template is
scored on having a fixed document set. Resolution: **fixed artifacts, composable
process.** The shape of `docs/` does not vary. Which skills you run to fill it does.
The reviewer gets consistency; you keep control.

**5. "Kill the backlog" vs. `to-tickets`.**
Direct contradiction on its face. Resolution: **tickets are session-scale scaffolding,
not project-scale debt.** They exist to survive context death within one effort. When
the effort ends, surviving tickets are deleted or spawned as agents. A ticket that
outlives its effort has become a backlog item, and Thorsten is right about those.

---

## 8. What you actually get from the stack

| Failure mode | Which layer catches it |
|---|---|
| Built the wrong thing | BRIEF: the announcement, the grilling frontier |
| Agent guessed and did not say | Layer 1: the `[GUESS: ...]` rewrite and the debrief line |
| Diff too large to review | Layer 3: vertical slices, tracer bullet first |
| Decided silently mid-implementation | Layer 3: DESIGN's least-confident list |
| Lost the reasoning between sessions | Layer 2 + Rule 4: compact to documents, resume rule |
| Ball of mud | Layer 2: deep modules, deletion test, the interface is the test surface |
| Scaffold that looks finished and runs nothing | Layer 4: Rule 2, Required vs Planned Checks |
| Feature 60% built and read as done | Layer 5: traceability, `FAIL` not blank |
| Works, costs too much to run | Layer 5: cost budget, escape-hatch ladder, CI check |
| Cannot explain what was done | Layer 5: `AI_WORKFLOW.md` compiles the account |
| Gate written but never runnable here | Layer 5, Rule 6a: toolchain declared and verified at CONTRACT |
| Gate that passes because it is broken | Layer 5, Rule 6b: negative control before the result is recorded |
| Green result that has silently rotted | Layer 5, Rule 6c: evidence expires; re-run, don't recall |
| Stated number quietly breached | Layer 5, Rule 6d: every figure bound to an assertion |
| Two correct halves, broken join | Layer 3 + DESIGN: a round-trip test per consumed field |

No single source framework catches more than four rows of that table. That is the
argument for stacking them.

The bottom five rows were added in v1.1, and every one of them came from running the
framework rather than reasoning about it. That is the argument for the last rule: **a
framework that has never been observed failing is in exactly the position of a gate that
has never been observed failing.**
