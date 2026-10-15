# CREW — a team that does not step on itself (Draft v0.1 — not yet a numbered rule)

**Status: provisional**, on the same footing as `LOOPS.md`. KEEL's standing rule is that a
rule earns its number from a named failure observed in the field. CREW is built from
failures observed *elsewhere* — published, primary, dated (see Sources) — plus principles
KEEL had already adopted. §12 says what would promote it.

**What it is for.** The rest of the factory was written for one agent working alone. Once
work is split across agents — subagents that write, parallel sessions, an agent team —
three new failures become possible: two workers change the same file, workers make
conflicting decisions nobody coordinated, and work comes back that nobody integrates or
checks. CREW is the discipline for that moment: who owns what, what everyone is told,
and how the work comes back. Its runnable half is the `crew` skill
(`../skills/crew/SKILL.md`), which builds on `orchestrate-implementation` instead of
replacing it.

**When it applies.** Whenever work is split across more than one agent. A split an
existing skill already governs — `keel-prove`'s three reviewers, the deep-research
sense's researchers — already complies (§2).

## Sources

Each was fetched on 2026-10-14, and every quotation below comes from that fetched text
(the MAST paper was read through its taxonomy and conclusions, not end to end). Inside
this factory, every claim drawn from them is **Inferred** until a CREW run here confirms
it.

