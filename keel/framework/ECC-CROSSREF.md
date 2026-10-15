# KEEL cross-referenced against ECC

**Source:** *ECC — Everything Claude Code*, Affaan Mustafa (`github.com/affaan-m/ECC`),
MIT licensed. Read at commit state of the `ECC-main` download, 2026-09-07. 286 skills,
~40 hooks, rules, agents, plugins; 3,520 files.

Cited, not absorbed. Where a mechanism below is adopted into KEEL, it is named as his.

**Provenance of the "eight hours" claim:** the repo's own Background section says the
author won the Anthropic × Forum Ventures hackathon in September 2025 and built
`zenith.chat` with agentic workflows. That is evidence about **speed**, not about
verification quality. Read §5 before deciding what to take.

---

## 1. The headline: ECC is on a sixth clock, below the whole stack

McKnight slotted one layer *above* KEEL. ECC slots one layer *below* it.

| Layer | Governs | Clock | Source |
|---|---|---|---|
| Organization | An operating model | Months to years | McKnight |
| Measure | Traceability, evidence, cost, instruments | Across projects | New in KEEL |
| Artifact | The fixed document set | Per project | The template |
| Process | Phases and gates | Per feature | Dex Horthy |
| Session | Grilling, slices, context hygiene | Per session | Matt Pocock |
| Brief | Prompt quality | Per message | Thorsten Ball |
| **Harness** | **What the agent is permitted to do, per tool call** | **Per tool call** | **ECC** |

This is the second independent confirmation of the clock model, and it is stronger than
the first. The model predicts that a genuinely new framework either conflicts with an
existing layer (same clock) or slots cleanly above or below (different clock). Two
outside frameworks have now been tested against it and both slotted cleanly, at opposite
ends. A model that survives two attempts to break it in opposite directions has earned
more than a mention in a provenance table.

**Consequence:** ECC is not a competitor to KEEL and the comparison "which framework is
better" is malformed. ECC is the layer KEEL's phases could *execute on*. KEEL says what
must be true; ECC decides what the agent is allowed to type next.

---

## 2. The asymmetry that actually matters: KEEL is prose, ECC is hooks

Strip away 286 skills and one difference explains most of the rest.

**KEEL's rules are written down. ECC's are enforced at the tool call.**

KEEL Rule 6b says prove the check can fail. ECC ships `block-no-verify.js`, which makes
`git commit --no-verify` return exit code 2. KEEL Rule 4 says respect the smart zone. ECC
ships a PostToolUse hook that computes `context_remaining_pct` and injects it back into
the model's own context. KEEL says the gate decides. ECC ships `config-protection.js`,
which refuses to let the agent edit the linter config at all.

This is Rule 6d turned on KEEL itself. **Prose does not fail a build** — that is KEEL's
own sentence, and most of KEEL is prose. The framework asserts numbers must be bound to
assertions while binding none of its own rules to anything.

That is the single most useful finding in this document, and it is not a criticism of a
rule. It is the observation that KEEL has no *enforcement layer*, and that ECC is one.

**The correct adoption posture:** take ECC's mechanisms, not its methodology. The
methodology overlaps almost entirely (§3) and is weaker where it differs (§5).

---

## 3. Independent convergence — what ECC restates

Skipped as already covered, one line each. Listed so the absence is deliberate rather
than an oversight.

| ECC | Already in KEEL as |
|---|---|
| `blueprint`, `orch-pipeline`, `plan-orchestrate`, `ralphinho-rfc-pipeline` | The five phases under other names — size classifier = tiers, Gate 1/Gate 2 = stop points, AC-NNN = the acceptance gate, task_list = slices |
| `contract-first`, `intent-driven-development` | CONTRACT |
| `tdd-workflow` | SLICE's red-before-green at confirmed seams |
| `architecture-decision-records` | `docs/adr/` at PLATFORM |
| `eval-harness`, `agent-eval`, `benchmark-optimization-loop` | Rule 6d. Measurement vocabulary, not a new rule |
| `verification-loop`, `production-audit`, `security-review` | Domain checklists under the Gate axis |
| `cost-aware-llm-pipeline` | The escape-hatch ladder, in Python |
| `agent-self-evaluation` | Contradicted by ECC's own `gateguard`: *"LLM self-evaluation doesn't work"* |

