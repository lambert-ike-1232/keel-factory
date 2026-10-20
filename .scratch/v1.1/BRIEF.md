# Brief: KEEL v1.1 — conform to what Claude Code and Codex really do

**Tier:** STANDARD. Ladder (`keel/framework/TIERS.md`): others depend on it within a week
(the manager, on real projects) → yes; outlives one session → yes; needs ops (deploys,
on-call, an SLA, real users) → no. So STANDARD, not PLATFORM.
**Stop mode for this build:** checkpoint (one round of questions with BRIEF and CONTRACT
together, then DESIGN → SLICE → PROVE without stopping), dogfooding the mode this brief
adds. The manager asked for exactly that in the feedback ("go nuts").
**Date:** 2026-10-18
**Grounding:** `RECON.md`, `keel/framework/HARNESS-PROBES.md` and the three `research-*.md` fact sheets in the
session scratchpad, summarized in `CONTRACT.md` §2.

---

## Part 1 — Intake (from the manager's message)

1. **What:** KEEL, changed so it only asks Claude Code and Codex for what they can do,
   and uses what they offer instead of working around it.
2. **For whom:** the manager, starting projects from an idea, taking codebases to
   production grade, and dropping into other people's packages; on Claude Code first,
   Codex second.
3. **Must-haves** (each becomes a traceability row):
   - M1. Install once per machine; every KEEL skill is visible in every project, from one
     master, with no per-project copies.
   - M2. One front door (HELM) and one opening line; HELM tells owner from operator, and
     asks with options when it can't tell.
   - M3. A stop-mode setting: supervised, checkpoint, unattended.
   - M4. The PROVE reviewers shipped as real agent definitions, so the fresh-context
     review doesn't depend on the agent remembering.
   - M5. An eval suite (vague idea, complete description, operator job) with a no-plugin
     baseline.
   - M6. Less always-loaded context: a short always-on layer, detail in skills.
   - M7. The same for Codex, as far as Codex really allows, with every gap named.
   - M8. The data-boundary guard keeps working, and arms in KEEL projects under the new
     install.
   - M9. KEEL's own documents say what each harness can and can't do (CAPABILITIES), with
     dated sources.
4. **Not doing:** changing the five phases, three tiers or six rules; editing the
   vendored `keel/skills-board/`; porting the Node hooks; a heavy orchestrator; a Stop
   hook that guesses "done" claims from wording.
5. **The hard part:** keeping one master that serves two harnesses whose mechanisms
   differ (Codex asks multiple-choice questions only in Plan mode on its newest models;
   its hooks, if any, are invisible to the model), without forking the content.
6. **Done and working looks like:** `claude plugin validate .claude-plugin/plugin.json`
   exits 0 with only the expected root-CLAUDE.md warning (strict fails on that warning by
   design); a fresh headless Claude Code session in a throwaway project sees `keel:helm`,
   gets the SessionStart context, and has its guard block a fake `.env`; KEEL's own check
   script proves the skill set is well-formed for both harnesses and fails on broken
   copies; the always-on cost is measured with `claude plugin details`; every old
   self-test still passes. *(Amended 2026-10-18, CONTRACT Amendments A7; was:
   "`claude plugin validate --strict` passes".)*
7. **Inputs / outputs:** in, the master folder; out, the same folder installable as a
   Claude Code plugin and as Codex skills, plus changed docs.
8. **Interaction:** a CLI install line, slash commands (`/keel:helm`), plain speech.
9. **Sensitive data:** none in KEEL itself; the guard protects the projects it runs in.
10. **Constraints:** Python standard library only; no Node; Claude Code 2.1.170 here (no
    `plugin eval`); no Codex CLI on `PATH`, Codex desktop app present; cost ceiling for
    live trials set in CONTRACT.

## Part 2 — The rewrite, with guesses tagged

KEEL becomes a plugin whose root is the master folder. Its 22 skills (HELM, keel,
keel-prove, crew, the two senses, the 16 vendored skills) load from where they already
are. The plugin's SessionStart hook replaces the 200-line `CLAUDE.md` with a short router
note, and only in projects that switched KEEL on; the same marker arms the guard. HELM
becomes the one front door and records the project's role. TIERS gains a stop-mode
setting that changes which stops block, never which phases run. `keel-prove`'s three
reviewers become agent files. An eval suite sits in `evals/`. Codex gets the same skills
through its own skill folder and a short `AGENTS.md` block, and an honest adapter for
what it lacks.

*Stale 2026-10-18: the plugin loads 18 skills by default, KEEL's six and twelve of the
board skills; the four Diataxis skills are opt-in (CONTRACT, Amendments A1).*

- [GUESS: the install method] Symlinking the master into `~/.claude/skills/keel` (a
  skills-dir plugin) is the default, because it is live (P9) and matches "one master,
  linked"; a marketplace install (P8, copied and versioned) is the alternative for a
  machine that wants pinned releases. **Resolved by probe P8/P9**, recorded in
  CONTRACT.
- [GUESS: what switches KEEL on in a project] A `.keel/` folder at the project root, or a
  linked `keel-factory/`. → question round.
- [GUESS: the default stop mode] Checkpoint at SPRINT and STANDARD, supervised at
  PLATFORM. → question round.
- [GUESS: guard scope] Armed only in projects that switched KEEL on. → question round.
- [GUESS: live trial budget] One fresh-agent owner-mode trial, capped. → question round.
- [GUESS: Codex question style] In Codex, interview rounds run in Plan mode where
  `request_user_input` exists; elsewhere one plain-text question with a stated default.
  → decided by research, recorded in CONTRACT.

## Announcement

KEEL now installs once. Link it into your Claude Code skills folder and `/keel:helm` is
in every project: it works out whether this is your project or someone else's package,
asks what it needs in one round with a recommended answer for each question, and then
builds to the stop mode you picked, stopping only for safety, a real fork, or a failing
check. Its reviewers ship as agents, so "done" always means an independent review ran.
It costs a few hundred tokens of context in a KEEL project and nothing but its skill list
anywhere else. On Codex the same skills install into Codex's own folder, and KEEL says
plainly where Codex can't do what Claude Code does.

*Stale 2026-10-18: "a few hundred tokens" is low. In a KEEL project the SessionStart
injection alone is 5,871 characters (`check_kit.py`, 2026-10-18), on top of the skill
listing every project pays: about 2,522 tokens by `claude plugin details`, measured before
phase 1's description edits ([PROVE-FINDINGS.md](PROVE-FINDINGS.md), G2). After fix
round 3, 2026-10-18: the injection is 5,903 characters (`check_kit.py`); live run L8,
run after PROVE pass 1's hook fixes on the layer as it then stood, measured 5,918
characters of injected context (its record corrected in fix round 3); and
`claude plugin details` gives ~2,530 tokens in this machine's config and ~1,953 in a
fresh config holding only the plugin, a figure that leaves the SessionStart injection
out (probe P14; both in [HARNESS-PROBES.md](../../keel/framework/HARNESS-PROBES.md)).*