- Anthropic, [*How we built our multi-agent research system*](https://www.anthropic.com/engineering/multi-agent-research-system)
  (2025-06-13) — the delegation contract, the duplicate-work failure, the token cost.
- Cognition (Walden Yan), [*Don't Build Multi-Agents*](https://cognition.com/blog/dont-build-multi-agents)
  (2025-06-12) and [*Multi-Agents: What's Actually Working*](https://cognition.com/blog/multi-agents-working)
  (2026-04-22) — implicit decisions conflict; keep writes single-threaded.
- Claude Code documentation, read 2026-10-14: [agent teams](https://code.claude.com/docs/en/agent-teams),
  [worktrees](https://code.claude.com/docs/en/worktrees), [running agents in parallel](https://code.claude.com/docs/en/agents)
  — file ownership, isolation, and where consent comes from.
- Cemri et al., [*Why Do Multi-Agent LLM Systems Fail?*](https://arxiv.org/abs/2503.13657)
  (arXiv 2503.13657 v3; NeurIPS 2025) — the MAST taxonomy: 14 failure modes in three
  categories, from 1,642 annotated traces.
- Prior art already in this factory: `orchestrate-implementation` (non-interfering
  streams), `LOOPS.md` §2 (the LAND requirement), `ECC-CROSSREF.md` §4.5–4.6 (reviewer
  independence, the LAND gap), and `../../harness/skills/autonomous-loops/` ("the
  orchestrator **assigns** each agent"; "ignoring file overlap in parallel work").

---

## 1. The rule: parallel thinking, single-threaded writing

> **Per file, per run, exactly one writer.** Any number of agents may read, search,
> research, and review in parallel. Writing fans out only along disjoint write sets, and
> every piece of written work comes back through one LAND step, owned by one lead, before
> anyone calls it done.

Four independent sources converge on it:

- Cognition, ten months after arguing against multi-agent systems: they "work best today
  when writes stay single-threaded and the additional agents contribute intelligence
  rather than actions."
- Claude Code's own documentation: "Two teammates editing the same file leads to
  overwrites. Break the work so each teammate owns a different set of files."
- Anthropic: "most coding tasks involve fewer truly parallelizable tasks than research,"
  and LLM agents "are not yet great at coordinating and delegating to other agents in
  real time."
- ECC, already cited here: "If two parallel agents might edit the same file, you need a
  merge strategy."

Reading parallelizes cheaply because readers cannot collide. Writing does not: a file two
workers edit is either silently overwritten or reconciled badly — the overlapping-surgery
failure `orchestrate-implementation` already names.

## 2. Split only what is genuinely parallel

One agent is the default. A split costs more than it looks — Anthropic measured
multi-agent runs at "about 15× more tokens than chats" — and adds coordination that can
itself fail.

| The work | Shape | Why |
| --- | --- | --- |
| Sequential, same-file, or dependency-heavy | **Don't split.** One writer, plus read-only helpers if a search or review would flood its context | Claude Code docs: "For sequential tasks, same-file edits, or work with many dependencies, a single session or subagents are more effective." |
| Breadth — research, review, competing hypotheses | Read-only workers, one distinct question each | Where parallelism pays (Anthropic: "breadth-first queries"), and nothing can collide |
| Independent pieces along confirmed seams | Write lanes with disjoint write sets (§5) | The only safe parallel write |

Start small: two to four workers. The Claude Code docs: "three focused teammates often
outperform five scattered ones." The plan states the token budget for the set (Rule 5);
a split that cannot justify its multiple of one session's cost does not happen.

Splits an existing skill already governs need nothing more. `keel-prove`'s reviewers and
the deep-research sense's researchers each get a distinct question and a return shape,
and share no context with an author.

## 3. Roles

| Role | Who | Owns | Never |
| --- | --- | --- | --- |
| **Manager** | the human | direction; approval of the lane plan; every escalated decision; every data-boundary or authorization *yes* | — |
| **Lead** | the agent the manager talks to | the plan, the lanes, every cross-lane decision, the briefs, dispatch, LAND, and every write to coordination state | implements inside a running lane's write set; leaves a worker to decide what the plan should have decided; relays or assumes the manager's approval |
| **Worker** | one agent per lane | its lane: the write set, the done condition, the return | writes outside its lane; widens its own lane; marks its own work done |
| **Reviewer** | an agent that wrote none of it | independent verification | reviews work whose authoring context it shares |

Two of those *nevers* carry the most weight:

- **Approval does not travel between agents.** The data-boundary rule — ask for the
  specific thing, every time — binds each worker. A worker that reaches it stops, and the
  lead asks the manager. Claude Code draws the same line at the host level: "A teammate
  can't approve a permission prompt or supply consent on your behalf."
- **The lead waits.** "Sometimes the lead starts implementing tasks itself instead of
  waiting for teammates" (Claude Code docs) — at which point the lead is a second writer
  in a lane it does not own.

## 4. One source of truth, one writer of it

Nothing that coordinates the team lives only in chat (Rule 4). There are three
artifacts, all on disk:

- **The board**: what work exists and whether it can start (`status`, `gate`,
  `blocked-by`). CREW leaves it unchanged.
- **The plan task**: `orchestrate-implementation`'s plan document (the set, the
  streams, the verification budget, the execution log), plus CREW's one addition, the
  `## Lanes` table (§5). Cross-lane decisions are recorded in its `## Open questions` as
  resolved items: the board's existing mechanism for a dated decision, so there is no
  second decisions ledger.
- **The brief**: one per worker, derived from the plan (§6).

**Only the lead writes coordination state** — the plan task, the board, the generated
index. Workers return; the lead records. Otherwise the coordination files become the one
file every writer touches. Ownership lives in the lane table, not in task frontmatter:
the board validator rejects unknown frontmatter keys (verified 2026-10-14: an `owner:`
field fails `frontmatter-unknown-key`), and the schema belongs to the vendored board
skills, which CREW wraps but does not edit.

Workers write anything bulky to files and return a pointer. Anthropic's subagents "store
their work in external systems, then pass lightweight references back to the
coordinator," which keeps the lead's context from becoming both the bottleneck and the
single point of loss.

## 5. Lanes — the who-owns-what contract

A **lane** is one `orchestrate-implementation` stream, plus an owner and an **exclusive
write set**:

```text
## Lanes

| Lane | Owner | Tasks | Writes | Mode |
| --- | --- | --- | --- | --- |
| api | worker-api | add-endpoint | `src/api/`, `tests/api/` | worktree |
| docs | worker-docs | update-guide | `docs/guide.md` | shared |
| survey | researcher | — | — | read-only |
```

- **Writes** are repo-relative files, or directories with a trailing `/`. **No globs.**
  Overlap between globs cannot be decided by inspection, and a fence nobody can check is
  not a fence.
- **Write sets are pairwise disjoint.** Tasks that must touch the same file go in the
  *same* lane, in a stated order. That is `orchestrate-implementation`'s own rule that
  streams touching the same files run in series.
- **Reads are open.** Anyone may read whatever the data boundary allows. Only writing
  is partitioned.
- **Mode** is `worktree` (an isolated checkout per lane), `shared` (the same working
  tree, safe only *because* the write sets are disjoint), or `read-only`.
- **Cut lanes along confirmed seams** (DESIGN). Where two lanes meet at an interface —
  an API, a schema, a shared type — the lead fixes it before dispatch, and both lanes
  build against it. Two workers who each discover the interface for themselves is
  exactly Cognition's failure: "Actions carry implicit decisions, and conflicting
  decisions carry bad results."

`check_lanes.py --plan` (`../skills/crew/scripts/`) checks that the write sets are
disjoint before anyone is dispatched.

## 6. The brief — what every worker is handed

A worker has no access to the lead's conversation. Teammates "don't inherit the lead's
conversation history" (Claude Code docs), and `keel-prove` already says the same of its
reviewers: "the sub-agent has no other access to it." So the brief is
**self-contained**, and each field exists because a named failure happens without it:

| Field | Holds | The failure it prevents |
| --- | --- | --- |
| Objective and intent | The one outcome, and why it matters to the whole | Duplicate work and gaps (Anthropic: vaguely briefed subagents "performed the exact same searches as other agents"); MAST *task derailment* |
| Lane | The write set; everything else off-limits | Two writers on one file; MAST *disobey role specification* |
| Decisions already made | Every cross-lane decision this lane depends on, verbatim | Conflicting implicit decisions (Cognition's second principle) |
| Context | Files to start from, house style (RECON), evidence so far | MAST *loss of conversation history*; Cognition's first principle, "share context" |
| Done when | A checkable condition: the command and what it must show | MAST *unaware of termination conditions* and *premature termination* |
| Budget | A ceiling on calls, time, or cost | Agents misjudge effort (Anthropic embedded explicit scaling rules for exactly this); Rule 5 |
| Stop and report if | The triggers in §8 | MAST *fail to ask for clarification* |
| Return | The shape in §7 | MAST *information withholding* |

Anthropic's own contract has four of these: "an objective, an output format, guidance on
the tools and sources to use, and clear task boundaries." CREW adds what writing needs
that research does not: the decisions, the done condition, and the stop triggers.

**Write lanes back-brief before they edit.** The worker's first reply is its plan: the
files it will touch, its approach, and how it will check "done." The lead checks that
plan against the lane before any edit. A misread brief costs one message here, and a
whole lane at LAND. The host affordance is continuing the same worker with its context
intact (Claude Code's `SendMessage`, or agent teams' plan approval). Where a host cannot
continue a worker, the plan opens the return instead, and the fence catches what the
back-brief would have.

Template: `../skills/crew/assets/brief.md`.

## 7. The return — what every worker hands back

1. **Outcome** against the done condition: done, partial, or blocked.
2. **Files written**: every path created or modified. LAND checks this against the
   write set rather than trusting it.
3. **Evidence**: each claim labeled Evidence (the command and its result), Inferred, or
   Missing evidence (Rule 2).
4. **Not done**: what, and why.
5. **Questions**: each carrying two or three concrete options and a recommended pick.
   The posture the lead owes the manager (`DOCTRINE.md` §2) runs the length of the
   chain: nobody hands anyone a blind question.
6. **Pointers** to anything long written to disk.

## 8. Escalation — stop instead of stepping on toes

A worker **stops and returns**, rather than proceeding, when:

- it needs to write a path outside its write set. It names the path, says why, and
  offers the options: the lead extends this lane (only if no other lane owns the path),
  the change goes to the owning lane, or it becomes a follow-on task;
- a decision not in its brief would change another lane, an interface, or the scope;
- a premise in its brief turns out false;
- anything touches the data boundary, authorization, or an irreversible or externally
  visible action. That question goes to the manager, through the lead, every time.

The lead settles what the approved plan already covers, and takes the rest to the
manager as options with a pick. Any change to a write set re-runs `check_lanes.py
--plan` before anyone resumes.

## 9. LAND — how parallel work comes back

`LOOPS.md` §2 requires a LAND step and defines no procedure for it. `ECC-CROSSREF.md`
§4.6 names the same gap and says it "arguably needs a phase." This is the procedure,
written as a step inside CREW, so the five phases stay as they are.

1. **One lane at a time**, in the order the plan states.
2. **Fence.** The lane's changed files must sit inside its write set: `check_lanes.py
   --lane <id> --changed`, fed from the lane's actual diff, never from its own report.
   The fence runs on worktree lanes too, because worktree isolation is not a fence. By
   Claude Code's own account, its isolation checks do not track "which files a shell
   command writes, so a command that writes into the main checkout without running git
   there, such as `cp` or a shell redirect, isn't refused by them." So before landing,
   also confirm the main checkout holds only changes you expect.
3. **Merge**, then **run the gate**: the set's verification, after every landing rather
   than once at the end, so a break is attributable to the lane that caused it.
4. **Log** the landing in the plan's execution log.

A fence or gate failure **evicts** the lane. It is not merged (or its merge is
reverted), and the worker gets back the offending files, the diff, and the failing
output. This is ECC's merge-queue lesson, where an evicted unit's full context "is
captured … and fed back to the implementer," together with its rule against retrying
the same failure blind.

After the last lane, each task closes per `orchestrate-implementation` (its own record,
links repaired, validator and index). Then `keel-prove` runs in a fresh context, and
every reviewer finding gets a recorded disposition: fixed, or rejected with the reason.
**A set is done when PROVE says so** — not when a worker says so, and not when the lead
does.

## 10. What each rule answers

The MAST study's central finding is that multi-agent failure "is not merely a function
of challenges in the underlying model." These are design failures, so they are the kind
a discipline can fix. The rules above, mapped to the three categories:

| MAST category | Its failure modes | CREW's answer |
| --- | --- | --- |
| System design | disobey task or role specification; step repetition; loss of conversation history; unaware of termination conditions | the brief (§6); distinct lanes on one board (§4–5); state on disk; "Done when" |
| Inter-agent misalignment | fail to ask for clarification; task derailment; information withholding; ignored other agent's input; reasoning–action mismatch; conversation reset | stop-and-report triggers (§8); intent in every brief; the fixed return (§7); a recorded disposition for every reviewer finding (§9); the fence, which compares what a worker did with what it was given (§9); the plan on disk, which a reset worker resumes from |
| Task verification | premature termination; no or incomplete verification; incorrect verification | the gate after every landing; `keel-prove` in a fresh context; evidence labels |

## 11. What CREW does not do

- It does not replace `orchestrate-implementation`. It starts from that skill's set and
  streams and adds owners, briefs, and landing. The vendored skill is wrapped, not
  edited (`TASK-BOARD-CROSSREF.md` §5).
- It does not add a phase or a rule number.
- It does not make parallel writing safe in general; it makes *partitioned* writing
  checkable. The fence catches file-level overlap. It cannot see two lanes that are each
  correct alone and wrong together. The gate after each landing and `keel-prove` are for
  that, and it is why the default is one writer.
- It does not run unattended by itself. A CREW run that keeps dispatching without a
  human re-prompting it is a loop, so `LOOPS.md`'s seven fields apply; CREW supplies the
  procedure for its LAND field.

## 12. Promotion bar

CREW stays a draft until a named failure is observed, or demonstrably prevented, in a
real CREW run on a KEEL project. That is the bar every numbered rule cleared. Watch for:

- a fence that passed while two lanes had in fact written the same file (a checker
  defect);
- a worker that widened its own lane and was not caught;
- two lanes that each passed alone and broke together, and whether the per-landing gate
  caught it;
- a brief that omitted a cross-lane decision, after which two lanes diverged.

The checker itself is held to Rule 6b already: its self-test
(`../skills/crew/scripts/test_check_lanes.py`) includes a round trip through a real git
diff, and on 2026-10-14 each of five deliberately broken copies of the checker failed
it. What remains unproven is the discipline in use, not the instrument.
