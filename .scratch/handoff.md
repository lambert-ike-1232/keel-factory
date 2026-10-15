# Handoff — KEEL FACTORY development

Written 2026-10-14 (the second session that day). Starting point for a fresh session with
no prior context. The work is the ongoing development of the **KEEL FACTORY**
meta-framework at `/Users/lambertike/Documents/KEEL-FACTORY` — a portable engineering
framework (prose disciplines plus a few runnable scripts) that gets copied into real
projects. You are developing the framework itself here. The previous session's handoff
is preserved at `.scratch/handoff-superseded-2026-10-14.md`; everything load-bearing in
it is carried forward below.

> **v1.0.0 released 2026-10-15. Development continues on the manager's other machine.**
> The master is now a git repository, tagged `v1.0.0`. It travels as a release folder
> (`KEEL-FACTORY-releases/v1.0.0/`: a git bundle, an archive, the manual, checksums),
> built and proven by `harness/make_release.py`.
>
> On the new machine the master is wherever the bundle was cloned, and `$KEEL` points at
> it (`MANUAL.md` section 3). Every path below that starts
> `/Users/lambertike/Documents/KEEL-FACTORY` means `$KEEL` there. Measure staleness by
> `git log` from now on, not by file times. Cut each later release per `MANUAL.md`
> section 11.

---

## Next session — start here

No `/handoff into` directive was given. The manager's most recent instruction in the
writing session was a pick from offered options:

**Agenda, verbatim:** "Port the guard to Python (Recommended)" — offered as: *"Pending
item 3: rewrite data-boundary-guard.js in Python so the one security-critical hook
actually runs on this machine, and show it blocking and allowing."*

**What it resolves to today:** **done** —
`harness/hooks/data-boundary-guard.py` plus its self-test
`harness/hooks/test_data_boundary_guard.py`, proven (see *Verified state*). Docs updated:
`harness/DATA-BOUNDARY.md`, `harness/README.md`, `README.md`, `CLAUDE.md`,
`keel/framework/CAPABILITIES.md`, `START-PROMPTS.md`. The manager then decided both
follow-up questions, and both are applied (see *Open questions*).

**Before acting on it:** nothing outstanding. When touching the guard, keep it a
backstop for the CLAUDE.md data-boundary rule, never a substitute.

### What is pending

- **The first live operator mission.** The manager will drop the factory into a real
  package and give it the one-line activation in `OPERATOR.md` → *Activation*. A full
  rehearsal passed (see *Verified state*). That mission's notes and debrief live in
  `keel-factory/.ops/` inside the package. Bring back what the factory should learn.
- **Machine-wide guard: done 2026-10-14, on the manager's explicit yes.** The
  self-disarming hook from `OPERATOR.md` is merged into `~/.claude/settings.json`.
  Every other setting and hook event was verified unchanged, and `disableAllHooks` is not
  set. The original is backed up at `~/.claude/settings.json.before-keel-guard`; restore
  it to undo. The hook is inert wherever `$CLAUDE_PROJECT_DIR/keel-factory/` doesn't
  exist, which includes this factory. Its first live arming is the probe at the start of
  the first mission (`OPERATOR.md` → Infil).
- **Superseded by v1.0.0 (the SSD now gets a release folder):** backup to the SSD `S-USB` (`/Volumes/S-USB`, exFAT). `MANUAL.md` was written
  2026-10-15 for this backup. The copy waits on macOS privacy: VS Code had no
  Removable Volumes access, so every `ls` of the drive returned "Operation not
  permitted", in and out of the sandbox. Once access is granted:
  `rsync -a ~/Documents/KEEL-FACTORY/ /Volumes/S-USB/KEEL-FACTORY/`, then
  `diff -rq` to verify, then a copy of `MANUAL.md` at the drive root.
