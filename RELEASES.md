# Releases

One section per release, newest first. A release is cut from `main` with
`harness/make_release.py`, which refuses to run on any other branch or without a section
here for the version in `VERSION`. How releases travel between machines is in section 11
of `MANUAL.md`.

Each section says what the release contains and, separately, how much of it is proven:
Evidence (a check was run and passed), Inferred (reasoned, not run), or Missing evidence.

---

## v1.1.0 — 2026-10-20

KEEL conformed to what Claude Code and Codex really do, built with KEEL itself (RECON →
BRIEF → CONTRACT → DESIGN → SLICE → PROVE, in checkpoint mode, on a task board, with
CREW runs). The plan and evidence are in the master's `.scratch/v1.1/` and
`keel/framework/HARNESS-PROBES.md`.

### What it contains

- **KEEL is a Claude Code plugin.** The master folder holds `.claude-plugin/plugin.json`
  (plugin `keel`, 18 skills: KEEL's six and twelve of the vendored board skills) and a
  marketplace entry. `harness/install_plugin.py` links it into `~/.claude/skills/keel`,
  where Claude Code loads it in place: edits to the master reach every project at the
  next session. The four Diataxis skills are opt-in (`--with-docs`), to keep the skill
  list short.
- **Codex gets the same skills** as links in `~/.agents/skills/` (`--codex`), listed by
  Codex as `keel:helm` and so on. `--codex` gives the skills only. The guard and the
  session hook need `--codex --codex-hooks`, which merges KEEL's two hooks, passing
  `--harness codex`, into `hooks.json` in the Codex home (`$CODEX_HOME` when it is set,
  else `~/.codex`), plus trusting both in `/hooks`. The Codex hook template no longer
  wires `config-protection.js` (it reads `tool_input.file_path`, and Codex edits through
  `apply_patch`) or `cost-tracker.js` (it parses Claude Code transcripts); both stay in
  `harness/settings.hooks.json` for Claude Code.
- **One hook script for both harnesses,** `harness/hooks/keel_hook.py`, with `session`
  and `guard` subcommands that take `--harness claude|codex`. At session start it
  injects the always-on layer, unless the project's own instruction files, as that
  harness loads them, already carry it. On every file-touching tool call it hands the
  call to the unchanged data-boundary guard, translating Codex's `apply_patch` into path
  checks. It blocks the direct ways of writing the guard's allowlist,
  `.keel/data-boundary-allow`, which only the user edits, even under the override: a
  tripwire, not a lock. A hand-wired bare guard has no such block. Both act
  only where KEEL is switched on: an entry named exactly `.keel` or `keel-factory` (a
  link or a copy of the kit) in the project's folder, or above it inside the same git
  repository. The master's own git checkout never switches on the folder that holds it
  (the exact rule is in `harness/README.md`).
- **One front door:** "Use KEEL: <what you want>". HELM decides owner or operator,
  records it in `.keel/keel.json` at the project root (never in `$HOME`, `/` or the
  kit), reads the always-on layer into that first session, proves the guard is live,
  and routes. In Codex owner mode it also adds the layer to the project's `AGENTS.md`,
  once. `keel` is no longer hidden from the model, and `keel`, `keel-prove` and `crew`
  switch KEEL on through HELM when it is off.
- **Stop modes** beside the tier: supervised, checkpoint (the default below PLATFORM) and
  unattended (`TIERS.md`, "Stop modes"). The phases are unchanged.
- **The PROVE reviewers are agents:** `agents/prove-standards.md`, `prove-spec.md`,
  `prove-gate.md`, called as `keel:prove-*`; PROVE always runs through `keel-prove`. At
  SPRINT it spawns Standards and Spec, and the builder may run the gate's commands, which
  the report then says.
- **The always-on layer** (`CLAUDE.md`) went from 12,773 to 5,595 characters; the detail
  lives in the skills.
- **An eval suite** (`evals/`, three cases with a no-plugin baseline) for
  `claude plugin eval`.
- **`harness/check_kit.py`**, KEEL's own check of the plugin, the Codex skill set, the
  agents, the evals, the always-on sizes, skill paths, the release record and every
  link. It reads the skill lists and the always-on mark from the installer and the hook,
  so each fact has one source. `make_release.py` now runs it and every self-test,
  the v1.1 ones included, from the fresh clone, and refuses to cut a release off `main`.
- **Documents:** a dated, evidence-labeled harness table in `CAPABILITIES.md`; the probe
  log `HARNESS-PROBES.md`; harness facts for unattended runs in `LOOPS.md` §6; how each
  harness asks questions in `DOCTRINE.md` §2; CREW's first field record. Fixed: `TIERS.md`
  said "these six" over seven items; `RULES.md` was titled "Five" over six rules.

### Upgrading from v1.0

- A project that copied v1.0's `CLAUDE.md` (it says "This project was started from KEEL
  FACTORY.") gets the session header plus a one-line note instead of a second layer.
  With a linked `keel-factory/`, replace that copy with the import line
  `@keel-factory/CLAUDE.md`. Under the plugin, with no `keel-factory/` in the project,
  delete KEEL's v1.0 text (the hook then supplies the layer), or replace it with v1.1's
  `CLAUDE.md`. The note offers the import only where `keel-factory/CLAUDE.md` exists and
  holds the always-on mark. In Codex, which has no imports, delete it, or replace it
  with the v1.1 layer as one block that opens with its mark line.
- A project holding a copied v1.0 `keel-factory/` re-copies it with MANUAL §4's rsync,
  or replaces it with a link (`link_kit.py`); until then its import carries v1.0's layer
  beside the hook's v1.1 layer. The session hook does not yet notice this layout and say
  so (a follow-on).
- On a machine with v1.0's machine-wide guard: with the plugin, that hook is optional,
  and `python3 harness/install_guard.py --remove` takes out only KEEL's entry. To keep
  it, re-run `harness/install_guard.py` from the master. It updates that entry in place,
  adding the exact-name test for `keel-factory` and repointing it at the master's own
  guard; v1.0's entry ran the project's copy.

### Proven — Evidence

Test counts measured on the release tree with each self-test's own runner; each count of
broken copies is a mutation run in which the unbroken script passed first, on the same
kit (the lead's gates, `.scratch/task_board/crew-plan-prove-fixes.md`, execution log:
"Fix round 4, phase A — landed" for the hook script, "Fix round 3, phase A — landed" for
the rest).

| What | How |
| --- | --- |
| Hook script | `harness/hooks/test_keel_hook.py`, 108 tests, hostile role files and padded Codex patch headers among them. 93 deliberately broken copies each failed it. |
| Installer | `harness/test_install_plugin.py`, 30 tests, temporary homes only. 27 broken copies each failed it. |
| Machine-wide guard installer | `harness/test_install_guard.py`, 18 tests, against temporary settings files and temporary projects. 18 broken copies each failed it, so R4 has now been seen failing. |
| Kit check | `harness/test_check_kit.py`, 34 tests, one break per rule. 36 broken copies of the checker each failed it. `check_kit.py` on the master: clean. |
| Release script | `harness/test_make_release.py`, 14 tests, in temporary git repositories only. 25 broken copies each failed it. |
| v1.0 self-tests | Still green: guard 27, link 9, lane checker 21. |
| Plugin manifest | `claude plugin validate` passes; its one warning (a root `CLAUDE.md` is not loaded by a plugin) is expected. `claude plugin details keel@skills-dir`: 18 skills, 3 agents, 2 hooks. Its always-on estimate depends on the config: ~1,953 tokens in a fresh config holding only the plugin, ~2,530 in the build machine's own (probe P14). It counts the hooks as costing no context, but in a KEEL project the SessionStart injection comes on top: 6,029 characters by `check_kit.py`, and 5,918 characters of context seen live in L8 (6,132 bytes of hook output, JSON-escaped), run 2026-10-18, before fix rounds 3 and 4, and docs round 5, changed `CLAUDE.md`. |
| Live, Claude Code 2.1.170 | L1–L8 in `HARNESS-PROBES.md`. The plugin loads from the link; the session layer arrives only where `.keel/` exists; the guard blocks `.env` there and not elsewhere; "Use KEEL:" alone fires HELM, records the role and probes the guard; checkpoint mode stops once up front and once at PROVE, building test-first between; `keel-prove` spawns the three reviewer agents, which found two defects the builder's own review had missed; in someone else's package (L7) it records the operator role, probes the guard, keeps the package's rules and leaves a labeled debrief in `.keel/ops/`. After the PROVE fixes (L8), a `general-purpose` and an `Explore` subagent each had their Read of `.env` blocked by the plugin's hook, so the guard covers subagents, `Explore` included, which does not load `CLAUDE.md`. |
| Codex 0.138 | Probes X1–X10, all without a model call: repo and user skills listed, links followed, KEEL's 17 implicit skills listed as `keel:<name>`, `AGENTS.md` injected, hooks present and trust-gated; `codex plugin` has `add`, `list`, `marketplace` and `remove`, and no eval command (X10). |
| Release tree, Claude Code 2.1.304 | Re-run on 2026-10-20 on v1.1's own tree, built apart from the michaelshimeles/skills work that shares the master and loaded with `claude --plugin-dir` (`HARNESS-PROBES.md`, "Release-tree re-runs"). The 261 self-tests above pass. Each mutation list passed its unbroken script first, then failed every broken copy: 93, 27, 18, 36 and 25. `check_kit.py`: clean. `claude plugin details`: 18 skills, 3 agents, 2 hooks, ~1,953 tokens always-on in a fresh config (P14). L8: the session asked the data-boundary question first; on a yes, both subagents' Reads of `.env` were blocked, the fake value reached neither trace, and the session hook injected 6,161 characters of context. Codex 0.138 lists the same 17 `keel:` skills (X9). |

### Written, not yet proven in use — Inferred

- The SessionStart injection's token cost: about 1,510 tokens, from `check_kit.py`'s
  6,029 characters at four characters a token; no run has counted it in tokens.
- Codex's session hook injecting the layer: the template and installer are written to
  the Codex docs (0.163); no Codex session has run it (needs `/hooks` trust and a Codex
  model call).
- HELM's switch-on as v1.1 rewrote it: reading the layer at switch-on, the Codex
  `AGENTS.md` block, refusing `$HOME`, `/` and the kit, the warning when `.keel/` is
  gitignored (checked before the role file is written), and the allowlist checks,
  nested `.keel/` folders included. Written, not yet run live.
- The unattended stop mode: specified in `TIERS.md` and `LOOPS.md` §6; no unattended run
  yet.
- A marketplace install (`claude plugin install keel@keel-factory`): validated and
  probed with a scratch config, not used day to day.

### Known gaps — Missing evidence

- The Codex guard: no Codex session has yet been seen blocking. It needs
  `--codex --codex-hooks`, trusting the hooks in `/hooks`, and a Codex model call to
  prove (`CAPABILITIES.md`). In Codex every file read is a shell command, so the guard
  sees it only as Bash and covers it only through its Bash heuristic: a blocked probe
  shows the hook is wired, not that reads are covered. That is Inferred from the Codex
  docs read 2026-10-18, which name no read tool (`harness/DATA-BOUNDARY.md`, "What this
  does not cover").
- MultiEdit: the plugin's matcher names it, but no run has shown a MultiEdit call
  reaching the guard.
- MCP tools: neither hook's matcher names them, so an MCP tool that takes a local path
  should never reach the guard; no run has checked it (`harness/DATA-BOUNDARY.md`, "What
  this does not cover").
- Claude Code's Monitor tool, and PowerShell on Windows, run shell commands that the
  matcher does not name, so the guard never sees them (Inferred from the matcher). No
  run has checked it; changing the matcher needs the manager's contract change (a
  follow-on).
- The gitignore rule asks git in the repository nearest the file: outside git no
  `.gitignore` applies, and a separate repository inside a gitignored folder is judged
  only by its own rules. Nothing in code widens it yet (a follow-on); secret-shaped
  names stay blocked in both (`harness/DATA-BOUNDARY.md`, "What this does not cover").
- An allowlist that comes with a repository: the guard honors a committed
  `.keel/data-boundary-allow` in every clone, and nothing in code stops that yet (a
  follow-on). The guard honors a `.keel/data-boundary-allow` at the nearest git root of
  each path, so a submodule or a nested clone can bring its own; HELM's switch-on check
  lists every `.keel/` folder below the root as well. That check, and `OPERATOR.md`'s
  infil, are all that stand in front of it (Inferred: written, not yet run live).
- Windows: nothing in KEEL has run on it
  ([`CAPABILITIES.md`](keel/framework/CAPABILITIES.md#windows-untested), "Windows:
  untested").
- The eval suite has run once: 2026-10-20, Claude Code 2.1.304, on the release tree
  (`HARNESS-PROBES.md`, "Release-tree re-runs"), three runs a case with the plugin and
  three without. `operator-job` scored 1.00 (0.89 without the plugin).
  `complete-description` scored 0.67 (0.33 without): with the plugin every reply raised
  the production concerns the case looks for and no baseline reply did, but the judge
  failed the question round in all six replies, and no run wrote `docs/BRIEF.md` or
  named the STANDARD tier. `vague-idea` scored 0.33 (0.50 without): HELM fired in every
  run, but none wrote `.keel/keel.json` or stated a tier, and the judge failed the
  question round in all six replies. A fourth `vague-idea` run, alone, did all of that
  and scored 1.00. Why the three fell short is not known (Missing evidence); three runs
  a case cannot tell a defect from run-to-run variation.
- On 2.1.170 a hook cannot be told to fail closed (`onFailure` arrives in 2.1.295).
  `keel_hook.py` blocks on its own errors where KEEL is on; a missing `python3` and a
  hook timeout still fail open. Two routes reach the timeout: a command with tens of
  thousands of path-shaped words (`harness/DATA-BOUNDARY.md`, K36), and an allowlist
  linked to a device or a pipe, which stalls every guarded call in its repository; an
  instruction file linked that way stalls the session hook instead. Both wait on
  `keel-hook-hardening` item 9.
- The three ECC Node hooks still have never run (no Node).
- PROVE approved this release on 2026-10-20 with four of its nine must-haves met and
  five named PARTIAL: M2, one front door (a dry run on 2.1.304 ran HELM end to end; the
  probe-order fix it led to has not run live since); M3, stop modes (SPRINT, below); M5,
  the eval suite (above); M7, Codex (the skills are listed; no Codex session has run the
  hooks); M9, `CAPABILITIES.md` (one claim in the row on when new wiring arms has no
  source).
- Checkpoint mode at SPRINT: the dry run asked no question and stopped only at PROVE,
  while `TIERS.md`'s stop-mode table and the `keel` skill promise an up-front round in
  checkpoint mode. The manager chose one up-front round at every tier; `TIERS.md`, the
  `keel` skill and `PHASES.md` change after 1.1.0.
- Fourteen small text items the last closure check found, none of which changes what
  KEEL does, are fixed after 1.1.0:
  - HELM: step 3(a) names the copy's installer as the fallback, then forbids running
    it, with no alternative; 3(d) sends the user to the wrong folder when the blocked
    check is the (c) listing; the wider listing surfaces nested `.keel` links that can
    point outside the project, and (c) says to read through them; the gloss on "File
    does not exist" names only Claude Code's Read reply.
  - `harness/DATA-BOUNDARY.md`: the listing still misses a nested allowlist reached
    through a linked folder, which the guard honors.
  - `CAPABILITIES.md`: the row on when new wiring arms states the plugin's next-session
    loading without a source, and leaves out `/reload-plugins`.
  - `MANUAL.md`: deleting KEEL's v1.0 text from `AGENTS.md` is gated on the guard
    probe, but relies on the SessionStart hook, which is trusted separately.
  - `OPERATOR.md`: its probe lacks HELM's clause to probe again; one line of its infil
    runs to 138 characters; S8 still sends the user to the ignored root folder when the
    nested listing is the blocked check.
  - This section: "Both wait on item 9" reads as covering the K36 route, which is item
    8; the 6,029-character session figure includes the kit's path, so it varies by
    machine (6,118 in the release tree's check).
  - Two in v1.1's build records (`.scratch/v1.1/CONTRACT.md`): a reading of D5 recorded
    as an entry, though it narrows D5; a note that says five in all, in a block of six.

### Fixed after PROVE pass 1

The first PROVE pass (`.scratch/v1.1/PROVE-FINDINGS.md`) refuted no finding. What changed,
by finding id:

- Evidence (a self-test, a live run, or a recorded check):
  - P10, WALKTHROUGH-1, COMPLETENESS-2, COMPLETENESS-3: the switch-on rule finds the git
    root first, compares names exactly, checks only the start folder outside git, never
    counts `$HOME`, `/` or the master's own git checkout (narrowed after pass 2: N2,
    below), and lets a worktree check its main checkout.
  - P5, COMPLETENESS-4: the session hook's carry check is per harness, and a v1.0 copy
    gets an upgrade note instead of a second layer (both refined after pass 2: N36, N3).
  - COMPLETENESS-6: the hook blocks the direct ways of writing
    `.keel/data-boundary-allow`, even under the override, and `CLAUDE.md` says so. It is
    a tripwire, not a lock (N34, below).
  - S4, S5, S6, P12: `check_kit.py` reads the skill lists and the mark from their one
    source, gains the `source` and `skill-set` rules, covers all 22 Codex skills and
    checks bare `agents/` and `harness/` paths.
  - H3, G1: `install_guard.py`'s command tests the exact name and updates a v1.0 entry
    in place; R4 has been seen failing. After pass 2 it also runs the master's own guard
    (N37, below).
  - COMPLETENESS-11, COMPLETENESS-12: `--codex-hooks` honors `$CODEX_HOME`, shell-quotes
    the kit path and reports a refused link clearly.
  - WALKTHROUGH-11: `make_release.py` refuses to run off `main`.
  - COMPLETENESS-9: L8, the guard on subagent tool calls.
  - WALKTHROUGH-5: `harness/DATA-BOUNDARY.md` gains an armed check that runs the wired
    hook command itself, run on every wiring form; the `/ABSOLUTE/PATH/TO/` instruction
    now names the kit root. After pass 2 the check runs in the real project and needs
    the BLOCKED reason as well as exit 2 (N2, below).
- Inferred (written, not run live):
  - P1, P4, S3, COMPLETENESS-1, COMPLETENESS-5, COMPLETENESS-7, COMPLETENESS-8: HELM
    reads the layer at switch-on, adds the Codex `AGENTS.md` block, refuses `$HOME`, `/`
    and the kit, warns when `.keel/` is gitignored, uses `<ops>` for notes, handoff and
    debrief, and no longer claims to hold no state; `keel`, `keel-prove` and `crew`
    switch KEEL on through it.
  - WALKTHROUGH-3: a copied skill resolves the kit's paths under `keel-factory/`
    (narrowed after pass 2: N25, below).
  - COMPLETENESS-14: at SPRINT the gate's commands may be run by the builder, and the
    report says so.
  - COMPLETENESS-15: reading the KEEL kit itself is an explicit exception in the
    data-boundary rule, beside the guard probe, and the secret and gitignore items still
    apply inside it. The manager approved it as an exception (P-B, below).
  - P6: the guard-probe exception is recorded.
- Documents:
  - WALKTHROUGH-2, S9: the Codex one-liner gives skills only, in `START-PROMPTS.md`,
    `OPERATOR.md`, `README.md`, `QUICKSTART.md` and `MANUAL.md`; START-PROMPTS' Codex
    text matches the v1.1 template.
  - WALKTHROUGH-6: the broken code fence in `START-PROMPTS.md`.
  - WALKTHROUGH-7: `OPERATOR.md`'s failed-probe step matches HELM's; `MANUAL.md` §5
    leads with the plugin.
  - WALKTHROUGH-4, WALKTHROUGH-8, WALKTHROUGH-9, S1: `MANUAL.md`'s restore commands, its
    folder table and the removable-media advice; no document calls one mode the usual
    one; README's size claim.
  - S7, S8, S10, S11, P13, G2, COMPLETENESS-10, COMPLETENESS-13: `LOOPS.md` cites
    shipped sources, the agent briefs carry data-boundary item 3, long lines are
    rewrapped, the dropped Codex hooks are recorded, the Codex guard is filed under
    Missing evidence, both context figures are given, and `TIERS.md` covers Codex's
    Default mode; `CAPABILITIES.md` says Windows is untested.
  - S2, P2, P3, P7, P9, P11, P12b: `check_links.py` is gone, and the contract's
    amendments record the rest (`.scratch/v1.1/CONTRACT.md`).

### Fixed after PROVE pass 2

The second PROVE pass (`.scratch/v1.1/PROVE-2.md`) verified 60 items and refuted none;
three were distinct major defects. Fix round 3 took the fix-now and docs-only items
(`.scratch/task_board/crew-plan-prove-fixes.md`, Open questions 16 to 19 and the
execution log). What changed, by finding id:

- The three major defects (Evidence: the self-tests and broken copies in the table above,
  and the end-to-end runs the execution log records):
  - N2 = N35: a `keel-factory` entry is skipped only when it is the master's own git
    checkout. A copy made with MANUAL §4's rsync (no `.git`) switches KEEL on; a copy
    that keeps `.git` (a `git clone`, `cp -R` or a Finder copy) counts as a master's own
    checkout and stays dormant when its own hooks run. The rsync copy, wired from its own
    hooks, blocks `.env` and injects the layer; the master, seen from the folder that
    holds it, stays dormant. The armed check in `harness/DATA-BOUNDARY.md` now runs the
    wired command in the real project, sets `CLAUDE_PLUGIN_ROOT` only for
    `plugin-hooks.json`, and needs the BLOCKED reason as well as exit 2.
  - N36 with N3: a file carries the layer through an import only when it has an import
    line `@keel-factory/CLAUDE.md` that resolves to a file holding the mark; a prose
    mention or a dangling import never counts. The v1.0 upgrade note offers the import
    only where `keel-factory/CLAUDE.md` exists and holds the mark, and otherwise says to
    delete or replace the v1.0 text.
  - N37: `install_guard.py`'s command runs the installing master's guard by its
    absolute, shell-quoted path, never the project's copy, and a re-run repoints an
    older entry. `OPERATOR.md` shows the master's path as a placeholder.
- Evidence (a self-test, a mutation run, or a recorded check):
  - N43: `install_plugin.py --codex` warns when one of KEEL's own six skills is skipped
    because its name is taken.
  - N44: a second `--codex-hooks` run no longer saves KEEL's own hooks as the original
    `hooks.json`.
  - N11: README-FIRST checks the checksums first, then clones with `--branch main` into
    your own local path, never the drive; `MANUAL.md` §3 matches it.
  - The armed-check recipe, run as printed under zsh and sh on every wiring form, with
    the cases that must fail (`harness/DATA-BOUNDARY.md`, the dated record).
- Inferred (written, not run live):
  - N23 = N28, N26: in operator mode, `keel` follows `OPERATOR.md` instead of its
    phases, and `keel-prove`'s and `crew`'s records go to `<ops>`.
  - N25, N30: in all six of KEEL's skills, a copied skill reads every `../` path under
    `keel-factory/keel/`, and root files under `keel-factory/`, even when the project has
    a file of that name.
  - N24: HELM's gitignore warning names the way out, for an owner and in operator mode.
  - N9, N14: HELM and `MANUAL.md` say the guard arms only where KEEL's hooks run.
  - N33, the switch-on half: HELM's switch-on and `OPERATOR.md`'s infil look for an
    allowlist that came with the repository and show it; in operator mode they stop to
    ask.
- Documents:
  - P-B: reading the KEEL kit itself is a second named exception in `CLAUDE.md`,
    beside the guard probe, as the manager chose; item 3 is back to its approved
    wording, and the other documents point at the exception.
  - N4, N34, N5: `CLAUDE.md`, `README.md`, `harness/README.md` and
    `harness/DATA-BOUNDARY.md` say KEEL's hook blocks the direct ways of writing the
    allowlist, a tripwire, not a lock, and that a hand-wired bare guard does not.
  - N32: `OPERATOR.md` §3 and `MANUAL.md` §10 warn that `git clean -fd` and
    `git stash -u` remove an untracked `.keel/` or `keel-factory/`, switching KEEL off.
  - N33: never commit `.keel/data-boundary-allow`; stage `.keel/keel.json` by name.
  - N38: the allowlist works only inside a git repository.
  - N39: no hook matches MCP tools (`harness/DATA-BOUNDARY.md`, `README.md`).
  - N41: START-PROMPTS' Claude Code prompt never opens an existing
    `.claude/settings.local.json`.
  - N45: QUICKSTART makes the new project's folder before linking the kit.
  - N8, N22, N40: the always-on figure gives both measurements and their conditions
    (probe P14); L8 records 5,918 characters of context; probe X10 is recorded.
  - N13, N29, N15: `CAPABILITIES.md` labels hooks in subagents Evidence (L8) and says
    the captured Codex prompts do not ship with the kit.
  - N16 to N19 and the docs-only spec:* items: the contract and acceptance records
    (`.scratch/v1.1/CONTRACT.md`, `.scratch/v1.1/ACCEPTANCE.md`).
  - std:selftest-line, std:mutate_hook, std:mutate-doc: both installers' docstrings name
    their self-test; the superseded hook-only mutation runner is gone, and the generic
    runner's docstring says what it copies.
- Not in this release: the follow-ons N1, N6, N7, N21 = N27, N31, N42 and
  std:hook-cmd-dup, the code halves of N5, N32, N33, N34 and N39, and N33's role
  sub-claim. Seven items were rejected, each with its reason (`PROVE-2.md`,
  "Dispositions recorded in fix round 3").

### Fixed after PROVE pass 3

The third PROVE pass (`.scratch/v1.1/PROVE-3.md`) verified 49 items and refuted none;
none was major after verification. Fix round 4 took its 5 fix-now and 28 docs-only items
(`.scratch/task_board/crew-plan-prove-fixes.md`, Open question 20 and the execution log).
What changed, by finding id:

- The fix-now items in the hook (Evidence: `harness/hooks/test_keel_hook.py`, 108 tests,
  and 93 broken copies each failing it, the identity baseline green first; the execution
  log, "Fix round 4, phase A — landed"):
  - K30: the hook now fails closed on a hostile role file. `.keel/keel.json` is opened
    without waiting and read only as a regular file of at most 64 KiB, so a named pipe, a
    link to a device, a file past the cap or JSON nested too deep reads as "not
    recorded", and KEEL stays on. The guard decides whether KEEL is on inside its
    fail-closed `try`: an error after a `.keel` or `keel-factory` entry was met blocks the
    call, and one before any such entry allows it, so no other project is touched.
  - K31: the hook now fails closed on padded patch headers. The Codex `apply_patch`
    adapter strips each line first, as Codex's parser does, and catches a header wherever
    it sits. Any other line that starts with `***` blocks the patch, except the frame,
    `Environment ID` and a space-led context line inside an `Update File` hunk; another
    tool's command that starts as a patch is also checked as it stands.
- The fix-now items in HELM and the skills (Inferred: written, not run live):
  - C14: HELM runs `git check-ignore -q .keel/keel.json` before writing the file, while
    KEEL is still off, so the guard it is about to arm cannot block the check. In HELM
    and `OPERATOR.md`, a check the guard blocks as gitignored is now the answer, never
    retried another way.
  - C15: `keel`, `keel-prove` and `crew` count the linked-kit route (no role recorded,
    and the project's own instructions are not KEEL's) as operator mode, and run HELM's
    switch-on when a `.keel/` holds no `keel.json`.
  - K20: HELM adds no Codex block to an `AGENTS.md` that holds KEEL's v1.0 text; it
    offers MANUAL §11's choice and changes the file only on the owner's yes.
- HELM's half of the follow-on K34 (Inferred: written, not run live): HELM loads the
  layer unless its Data boundary section is in context; the session note alone does not
  count.
- Documents, the limits now named (Inferred where they describe untested behavior, as
  each document labels it):
  - K32 (Codex reads), K18 (the gitignore rule's scope), K29 (Monitor and PowerShell)
    and K19 (nested allowlists): "Known gaps" above, `harness/DATA-BOUNDARY.md`,
    `harness/README.md`, `CAPABILITIES.md`, `README.md` and `MANUAL.md`. HELM's
    switch-on and `OPERATOR.md`'s infil list every `.keel/` folder below the root too.
  - K36: a long shell command can outlast the hook's timeout, which lets the call
    through (`harness/DATA-BOUNDARY.md`).
  - C4 (the Codex installer run from a copy), K26 (when new wiring arms) and K35 (a
    `.keel` that is not a folder): HELM and `OPERATOR.md`; C4 also in START-PROMPTS and
    `harness/DATA-BOUNDARY.md`.
  - C2 (which copy switches on): N2 = N35 above, `README.md`, MANUAL §4, START-PROMPTS
    and `harness/README.md`.
  - C1 (a copied v1.0 kit): "Upgrading from v1.0" above and MANUAL §11.
  - C3's documents (an import through a linked kit may ask the user first): a
    `CAPABILITIES.md` row and a MANUAL §10 entry, Inferred from Claude Code's memory
    documentation.
  - C8: the armed check in `harness/DATA-BOUNDARY.md` prints the hook's matcher too.
- Documents, wiring and names:
  - K23: hand-wiring goes into `.claude/settings.local.json` or `~/.claude/settings.json`,
    never the shared `.claude/settings.json`.
  - K21: START-PROMPTS' Codex prompt no longer wires KEEL's two hooks a second time
    beside `block-no-verify.js`.
  - K22: `CLAUDE.md` and START-PROMPTS name a copied skill `$helm` in Codex.
  - K25: HELM and `OPERATOR.md` now say "`<ops>` is `keel-factory/.ops/` whenever the
    project holds a `keel-factory/` (linked or copied), else `.keel/ops/`", and the
    hook's operator note agrees. That rewords D2's rule for operator notes, so the
    contract records it as proposed to the manager (F4-8).
  - K28, C7: MANUAL §10's "You moved the master", and what the agent does before a
    `git clean`, by whose project it is.
- Documents, the records:
  - C5, K27: `CAPABILITIES.md`'s legend reaches P14 and its `keel:*` row gives 18 loaded,
    17 listed; `HARNESS-PROBES.md`'s preamble names P14's exception.
  - S-c1: the contract's §2 Codex-names row carries a dated stale note (probe X9).
  - S-a1, C11: the manager approved F3-7's reading of D7 and the 8,000-character
    listing bound (`.scratch/v1.1/CONTRACT.md`, "Approved at the PROVE pass 3 report").
  - S-c2, C12: F3-1, F3-2, F3-4 and F3-6 reword approved decisions, so they go to the
    manager again at the PROVE pass 4 report, with F4-8 ("Proposed, awaiting the
    manager"). Round 4's other changes to decisions are F4-1 to F4-7.
  - C9, C17, C13, T9: PROVE-2's coverage sentence is corrected; the crew plan's
    superseded decisions point at what replaced them; ACCEPTANCE's re-measure is in the
    past tense and TRACEABILITY cites L8; the scope of a `.scratch/v1.1/` commit is the
    manager's call (`.scratch/v1.1/STATE.md`).
- Not in this release: the follow-ons C3's probe, K34's hook half, S-b5, T1 and T7, and
  the code halves of C1, C4, K18, K19, K20, K28, K29, K32 and K36, all board tasks; C10,
  the stale handoff, closes with a new handoff at the PROVE pass 4 stop. Ten items were
  rejected, each with its reason (`PROVE-3.md`, "Dispositions recorded in fix round 4").

### Fixed after PROVE pass 4

The fourth PROVE pass (`.scratch/v1.1/PROVE-4.md`) verified 27 items and refuted none;
none was major or fix-now. Docs round 5 took its 20 docs-only items and changed no script
and no test (`.scratch/task_board/crew-plan-prove-fixes.md`, Open questions 21 and 22).
What changed, by finding id:

- The data boundary's limits, now named:
  - D1: "Known gaps" above and `harness/README.md` name a hook timeout, beside a missing
    `python3`, as a way the hook fails open. An allowlist linked to a device stalls every
    guarded call in its repository, and a linked instruction file stalls the session
    hook (Evidence: D1's verifier, temp projects; the outcome at the real timeout is
    Inferred).
  - D8, D9: HELM, `OPERATOR.md`'s infil and `harness/DATA-BOUNDARY.md` list nested
    `.keel` entries with `find . -path ./keel-factory -prune -o -name .keel -print`, so
    a symlinked `.keel` is listed too. Where `.keel/` or `keel-factory` is gitignored,
    the guard blocks that listing, and the block is handled like any other blocked check
    (Evidence: the lead's probe in three scratch projects, 2026-10-20).
  - D15, P-K23: MANUAL §10 says an allowlist entry is relative to the root of the git
    repository that holds the file, and its "can't open file" entry is reworded.
- Wiring and switch-on (Inferred: written, not run live):
  - D4: HELM, `OPERATOR.md` and START-PROMPTS say that all of KEEL's installers write
    machine-wide entries that run the kit they were run from, so they run from the
    master. `OPERATOR.md`'s `$KEEL` now names the master.
  - D17: in Claude Code, a settings-file hook also arms once `/hooks` is opened, and the
    plugin only from the next session (HELM, `OPERATOR.md` and a `CAPABILITIES.md` row).
  - D16: `OPERATOR.md`'s sentence on a `.keel` that is not a folder applies only under
    the plugin, with no `keel-factory/`.
  - D5: HELM step 4 and MANUAL §11 offer deleting KEEL's v1.0 text from `AGENTS.md`, and
    relying on the hook, only where KEEL's Codex hooks are wired and trusted.
  - P-K34, the layer's half: `CLAUDE.md` says the session note is the SessionStart
    hook's context, never text in a project file. The layer is now 5,595 characters
    (Evidence: `check_kit.py`).
  - D7: crew's worker brief carries a "KEEL role" line.
  - T4-7: the Codex hook template's description says ECC's check needs Node.js.
- Records:
  - D2: `harness/README.md` gives the hook's self-test as 108 tests and 93 broken copies.
  - D11, P-C5: `HARNESS-PROBES.md`'s L8 row and its preamble.
  - D18: the phase-5 row of `.scratch/v1.1/STATE.md`.
  - D19: ACCEPTANCE's R9 seen-failing row cites PROVE pass 3's arming record.
  - D6: `keel-hook-hardening` item 5 restates K19's code half as its verifiers designed
    it.
  - S4-c, S4-a2: the manager approved F3-1 (with its third residual), F3-2, F3-3, F3-4,
    F3-6 and F4-8 on 2026-10-20. `.scratch/v1.1/CONTRACT.md` records them as approved,
    and D5 gains a dated pointer line.
- Not in this release: the follow-ons D3, P-K28 and P-K32, and the code halves of D1
  (`keel-hook-hardening` item 9), D4 (`installer-hooks-json-robustness` item 3) and D8
  (`keel-hook-hardening` item 5), all board tasks. M2, M3, M5 and M7 stay PARTIAL by the
  manager's choice, since they need runs only the manager can approve. Four items were
  rejected, each with its reason (`PROVE-4.md`, "After the report").

---

## v1.0.0 — 2026-10-15

The first versioned release. It's meant to be carried to another machine and used on
real projects from there.

### What it contains

- **KEEL:** the five phases, three tiers, and six rules, plus RECON, the doctrine, the
  grounding rule (`CAPABILITIES.md`), LOOPS, and CREW (several agents on one project).
- **HELM,** the router every session starts with, and **operator mode**
  (`OPERATOR.md`): the drop-in protocol for someone else's package.
- **The skills:** `helm`, `keel`, `keel-prove`, `crew`, Miguel Hernandez's 16 board and
  workflow skills, and the two senses (`deep-research`, `reverse-engineering`).
- **The harness:**
  - the data-boundary guard, in Python, and self-disarming when wired machine-wide;
  - three ECC hooks, which need Node;
  - `link_kit.py`, which links the master into projects instead of copying it;
  - `install_guard.py`, which sets the guard up on a machine;
  - `make_release.py`, which cuts releases.
- **Documents:** `MANUAL.md`, written to be enough on its own, plus `START-PROMPTS.md`,
  `QUICKSTART.md`, `ARCHITECTURE.md`, and the framework documents under
  `keel/framework/`.

### Proven — Evidence

The self-tests below are run again from a fresh clone of this release by
`make_release.py`.

| What | How |
| --- | --- |
| Data-boundary guard | 27-test self-test. Fifteen deliberately broken copies each failed it. It blocked secrets and allowed real work against a real project. |
| `link_kit.py` | 9-test self-test, including the guard working through links in a git repo. A round trip with the real master left it unchanged. |
| `install_guard.py` | 6-test self-test, against temporary settings files. |
| CREW's lane checker | 21-test self-test, including a real git diff. |
| Task-board validator | Proven to pass a clean board and fail a broken one. |
| Operator mode | Rehearsed on a throwaway package, then a read-only test drive on a real project. The project's own 1151 tests ran with its real database untouched, and no tracked file changed. |

### Written, not yet proven in use — Inferred

- CREW as a practice: no real multi-agent run yet. It stays Draft v0.1 until one.
- The suggest-don't-ask-blind posture: it is wording; no real interview has followed it
  yet.
- The guard arming itself inside a live session started in a package: rehearsed piece by
  piece, never yet observed live.

### Known gaps — Missing evidence

- The three ECC hooks (`block-no-verify.js`, `config-protection.js`, `cost-tracker.js`)
  have never run, because there was no Node.js on the machine that built this release.
- The guard doesn't follow symlinks, and it judges a searched directory as one path, not
  file by file. Both gaps are written up in `harness/DATA-BOUNDARY.md`.
- Reverse engineering needs REA installed separately; it isn't part of this release.
