---
name: crew
description: Split work across more than one writing agent without two writers on one file. Decides whether to split, cuts lanes with exclusive write sets, briefs each worker, and lands each lane behind a fence check. Use before dispatching parallel writers, a subagent team or worktrees. Builds on orchestrate-implementation.
---

# CREW — split the work, never the files

One rule: **parallel thinking, single-threaded writing.** Any number of agents may read,
search, research, and review at once; every file has exactly one writer per run. The
steps below keep that true and checkable. The reasoning and sources are in
`../../framework/CREW.md`.

You are the **lead**. You own the plan, the lanes, the cross-lane decisions, the landing,
and the line to the manager. Each worker owns its lane and nothing else.

In a copied skill (this file sits under a project's `.claude/skills/` or
`.agents/skills/`, not under `keel/`), read every `../` path under `keel-factory/keel/`,
and root files such as `CLAUDE.md` under `keel-factory/`, even when the project has a
file of that name.

## First, is KEEL switched on here?

If KEEL is not switched on here (no `.keel/` or `keel-factory/` by HELM's rule), or a
`.keel/` holds no `keel.json`, run HELM's switch-on first (`../helm/SKILL.md`, its
"First — is KEEL switched on here" section), then come back.

In operator mode (`.keel/keel.json` says operator; or no role is recorded, as with a
linked or copied `keel-factory/`, and by HELM's rule the project carries its own
instructions that are not KEEL's; or the session note, the user or your brief says so; or
switch-on just decided it), `../../../OPERATOR.md` governs: every record this skill would
keep under `docs/` or on the task board goes in `<ops>`, KEEL's notes folder defined
there, never in the package's own tree.

## 0. Should this be split at all?

One agent is the default. Split only work that is genuinely independent:

| The work | Team |
| --- | --- |
| Sequential, same files, or many dependencies | **Don't split.** One writer under `focused-implementation`; add read-only helpers if a search or review would flood its context. |
| Breadth — research, review, competing hypotheses | Read-only workers, one distinct question each. |
| Independent pieces along confirmed seams | Write lanes with disjoint write sets. |

Start with two to four workers. A multi-agent run costs many times the tokens of one
session, so the plan states the budget (Rule 5). If the only split is `keel-prove`'s
reviewers or the deep-research sense's researchers, those skills already govern it.

## 1. Select and sequence

Board work: run `orchestrate-implementation`'s selection and raise its plan task — the
set, the streams, the exclusions. **Each stream becomes one lane.** Work that is not on
the board, such as a research fan-out, still gets a plan on disk (a board task or a
`docs/` note): the lanes must live in a file, not in chat.

## 2. Cut the lanes

Add a `## Lanes` table to the plan task:

```text
## Lanes

| Lane | Owner | Tasks | Writes | Mode |
| --- | --- | --- | --- | --- |
| api | worker-api | add-endpoint | `src/api/`, `tests/api/` | worktree |
| docs | worker-docs | update-guide | `docs/guide.md` | shared |
| survey | researcher | — | — | read-only |
```

- **Writes**: repo-relative files, or directories with a trailing `/`. No globs.
  **Exclusive**: no two lanes share a path. Tasks that must touch the same file go in
  the same lane, in a stated order.
- **Mode**: `worktree` (its own isolated checkout), `shared` (the same working tree,
  safe only because write sets are disjoint), or `read-only`.
- The plan task and the board are yours; they never go in a worker's write set.
- **Decide before you dispatch.** Every choice two lanes depend on — an interface, a
  name, a format, a convention — is decided now and recorded in the plan task's
  `## Open questions` as a resolved item. Where lanes meet at a seam, fix the seam
  first. Two workers discovering the same interface separately is how parallel work
  comes back incompatible.

## 3. Check the lanes

```text
python3 scripts/check_lanes.py --plan <plan-task.md>
```

It must report no findings. Then run the board validator: the plan is a board task.

## 4. Get agreement

Present the lanes alongside `orchestrate-implementation`'s set and exclusions: who owns
what, in which mode, the landing order, and the budget. Put every judgment call to the
manager as two or three options with your recommended pick, never as an open question.
Do not dispatch before the manager agrees. In checkpoint mode, an approved BRIEF and
CONTRACT plus the manager's own words allowing agents count as that agreement: quote the
words in the plan, and still stop for anything those approvals did not cover.

## 5. Brief each worker