- **Kit is now linked into projects, not copied (2026-10-15, the manager's idea).**
  `harness/link_kit.py <project>` makes a real `keel-factory/` folder of symlinks to
  the master, plus a real `.ops/` for that project's notes. `--remove` deletes only
  links, and the script refuses any `keel-factory/` it didn't make.
  - Self-test: `harness/test_link_kit.py`, 9 tests, guard-through-links included.
    Three deliberately broken copies each failed it, and a real round trip left the
    master at 297 files.
  - Whole-folder `ln -s` was rejected for two reasons. `.ops` notes would land in the
    shared master. And `rm -rf keel-factory/`, with a trailing slash, can delete the
    master's contents.
  - Docs switched: OPERATOR, MANUAL, START-PROMPTS, QUICKSTART, README, harness/README.
  - Still copied, not linked: owner-mode setup copies skills into
    `.claude/skills/`, and those copies don't follow the master. Offered to the
    manager.
- **First real test drive: `~/Documents/case-platform`, 2026-10-15.** Run in
  operator mode from a session started in `~`, so the guard was not live and the rule
  was applied by hand. Results:
  - The project's own checks: pytest 1151 passed; ruff clean; mypy clean on 274 files
    with the kit excluded. The frontend was not checked, because there is no Node.
  - The real database was untouched, and no tracked file changed. Only
    `case-platform/keel-factory/.ops/debrief.md` remains, for the manager to read
    and delete.
  - Factory defects it found:
    1. `mypy .` walks the linked kit and stops on duplicate module names (the
       claude and codex copies), so it checks nothing. OPERATOR now says to exclude
       the kit from whole-tree checks.
    2. The armed guard blocks `.venv/bin/python`, because `.venv/` is gitignored.
       An operator could not run a Python project's checks. RESOLVED 2026-10-15
       by the manager: shell commands may use `.venv/bin/`, `venv/bin/` and
       `node_modules/.bin/`. The file tools stay strict there, secret names stay
       blocked, and paths are normalized first so `..` can't escape.
       - Guard self-test: 27 tests. Four deliberately broken copies failed it.
       - Rejected: per-project allowlist files (one more file in someone else's
         package), and asking the user to run the checks (slow).
    3. The guard arms only in the project the session starts in, so start the
       session inside the package. OPERATOR and MANUAL now say so.
  - Confirmed: `keel-factory/CLAUDE.md` loads automatically through the links,
    operator-mode gate first.
  - MANUAL.md gained a short version, a test-drive walkthrough, and a list of things
    to say. It stays generic on purpose: the manual travels into other people's
    packages, so no project's internals belong in it.
- **Guard hardening, offered not done** — follow symlinks to their target; check
  secret-shaped files inside a directory a Glob or Grep targets. Both gaps are written up
  under "What this does not cover" in `harness/DATA-BOUNDARY.md`. Owner: agent, if the
  manager wants it. Ungated.
- **Independent review of this session's work** — a fresh-context reviewer critiques
  `keel/framework/CREW.md`, `keel/skills/crew/`, and the directive-1 edits. Owner:
  agent, but spawning a reviewer needs the manager's explicit OK (the session's host
  rule: no subagents unless asked). Ungated otherwise. This was offered and not picked.
- **RECON dogfood on a real project** — gated: the manager must name an authorized
  target project.
- **A first real CREW run** — the only way to move CREW off Draft v0.1 (`CREW.md` §12).
  Gated on a genuinely parallel task in a real git project.

Deliberately **not** candidates: rewriting or adding to KEEL's five phases; copying
REA's 3,800 files in; building a heavy orchestrator (HELM stays thin); editing the
vendored `keel/skills-board/` bundles (see conventions).

---

## Orientation

`/Users/lambertike/Documents/KEEL-FACTORY/` is the **master copy**. It was not a git repo
until v1.0.0; it is now, tagged `v1.0.0`. Real projects receive a copy of it as `./keel-factory/`; those are the repos.

