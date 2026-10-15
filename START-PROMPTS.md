# Starter prompt

## How this is meant to be used

1. Put the kit in the project's root as `keel-factory/`. By default, link it, so the
   master stays the only copy and every edit to it reaches every project:

   ```bash
   python3 "$KEEL/harness/link_kit.py" /path/to/your-project
   ```

   Copy it instead only when the project must carry its own copy — committed to a shared
   repo, or worked on from another machine. The links point at this machine:

   ```bash
   rsync -a --exclude '.git/' --exclude '.scratch/' --exclude '__pycache__/' \
     "$KEEL/" /path/to/your-project/keel-factory/
   ``` **Dropping it
   into someone else's package to do a job?** Use the one-line operator activation at the
   end of this file instead of the prompt below.
2. Paste the prompt below as your first message to whichever coding agent you're using,
   in that project.
3. **That's the only time you need this file.** Step 2 has the agent write a
   project-local instruction file (`CLAUDE.md`, `AGENTS.md`, or whatever your tool
   reads) whose first section says: the presence of this file is itself the trigger —
   check project state and orient, no special phrasing required. From then on, opening
   a new session in this project and sending *any* first message — "let's continue,"
   a bug report, literally anything — is enough for the agent to reconstruct where
   things stand and act. You don't re-paste this prompt after the first time, and you
   don't have to remember which phase you left a given project at.

This one prompt is written to work under any LLM coding agent that can read/write files
in the project and ask you questions in chat — Claude Code, Codex CLI, Cursor, Windsurf,
Cline, Aider, Copilot Chat, whatever comes next. It deliberately does not name a specific
hook-config file format, because most of those tools don't share one; where your
particular agent has no enforcement mechanism, the prompt has it say so rather than
imply protection that isn't actually there.

---

## The prompt

```text
There is a folder in this project's root called keel-factory/ — an engineering
framework plus an optional enforcement layer. Set this project up from it, then help me
build. I work across a lot of different projects and won't always remember the exact
state I left one in, so treat reconstructing that as part of your job, not mine.

1. Read keel-factory/README.md and keel-factory/QUICKSTART.md in full before doing
   anything else.

2. Check project state first:
   - If a handoff document exists at the expected scratch path, resume from that
     instead of the rest of this list.
   - Otherwise, if docs/BRIEF.md or docs/STATE.md already exist here, this project was
     already set up. Read everything in docs/ plus the task board if one exists, tell
     me plainly where it stands (which phase is approved, what's next, anything that
     looks stale), and pick up from there — skip the rest of this list.
   - Otherwise, this is a fresh start. Continue below.

3. Scaffold the project. Nothing in this step may overwrite a file that already exists;
   where something is already there, skip it and tell me.
   - Copy keel-factory/keel/templates/* into ./docs/ without overwriting. On an existing
     system, skip this entirely: create each artifact from its template when its phase
     starts.
   - Set up this project's own persistent instruction file, in whatever convention
     your harness actually reads (CLAUDE.md, AGENTS.md, .cursorrules, or similar — you
     know which one applies to you). Use keel-factory/CLAUDE.md as the source content
     verbatim; nothing in it is specific to one tool. If that file already exists, never
     replace it: add a pointer to keel-factory/CLAUDE.md (in Claude Code, the import line
     @keel-factory/CLAUDE.md), or ask me where it should go. If your harness has a
     skill-loading mechanism, install everything under keel-factory/keel/skills/ (helm,
     keel, keel-prove, crew), everything under keel-factory/keel/skills-board/claude/ (or
     .../codex/ if that's the runtime), and keel-factory/keel/capabilities/ (the two
     senses, reverse-engineering and deep-research) into wherever it looks for skills,
     skipping any skill whose name is already taken there. If it doesn't, that's fine —
     just read the SKILL.md files yourself and follow them as written instructions. Read keel-factory/ARCHITECTURE.md once so you understand how
     these relate before you start routing between them.

4. Check whether your harness supports blocking a tool call before it runs (a
   "PreToolUse"-style hook, or equivalent). If it does:
   - Read keel-factory/harness/README.md and keel-factory/harness/DATA-BOUNDARY.md.
   - Wire in the hooks under keel-factory/harness/hooks/ using whichever of
     keel-factory/harness/settings.hooks.json or settings.hooks.codex.json is closer to
     your harness's config format, adapted as needed. Point each hook command at this
     project's actual resolved absolute path to keel-factory/harness/hooks/ — not a
     relative path, since a hook command isn't guaranteed to run with this project as
     its working directory.
   - Run every armed-check command listed in those two files yourself, right here, and
     show me the actual output — block cases and allow cases both. Don't tell me a
     hook is active unless you've watched it work. If Node.js isn't installed, tell me
     rather than skipping this: the three ECC hooks need it, but the data-boundary guard
     runs on python3, so wire and arm that one anyway.
   If your harness has no such mechanism at all, tell me plainly that this project has
   no enforced backstop and the data-boundary rule in the instruction file from step 3
   is running as policy only, not as something technically blocked.

5. Regardless of what step 4 found: treat the "Data boundary" section of the
   instruction file you just wrote as binding for every action, from now on. Ask before
   any invasive or sensitive access, every time, naming the exact path or action — not
   a one-time blanket yes.

6. Now the actual work — route with HELM (keel-factory/keel/skills/helm/SKILL.md), don't
   assume BRIEF. Work out which this is — a fresh idea, a roadmap, or an
   existing/inherited system — from what you can see, then tell me which you think it
   is and why, and let me confirm or correct it.
   - **Existing or unfamiliar system?** Run RECON first
     (keel-factory/keel/framework/RECON.md): read it, learn its conventions, map it, and
     propose a prioritized improvement backlog that respects its house style — before any
     BRIEF. For opaque parts (a binary, a running service, no full source), reach for
     perception (keel-factory/keel/capabilities/reverse-engineering/) under its
     authorization gate: authorized targets only, read-only before anything that executes
     or mutates, ask me first naming the exact target.
   - **Fresh idea or roadmap?** Go to BRIEF. Reconstruct what you can from anything I
     gave you first, then run the task-interview skill (or, if unavailable, the numbered
     Interviewing round in keel-factory/keel/skills/keel/SKILL.md) to fill the real gaps.
   Either way, the point of asking is to jog my memory on this specific project, not to
   make me re-explain what you could find by looking.

Report back after each numbered step before moving to the next one.
```