`contract-first` contributes one sentence worth stealing outright — both sides must pass
against the **same artifact**, not against their own copy of it — and that is a paragraph
inside CONTRACT, not a rule.

---

## 4. What ECC has that KEEL lacks

Ten adoptions, ordered by how much they change. Each is marked **MECHANISM** (code that
enforces) or **PROSE** (a written guideline), because that distinction is the whole point
of §2.

### 4.1 Gate immutability — proposed Rule 6e · MECHANISM

> **The agent must not be able to weaken its own gate.**

Rule 6b proves a check *can* fail. Nothing in KEEL stops the agent from editing the check
until it doesn't.

`scripts/hooks/config-protection.js`:
> "BLOCKED: Modifying ${basename} is not allowed. Fix the source code to satisfy
> linter/formatter rules instead of weakening the config."

`scripts/hooks/block-no-verify.js` blocks `--no-verify` and `-c core.hooksPath=`.

Both are wired live in `hooks/hooks.json`, exit 2 on PreToolUse, and have unit tests
asserting the *blocking* path — including `blocks case-variant writes that resolve to an
existing protected config` and `blocks protected paths that exist as a dangling symlink`.
Those are genuine negative controls on the hooks themselves.

**Why this is a real gap and not a nicety:** KEEL's clause list runs *declare the
toolchain → prove it can fail → evidence expires → bind the numbers*, and every one of
them assumes a gate that stays put. A gate the agent can rewrite is not a weaker gate; it
is a gate whose green result is uninterpretable, which is exactly the condition 6b exists
to eliminate. 6e closes the loop 6b opens.

### 4.2 Reconciliation beats assertion · PROSE

`skills/loop-design-check/SKILL.md`:
> "'All tests pass' can be gamed (loosen asserts, fake mocks, swallow exceptions); 'diff
> vs the reference < 0.01' can't."

A ranking of check *classes* by how gameable they are. KEEL treats all Required Checks as
equivalent once they run; this says a check that reconciles against an independent
reference is structurally stronger than one that asserts a property, and should be
preferred where both are available.

The paired rule from the same file is the better half: **every acceptance criterion ships
with an explicit statement of what it must NOT do.** ECC calls it the Goodhart antibody.
Attaches to Rule 3 — a bound check should also declare its anti-gaming boundary.

Worth noting this is what SOUNDING already does by accident: verifying nDCG against
published reference values is reconciliation; asserting "nDCG went up" would have been
assertion.

### 4.3 The Learning Rule — proposed Rule 7 · MECHANISM + threshold

**This is KEEL's single biggest structural gap.** KEEL has `AI_WORKFLOW.md` per project
and nothing that carries a lesson between projects. Its own §7 says to grow the rule set
"by getting something wrong, diagnosing the root cause, and building a mechanism" — with
no mechanism for doing that, which is the failure mode the sentence describes.

`skills/continuous-learning-v2/SKILL.md` supplies the missing threshold:
> "Auto-promotion criteria: Same instinct ID in 2+ projects; Average confidence >= 0.8"

Three design decisions worth taking wholesale:

1. **Project-scoped by default; global is earned, not assumed.** Scoped by hashed git
   remote. Stops a lesson from one stack leaking into unrelated work.
2. **Confidence decays on contradiction.** A lesson is not permanent; it is a standing
   observation with a half-life. This is Rule 6c — evidence expires — applied to the rule
   set instead of to a build.
3. **Atomic form: one trigger, one action.** A lesson too large to state that way is not
   yet understood.

And the reason it is a hook rather than a skill, from the same file:
> "v1 relied on skills to observe. Skills are probabilistic -- they fire ~50-80% of the
> time based on Claude's judgment."

`skills/rules-distill/SKILL.md` supplies the governance loop one level up: a candidate
becomes a rule only if it appears in 2+ places, is phrased as do-X/don't-Y, and carries a
stated violation risk — with verdicts including `Already Covered` and `Too Specific`.
That is precisely the review this document should have been run through, and §3 is a
hand-rolled version of it.

### 4.4 Measure whether your own rules are followed · MECHANISM