```text
KEEL-FACTORY/
├── ARCHITECTURE.md      # THE MAP. 8 sections; §3 now has Gap 4 (CREW)
├── CLAUDE.md            # copied into projects; HELM routing + standing rules,
│                        #   incl. "suggest, never ask blind" and the CREW tripwire
├── README.md · QUICKSTART.md · START-PROMPTS.md
├── keel/
│   ├── framework/       # DOCTRINE, CAPABILITIES, RECON, RULES, PHASES, TIERS, COST,
│   │                    #   LOOPS, THE-STACK, CREW (new), 4 cross-refs
│   ├── skills/          # helm, keel, keel-prove, crew (new: SKILL.md, assets/brief.md,
│   │                    #   scripts/check_lanes.py + scripts/test_check_lanes.py)
│   ├── skills-board/    # Miguel's 16 vendored skills, claude/ + codex/ — DO NOT EDIT
│   ├── capabilities/    # the two senses: reverse-engineering/, deep-research/
│   └── templates/       # artifact set (RECON.md, DESIGN.md, STATE.md, BRIEF.md, ...)
├── harness/             # ECC hooks (Node) incl. data-boundary-guard.js, DATA-BOUNDARY.md,
│                        #   settings.hooks*.json, 12 cited ECC skills under skills/
└── .scratch/            # handoff.md (this file), handoff-superseded-2026-10-14.md
```

Elsewhere: `/Users/lambertike/Documents/FRAMEWORK/` is the original KEEL v1.1 source
(not needed day to day). Cited-not-copied downloads: `~/Downloads/ECC-main`,
`~/Downloads/skills-main 2`, `~/Downloads/rea-main`.

---

## The task

Developing the factory against the manager's directives. This session resumed from the
previous handoff, verified it, got the three open questions answered, and built both
directives.

**Done:**

- Verified the previous handoff against disk. Four of its claims were wrong or
  incomplete; they are recorded under *Traps*.
- Open questions answered by the manager (each picked from offered options): team
  coordination lives in a new framework doc plus a new KEEL-owned skill that wraps
  `orchestrate-implementation` without editing it; "suggest, never ask blind" is a
  DOCTRINE §2 principle plus an always-on CLAUDE.md rule plus fixes at KEEL's own
  question points; the team discipline switches on by a CLAUDE.md tripwire, not
  always-on doctrine.
- **Directive 2 — CREW** (team coordination): `keel/framework/CREW.md` (Draft v0.1:
  one rule, "parallel thinking, single-threaded writing"; roles; lanes with exclusive
  write sets; the worker brief; the return; escalation; the LAND procedure; a map from
  each rule to the MAST failure modes; dated primary sources) and `keel/skills/crew/`
  (procedure, brief template, lane checker with self-test). Wired into CLAUDE.md
  (tripwire section), ARCHITECTURE §1/§3/§8, `LOOPS.md` §2 and `ECC-CROSSREF.md` §4.6
  (the LAND gap now points at `CREW.md` §9), `CAPABILITIES.md` (worktree and
  continuation affordances), `TASK-BOARD-CROSSREF.md` §5 (the wrap-don't-edit
  decision), the `keel` skill's Building section, and every skill list.
- **Directive 1 — suggest, never ask blind:** `DOCTRINE.md` §2 paragraph; CLAUDE.md
  section "When the user has to decide — suggest, never ask blind"; `keel` skill
  Interviewing overlay, stop-point summary, after-slice step; `PHASES.md` BRIEF rounds
  (all tiers), DESIGN least-confident list, SLICE step 7; `templates/DESIGN.md`;
  `RECON.md` step 6 and `templates/RECON.md` §5; HELM ("never ask cold");
  deep-research ("before a question goes to the user"); START-PROMPTS step 6;
  QUICKSTART §3; a dated amendment in `TASK-BOARD-CROSSREF.md` §3. The PHASES vs
  `task-interview` batching contradiction is settled: ask every question whose
  prerequisites are settled together; dependent ones wait for the next round.