---

## If you want the harness wiring done precisely instead of adapted on the fly

The universal prompt above asks the agent to figure out your harness's hook format
itself, which is more robust across unknown tools but less precise for the two harnesses
this factory's hooks were actually written and reasoned about. If you're specifically on
**Claude Code** or **Codex CLI**, the exact wiring — file locations, JSON shapes, the
Codex-specific hook-trust step, the two open verification questions about Codex's tool
names and skills directory — is spelled out step by step below. Same outcome, less for
the agent to infer.

**Claude Code:**

```text
Set this project up from ./keel-factory/ (an engineering framework + harness). Read
keel-factory/README.md and QUICKSTART.md first.

Scaffold, overwriting nothing that already exists (skip it and tell me): copy
keel-factory/keel/templates/* into ./docs/ (on an existing system, skip this and create
each artifact from its template when its phase starts), copy everything under
keel-factory/keel/skills/ (helm, keel, keel-prove, crew), everything under
keel-factory/keel/skills-board/claude/, and keel-factory/keel/capabilities/ (the two
senses, reverse-engineering and deep-research) into ./.claude/skills/, skipping any skill
whose name is already taken there, and copy keel-factory/CLAUDE.md into ./CLAUDE.md as-is
if there is no CLAUDE.md yet (it already references keel-factory/ by relative path). If
there is one, never replace it: add the import line @keel-factory/CLAUDE.md to it. If the
project relies on AGENTS.md and has no CLAUDE.md, the new CLAUDE.md must also import
@AGENTS.md, or Claude Code stops reading AGENTS.md. Read keel-factory/ARCHITECTURE.md once
so you know how these relate.

Wire the harness hooks in before anything else: read keel-factory/harness/README.md and
DATA-BOUNDARY.md, and write the hooks into ./.claude/settings.local.json, merging if it
exists (it will hold this machine's absolute path, so it never goes in the shared
settings.json). Use keel-factory/harness/settings.hooks.json as the template, with the
/ABSOLUTE/PATH/TO/ placeholders replaced by this project's actual absolute path to
keel-factory/harness/hooks/ (resolve it, don't guess — a relative path isn't safe here
since hook commands aren't guaranteed to run with this project as their working
directory). Wire only the hooks whose interpreter is installed: a hook whose interpreter
is missing exits 127, which Claude Code treats as a non-blocking error, so it guards
nothing. Then run every armed-check command in those two files yourself and show me the
real output — block and allow cases both. If Node isn't installed, tell me: the three ECC
hooks need it, but the data-boundary guard runs on python3, so wire and arm that one
anyway.

From here on, CLAUDE.md's "Data boundary" section is binding regardless of whether the
hooks actually got wired correctly.

Then route with the helm skill — don't assume BRIEF. If this is an existing or
unfamiliar system, run RECON first (keel-factory/keel/framework/RECON.md): learn its
conventions and map it before proposing changes, reaching for perception
(keel-factory/keel/capabilities/reverse-engineering/) on any opaque part, under its
authorization gate. If it's a fresh idea or roadmap, go to BRIEF and grill me with the
task-interview skill on whatever's still unclear. Either way, treat me as someone who may
not remember this project's exact state. Once SLICE work starts, file it as board tasks
(task-board-init, to-task), not a SLICES.md checklist, and use handoff/resume-handoff at
any context boundary.

Report back after each step.
```