`skills/skill-comply/SKILL.md`:
> "Measures whether a skill/rule is followed even when the prompt doesn't explicitly
> support it."

Generates scenarios at three strictness levels — supportive, neutral, and **competing** —
runs the agent, classifies the tool-call trace against an expected sequence, and reports a
compliance rate per rule. It then *"include[s] hook promotion recommendations for steps
with low compliance"*: a loop that converts failing prose into machinery.

`AI_WORKFLOW.md` records what the process **caught**. Nothing records what it **missed**.
Given that Rules 4 and 5 are KEEL's weakest precisely because they are unmechanised, this
is how you would get a number on them instead of an opinion.

### 4.5 Author independence as structure, not habit · PROSE

KEEL's three PROVE axes run in parallel sub-agents with clean windows. Clean *context* —
same *author*, same *model*. ECC states the stronger constraint three separate times:

`skills/loop-design-check/SKILL.md`:
> "the judge must be independent — not the same agent as Build (grading your own homework
> always inflates)"

`skills/autonomous-loops/SKILL.md`:
> "**Critical design:** The reviewer never wrote the code it reviews."

`skills/santa-method/SKILL.md`, on why reviewers must be *fresh each round*:
> "if only one reviewer catches an issue, that issue is real. The other reviewer's blind
> spot is exactly the failure mode Santa Method exists to eliminate."

`skills/council-multi-model/SKILL.md` adds a fourth axis run outside the model entirely —
and, more valuably, the honesty rule that goes with it:
> "An external process is not automatically a heterogeneous reviewer... Never claim
> provider diversity when the current host is already OpenAI-backed."

When its adapter fails it writes **"external review absent"** with a reason rather than
fabricating a review. That is Rule 2's Missing-evidence label, implemented.

**The KEEL edit this implies:** PROVE's axes get a fourth optional row, and the existing
three get a stated independence property — clean window is the floor, different model is
the target, and claiming the second when you only have the first is a false evidence
label.

### 4.6 The LAND gap — concurrent slices have no integration story · PROSE

KEEL says vertical slices only, and says nothing about slices built *concurrently*.

`skills/autonomous-loops/SKILL.md`:
> "When evicted, full context is captured (conflicting files, diffs, test output) and fed
> back to the implementer on the next Ralph pass"

A merge queue where non-overlapping units land speculatively in parallel, conflicts or
test failures **evict** the unit, and the eviction context is injected into the next
implementation pass rather than discarded.

Given CASE already coordinates parallel development across branches — and one of its
harder episodes was reconciling a feature branch that had diverged across many files —
this is the adoption with the most immediate practical value. It arguably needs a phase,
not a rule: a **LAND** step between SLICE and PROVE.

**Addressed 2026-10-14 by CREW** (`CREW.md` §9), as a step inside the team discipline
rather than a phase, so the five phases stay intact. Its fence check is mechanical
(`../skills/crew/scripts/check_lanes.py`), and an evicted lane gets its context fed back
as described above.

### 4.7 Context accounting on two axes KEEL does not have · MECHANISM + PROSE

**The standing tax.** `skills/context-budget/SKILL.md`:
> "each tool schema costs ~500 tokens; a 30-tool server costs more than all your skills
> combined"

Rule 4 governs conversation *growth*. This governs what is spent before turn one — and an
agent's `description` frontmatter loads into every Task invocation whether the agent is
used or not.

**The zone is a fraction, not a constant.** `skills/strategic-compact/SKILL.md`:
> "Suggests `/compact` at a window-scaled threshold — 160k tokens on a 200k window, 250k
> on a 1M window"

**Rule 4's ~150k is now wrong.** It was right for a 200k window and it is wrong on
anything larger. Restate the smart zone as ~80% of the detected window, read from the
transcript's `usage` record rather than assumed, with an override.

One concrete new failure mode for Rule 4, also from that file: Claude Code's todo tools
were removed by default in 2.1.233, so "my task list survives compaction" is now false.
Write the plan to a file before compacting.

### 4.8 Two named failures in cost measurement — cite them, they are free · MECHANISM

These are ECC's observed failures, not ours, and both are exactly Rule 6 shaped: an
instrument that ran for weeks and produced readings nobody could use.