- Six stale `capabilities/` descriptions (reverse-engineering only) now name both senses.
- **Python port of the data-boundary guard**: `harness/hooks/data-boundary-guard.py`
  keeps every rule, pattern, the allowlist, the override, the Bash tokenizer, and the
  block message of the `.js`, with three deliberate differences, each closing a way
  through: it reads all of stdin (the `.js` keeps 1 MiB), it fails closed on unparseable
  input and on its own errors, and it prints nothing on allow. Self-test beside it.

- **Guard wiring and Bash rule, per the manager's picks:** both settings templates now
  run `python3 /ABSOLUTE/PATH/TO/harness/hooks/data-boundary-guard.py`. The `.js` carries
  a header saying it is the never-executed Node original and listing its two
  differences. In Bash, a plain word now counts as a path only when a regular file by
  that name exists in the working directory. The starter prompts no longer say to stop
  when Node is missing; they say to wire and arm the Python guard anyway.

- **Made ready for an existing production codebase.** Setup never overwrites anything
  now:
  - QUICKSTART's copy command used a folder name that does not exist ("KEEL FACTORY"); it
    is now an `rsync` from `~/Documents/KEEL-FACTORY/` that leaves out `.git/`,
    `.scratch/` and `__pycache__/`.
  - A skill whose name is taken is skipped. Templates are copied with `cp -n`, and on an
    existing system only as each phase starts.
  - An existing `CLAUDE.md` gets one `@keel-factory/CLAUDE.md` import line instead of
    being replaced.
  - Hooks go in `settings.local.json`, and only those whose interpreter is installed.
  - `DATA-BOUNDARY.md` warns to unwire the guard before removing it.
- **Operator mode** (`OPERATOR.md`), at the manager's direction: *"be able to be plopped
  in and go Delta Force or MI6 on it … the secret weapon, in and out."* The package's own
  instructions are the mission and KEEL is the kit. It has four fixed rules of
  engagement, fast infil, the lightest tier that does the job well, and a footprint
  rule: everything KEEL keeps goes in `keel-factory/.ops/`. Exfil is a debrief plus a
  clean tree.
  - The guard uses a self-disarming hook form, so it leaves with the kit.
  - It's wired into `CLAUDE.md` (an operator-mode gate at the top), HELM ("whose project
    is this?"), `ARCHITECTURE.md` §2, `README.md`, `QUICKSTART.md` and `START-PROMPTS.md`.
  - It replaced a heavier "guarded trial" prompt that the manager rejected as too much
    ceremony.

**In progress:**

- Nothing mid-edit.

**Not started:**

- The independent review, RECON dogfood, and a first real CREW run (see *What is
  pending*).

---

## Open questions — must be resolved before proceeding

All three questions the previous handoff left open were answered by the manager this
session (see *The task → Done*). Two more came up while porting the guard, and both are
resolved:

- **Which guard do the settings templates wire?** RESOLVED 2026-10-14 by the manager:
  Python by default, with the `.js` kept as the Node original. Rejected: keeping `node`
  in the templates, because a machine without Node would then get no guard; and retiring
  the `.js`, because this folder has no version control to undo that.
- **How should the Bash rule treat plain words like `config` or `secret`?** RESOLVED
  2026-10-14 by the manager: check one only when a file by that name exists where the
  command runs. Rejected: keeping the `.js` behaviour, which blocks `git config user.name`
  and `grep -rn secret src/` and pushes people to the session-wide override; and ignoring
  plain words entirely, which misses `cat id_rsa` beside a real key.

Nothing is open now.

---

## Non-negotiable conventions

**Cite these by name, never by number. The numbering is local to this document and dies
when it is replaced.**

