# KEEL cross-referenced against McKnight

**Source:** Charles McKnight, *Hybrid Deterministic–Probabilistic Systems: Architectural
Discipline Before Acceleration*, 24 February 2026. Copyright © 2026 Charles McKnight.
Toolkit at `github.com/senestone/hybrid-systems-discipline`.

Cited, not absorbed. Where a mechanism below is adopted into KEEL, it is named as his.

---

## 1. The headline: he is on a fifth clock

KEEL's central claim is that its four source frameworks nest rather than compete
because they run at different frequencies: message, session, feature, project.

McKnight's paper sits **one layer above the whole stack**.

| Layer | Governs | Clock | Source |
|---|---|---|---|
| **Organization** | An operating model | **Months to years** | **McKnight** |
| Project | The artifact set | Weeks | The template |
| Feature | Phases and gates | Days | Dex Horthy |
| Session | Context and slices | Hours | Matt Pocock |
| Message | The brief | Seconds | Thorsten Ball |

This is not a coincidence and it is worth taking seriously as evidence. The clock model
predicted that a genuinely new framework would either conflict with an existing layer
(same clock) or slot cleanly above or below it (different clock). McKnight slots
cleanly above. He is answering "how does an *organization* get from informal
experimentation to governed AI-native workflows," where KEEL answers "how does *this
build* get from idea to production."

**Consequence:** KEEL is, in his terms, a Level 4-to-5 artifact — a defined, documented,
repeatable human-AI workflow with governance checkpoints. It is one team's or one
person's instance of the discipline his paper argues organizations need. His maturity
model is the ladder; KEEL is a rung you can actually stand on.

---

## 2. Independent convergence

These arrived from different directions and landed in nearly the same place. That is
the strongest signal in this document: he reasons from enterprise governance and audit
exposure, KEEL reasons from cost of change and cost of tokens, and the mechanisms match.

| McKnight | KEEL | Note |
|---|---|---|
| **Modality discipline** — classify deterministic vs probabilistic *before* implementation; "LLM invocation requires explicit written justification" | **The escape-hatch ladder** — deterministic code → cached → small model → large model → human, each rung justifying why the rung below fails | Near-identical mechanism. He reaches it via auditability; KEEL via cost |
| **Deterministic Post-Processing Validation** — schema enforcement and constraint checks on generative output before downstream execution | **Schemas outrank prose**; `additionalProperties: false`; contract tests on real payloads | Same pattern, same rationale |
| **Multi-Model Critique** — a secondary model evaluates the primary's output, introducing "adversarial scrutiny" against "single-model overconfidence" | **Three-axis review in parallel sub-agents**; "an agent that just wrote code is the worst possible reviewer of it" | Same insight, independently stated |
| **Structured Human Review Gates** — "systematic rather than ad hoc" | **Human Review Gates** in `ACCEPTANCE.md` — routed by the gate, not by whoever is coding | Nearly identical wording |
| **Dual-Modality Cross-Checking** — deterministic subsystem validates probabilistic output | The **acceptance gate** itself: deterministic checks bounding probabilistic work | Same |
| **Traceability:** Requirement → Modality Selection → Implementation → Test Validation | **`TRACEABILITY.md`:** Feature line → acceptance check → test → status | His has a column KEEL lacks. See §3.1 |
| **Economic implications of modality discipline** — deterministic scales predictably at low marginal cost; probabilistic is variable and usage-dependent | **Rule 5**, the cost budget as a contract line, cost regression as a CI failure | Same economics |
| **"Architectural sequencing must precede acceleration"** | **Front-load contracts, learn implementations**; phases ordered by cost of change | Same principle, his phrasing is better |
| **"Governance before automation"** — velocity without guardrails introduces deferred instability | **The Floor**, non-negotiable at every tier including the fastest | Same |

### The one that matters most

> "Prompt engineering influences outputs. **Context engineering designs the conditions
> under which outputs are produced, evaluated, and governed.**"

That is Rules 1 and 4 stated in one sentence, and better than KEEL states them. His five
Level-6 workforce capabilities map one-to-one onto KEEL's phases, which is either
convergence or coincidence and reads like the former:

| McKnight, Level 6 capability | KEEL phase |
|---|---|
| Frame problems before generation | **BRIEF** |
| Classify tasks by computational modality | **DESIGN** (cost ladder) |
| Define constraints and success criteria explicitly | **CONTRACT** |
| Design validation checkpoints | **CONTRACT** (acceptance gate) |
| Evaluate outputs for structural, semantic, and policy alignment | **PROVE** |

---

## 3. What he has that KEEL is missing

Four real gaps. The first two are worth closing now.

### 3.1 Modality is a *correctness* decision, not only a cost one — **close this**

KEEL's cost ladder asks "what is the cheapest rung that passes the gate?" McKnight's
classification checkpoint asks four questions, and only one of them is cost:

- **A. Primary task nature** — linguistic, mathematical, constraint-bound, statistical,
  optimization, creative, or hybrid. The dominant characteristic sets the default.
- **B. Determinism requirement** — does it need exact correctness, guaranteed constraint
  satisfaction, reproducibility across executions, or regulatory defensibility? If yes,
  deterministic wins and **LLM use requires written justification**.
- **C. Cost and frequency** — this is the one KEEL already has.
- **D. Explainability and auditability** — if the output must be traceable to
  mathematical logic, deterministic or interpretable methods are mandatory.

KEEL can reach the right answer through cost alone and often will, but not always: a
low-frequency call where the model is cheap and the output must be audit-defensible
passes KEEL's ladder and fails his checkpoint. **His framing is stricter and correct.**

