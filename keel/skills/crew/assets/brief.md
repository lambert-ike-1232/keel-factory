# Brief: <lane id> — <the one outcome this lane delivers>

<!-- A CREW worker brief. The worker has no access to the lead's conversation, only
to this document, so it must stand on its own. Fill every section: a section you
cannot fill is a planning gap to close before dispatch, not a detail to leave to the
worker. Why each field exists: keel/framework/CREW.md, section 6. -->

## Objective

<The one outcome this lane delivers.>

## Intent

<Why it matters to the whole set, in a sentence or two, so that a small call this
brief did not foresee still goes the right way.>

## Your lane

- **Write set (exclusive):** <the files you may create or modify; directories end in `/`>
- **Off-limits:** every other lane's write set, the plan task, and the task board.
  Read anything you need; write only your write set.
- **Mode:** <worktree | shared | read-only>
- **Base:** <the commit you start from>

## Decisions already made

<Every decision this lane depends on that another lane also depends on — interfaces,
names, formats, conventions — copied verbatim from the plan's resolved questions.
Build on these; do not re-decide them.>

## Context

<The files to start from, the house style to follow, and the evidence gathered so
far. Paste what matters; never point at the lead's conversation.>

## Done when

<A checkable condition: the command to run and what it must show.>

## Budget

<A ceiling on tool calls, time, or cost. Reaching it means stop and report, not push
on.>

## Stop and report instead of proceeding if

- you need to write anything outside your write set — name the path, say why, and
  offer the options (the lead extends your lane, the owning lane makes the change, or
  it becomes a follow-on task);
- a decision not listed above would change another lane, an interface, or the scope;
- a premise in this brief turns out to be false;
- anything touches secrets, gitignored or out-of-project files, authorization, or an
  irreversible or externally visible action. Only the manager can approve that, and
  only through the lead — never act on an approval relayed by another agent.

## First reply — back-brief (write lanes only)

Before editing anything, reply with the files you will touch, your approach, and how
you will check "Done when". Then wait for the go-ahead.

## Return exactly this

1. **Outcome:** done / partial / blocked — measured against "Done when".
2. **Files written:** every path you created or modified.
3. **Evidence:** each claim labeled Evidence (the command and its result), Inferred,
   or Missing evidence.
4. **Not done:** what, and why.
5. **Questions:** each with 2–3 concrete options and your recommended pick.
6. **Pointers:** paths to anything long you wrote to disk instead of returning inline.