1. **Cited, not absorbed.** Outside sources (ECC, Miguel's Skills, REA) are referenced
   and curated, never bulk-copied. Avoids rot against upstream; it is the stated posture
   of every cross-ref.
2. **Reconcile, don't stack.** When something new overlaps something KEEL has, map or
   merge it — never run two systems for one job. Two sources of truth drift. Examples:
   the board replaced `SLICES.md`; CREW wraps `orchestrate-implementation`; the
   recommended-answer rule was restored as an overlay rather than a second interview
   mechanism.
3. **The vendored skills-board bundles are never edited.** `keel/skills-board/README.md`:
   the bundles are generated from an upstream authoring repo and local "edits … would be
   overwritten by the next publish"; claude/ and codex/ copies are byte-identical.
   Extend them with a KEEL-owned layer instead. Recorded in `TASK-BOARD-CROSSREF.md` §5.
4. **HELM stays thin.** A routing procedure, never an engine. A heavy orchestrator would
   be a second method competing with KEEL (`ARCHITECTURE.md` §2).
5. **The grounding rule.** Never write a step no real tool can execute; name the gap
   instead (`CAPABILITIES.md`).
6. **Evidence labels everywhere.** Evidence (ran it) / Inferred / Missing evidence.
   Researched or perceived facts stay Inferred until the system confirms them.
7. **The five KEEL phases are never renumbered or added to.** New disciplines (RECON,
   LOOPS, CREW) are placed around them. CREW's LAND is a step, not a phase.
8. **Prove a check can fail before trusting it (KEEL Rule 6b)** — applied to the
   factory's own scripts. The board validator and `check_lanes.py` were both proven in
   both directions.
9. **Suggest, never ask blind.** Every question to the manager carries two or three
   concrete options with a recommended pick (`DOCTRINE.md` §2; CLAUDE.md). The
   data-boundary question is the exception and keeps its strict yes/no shape on one
   named action. The manager is often on a phone: one-tap choices beat open questions.
10. **The perception capability is safety-bound.** Authorized targets only; read-only
    before anything that executes or mutates; ask first naming the exact target. REA's
    lawful-use boundary is adopted verbatim. Do not weaken this.
11. **Commit and PR attribution**, if this ever becomes a repo: use the model name the
    *current* session's system reminder gives (it has changed between sessions; this one
    said `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`). Never hardcode.

---

## Commands

All from `/Users/lambertike/Documents/KEEL-FACTORY` unless stated.

```bash
# What actually runs here (grounding rule):
python3 --version; command -v node || echo "node ABSENT"; git --version; rg --version | head -1

# Lane checker self-test (21 tests, incl. a round trip through a real git diff):
cd keel/skills/crew && PYTHONDONTWRITEBYTECODE=1 python3 -B scripts/test_check_lanes.py

# Data-boundary guard: self-test (22 tests) and the armed check from DATA-BOUNDARY.md:
PYTHONDONTWRITEBYTECODE=1 python3 -B harness/hooks/test_data_boundary_guard.py
echo '{"tool_input":{"file_path":"/path/to/some/.env"}}' | python3 harness/hooks/data-boundary-guard.py; echo "exit=$?"   # must be 2
echo '{"tool_input":{"file_path":"/path/to/some/normal/file.md"}}' | python3 harness/hooks/data-boundary-guard.py; echo "exit=$?"   # must be 0, silent

# Board validator and index on a board (build a scratch board outside the factory):
python3 -B keel/skills-board/claude/task-board-init/scripts/validate_board.py --board <BOARD_DIR>
python3 -B keel/skills-board/claude/task-board-init/scripts/generate_index.py --board <BOARD_DIR>

# Files changed since this handoff was written:
find . -type f -newer .scratch/handoff.md -not -path './.scratch/*' | sort
```

The relative-link checker is not saved in the repo. Re-derive it: walk every `*.md`
(skip `.scratch/`), skip fenced blocks and inline code spans, extract `[..](..)`
targets, skip `http(s)`/`mailto`/`#`, and check each resolves relative to its file's
directory. Last result: 200 links across 180 docs, 0 broken.

---

## Traps found the hard way

