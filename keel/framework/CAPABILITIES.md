# CAPABILITIES — what the agent can physically do, and the rule that the framework never asks for more

The hardest failure mode for a framework like this is not asking too little. It is asking
for something the agent **cannot actually do**, and getting a confident fabrication back
instead of a refusal. A skill that says "ensure the deployment is healthy" to an agent
with no access to the deployment does not produce a healthy deployment; it produces a
sentence that says it did. The whole evidence discipline exists to prevent exactly that,
and it starts here: **every action the framework asks for must map to a real affordance
the agent has in the environment it is running in.**

> **The grounding rule.** A skill, phase, or doctrine may only instruct an action that
> some actual tool can carry out. If a step cannot be executed by a real affordance, it is
> not a step — it is a wish, and it gets rewritten into something that can be done, or
> handed to the human as a gate. "Do X" where no tool does X is a bug in the framework,
> not an instruction to the agent.

## The affordance classes an AI coding agent actually has

These are the *kinds* of thing an agent in this class can do. The exact tool names differ
by host (Claude Code, Codex, Cursor, …), but the classes are stable, and the framework is
written against the classes, not one host's names. **Check what is actually present in the
session before relying on it** — the roster below is the superset, not a guarantee.

| Affordance | What it enables | The framework work it backs |
|---|---|---|
| **Read files** | Comprehension of anything on disk | RECON mapping, resume, reading `docs/` and the board |
| **Search / grep / glob** (e.g. ripgrep) | Finding symbols, usages, patterns at scale | "what does the code say," crossing joins, convention-reading |
| **Explore (read-only subagent)** | Breadth-first codebase survey without burning main context | RECON, "find where X is," broad lookups |
| **Write / edit files** | Authoring code, docs, artifacts | every phase's output; board tasks; the slices themselves |
| **Run commands (terminal)** | Build, test, run, measure, verify — the only affordance that produces **Evidence** | PROVE's gate, arming checks, the board validators, cost measurement, spikes |
| **Web search + fetch** | Learning external knowledge from authoritative sources | the deep-research sense (`../capabilities/deep-research/`) |
| **Subagents (parallel, clean-context)** | Independent review; parallel investigation; work that must not share context with its author | PROVE's three-axis review; parallel research; CREW's lanes (`../skills/crew/`) |
| **Isolated checkouts (git worktrees)** | A separate working copy per worker, so parallel edits cannot touch each other's files | CREW's `worktree` lanes. Needs git; in Claude Code, `isolation: "worktree"` on a subagent. Not a fence by itself (`CREW.md` §9) |
| **Continuing a worker / agent messaging** | Following up with a worker that keeps its context; agents on a shared task list | CREW's back-brief. Claude Code's agent teams are experimental and off by default, so check before relying on them |
| **Perception (via an external tool like REA)** | Seeing systems with no readable source | the reverse-engineering sense (`../capabilities/reverse-engineering/`) |
| **Scheduled / background execution** | Work that continues without a prompt each cycle | LOOPS.md loops — under its seven guardrails, never unbounded |
| **Tool-call hooks (host-dependent)** | Enforcing a rule at the moment of action | the harness (`../../harness/`) — see the honesty note below |
| **Put a file in front of the user** | Hand over a report/artifact across devices | status reports, RECON maps, review findings |

## The rule of mapping need → affordance

When a discipline needs something done, route it to the affordance that actually delivers
it, and prefer the one that produces the strongest evidence:

- **"Is it true?"** → *run the command.* Reading the code tells you what it should do;
  running it is the only thing that produces Evidence (Rule 2). A claim that was only read
  is `Inferred` at best.
- **"What does the world know?"** → *the deep-research sense*, authoritative sources,
  triangulated — not a guess dressed as fact.
- **"What is this opaque thing doing?"** → *the perception sense*, under its authorization
  gate — not a guess about a binary.
- **"Is this review independent?"** → *a clean-context subagent*, because an agent
  reviewing its own fresh output inflates, structurally. Same-context "review" is not
  independent and the framework does not pretend it is.
- **"Can this run without a human each cycle?"** → *scheduled/background execution*, but
  only with LOOPS.md's stop condition, cost ceiling, and escalation trigger in place.

## Honesty about this environment — a worked example of the rule

This is not abstract. On the machine where this factory was last built:

- **Python 3.13, git 2.50, ripgrep 14 are present** → the task-board validators and index
  generator actually run. Tested, both directions: clean board exits 0, a board with a
  dangling reference exits 1 with the finding named. That layer is **Evidence-grade
  functional**, not prose.
- **Node.js is absent** → the harness hooks (`block-no-verify.js`, `config-protection.js`,
  `data-boundary-guard.js`, `cost-tracker.js`) **cannot execute here.** The grounding rule
  forbids pretending otherwise. So on a Node-less machine the harness enforcement is
  `Missing evidence`, and the framework says so rather than implying a backstop that isn't
  running. Two honest remedies: install Node where the hooks are needed, or port the
  critical hook to Python, which *is* present. The second is done: the data-boundary
  guard's Python version (`../../harness/hooks/data-boundary-guard.py`) was executed and
  proven in both directions here on 2026-10-14. The other three hooks remain Node-only
  and unexecuted, so they stay `Missing evidence`.

That is the rule doing its job: the framework states what actually runs, flags what does
not, and never asks the agent to rely on a capability the environment does not provide.

## When a needed affordance is genuinely absent

Do not fabricate the result, and do not silently skip the step. Instead:

1. **Name the gap** — "this step needs X; X is not available in this session."
2. **Offer the real alternatives** — a different affordance that gets partway, a human
   gate for the part only a person can do, or installing/enabling the missing tool.
3. **Label the consequence honestly** — what stays `Missing evidence` because the check
   could not run. A gate that cannot run is `FAIL`/`PARTIAL`, never a silent `PASS`.

This is the same posture the data-boundary rule takes when a harness has no hooks: state
the limitation once, plainly, and operate within what is actually there.
