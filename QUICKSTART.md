# Quickstart — from roadmap to running code

**Fastest path:** copy this whole folder into the new project's root as `keel-factory/`,
paste the prompt from [`START-PROMPTS.md`](START-PROMPTS.md) as your first message to
whichever coding agent you're using, and it does everything below itself — scaffolding,
wiring and proving the hooks, then interviewing you for the brief. What follows is what
that prompt is actually asking the agent to do — read it if you want to do any step by
hand.

## 0. Set up the new project

```bash
# Link the kit in, so the master stays the only copy (or rsync a full copy instead,
# leaving out .git/, .scratch/ and __pycache__/, if the project must carry its own):
python3 "$KEEL/harness/link_kit.py" ~/path/to/new-project
cd ~/path/to/new-project
mkdir -p docs
cp -Rn keel-factory/keel/templates/. docs/   # -n: never overwrite a file already there
mkdir -p .claude/skills   # or wherever your agent's harness looks for skills
# helm, keel, keel-prove, crew; the board skills (or .../codex/ for Codex); the two senses.
# A skill whose name is already taken is skipped, not overwritten:
for d in keel-factory/keel/skills/*/ keel-factory/keel/skills-board/claude/*/ keel-factory/keel/capabilities/*/; do
  n=$(basename "$d"); [ -e ".claude/skills/$n" ] && echo "skipped $n" || cp -R "${d%/}" ".claude/skills/$n"
done
[ -e CLAUDE.md ] || cp keel-factory/CLAUDE.md CLAUDE.md   # or AGENTS.md / .cursorrules
```

`CLAUDE.md` already references `keel-factory/` by relative path, so this works as soon
as it's copied in — nothing to edit. **If the project already has a `CLAUDE.md`, the last
line leaves it alone:** add the line `@keel-factory/CLAUDE.md` to it instead, which Claude
Code reads as an import. If the project relies on `AGENTS.md` and has no `CLAUDE.md`, a new
`CLAUDE.md` must also say `@AGENTS.md`; once a `CLAUDE.md` exists, Claude Code stops
reading `AGENTS.md` by itself.

**Dropping it into someone else's package to do a job?** Skip this setup entirely: link
the kit in and point the agent at `keel-factory/OPERATOR.md`. The package's own
instructions become the mission, KEEL keeps its working notes inside `keel-factory/.ops/`,
and nothing in the package changes except what the mission changes. Whatever you do,
don't gitignore `keel-factory/`, `.scratch/` or `docs/` — the data-boundary guard blocks
gitignored paths, so KEEL would be locked out of its own files. Its "On session start" section **is** HELM, the
router: from the first message on, the agent orients itself and picks resume / recon /
brief / perception / audit without you having to say which.

**Before pointing this at a real project, wire in the data boundary** — see
`keel-factory/harness/DATA-BOUNDARY.md`. It takes one hook-config entry and one command
to prove it's actually armed. Do this before step 1, not after something has already
leaked.

## 1. Bring what you have

Whatever exists — a roadmap, a product brief, a one-paragraph pitch, nothing but an idea,
or an **existing codebase you want understood and improved** — hand it to the agent. If
you used the starter prompt, HELM routes it automatically; otherwise say **"run helm"**.

- **Nothing written down yet?** Say so. The agent starts BRIEF from a blank page.
- **A roadmap or brief already exists?** Hand it over. The agent treats it as a first
  draft to grill, not a finished spec.
- **An existing or inherited system?** The agent runs **RECON first**
  (`keel-factory/keel/framework/RECON.md`): it reads the system, learns its conventions,
  maps it — including any opaque parts, via perception (below) — and only then proposes a
  prioritized, convention-respecting improvement backlog. This is "take on any project and
  learn how it already does things" made concrete. It does this *before* BRIEF.