`scripts/hooks/cost-tracker.js`:
> "The previous version of this hook expected those fields and silently produced
> zero-filled rows (verified: 2,340 rows captured with 0.0% non-zero token rate over 52
> days)."

And the second, from the same file: Claude Code writes one JSONL line per content block,
so *"Summing every line inflates totals ~2.5-3x"* unless you dedupe by `message.id`.

**The Rule 5 addition:** a cost meter needs a **non-zero-rate assertion**. A pipeline that
records zeros exits 0 and reports success, which is 6b's silent-crash failure wearing
different clothes. Any cost measurement gets a check that the measurement is non-degenerate
before its numbers are treated as Evidence.

### 4.9 The decision ledger with decaying marks · PROSE

`skills/recursive-decision-ledger/SKILL.md`:
> "Downgrade candidates when drift, tail risk, stale data, or failed replay invalidates
> the previous mark."

Upgrades DESIGN's numbered least-confident list from a static list into an append-only
ledger where each entry carries a mark — `accept | watch | reject | decay watch | needs
replay` — and is re-scored against the prior ledger. Its promotion gate is the right
sentence: *recursive confidence is not approval.*

The least-confident list is currently the most persuasive artifact in the set precisely
because it is visibly not fakeable after the fact. Making it append-only makes that
property structural rather than incidental.

### 4.10 Four small ones

| Idea | Source | Attaches to |
|---|---|---|
| **The de-sloppify pass.** *"Rather than adding negative instructions which have downstream quality effects, add a separate de-sloppify pass. Two focused agents outperform one constrained agent."* | `skills/autonomous-loops/SKILL.md` | SLICE, after each green |
| **Test where bugs were found, not for coverage.** *"write tests for bugs that were found, not for code that works"* | `skills/ai-regression-testing/SKILL.md` | Rule 3 — a defect becomes a new bound row; untouched code does not |
| **The delete-zone.** A table of intentionally removed paths with `Replacement` and `Revisit condition`, kept *"until recreation is no longer a realistic risk."* Stops agents resurrecting deleted code | `skills/living-docs-governance/SKILL.md` | PROVE's status report |
| **Every step carries a self-contained context brief so a fresh agent can execute it cold** | `skills/blueprint/SKILL.md` | SLICE — KEEL's slices implicitly assume session continuity |

`skills/delivery-gate/hooks/quality-gate.py` also contributes a cheap warn-only detector:
regexes for rationalization language — `skipping\s+(?:tests?|lint|coverage)\s+for\s+now`,
`(?:this|that)\s+is\s+a\s+pre[- ]existing\s+(?:issue|bug)` — which is a Rule 2 status
downgrade smuggled in as prose. ECC is honest that it *"never blocks on its own, because
regex heuristics can false-positive."*

---

## 5. What KEEL has that ECC does not

Adopt from a position of knowing what you are giving up. Three things, and the first is
significant.

**1. ECC has no in-session negative-control doctrine.** A repo-wide grep for
`negative control|known.bad|prove.*can fail|mutation test|test the test` returns exactly
one unrelated hit. ECC tests the ~40 hooks it *ships* — genuinely, in CI, asserting the
blocking path. It has nothing instructing an agent to feed a known-bad input through a
gate **it just authored during a task** and confirm the probe reached the thing under
test. Rule 6b has no counterpart in 286 skills. This is KEEL's strongest card and it is
not close.

**2. ECC never blocks on cost.** Its cost hook's own critical message reads
*"Informational only — not an instruction to stop."* `.github/workflows/` contains zero
cost gates. Rule 5's *a cost ceiling is a contract line, and a cost regression fails CI*
is stronger than anything ECC ships. Take ECC's measurement plumbing (§4.8); keep KEEL's
enforcement posture.

**3. ECC has no traceability matrix.** Nothing binds a feature line to a check and
forbids a blank. Rule 3 exists because of a measured 78% and there is no equivalent here.

`skills/delivery-gate/SKILL.md` states the trade-off better than either framework does
alone:
> "Having enforcement without methodology → empty entries. Having methodology without
> enforcement → forgotten captures."

KEEL is the second condition. ECC is the first. That sentence is the argument for the
stack.

---

## 6. The provenance problem, and how to adopt honestly