**Codex CLI:**

```text
Set this project up from ./keel-factory/ (an engineering framework + harness). Read
keel-factory/README.md and QUICKSTART.md first.

Scaffold, overwriting nothing that already exists (skip it and tell me): copy
keel-factory/keel/templates/* into ./docs/ (on an existing system, skip this and create
each artifact from its template when its phase starts), copy everything under
keel-factory/keel/skills/ (helm, keel, keel-prove, crew), everything under
keel-factory/keel/skills-board/codex/, and keel-factory/keel/capabilities/ (the two
senses, reverse-engineering and deep-research) — each its own folder with SKILL.md — into
./.codex/skills/, skipping any skill whose name is already taken there. Start a fresh
session and confirm they got picked up — if not, also copy them into ./.agents/skills/
and retry, the convention has moved before. Copy keel-factory/CLAUDE.md into ./AGENTS.md
as-is if there is no AGENTS.md yet; if there is one, never replace it — add a short,
clearly headed section telling the agent to read and follow keel-factory/CLAUDE.md, or
ask me where it should go. Read keel-factory/ARCHITECTURE.md once so you know how these
relate.

Wire the harness hooks in before anything else: read keel-factory/harness/README.md and
DATA-BOUNDARY.md, create ./.codex/hooks.json (merging if it exists) using
keel-factory/harness/settings.hooks.codex.json as the template with the
/ABSOLUTE/PATH/TO/ placeholders replaced by this project's actual absolute path to
keel-factory/harness/hooks/ (resolve it, don't guess — a relative path isn't safe here
since hook commands aren't guaranteed to run with this project as their working
directory). That template assumes Codex reports tool calls as "Bash"/"Read"/"Edit"/
"Write" the same as Claude Code — verify that's actually true for this Codex version
before trusting it, and fix the matcher regexes if not. Codex requires
each hook explicitly trusted before it runs — walk me through the /hooks review command
and tell me exactly what to approve; don't say the hooks are active until that's done.
Then run every armed-check command in those two files yourself and show me the real
output. If Node isn't installed, tell me: the three ECC hooks need it, but the data-boundary
guard runs on python3, so wire and arm that one anyway.

From here on, AGENTS.md's "Data boundary" section is binding regardless of whether the
hooks actually got wired and trusted correctly.

Then route with the helm skill (.codex/skills/helm/, or wherever it landed) — don't
assume BRIEF. If this is an existing or unfamiliar system, run RECON first
(keel-factory/keel/framework/RECON.md): learn its conventions and map it before
proposing changes, reaching for perception
(keel-factory/keel/capabilities/reverse-engineering/) on any opaque part under its
authorization gate. If it's a fresh idea or roadmap, go to BRIEF and grill me with the
task-interview skill on whatever's still unclear. Treat me as someone who may not
remember this project's exact state. Once SLICE work starts, file it as board tasks
rather than a SLICES.md checklist, and use handoff/resume-handoff at any context
boundary.

Report back after each step.
```

---

## Dropped into someone else's package — operator mode

When the job is someone else's package, use this instead of everything above. Nothing
gets set up: the package's own instructions are the mission, KEEL is the kit underneath,
and the package ends up changed only by the mission itself. The protocol the agent
follows is [`OPERATOR.md`](OPERATOR.md).

Link the kit in. The master stays the only copy:

```bash
python3 "$KEEL/harness/link_kit.py" /path/to/package
```

Then say:

```text
keel-factory/ is your kit. Read keel-factory/OPERATOR.md and take on this package: its own instructions are the mission.
```

The agent proves the guard is live, reads the package's instructions, does the job,
proves it with the package's own checks, and debriefs. Unlinking afterwards
(`link_kit.py … --remove`) removes every trace. For the guard to arm itself on arrival, set it up once
per machine as `OPERATOR.md` → *Activation* describes.