**Change:** add columns B and D to the cost-ladder table in `DESIGN.md`, and add a
`Modality` column to `TRACEABILITY.md` so the chain becomes
*feature line → modality + justification → check → test → status*. That is his
traceability chain and KEEL's matrix merged, and it costs two columns.

### 3.2 No guidance for testing a probabilistic component — **close this**

He names the probabilistic failure classes explicitly: non-reproducible outputs,
context sensitivity, latent hallucination risk, semantic variance not traceable to a
deterministic defect, variable cost, explainability constraints, distributional drift.

KEEL's entire testing discipline — red before green, tests that must be able to fail,
expected values from an independent source of truth — **silently assumes determinism.**
It has no answer to "how do you write an acceptance check for something that varies
between runs?"

The answer exists in the phase-1 project (an eval harness scoring against golden
fixtures and a rubric) but KEEL never teaches it, which means it will get rebuilt or
forgotten.

**Change:** a section in `framework/RULES.md` under Rule 2 covering probabilistic
acceptance — golden fixtures plus a scored rubric, threshold rather than equality,
adversarial fixtures, n-run variance bounds, and drift as a CI check alongside cost
regression.

### 3.3 No architecture for a product that is itself hybrid

His Appendix C defines six layers: Interface, Classification, Routing, Processing,
Governance and Validation, Orchestration — with the rule that **modality decisions must
never occur implicitly inside the processing layer**, and implicit fallback to
probabilistic systems is prohibited without a documented override.

KEEL governs *how you build*. It says nothing about *what you build* when the product
embeds an LLM, and `CONTRACT.md`'s architecture section is generic prose. Given that
essentially everything being built now is hybrid, this is a hole.

**Not closing it yet** — this is a reference pattern to cite in `CONTRACT.md`, not a
rule to absorb, and adopting a six-layer architecture as a default would violate KEEL's
own "fixed artifacts, composable process" principle. Point at it; do not mandate it.

### 3.4 Audit logging as an obligation

He requires modality decisions to be documented and preserved alongside architectural
artifacts, traceable and auditable. KEEL's `AI_WORKFLOW.md` is close but framed as a
case-study byproduct, not as an audit record. In a regulated setting that distinction
matters. Worth a line, not a restructure.

---

## 4. What KEEL has that he does not

Stated plainly, because the cross-reference runs both ways and his paper has real holes
at the operational end.

**1. Session-level context discipline.** He lists "fewer context-loss incidents in
long-running projects" as a measurable Level-6 outcome and gives no mechanism for
producing it. KEEL has the phase-boundary tree, the primary-versus-secondary-source
trade, the smart-zone budget, and the compact-at-boundaries rule. His Level 5→6
transition needs exactly this and does not specify it.

**2. An epistemics for claims.** He has governance, traceability, and audit logging, but
nothing equivalent to Evidence / Inferred / Missing evidence, and nothing equivalent to
"specified is never implemented" or "a gate whose command does not run is FAIL, not
UNKNOWN." His framework can produce a fully governed, fully documented, fully traceable
scaffold that runs nothing. Rule 2 is the guard against that and he has no counterpart.

**3. Right-sizing.** The paper is enterprise-scale throughout. There is no notion of a
three-hour task, and applying its classification checkpoints, documentation
requirements, and governance enforcement to one would be absurd. KEEL's tiers and the
six-item Floor solve a problem he does not acknowledge.

**4. Runnable artifacts.** His toolkit is starter configurations and appendices. KEEL is
a template set plus invocable skills. His paper is the argument; KEEL is an
implementation of a slice of it.

**Do not conflate his maturity levels with KEEL's tiers.** They are orthogonal.
Maturity is *organizational capability* and only moves up. Tier is *per-effort weight*
and is chosen fresh each time. A Level 6 organization still runs Sprint-tier work.
Reading tiers as maturity would be the single most damaging misreading of both
documents.

---

## 5. Vocabulary to adopt

His terms are sharper than KEEL's in four places. Adopt them into `CONTEXT.md`:

- **Modality** — deterministic, probabilistic, statistical, or hybrid. KEEL currently
  says "rung," which is about cost. "Modality" is about kind, and kind comes first.
- **Compensating verification patterns** — the correct umbrella for what the acceptance
  gate, contract tests, three-axis review, and human review gates collectively are:
  mechanisms that relocate rigor from model internals to system design, because
  probabilistic systems lack intrinsic mechanistic verification.
- **Architectural drift** and **stochastic sprawl** — precise names for what KEEL's
  Rules 2 and 3 prevent.
- **"LLM usage must be intentional, not ambient."** The best single sentence in the
  paper and a direct statement of Rule 5's intent.

---

## 6. Verdict

**Do not merge the paper into KEEL.** It is a different clock, it is someone else's
copyrighted work, and flattening an organizational-maturity argument into a per-effort
build framework would damage both.

**Do take three things:**

1. **Modality classification as a first-class step**, replacing the cost-only ladder.
   Cost is one of four tests, not the test. (§3.1)
2. **Probabilistic acceptance testing**, which KEEL currently lacks entirely and which
   is a genuine correctness hole, not a polish item. (§3.2)
3. **His vocabulary**, which is more precise than KEEL's in four named places. (§5)

**And cite him.** In `EXPLAINING-KEEL.md`, the strongest available answer to "how do you
know this is the right shape?" is that an independent enterprise architecture paper,
reasoning from governance and audit exposure rather than from cost of change, arrived at
the same four compensating verification patterns KEEL arrived at from the other
direction. Convergence from independent premises is the closest thing to external
validation this framework currently has.