Fill [assets/brief.md](assets/brief.md) once per lane. It must be **self-contained**: a
worker has no access to your conversation, only to what you hand it. A section you
cannot fill is a planning gap to close now, not a detail to leave to the worker.

## 6. Dispatch

- **Write lanes back-brief first.** Dispatch with "reply with your plan; do not edit
  yet." Check the plan against the lane — every file inside the write set, the done
  check concrete — then let the same worker continue with its context intact (in
  Claude Code, `SendMessage` to that agent). If the host cannot continue a worker,
  have the plan open its return instead; the fence at landing catches the rest.
- **worktree**: one isolated checkout per lane. In Claude Code, the `Agent` tool with
  `isolation: "worktree"`. Its worktree branches from the repository's default branch
  unless the `worktree.baseRef` setting is `"head"`, so set that when a lane builds on
  unmerged work. Worktrees need git (or a `WorktreeCreate` hook for another VCS);
  without them, run the lane `shared` or in series, and say which.
- **shared**: an ordinary subagent in the same tree. Legal only because the write sets
  are disjoint. Workers do not commit; you commit each lane at landing. If you keep
  writing while shared lanes run, declare your own write set as a lane too, or the fence
  cannot tell your changes from theirs (`../../framework/CREW.md`, field record).
- **read-only**: research or review subagents (`Explore` for codebase sweeps). A
  reviewer never shares context with the author of what it reviews.
- **Agent teams** (Claude Code, experimental): teammates share a task list but are not
  isolated in worktrees, so partition them by write set exactly as above.

Record each lane's base commit in the plan's execution log as you dispatch it.

## 7. While lanes run

- Write nothing inside a running lane's write set. Wait for the workers rather than
  doing their work.
- You are the only writer of the plan task and the board. Workers return; you record.
- Answer escalations (`../../framework/CREW.md` §8). Any change to a write set re-runs
  step 3 before anyone resumes.
- Data-boundary and authorization questions go to the manager, through you, every
  time. An approval relayed by another agent is not the manager's approval.

## 8. Land — one lane at a time

In the order the plan states, for each lane:

1. **Fence.** The lane's real changes, not its own list of them, must sit inside its
   write set:

   ```text
   { git -C <worktree> diff --name-only -z --no-renames <base>;
     git -C <worktree> ls-files -z --others --exclude-standard; } \
     | python3 scripts/check_lanes.py --plan <plan-task.md> --lane <id> --changed -
   ```

   For shared lanes, run the same pipe in the main checkout against `HEAD` and drop
   `--lane`: every change must belong to some lane. Also confirm the main checkout holds
   no change you did not expect. Worktree isolation does not track what a shell command
   writes, so a worktree lane can still reach outside its checkout.
2. **Merge** the lane, or commit a shared lane by staging exactly its write set.
3. **Gate.** Run the set's verification now, not once at the end, so a break belongs to
   the lane that caused it.
4. **Log** the landing in the plan's execution log.

A fence or gate failure **evicts** the lane. Do not merge it, or revert the merge, and
send the worker the offending files, the diff, and the failing output. Never re-dispatch
a lane blind.

## 9. Close

Close each task per `orchestrate-implementation` (its own record, links repaired,
validator and index). Then run `keel-prove` in a fresh context, and record a
disposition for every reviewer finding: fixed, or rejected with the reason. The set is
done when PROVE says so, not when the workers or you do.

## Guardrails

- Never put two writers on one file in one run.
- Never dispatch a writer without a brief that names its write set and its done
  condition.
- Never let a worker widen its own lane. Widening is the lead's call and re-runs the
  check.
- Never edit inside a running lane's write set yourself.
- Never treat a worker's "done" as done. Fence, gate, then `keel-prove`.
- Never relay or assume the manager's approval between agents.
- Never split sequential or same-file work to make it look parallel.
- Only the lead dispatches writers. A worker may use read-only helpers; it never spawns
  a writer.

## Resources

- Principles, sources, and the failure each rule answers: `../../framework/CREW.md`
- Worker brief template: [assets/brief.md](assets/brief.md)
- Lane checker: [scripts/check_lanes.py](scripts/check_lanes.py), with its self-test
  [scripts/test_check_lanes.py](scripts/test_check_lanes.py) (`python3
  scripts/test_check_lanes.py`)
- Task selection and the plan task: `orchestrate-implementation`
  (`../../skills-board/claude/orchestrate-implementation/`)