- **An opaque target — a shipped binary, a running service, a capture, firmware?** The
  agent reaches for **perception** (`keel-factory/keel/capabilities/reverse-engineering/`,
  which drives REA) — but only on targets you're authorized to analyze, read-only first,
  and it asks before anything that executes or mutates. Source you can read is handled with
  ordinary tools; perception is for when source isn't the whole truth.
- **Hits something it doesn't know how to do?** It doesn't guess — it reaches for the
  **deep-research** sense (`keel-factory/keel/capabilities/deep-research/`): authoritative
  sources, triangulated, tied to the decision, labeled `Inferred` until the system itself
  confirms it. "When you don't know, find out, properly" is a real wired mechanism (web
  search/fetch, research subagents), not an aspiration.

## 2. It picks a tier

SPRINT (hours, presentable) / STANDARD (days, production-ready, the default) / PLATFORM
(weeks, full product) — via the ladder in `keel-factory/keel/framework/TIERS.md`. It will
state which one and why. Correct it if it guessed wrong.

## 3. It asks clarifying questions — this is the part you asked about

At STANDARD or above, the agent runs the **`task-interview`** skill
(`keel-factory/keel/skills-board/claude/task-interview/`): it explores the codebase for
anything the code can answer, and asks you only what the code genuinely cannot — every
open question walked down to a recorded decision, and every question it asks you carrying
two or three concrete options with its recommended pick (a KEEL rule layered over
`task-interview`), so you're steering, not writing from scratch. It repeats this until nothing
is left open, then writes `docs/BRIEF.md` with every remaining gap tagged
`[GUESS: ...]` and resolved.

That's the whole answer to "what if I don't have a full brief yet" — you don't need one.
A rough idea plus a few rounds of answering numbered questions produces one.

## 4. It proceeds through the rest, stopping for approval at each phase

CONTRACT (what must be true) → DESIGN (the shapes, no implementations) → SLICE (thin
vertical slices, filed as board tasks and run under `focused-implementation`/
`orchestrate-implementation`, not a SLICES.md checklist — see
`keel-factory/keel/framework/TASK-BOARD-CROSSREF.md`) → PROVE (three-axis review + the
gate actually run). At each stop it asks exactly: *"Approve `<PHASE>`, or what should
change?"* Nothing proceeds on a partial yes.

## 4b. Working with less supervision between check-ins

This is the actual answer to "how do I not babysit every step": the task board
(`task-board-init`, `to-task`, `focused-implementation`, `orchestrate-implementation`,
`task-board-triage`) gives SLICE-phase work real state that survives losing a session,
and `handoff`/`resume-handoff` give you a clean way to end one session and pick up in
another with no shared memory — the agent writes what it did, what's still undecided,
and the exact commands; the next session verifies the repo against that before acting,
rather than just trusting it. Together these are what let you walk away mid-project and
come back without re-explaining anything.

**This is not a substitute for `keel-prove`.** A board task reaching a closed status is
the same agent's own claim that it's ready — not the independent review Rule 6 and
`LOOPS.md` both require before something actually counts as done. Still run `keel-prove`
in a fresh context before treating a phase or project as finished.

## 5. Bring in the harness when the project needs enforcement, not just prose

If a rule keeps getting silently skipped under pressure ("just this once, skip the
gate"), that's the signal to promote it from a KEEL rule to an ECC hook. Start with
`keel-factory/harness/hooks/block-no-verify.js` and
`keel-factory/harness/hooks/config-protection.js` — see `keel-factory/harness/README.md`
for what each one actually enforces and how to wire it in.

## 6. Building an unattended or recurring loop

Don't improvise one. Read `keel-factory/keel/framework/LOOPS.md` first — it defines the seven fields
a loop must declare before it's allowed to run unattended (trigger, done condition,
*independent* done-checker, stop-entirely condition, escalation trigger, cost ceiling,
LAND step for reconciling concurrent work). It's still a draft inside KEEL, not a numbered
rule, precisely because none of this has failed in the field yet — treat it as the current
best answer, not gospel, and log what actually happens against it.