KEEL's `CHANGELOG.md` opens with a standing constraint: *"Every rule here has a named
failure behind it."* `EXPLAINING-KEEL.md` §7 sharpens it — the honest way to grow the
framework is *"by getting something wrong, diagnosing the root cause precisely, and
building a mechanism rather than forming an intention."*

**Nothing in §4 has a failure you observed.** Adopting all ten because a well-starred repo
does them would break the discipline that makes KEEL worth having, and would do it in the
document that records the discipline.

Three honest routes, in order of strength:

1. **Adopt on a borrowed named failure, cited as borrowed.** §4.8 qualifies outright —
   2,340 zero-filled rows over 52 days is a real, specific, dated failure with a
   diagnosis. It is not yours, and the changelog can say so.
2. **Adopt on a failure KEEL already has on file.** §4.1 (gate immutability) attaches to
   the v1.1 lint-crash failure: that gate was broken by a config incompatibility, and
   nothing prevents an agent from breaking one deliberately. §4.6 (LAND) attaches to
   CASE's diverged-branch reconciliation. Same shape, existing evidence.
3. **Adopt provisionally, and instrument it.** Everything else. §4.4 is the tool for this
   — take a rule, measure its compliance under competing prompts, and promote it to
   machinery only when the number says the prose is not holding.

**Recommended for v1.2, on that basis:** 6e and the Rule 5 non-zero-rate assertion by
route 1 or 2, Rule 4's window-scaled zone as a straight correction of a number that has
since become wrong, and everything else parked in this file until it earns its way in.

Rule 7 is the interesting case. It is the largest gap and it has no failure behind it
because a framework used on one project at a time cannot observe a cross-project failure.
That is not an argument against the rule; it is an argument that the evidence arrives on
the second project. The v1.2 entry should say exactly that.

---

## 7. Draft changelog entry for v1.2

> ## v1.2 — [date]
>
> **Added Rule 6e, gate immutability**, and corrected two numbers that had gone stale.
>
> ### What happened
>
> Read ECC (Affaan Mustafa, MIT), an agent harness of 286 skills and ~40 enforcement
> hooks. It sits one clock *below* KEEL's whole stack — per tool call — which makes it the
> second outside framework to slot cleanly rather than conflict, and the first to slot
> below.
>
> The finding was not any single skill. It was that **ECC enforces at the tool call what
> KEEL only writes down**, and that this is Rule 6d turned on the framework itself: prose
> does not fail a build, and KEEL is prose.
>
> ### Changes
>
> - **New 6e — the gate must be immutable to the thing it gates.** 6b proves a check can
>   fail; nothing stopped the agent editing the check until it didn't. Named failure: the
>   v1.1 lint gate was broken by a config incompatibility nobody chose. An agent under
>   pressure to reach green will choose it.
> - **Rule 5 — a cost meter needs a non-zero-rate assertion.** Borrowed named failure,
>   cited: ECC's cost hook recorded 2,340 rows over 52 days at a 0.0% non-zero token rate.
>   A measurement pipeline that records zeros exits 0 and reports success. 6b's silent
>   crash, wearing different clothes.
> - **Rule 4 — the smart zone is ~80% of the detected window, not ~150k tokens.** The
>   constant was right for a 200k window and is wrong on anything larger. Read the window
>   from the transcript's usage record rather than assuming it.
> - **Rule 4 — a new failure mode.** Claude Code removed the todo tools by default in
>   2.1.233. "My task list survives compaction" is no longer true. Write the plan to a file
>   before compacting.
> - **PROVE — the three axes gain a stated independence property.** Clean window is the
>   floor, different model is the target, and claiming the second while only having the
>   first is a false evidence label.
> - **`framework/ECC-CROSSREF.md`** — full cross-reference, including six adoptions parked
>   pending evidence.
>
> ### The one that is parked, and why
>
> **Rule 7, the Learning Rule** — cross-project lessons with an explicit promotion
> threshold (same lesson in 2+ projects at confidence ≥ 0.8, scoped by default, decaying on
> contradiction). This is the largest gap in KEEL and it has no named failure behind it,
> because a framework used on one project at a time cannot observe a cross-project failure.
> The evidence arrives on the second project. Parked, not rejected.