- **"Tasks carry owner, status, gate, blocked-by."** False for `owner`: ownership is
  only a prose `## Owner` body section, and an `owner:` frontmatter key fails
  validation with `frontmatter-unknown-key` (tested on a scratch board). CREW records
  ownership in the plan task's `## Lanes` table for this reason.
- **"task-interview already attaches a recommended answer to each question."** False.
  It only narrows to concrete choices after the user answers "whatever you think". The
  rule lived in `PHASES.md`, `THE-STACK.md`, and the `keel` skill's fallback path, and
  `PHASES.md` ("one numbered round") contradicted `task-interview` ("do not batch every
  question"). Both fixed this session.
- **Extending a vendored skill looked like the obvious home for new mechanics.** The
  bundle README says local edits are overwritten on the next publish. Found by reading
  `keel/skills-board/README.md` while weighing the options.
- **The prior-art list for team coordination was incomplete.** `LOOPS.md` §2 (LAND
  required, no procedure), `ECC-CROSSREF.md` §4.5–4.6, and
  `harness/skills/autonomous-loops/` were all relevant and unlisted. Found by grepping
  for subagent/parallel/worktree across the factory.
- **`python3 -I` breaks `generate_index.py`.** Isolated mode drops the script's own
  directory from `sys.path`, so `from validate_board import …` raises
  `ModuleNotFoundError`. Not a factory defect; use `-B` (no bytecode), not `-I`, for
  the factory's own scripts.
- **The host's safety check refuses `rm -rf "$VAR/…"`.** A variable that could expand
  to `/` is blocked. Use fresh directories, a literal absolute path, or `${VAR:?}`.
- **WebFetch returns extracted passages, not full text,** and does not follow
  cross-host redirects (`cognition.ai` → `cognition.com`). Never write "read in full"
  from a fetch; `CREW.md`'s Sources say what was actually read.
- **`${PIPESTATUS[0]}` is empty in this shell (zsh).** Use `$pipestatus`, or avoid a
  pipe when the exit code matters.
- **The safety classifier stops responses that drift into reverse-engineering framing**
  without the authorized-use posture up front. Lead with REA's lawful-analysis boundary
  and keep every mention bound to authorization and read-only-first.
- **Node is absent, and has been for four sessions.** No JS hook has ever run on this
  machine. Do not claim they work — hence the Python port.
- **A wired hook whose interpreter is missing does not block.** Claude Code treats any
  exit other than 0 or 2 as a non-blocking error and lets the call proceed. A missing
  `node` exits 127, so the JS guard wired here would guard nothing. Confirmed from the
  Claude Code hooks documentation on 2026-10-14.
- **The `.js` guard lets large calls through unchecked.** It keeps only the first 1 MiB
  of stdin. A bigger Write/Edit JSON fails to parse, which it treats as "no input", so
  it allows. Found by reading the source; not executed, because there is no Node. The port has
  a regression test for it.
- **The `.js` Bash rule blocks routine commands.** It treats every word that matches a
  secret pattern as a path, so `git config user.name`, `kubectl config get-contexts`,
  `npm config get registry`, `grep -rn secret src/` and `git commit -m fix-password-reset`
  are all blocked. This was observed by running the port while it still had the
  inherited rule. Narrowed in the Python version at the manager's call.
- **Setup used to assume a fresh project.** Copying `CLAUDE.md` "as-is", creating
  `.claude/settings.json`, and `cp -R` of the templates into `docs/` would each overwrite
  an existing repo's files. The templates include `README.md`, `DESIGN.md`,
  `DECISIONS.md` and `CONTEXT.md`. All fixed; found by reading the setup against a
  production repo's likely contents, then rehearsing it.
- **The guard and gitignore collide.** The guard blocks gitignored paths, so gitignoring
  `keel-factory/`, `.scratch/` or `docs/` locks KEEL out of its own files. The board
  skills suggest gitignoring the board, and Claude Code suggests gitignoring
  `.claude/worktrees/`, which also blocks CREW's fence there. The allowlist takes exact
  file paths only, not directories. Tested in a throwaway repo.
- **Adding a `CLAUDE.md` or `CLAUDE.local.md` to a repo that relies on `AGENTS.md` makes
  Claude Code stop reading `AGENTS.md`,** unless the new file imports `@AGENTS.md`.
  Source: the Claude Code memory docs, 2026-10-14.
- **`python3` exits 2 when its script is missing,** which Claude Code reads as a block. A
  guard wired in `settings.local.json` therefore bricks every tool call once the
  framework is gone, for example after switching back to a branch without it. The
  self-disarming form in `OPERATOR.md` tests for the script first, for exactly this
  reason. Verified by running it.
- **Git on this machine ignores `.claude/settings.local.json` globally**
  (`~/.config/git/ignore`, line 1). So an armed guard blocks an agent from editing its
  own local wiring, and the guard's message calls this "matches this repo's .gitignore"
  even though the rule is global. That is why the recommended home for the hook is
  `~/.claude/settings.json`.
- **The host refuses any `sh -c` script that runs a command it can't pin down,** such as
  `exec python3 "$g"`, even with no removal in it. Test the hook's pieces directly
  instead: check the string for exact equality, run the guard directly, and test the
  file check on its own.
- **The manager wants decisive operator behavior, not ceremony.** The rejected guarded
  trial stopped after every step and built nothing until approval. Keep the rules of
  engagement and cut everything else.
- **The host refuses `sh -c "$VAR"`.** Its safety check cannot inspect a script held in
  a variable, so it refused one, even though nothing was being removed. Run the command
  directly instead.
- **A long mutation run can exceed the 2-minute foreground limit.** Twelve suite runs of
  the guard took longer than 120 s and moved to the background. Expect it, and read the
  output file when the completion notice arrives.
- **Echoing the hook input to stdout, as the `.js` does, is not harmless** under Claude
  Code: stdout that is one JSON object is parsed as hook output, and output that fails
  validation is a non-blocking error. The port prints nothing on allow.
- **KEEL-FACTORY was not a git repo before v1.0.0.** Staleness used to be measured by
  file modification times. From v1.0.0 on, use `git log` and `git status`.

---

## Loose ends

| Item | State |
| --- | --- |
| Python data-boundary guard | done, proven, and the templates' default; the `.js` is kept as the unexecuted Node original |
| Guard hardening (symlinks, directory-wide searches) | offered, not done; gaps written up in `harness/DATA-BOUNDARY.md` |
| Wiring the guard live on this machine | not done: it changes security tooling, so it needs the manager's explicit yes for the exact settings file |
| Independent review of CREW + directive 1 | offered, not picked; needs the manager's OK to spawn a reviewer |
| RECON dogfood | needs the manager to name an authorized project |
| CREW promotion | Draft v0.1 until a real CREW run (`CREW.md` §12) |
| `THE-STACK.md`, `keel/HOW-TO-USE.md` say "recommended answer attached" | left on purpose: they describe provenance and agree with the new rule |
| Pre-existing markdownlint warnings (table pipes, a fence without a language) in older docs | untouched; not introduced this session |
| Harness hooks executing at all | blocked: Node absent |

---

## Verified state

Checked against disk immediately before writing (2026-10-14), not recalled:

- Tools: Python 3.13.13; Node absent; git 2.50.1; ripgrep 14.1.1.
- Board validator re-proven both directions on a scratch board outside the factory:
  clean board → exit 0 and the index generated; dangling `blocked-by` → exit 1 naming
  `references-resolve` and `folder-matches-frontmatter`; a plan task carrying a
  `## Lanes` table → exit 0.
- `check_lanes.py` self-test: 21 tests OK, including the git round trip (not skipped).
  Five deliberately broken copies of the checker each failed the suite.
- Relative links: 200 across 180 docs, 0 broken. Every new `§` reference points at an
  existing heading.
- Data-boundary guard (`harness/hooks/data-boundary-guard.py`): self-test 27 tests OK,
  gitignore cases included (they ran against a real `git init` repository rather than
  being skipped). Eleven deliberately broken copies each failed the suite, including one
  with the `.js`'s 1 MiB truncation put back and one with the `.js`'s broad Bash rule put
  back. Both settings templates parse as JSON and wire `data-boundary-guard.py`. The armed check in `DATA-BOUNDARY.md` exits 2
  on `.env` and exits 0 silently on a normal file. A full Claude Code PreToolUse payload
  reading `config/.env.local` was blocked, and `pytest -q tests/` was allowed. Imports:
  standard library only. The `.js` original: `node` exits 127 here (not installed).
- Operator rehearsal, in a throwaway package whose own README carried the mission:
  - The documented `rsync` dropped 291 files in. The hook JSON in `OPERATOR.md` parses,
    and its command equals the tested logic.
  - The guard blocked the probe and the package's gitignored `.env`, and allowed the
    package's files, `keel-factory/` and `keel-factory/.ops/`. With the script absent,
    the file test exits 0, so nothing is bricked.
  - The package's own test went from 1 failure to OK; the fix was committed on a mission
    branch by name.
  - `git status` showed only `?? keel-factory/`; the package's own files were
    byte-identical, and no `docs/` or `.scratch/` appeared.
  - Not executed: deleting the local `.claude/settings.local.json`, refused by the
    host's safety check.
- Earlier guarded-trial rehearsal, prompt since withdrawn; its non-destructive mechanics
  still apply (a throwaway repo standing in for production, with a team
  `CLAUDE.md`, `.claude/settings.json`, a team `commit` skill and `docs/README.md`):
  - The documented `rsync` copied 290 files with no `.scratch/`, no caches and no nested
    `.git`.
  - The team's `commit` skill was skipped, and the team's permissions survived the hook
    merge.
  - The guard blocked the probe and the team's gitignored `.env`, and allowed KEEL's
    framework, scratch and docs paths and the prompt's own git commands.
  - After one commit the tree was clean. Back on `main`, every team file was
    byte-identical, `keel-factory/` was gone, and no hook remained.
  - Not rehearsable outside a live session: the hook firing inside Claude Code itself.
    Step 5 of the prompt checks that.
- Created this session: `VERSION`, `RELEASES.md`, `.gitignore`, `harness/install_guard.py`, `harness/test_install_guard.py`, `harness/make_release.py`, `harness/link_kit.py`, `harness/test_link_kit.py`, `MANUAL.md`, `OPERATOR.md`, `keel/framework/CREW.md`, `keel/skills/crew/SKILL.md`,
  `keel/skills/crew/assets/brief.md`, `keel/skills/crew/scripts/check_lanes.py`,
  `keel/skills/crew/scripts/test_check_lanes.py`, `harness/hooks/data-boundary-guard.py`,
  `harness/hooks/test_data_boundary_guard.py`.
- Edited this session: `ARCHITECTURE.md`, `CLAUDE.md`, `QUICKSTART.md`, `README.md`,
  `START-PROMPTS.md`, `harness/DATA-BOUNDARY.md`, `harness/README.md`,
  `harness/settings.hooks.json`, `harness/settings.hooks.codex.json`,
  `harness/hooks/data-boundary-guard.js` (header comment only, no code change),
  `keel/README.md`, `keel/capabilities/deep-research/SKILL.md`,
  `keel/framework/{CAPABILITIES,DOCTRINE,ECC-CROSSREF,LOOPS,PHASES,RECON,TASK-BOARD-CROSSREF}.md`,
  `keel/skills/{helm,keel}/SKILL.md`, `keel/templates/{DESIGN,RECON}.md`.
- Vendored `keel/skills-board/`: 0 files touched. No `__pycache__` written.
- Status by evidence label: the lane checker is implemented and verified (command
  above); CREW as a practice and the directive-1 posture are specified only — neither
  has been exercised in a real session yet. Harness hooks: Missing evidence (Node
  absent).
