# PROVE pass 3 — KEEL v1.1, 2026-10-19

The third PROVE pass on v1.1, run on the uncommitted working tree against `e09480c` (tag
`v1.0.0`) after fix round 3 (`.scratch/task_board/crew-plan-prove-fixes.md`, Open questions
16–19 and the execution log). Raw results: `round3/pass3-raw.json` (the reviewers, closure
checkers and critics), `round3/pass3-findings.md` (every new finding in full) and
`round3/verify3.json` (every skeptic's verdict).

## How the review was done

- **Three reviewers in fresh contexts**: the plugin's own agents `keel:prove-standards`,
  `keel:prove-spec` and `keel:prove-gate`, each handed only the fixed point and its source
  paths, nothing of the session that made the fixes.
- **Four closure checkers** re-tested every one of pass 2's verified items against the fixed
  tree, reproducing the original failure where they could.
- **Two fresh critics**, blind to each other: one followed README, QUICKSTART, MANUAL and
  START-PROMPTS literally as a new user, for Claude Code and Codex; one tried to make the
  guard, the switch-on rule or the data-boundary rule fail open.
- **Twenty-seven skeptics** then tried to refute every new finding, by default: three per
  claimed major, each with its own lens (reproduce it; judge it against the decisions; judge
  its real severity), and one per area for the rest. **None was refuted.**
- Everything ran read-only against the master, in temporary folders and homes. Nothing was
  committed. One skeptic read Codex's public parser source from GitHub to check K31 (a
  read; no project data was sent).

## What fix round 3 did

The manager picked "Fix round 3 → pass 3 (Recommended)". Two CREW phases, each fenced and
gated (the execution log):

- **Phase A (code, skills, the layer), landed 2026-10-18:** the three majors of pass 2 (N2 =
  N35, N36 with N3, N37) and the code and skill items.
- **Phase B (documents and records), landed 2026-10-19:** a usage limit cut off two of its
  three lanes mid-build; they were re-dispatched, each lane was audited by a fresh reader,
  and the gaps the audits found were repaired. Two of pass 2's follow-ons that the board
  lacked were filed (N33's code half; N33's role sub-claim).
- **Gate at landing (Evidence):** self-tests 27, 86, 9, 18, 30, 34, 14, 21 (239, all OK);
  `check_kit.py` no findings (91 skill paths, `CLAUDE.md` 5,469 characters, session 5,903,
  229 links); plugin validate with the one expected warning; board OK (26 tasks); R11
  loaded; R12 17 `keel:*` skills. Mutation proofs, each identity baseline green first:
  keel_hook 62/62, check_kit 36/36, install_plugin 27/27, install_guard 18/18, make_release
  25/25 (168 broken copies, all caught).

## Arming (keel-prove step 0)

| Check | Armed? | Evidence |
| --- | --- | --- |
| R2, R4, R5, R6 (and R8 through R6's cases), R13 | armed | this pass's mutation proofs, 168 of 168, identity baselines green first (execution log, phase B landing) |
| R9 | armed (newly Evidence) | the Gate reviewer: a manifest copy with no skill paths gave exit 1 and "Validation failed" |
| R11, R12 | armed | the Gate reviewer: an empty `CLAUDE_CONFIG_DIR` listed 0 `keel@` plugins; empty `HOME` and `CODEX_HOME` listed 0 `keel:*` skills |
| R1, R3, R7, R10 | armed | earlier records (ACCEPTANCE's seen-failing rows; v1.0's broken copies); not re-run this pass |

Every check reports its scope (tests run, files and links checked, tasks, skills).

## Standards

No hard violations found. Every finding below is a judgement call.

**Hard violations (documented standards)**
None found. What I checked:
- **Evidence:** `python3 -B harness/check_kit.py` exits clean ("no findings").
- **Evidence (read):** The new scripts follow RECON §2's script rule: standard library only, a usage docstring, exit 0/1 (`keel_hook.py`'s exit 2 is documented), and a `test_*.py` beside each.
- **Evidence (read):** `RELEASES.md` v1.1 keeps Evidence, Inferred and Missing apart. `PHASES.md` keeps the five phases. The diff does not touch `keel/skills-board/`.

**Judgement calls**

1. **Duplicated Code / Shotgun Surgery.** The hook command text, statusMessage and `Bash|apply_patch` are written in three places: `harness/plugin-hooks.json`, `harness/settings.hooks.codex.json`, and `harness/install_plugin.py` lines 65, 124-126 and 172-177. The MultiEdit matcher also differs from `install_guard.py:43`. Already ticketed (`hook-commands-single-source`).
2. **Duplicated knowledge vs "Reconcile, don't stack" (RECON §2).** There are two "is KEEL on" rules:
   - `keel_hook.keel_state` walks up to the git root and accepts `.keel` or `keel-factory`.
   - `install_guard.py` COMMAND (`ls -1 "$CLAUDE_PROJECT_DIR" | grep -qxF keel-factory`) checks only the start folder and ignores `.keel`.

   `DATA-BOUNDARY.md:65-68,185` documents this as by design. Still, changing the switch now means editing it in Python and in shell.
3. **Repeated Switches.** `keel_hook.py` checks `harness == "codex"` / `!= "codex"` in `instruction_files` (263), `carries_layer` (278) and `upgrade_note` (294, 297).
4. **Speculative Generality.** `def guard(raw: str, harness: str = "claude")` (`keel_hook.py:394`) never reads `harness`. Its own docstring says guard behaves the same for both harnesses.
5. **Primitive Obsession.**
   - `layer_status` (`keel_hook.py:282-290`) returns string tuples: `("v1.0", name)`, `("carries", "")` or `("", "")`.
   - `install_plugin.py:233` decides whether a skill was skipped by parsing its own report text: `report[-1].startswith("skipped ")`.
6. **Duplicated Code (minor).**
   - `keel_state`'s home/root exclusion test appears twice (241, 247).
   - `check_kit.py` reads VERSION in both `check_manifest` (191) and `check_release` (406).
   - In `install_guard.py:103-105`, the `is_keel(entry)` filter repeats what the inner `is_keel_command` already checks.
7. **"HELM stays thin" and short-sentenced docs (RECON §2).** `keel/skills/helm/SKILL.md` grew from 130 to 236 lines.
   - Switch-on steps 1-4 (lines 73-114) now do setup work: write `.keel/keel.json`, probe the guard, inspect the allowlist and write an `AGENTS.md` block.
   - Step 3 packs about six branches into one list item.
   - It is still a procedure, not an engine, but it is drifting.
8. **Mysterious Name.** The loop variable `one` holds a payload (`keel_hook.py:366, 401`). Separately, `ROLE_NEXT` (98) says `keel:helm` where `CLAUDE.md:12` says `/keel:helm`.
9. **Scratch code is tracked**, so it ships in the release archive:
   - `.scratch/v1.1/round3/ref3arm_driver.py:15` hard-codes `MASTER = Path("/Users/lambertike/Documents/KEEL-FACTORY")`.
   - `.scratch/v1.1/tools/mutate.py` has no self-test and puts several imports on one line.

   The house script rule may not be meant for scratch files. The owner should decide.

I did not open the `.scratch/v1.1/trials/*.jsonl` transcripts or anything gitignored. No review step needed them.

**Worst issue in this axis:** no hard violation; the most consequential judgement call is
HELM's growth (T7), since HELM must stay a router.

## Spec

**Spec review: v1.1 working tree against e09480c**

Scope: I read `git diff e09480c` and the untracked files. Most of D1–D11 is implemented as approved, with A1–A7, P-A–P-H and F3-1–F3-9 applied. I ran `python3 -B harness/check_kit.py` and it reported no findings: 18 skills, 7,038 listing characters, `CLAUDE.md` at 5,469 characters, session injection at 5,903 (Evidence). Nothing is committed and no tag exists, which is correct.

**(a) Missing or partial**
1. The agent bodies do not yet match approved D7. The contract says: "Their bodies are the review prompts `keel-prove` holds today, moved, not rewritten." P-E allows only "one sentence added to each". `/Users/lambertike/Documents/KEEL-FACTORY/agents/prove-spec.md` (and the other two) add an opening paragraph, how to read the change, "Do not edit any file", the Gate's rules and data-boundary items 1–3. The fix for this, F3-7's "moved, with those added", is still under "Proposed, awaiting the manager". Until the manager answers, this conflicts with the approved text.

**(b) Not asked for (minor)**
1. The production-question list grew. D6 lists "users, auth, data, secrets, deploy target, external services, toolchain, cost ceiling". The TIERS.md "Stop modes" section also asks "how anyone will know it is healthy (logs, monitoring)", and the `complete-description` eval grades observability as one of its five topics. No amendment covers this.
2. Unattended mode widened. D6 says "write it as a board task with `gate: owner`", but TIERS.md says "`gate: owner` or `gate: manual`".
3. The docs' default install line differs from D1. D1's default is `python3 "$KEEL/harness/install_plugin.py"`, but README, QUICKSTART, MANUAL and START-PROMPTS lead with `install_plugin.py --codex`.
4. Some documentation goes beyond D11's list: the CREW.md "Field record" (runs 1–2) and the new LOOPS.md §6 harness table. Both serve A3, M7 and M9, but D11 does not name them.
5. `install_plugin.py` reads `~/.claude/plugins/installed_plugins.json` to warn when a marketplace copy is also installed. Nobody specified this, though it matches D1's "Pick one".

**(c) Implemented but possibly wrong, or the record is stale**
1. Contract §2 contradicts the build. Its row says Codex namespaced names exist "Only inside a Codex plugin (`plugin:skill`); plain skills are bare names". HELM and CAPABILITIES.md say linked skills list as `keel:helm`, citing X9 as Evidence. This agrees with §1's `$keel:helm`, but §2 was never amended, so the contract disagrees with itself.
2. A process risk to note, not a finding. F3-1, F3-4 and F3-6 change approved decision wording: P-A's kit exclusion, D3's "only the kit-root line", and D4's "gives the same answer". Their only authority is the pick "Fix round 3 → pass 3 (Recommended)", which approved fixing items, not rewording the contract. D6 itself says "a finding that breaks the approved CONTRACT" must halt. Under the rule I was given (approved sections count as approved), I accepted them.

No other deviations found. The data-boundary guard is unchanged, `keel/skills-board/` is unchanged, the plugin manifest and hooks match A1, A5 and P-G, the six `openai.yaml` files are present, the three eval cases each have one `llm` grader plus baseline graders, and `make_release.py` refuses to run off `main` and runs `check_kit` and all eight self-tests.

The pass/fail state of the test suites (75 old tests plus the new suites) is for the Gate reviewer to establish; I did not run them (Missing evidence).

**Worst issue in this axis:** the agent bodies against approved D7 (S-a1), which stands
until the manager answers F3-7's proposal.

## Gate

Gate, KEEL v1.1 (uncommitted working tree against e09480c)

All 13 Required Checks exist and exit 0. No CRITICAL findings. I ran them from `/Users/lambertike/Documents/KEEL-FACTORY` with `PYTHONDONTWRITEBYTECODE=1`. The working tree was the same before and after the runs.

**Required Checks (Evidence: each one run)**

| ID | Exit | Output | Scope it reported |
|---|---|---|---|
| R1 | 0 | OK | 27 tests |
| R2 | 0 | OK | 86 tests |
| R3 | 0 | OK | 9 tests |
| R4 | 0 | OK | 18 tests |
| R5 | 0 | OK | 30 tests |
| R6 | 0 | OK | 34 tests |
| R7 | 0 | OK | 21 tests |
| R8 | 0 | `OK: … no findings` | 14 skill paths, 2 hook commands, 18 skills, 7038 listing characters, 91 skill paths checked, 22 Codex skills, 3 agents, 3 eval cases, 5469 `CLAUDE.md` characters, 5903 session characters, 213 docs, 229 links |
| R9 | 0 | Validation passed with 1 warning, the root `CLAUDE.md` one | the manifest |
| R10 | 0 | `OK: 26 task(s) … no findings` | 26 tasks |
| R11 | 0 | `keel@skills-dir`, v1.1.0, Status loaded, Path `~/.claude/skills/keel` | 1 plugin |
| R12 | 0 | 17 skills listed as `keel:<name>`, from crew to to-task | 22,761-byte rendered prompt, no model call |
| R13 | 0 | OK | 14 tests |

- **R8:** the output gives counts but does not name its 14 rules. That is minor: the scope it states is still specific.
- **R12:** I ran it in a scratch git repo holding `.keel/keel.json`, with a scratch `CODEX_HOME`. Every `keel:*` skill path I could extract (12 of 17) resolves inside this master; the other 5 lines did not match my pattern.
- **R11:** I did not follow the `~/.claude/skills/keel` link, because it is outside the working tree.
- No suite reported any skipped tests, and every count matches ACCEPTANCE.md.

**Arming I re-checked myself (Evidence)**
- **R9:** a copy of the manifest in a folder with no skill paths gave exit 1 and "Validation failed". This moves R9 from Inferred to Evidence.
- **R11:** with an empty `CLAUDE_CONFIG_DIR`, the list showed 0 `keel@` plugins.
- **R12:** with an empty `HOME` and `CODEX_HOME`, the prompt listed 0 `keel:*` skills.
- **R1–R8, R10, R13:** I did not re-run the mutation records; their arming rests on the cited records.

**Traceability**

| # | Bound checks: exist / armed / pass | Not run |
|---|---|---|
| M1 | R5, R11 | L1, L3 (live model runs) |
| M2 | R2 | L3, L4, L7 (live) |
| M3 | no runnable check bound | L4 (live) |
| M4 | R8 | L5 (live) |
| M5 | R8 | P1: needs Claude Code 2.1.269 or later, installed is 2.1.170 (Evidence) |
| M6 | R8, R9 (R9 now armed by Evidence) | `claude plugin details` is not an ACCEPTANCE check |
| M7 | R8, R12 | P2: needs a Codex model call that has not been approved |
| M8 | R1, R2 | L1–L3 (live) |
| M9 | R8 (229 links) | "reviewer reading" is not a check |

I did not re-run the L1–L8 live runs or P2, because each needs a paid model call.

**What the gate does not settle**
- M3 has no runnable check behind it at all.
- M8's FAIL in PROVE-2 (the copied-kit route does not arm, N2 = N35) has no Required Check covering it, so passing R1 and R2 cannot promote that row.
- The PARTIAL rows (M2, M3, M5, M7, M9) depend on live runs or reviewer reading, which these checks don't carry.
- Every bound R-check passed, so no row should be demoted on gate evidence.

Files: `/Users/lambertike/Documents/KEEL-FACTORY/.scratch/v1.1/ACCEPTANCE.md`, `/Users/lambertike/Documents/KEEL-FACTORY/.scratch/v1.1/TRACEABILITY.md`

**Worst issue in this axis:** none failing; M3 has no runnable check bound to it.

## Closure of pass 2

Every one of pass 2's items was re-checked: **64 fixed, 5 partly, 0 not fixed, 0 regressed.** The three
majors of pass 2 (N2 = N35, N36 with N3, N37) were each reproduced end to end and are fixed;
the follow-ons are on the board and the rejects carry their reasons. The partly-fixed items
carry into pass 3's verified list:

- **N10** → C10: MANUAL §8 still sends developers to the handoff, which is stale (see N12). STATE.md:18 says "Resume from `.scratch/handoff.md`", and handoff.md:5 says "The current state is in `.scratch/v1.1/STATE.md`", so each points at the other. Following the handoff, a fresh session would redo row 13's full re-r…
- **N12** → C10: The handoff contradicts STATE and the execution log on item 2. It also omits the F3-7 D7 proposal that is pending for the pass-3 report: its item 3 (:90-91) asks only "Approve PROVE, or what should change?", while CONTRACT:500-515 and STATE:47-49 hold the pending proposal. Rewrite or supersede the h…
- **N23** → C15: One documented operator route is still not handled in keel: a linked keel-factory/ in someone else's package. Repro: a scratch package (README plus its own CLAUDE.md) with link_kit.py; `keel_hook.py session` prints 'role: kit' and 'if the project's own instructions are not KEEL's, that is operator m…
- **N24** → C14: The words changed, but where the guard is armed the warning that carries the new remedy never fires. Its trigger command names .keel/keel.json, which the guard blocks in exactly the gitignored case it is meant to detect. CLAUDE.md then tells the agent to report the block and ask the data-boundary qu…
- **N26** → C15: N26 inherits N23's remainder: under a linked keel-factory/ (role kit, nothing recorded), keel's step 0 still has no signal for operator mode, so its phases can write docs/ into a package.

**A correction to PROVE-2 (C9).** Pass 2's skeptics verified 42 of the checkers' and
critic's items and 18 reviewer items, not "45 … and 15": N10, N12 and N20 were never given
to a skeptic, so they got no disposition. N12 and N20 were closed by the lead's STATE.md
rewrite; N10 is the stale-handoff item, open as C10 here. PROVE-2.md's "How the review was
done" should read 42 + 18 with the three omissions named (docs-only, below).

## Verified findings of pass 3

Forty-nine distinct items (duplicates merged), all reproduced: 35 confirmed and 14
partly; **none refuted**. Severity after verification: **0 major**, 34 minor, 15 none.
Origin: 22 from the v1.1 build, 13 from fix round 3, 7 from the first fix run, 5 from
v1.0, 2 mixed or unclear. Dispositions: 5 fix-now, 28 docs-only, 5 follow-on, 10 reject, and 1 for the manager.

### The seven claimed majors

Each was judged by three skeptics. All seven reproduce. The severity and contract lenses
judged every one minor: each needs a hostile package or input, or an agent already breaking
CLAUDE.md's rule, which the guard backs up rather than replaces (pass 2's N33 standard). The
reproduce lens called five of them major. The split is shown so the manager can weigh it.

| Id | Finding | Votes (lens: severity) | After verification | Disposition |
| --- | --- | --- | --- | --- |
| C4 | A Codex hook written from a copied kit runs that project's own guard machine-wide; DATA-BOUNDARY says no machine-wide hook ever does | reproduce major, contract minor, severity minor | partly, minor, fix round 3/fix run/v1.1 build | docs-only |
| K18 | Guard's gitignore rule fails open outside git and inside nested git repositories, and no document says so | reproduce major, contract minor, severity minor | confirmed, minor, v1.0 | docs-only |
| K19 | An allowlist committed inside a submodule or nested repo is honored and invisible to HELM's and OPERATOR's switch-on check (also C16, K33) | reproduce minor, contract minor, severity minor | confirmed, minor, fix round 3 | docs-only |
| K29 | Claude Code's built-in Monitor tool runs shell commands and is not in the guard's matcher | reproduce minor, contract minor, severity minor | confirmed, minor, v1.0 | docs-only |
| K30 | keel_hook guard fails open (exit 1) on a deeply nested .keel/keel.json, and hangs on a FIFO; switch-on code runs outside the fail-closed try | reproduce major, contract minor, severity minor | confirmed, minor, v1.1 build | fix-now |
| K31 | Codex apply_patch adapter misses hunk headers with leading whitespace, which Codex accepts: a patch can edit .env or write the allowlist unchecked | reproduce major, contract minor, severity minor | confirmed, minor, v1.1 build | fix-now |
| K32 | In Codex every read is a shell command, so the guard there is only the Bash heuristic (`cat .env;`, `cat <.env`, gitignored plain names pass) while HELM's probe reports armed | reproduce major, contract minor, severity minor | confirmed, minor, v1.1 build | docs-only |

The two that are code defects in v1.1's own hook, and fix-now:

- **K30.** `keel_hook.py guard` reads the role before its fail-closed `try`, and `role_of`
  does not catch `RecursionError`. A committed `.keel/keel.json` nested 20,000 deep makes
  every guarded call exit 1, which both harnesses read as allow; a symlink to `/dev/zero`
  hangs it until the hook times out. The probe then fails open too. A prototype passed all 86
  tests and blocked every case.
- **K31.** The Codex `apply_patch` adapter matches hunk headers only at the start of a line;
  Codex's own parser trims whitespace first. A patch whose second header is indented edits
  `.env` or writes `.keel/data-boundary-allow` with the guard answering exit 0.

### Every verified item

Sorted by severity, then disposition. The fix text is the verifier's, shortened; the full
text is in `round3/verify3.json`.

| Id | Finding | Verdict | Severity | Origin | Disposition | Fix |
| --- | --- | --- | --- | --- | --- | --- |
| K30 | keel_hook guard fails open (exit 1) on a deeply nested .keel/keel.json, and hangs on a FIFO; switch-on code runs outside the fail-closed try | confirmed | minor | v1.1 build | fix-now | In keel_hook.py only. I prototyped this in a temp copy of the kit: all 86 test_keel_hook tests passed (1 skipped), and the deep-nested file, the FIFO, /dev/zero and /dev/urandom now all give Read .env exit 2, probe exit 2, and a f … |
| K31 | Codex apply_patch adapter misses hunk headers with leading whitespace, which Codex accepts: a patch can edit .env or write the allowlist unchecked | confirmed | minor | v1.1 build | fix-now | In keel_hook.guard_payloads, parse the way Codex does: split the patch on newlines, call str.strip() on each line (a superset of Rust's trim), and capture every line that then starts with '*** Add File: ', '*** Update File: ', '** … |
| C4 | A Codex hook written from a copied kit runs that project's own guard machine-wide; DATA-BOUNDARY says no machine-wide hook ever does | partly | minor | fix round 3/fix run/v1.1 build | docs-only | Docs now. (1) START-PROMPTS.md:260-265: change the precise way to `python3 "$KEEL/harness/install_plugin.py" --codex-hooks`, run from your KEEL master. Add this sentence: with a linked kit, keel-factory/ resolves to the master; … |
| K18 | Guard's gitignore rule fails open outside git and inside nested git repositories, and no document says so | confirmed | minor | v1.0 | docs-only | Now, docs only. The guard and the contract stay unchanged. 1. DATA-BOUNDARY.md:30, qualify the bullet: 'Anything the project's own .gitignore would exclude, inside a git repository: the guard asks git check-ignore in the repositor … |
| K19 | An allowlist committed inside a submodule or nested repo is honored and invisible to HELM's and OPERATOR's switch-on check (also C16, K33) | confirmed | minor | fix round 3 | docs-only | Docs now: (1) In DATA-BOUNDARY.md 'What this does not cover' (the bullet 'An allowlist that came with the repository'), replace 'at the git root' with 'at the nearest git root of each path, so a submodule or a nested clone can bri … |
| K29 | Claude Code's built-in Monitor tool runs shell commands and is not in the guard's matcher | confirmed | minor | v1.0 | docs-only | Now (docs-only, no contract change): (a) add one bullet under DATA-BOUNDARY.md 'What this does not cover', beside the MCP bullet: 'Built-in tools outside the matcher. … |
| K32 | In Codex every read is a shell command, so the guard there is only the Bash heuristic (`cat .env;`, `cat <.env`, gitignored plain names pass) while HELM's probe reports armed | confirmed | minor | v1.1 build | docs-only | Docs-only, this round: 1. CAPABILITIES.md, Codex table: add a row. Need: File reads. What it does here: 'No dedicated read tool; … |
| C14 | HELM's gitignore warning is triggered by a command the armed guard blocks in exactly the case it detects (also K24; closes N24's remainder) | confirmed | minor | fix run | fix-now | HELM step 1: run `git check-ignore -q .keel/keel.json` at the git root before writing .keel/keel.json. At that point KEEL is off and the guard is idle, and git answers for a path that does not exist yet. … |
| C15 | keel/keel-prove/crew operator test misses the linked-kit route (role `kit`, nothing recorded) (N23's and N26's remainder) | confirmed | minor | fix round 3 | fix-now | In the three step-0 texts, widen the test to: 'In operator mode: `.keel/keel.json` says operator; … |
| K20 | HELM step 4 appends the v1.1 block to an AGENTS.md that still holds v1.0's copy: two layers load, and the hook keeps reporting 'not added' | confirmed | minor | fix run | fix-now | HELM step 4: if AGENTS.md contains 'This project was started from KEEL FACTORY.', add no block. … |
| S-a1 | Spec (a)1: the agent bodies do not match approved D7 until F3-7's proposal is answered | confirmed | minor | v1.1 build | for the manager | No change to the tree. Put F3-7's proposal to the manager at the pass-3 report, as already queued. If the manager declines, take F3-7's stated alternative: D7 keeps its words and F3-7's list stands as the record of what was added. |
| C1 | A v1.0 copied kit reached through the v1.0-recommended import now gets two layers and no upgrade note | confirmed | minor | fix round 3 | docs-only | Now, docs only: add a bullet to MANUAL section 11 step 2 and to RELEASES 'Upgrading from v1.0'. … |
| C10 | The handoff contradicts STATE and the execution log, and MANUAL §8 still sends developers to it (N10's and N12's remainder) | confirmed | minor | fix round 3 | docs-only | At the PROVE pass 3 stop, write a new handoff with the handoff skill, covering the landed state: phase B and the re-run done; PROVE pass 3 run and verified; F3-7, plus any C11 confirmation, waiting for the manager. … |
| C11 | C2 counts a stated reason as approval of the 8,000-character listing bound | confirmed | minor | fix round 3 | docs-only | Reword C2 to 'The bound rests on A1's stated reason, which the manager ticked; it was not put to the manager as a bound.' Add one line beside F3-7 under 'Proposed, awaiting the manager' asking the manager to confirm the 8,000-char … |
| C17 | Crew-plan decisions 9 and 12 still state superseded rules without a pointer | confirmed | minor | fix round 3 | docs-only | Append to decision 9: '*Superseded 2026-10-18 by Open question 17 (the copied-skill line, N25).*' Append to decision 12: '*Superseded 2026-10-18 by Open questions 16 and 17: P-B became a second named exception; … |
| C2 | A kit copied into a project with git clone (own .git), wired from itself, is still dormant, as N2 was (also C6) | confirmed | minor | fix round 3 | docs-only | Docs only. README.md:12: 'copying it (MANUAL.md section 4's rsync, which leaves .git out)'. RELEASES.md:218: 'An rsync copy of the kit (no .git), wired from its own hooks, now switches KEEL on'. … |
| C5 | HARNESS-PROBES' preamble says the real ~/.claude was never touched, but P14 measured this machine's own config; CAPABILITIES still lists P1–P13 (also K27's legend half) | confirmed | minor | fix round 3 | docs-only | In HARNESS-PROBES.md:11-13, scope the preamble to P1–P13 and add: "P14 read this machine's own config (nothing written) and a fresh scratch CLAUDE_CONFIG_DIR." In CAPABILITIES.md:65, change P1–P13 to P1–P14. … |
| C7 | MANUAL §10 promises the agent asks before any git clean, but only operator mode's protocol tells it so | partly | minor | fix round 3 | docs-only | Docs-only, in MANUAL.md:511-514. Keep the always-on layer unchanged; it has a size bound. … |
| C8 | The armed check never exercises the hook's matcher | partly | minor | fix run | docs-only | Keep the Read payload (OQ17). Change the one-liner to select the entry whose command names keel_hook.py or data-boundary-guard, and to print its matcher above the command, e.g. … |
| C9 | PROVE pass 2 dropped N10, N12 and N20 from verification and disposition, and misstates its own coverage | confirmed | minor | fix run | docs-only | Add a dated correction at the end of PROVE-2.md, or in PROVE-3.md with a pointer to it. It should say that N10, N12 and N20 were never given to a skeptic. N12 and N20 are closed by the lead's STATE.md rewrite (STATE:12, :43-49). … |
| K21 | START-PROMPTS' Codex prompt double-wires KEEL's two hooks when block-no-verify.js is added after --codex-hooks | confirmed | minor | fix run | docs-only | START-PROMPTS.md:266-272: "If you ran --codex-hooks, KEEL's two hooks are already wired: to add block-no-verify.js, put only its entry in ./.codex/hooks.json. … |
| K22 | Copied-skill flows name the skill $helm, but CLAUDE.md/AGENTS.md and the skills' openai.yaml tell Codex to use $keel:helm | confirmed | minor | v1.1 build | docs-only | CLAUDE.md:12: "`$keel:helm` in Codex (`$helm` where the skills were copied into `.agents/skills/`)". That is about 60 characters, well inside the 6,000 bound (5,469 now). Re-run check_kit for the session size. … |
| K23 | Hand-wiring docs send the raw, absolute-path guard into the shared .claude/settings.json, which START-PROMPTS forbids and which locks out every other machine | confirmed | minor | v1.0 | docs-only | Docs-only; settings.hooks.json, OPERATOR.md's pinned block and the guard stay as they are. … |
| K25 | Following MANUAL section 10 in a linked-kit project (creating .keel/ for the allowlist) flips the role from 'kit' to 'not recorded' | confirmed | minor | v1.1 build | docs-only | Docs: in HELM:63-64 and OPERATOR.md:127, <ops> is keel-factory/.ops/ whenever a linked keel-factory/ is present, or wherever KEEL's notes already are. … |
| K26 | Fallback wiring is described as live in the same session, but KEEL's own documents say it is not | partly | minor | v1.0 | docs-only | OPERATOR.md:47-48, outside the pinned JSON block and its intro sentence: "...only if that file doesn't exist yet. It arms after the user opens /hooks or starts a new session; … |
| K27 | CAPABILITIES.md keeps a stale Evidence row ('16 keel:* skills') and a legend that omits P14 | confirmed | minor | v1.1 build | docs-only | CAPABILITIES.md:85: "Plugin skills are namespaced `keel:<name>`: the master loads 18 (P14), 17 listed to the model because `commit` is hidden (P5's flag). L1, run before `keel` was unhidden, saw 16." Cite P4, L1 and P14. … |
| K28 | install_plugin.py cannot recover from a moved master, and misreports a remove when hooks.json is missing | confirmed | minor | v1.1 build | docs-only | Docs now: a MANUAL section 10 entry, 'You moved the master'. Remove the old link yourself (`rm ~/.claude/skills/keel`, a link, never `rm -r`, and any dangling links under ~/.agents/skills/), then re-run install_plugin.py from the … |
| K35 | A committed regular file named `.keel` keeps KEEL (and the guard) off, and HELM has no step for it | confirmed | minor | v1.1 build | docs-only | Docs: add one clause to HELM step 1. If .keel exists and is not a folder, say so and leave it untouched; KEEL stays off and the data-boundary rule runs as strict policy. … |
| S-c1 | Spec (c)1: CONTRACT §2's Codex-namespacing row contradicts the build (X9: linked skills list as `keel:helm`) | confirmed | minor | v1.1 build | docs-only | Add a dated Stale note under §2's table: 'Stale 2026-10-18: probe X9 shows that a linked skill whose real folder sits under a .claude-plugin/plugin.json is named after that plugin. … |
| S-c2 | Spec (c)2: F3-1, F3-2, F3-4 and F3-6 reword approved decisions on the umbrella pick (also C12) (also C12) | partly | minor | fix round 3 | docs-only | At the pass-3 report, ask about F3-1, F3-2, F3-4 and F3-6 alongside F3-7 in one question: approve the decision rewordings fix round 3 applied, as written (Recommended), or revert one and change the code to the approved text. … |
| C3 | The carry check assumes Claude Code loads `@keel-factory/CLAUDE.md` through a linked folder; that is unprobed | confirmed | minor | v1.1 build | follow-on | Now, docs: add a CAPABILITIES row, Inferred, citing the memory docs: an import through a linked keel-factory/ is external and needs the user's approval. … |
| K34 | A package can suppress KEEL's always-on layer, data-boundary rule included, by putting the mark line in its own CLAUDE.md or AGENTS.md; HELM then skips loading it | confirmed | minor | v1.1 build | follow-on | Fold into codex-agents-block-refresh, with a contract amendment to P-C. Count a marked file as carrying the layer only when its block (minus the kit-root line) matches the kit's CLAUDE.md, under either harness. … |
| S-b5 | Spec (b)5: install_plugin.py reads installed_plugins.json to warn about a marketplace copy, unspecified | confirmed | minor | v1.1 build | follow-on | Fold this into board task installer-hooks-json-robustness. Parse the JSON, swallowing read and parse errors. Match only keys under "plugins" that start with 'keel@' and are not 'keel@skills-dir'. … |
| T1 | Standards 1: the hook command text is written in three places | confirmed | minor | v1.1 build | follow-on | None in v1.1. Carry out the filed task hook-commands-single-source after PROVE passes: add a test_install_plugin case that loads settings.hooks.codex.json, substitutes the path and asserts equality with codex_hooks' output, then d … |
| C12 | F3-2, F3-4 and F3-6 change approved decisions on the umbrella pick, while F3-7 waits for the manager | partly | none | fix round 3 | docs-only | Add one clause to the F3 preamble: 'F3-2, F3-4 and F3-6 carry the verifier's fix wording from PROVE-2's table, which the pick approved; … |
| C13 | Small record drift in TRACEABILITY and ACCEPTANCE | partly | none | fix run | docs-only | While promoting the matrix for pass 3: change 'L3–L7' to 'L3–L8', and add L8 to M8's bound checks. Put ACCEPTANCE's sentence in the past tense: 'the lead re-measured both at phase B's landing (229 links, 26 tasks; … |
| K36 | A long shell command pushes the guard past Claude Code's hook timeout before it reaches the secret token (fail-open by timeout) | partly | none | v1.0 | docs-only | Docs: add a clause to DATA-BOUNDARY's 'Bash coverage is heuristic' bullet: a command with thousands of path-shaped words can outlast the hook's timeout (600 s by Claude Code's documented default), and a timed-out hook lets the cal … |
| T9 | Standards 9: scratch code with a hard-coded path would ship if `.scratch/v1.1/round3/` were committed | partly | none | fix round 3 | docs-only | Add one line to the handoff's step 4 (commit) and to STATE: the scope of the .scratch/v1.1/ commit is the manager's decision. … |
| T7 | Standards 7: HELM grew from 130 to 236 lines; switch-on drifting from 'HELM stays thin' | partly | none | fix run | follow-on | No v1.1 edit: rewording HELM now would also touch text no live run has exercised since L7 (PROVE-2's M2). … |
| S-b1 | Spec (b)1: the production-question list grew (observability) without an amendment | confirmed | none | v1.1 build | reject | None. The pass-2 reject stands. |
| S-b2 | Spec (b)2: unattended mode allows `gate: manual` as well as `gate: owner` | confirmed | none | v1.1 build | reject | None. The pass-2 reject stands. |
| S-b3 | Spec (b)3: the docs' default install line leads with `--codex`, not D1's bare line | partly | none | v1.1 build | reject | None required. Optional: where the line appears, add one clause: 'Claude Code only: leave off --codex.' |
| S-b4 | Spec (b)4: CREW.md's field record and LOOPS.md §6 go beyond D11's list | partly | none | v1.1 build | reject | None. |
| T2 | Standards 2: two 'is KEEL on' rules (keel_hook in Python, install_guard in shell) | partly | none | v1.1 build | reject | None. If anything, add one comment above install_guard.COMMAND saying it is deliberately narrower than keel_hook.keel_state (D4, Open question 17), so a future edit does not try to sync it. |
| T3 | Standards 3: repeated `harness == "codex"` switches in keel_hook | confirmed | none | v1.1 build | reject | None for v1.1; it stays under pass 2's std:smells rejection. In a later keel_hook refactor, a small per-harness table (instruction files, whether imports count, upgrade text) would replace the four compares. |
| T4 | Standards 4: `guard(raw, harness)` never reads `harness` | confirmed | none | v1.1 build | reject | None. If touched later, either drop the parameter (guard(raw)) and have main ignore harness for guard, or keep it for symmetry as documented. |
| T5 | Standards 5: primitive obsession (layer_status tuples; install_plugin parses its own report) | confirmed | none | fix round 3 | reject | None before release. In a later refactor, have link() return a status ('linked'\|'skipped'\|'refused') instead of a bool, and test that rather than report[-1]. |
| T6 | Standards 6: small duplications (keel_state's exclusion test, VERSION read twice, an is_keel filter) | confirmed | none | unclear | reject | None for v1.1, since each change would mean re-running suites and mutation proofs for no behavior change. Later: drop `and is_keel(entry)` at install_guard.py:103, and give keel_state a `skip(f)` helper for the home/root test. |
| T8 | Standards 8: the name `one`; ROLE_NEXT says `keel:helm` where CLAUDE.md says `/keel:helm` | partly | none | v1.1 build | reject | None. Optionally, in a later edit, write ROLE_NEXT as '`/keel:helm` (skill `keel:helm`) in Claude Code' and rename `one` to `call`. |

## Traceability, promoted

| # | Must-have | After pass 2 | After pass 3 | Why |
| --- | --- | --- | --- | --- |
| M1 | Install once; every skill visible in every project | PASS | **PASS** | R5 (30 tests, 27/27 mutants) and R11, both armed; L1, L3 |
| M2 | One front door; HELM tells owner from operator | PARTIAL | **PARTIAL** | R2 armed (86 tests, 62/62); HELM's switch-on text changed again and no live run has followed it since L7; C14 (HELM's own gitignore check is blocked by the guard it arms) and C15 (`keel` misses operator mode in a linked-kit package) are fix-now |
| M3 | Stop modes | PARTIAL | **PARTIAL** | checkpoint live (L4); supervised and unattended not exercised; no runnable check is bound to this row |
| M4 | PROVE reviewers shipped as agents | PASS | **PASS** | R8's agent rule armed (36/36); this pass ran all three; D7's wording waits on the manager (S-a1), the agents themselves are unaffected |
| M5 | Eval suite with a baseline | PARTIAL | **PARTIAL** | written and checked by R8; never run: P1 needs Claude Code ≥ 2.1.269 (installed: 2.1.170) |
| M6 | Less always-on context | PASS | **PASS** | R8's sizes armed: `CLAUDE.md` 5,469 characters (v1.0: 12,773); R9 now armed by Evidence |
| M7 | Codex, as far as Codex allows, gaps named | PARTIAL | **PARTIAL** | skills proven (R8, R12); Codex hooks unproven live (P2, owner-gated); a gap still unnamed: Codex reads reach the guard only as shell commands (K32); the docs steer to a copied kit's machine-wide installer (C4) |
| M8 | Guard keeps working and arms in KEEL projects | FAIL | **PARTIAL** | the copied-kit route now arms (N2 = N35 fixed, reproduced end to end by the closure checker); R1, R2 armed; but two fail-open defects in `keel_hook.py` (K30, K31, fix-now) and limits the docs do not name (K18, K19, K29) |
| M9 | CAPABILITIES says what each harness can and can't do | PARTIAL | **PARTIAL** | N13 and N15 fixed; still a stale Evidence row and legend (C5, K27), no row for Codex reads (K32), and the linked-import premise is unprobed (C3) |

Coverage = (PASS + DESCOPED) / total = **3 / 9 (33%)**, as after pass 2; M8 moved from FAIL to
PARTIAL. M3, M5 and M7 cannot reach PASS without runs the manager gates (P1 needs a newer
Claude Code; P2 needs a Codex model call).

## Cost

Measured from the workflow runs of this session (Evidence: the harness's own counts):

| Run | Agents | Subagent tokens |
| --- | --- | --- |
| Phase B re-dispatch: build, audit, fix-up, re-audit | 8 | 1,792,922 |
| Phase B repair round (guides3's first audit) | 7 | 1,168,627 |
| Phase B last narrow repair | 3 | 257,100 |
| PROVE pass 3 | 9 | 1,948,105 |
| Verification | 27 | 3,807,818 |

That is 54 agents and about 9.0 million subagent tokens, on the manager's plan
(`ANTHROPIC_API_KEY` unset). No headless run and no Codex model call. The cost of using
KEEL itself (keel-prove step 6's fixture set) was not measured: the eval suite needs Claude
Code ≥ 2.1.269 (Missing evidence; M5).

## Honest status

- **Implemented and verified:**
  - the hook's switch-on rule, copied kits included, the import rule and the allowlist
    block (R2, 86 tests, 62/62; N2 = N35 and N36 reproduced as fixed);
  - install_guard running the installing master's guard (R4, 18/18; N37 reproduced as
    fixed);
  - the installer (R5, 27/27); check_kit (R6, 36/36); make_release's main-only refusal and
    README-FIRST (R13, 25/25);
  - the plugin loading (R11); Codex skill links (R12); the manifest (R9, now armed); the
    guard in subagents (L8).
- **Implemented, unverified:**
  - HELM's switch-on steps and the operator-mode text in `keel`, `keel-prove` and `crew`:
    written, no live run since L7.
  - The Codex hooks (P2, owner-gated).
  - Supervised and unattended stop modes.
- **Specified only:**
  - The eval suite's run (P1).
  - F3-7's reading of D7, proposed and not yet approved.
- **Known open defects:** K30 and K31 (fail-open paths in `keel_hook.py`), C14, C15 and
  K20 (HELM and the skills), all fix-now; 28 docs-only items, most of them limits the
  documents do not yet name.

## For the manager

PROVE pass 3 does **not** pass yet. No major defect survived verification, and pass 2's
three majors are closed. But coverage is still 3 / 9, and five fix-now items are open. Two
of them are fail-open paths in v1.1's own hook (K30, K31), which contradict RELEASES'
"`keel_hook.py` fails closed itself".

Recommended: a fix round 4 over the 5 fix-now and 28 docs-only items, the 5 follow-ons filed
as board tasks and the 10 rejects recorded with their reasons. Then a closure-focused PROVE
pass 4: the three reviewers and closure checkers over these 49 items, with no new critic,
stopping at its report. The search is converging (pass 2: 60 items, 4 major; pass 3: 49
items, 0 major after verification), so pass 4 checks the fixes without reopening the hunt.

Also for the manager, one contract question: approve as written F3-7's reading of D7
("moved, with those added"), the 8,000-character listing bound (C11: it was approved only as
A1's stated reason), and the decision rewordings F3-1, F3-2, F3-4 and F3-6 that fix round 3
applied under the pick (S-c2).

## Dispositions recorded in fix round 4 (2026-10-19)

The manager picked "Fix round 4 → pass 4 (Recommended)" and approved F3-7's reading of D7
and the 8,000-character listing bound. The answer was cut before F3-1, F3-2, F3-4 and F3-6,
so those go to the manager again at the PROVE pass 4 report (the crew plan's Open question
20, verbatim). Fix-now and docs-only items are fixed in fix round 4 under that plan. The
rest:

**Follow-ons, filed as board tasks** (`.scratch/task_board/`):

| Item | Board task |
| --- | --- |
| C3 (the linked-import premise; needs an interactive session) | `owner-deferred/claude-linked-import-probe` |
| K34 (a package's mark line stands in for the layer) | `codex-agents-block-refresh`, item 6 |
| S-b5 (the marketplace note parses raw text) | `installer-hooks-json-robustness`, item 5 |
| T1 (hook text in three places) | `hook-commands-single-source`, already filed; noted |
| T7 (HELM's growth) | `codex-agents-block-refresh`, item 7; `helm-role-override`, item 3 |
| The code halves of C1, K18, K19 (honor an allowlist only at the KEEL root), K36 | `keel-hook-hardening`, items 5 to 8. Corrected 2026-10-20 (PROVE pass 4, D6): K19's code half is now its verifiers' design, the tracked-file test at the nearest git root, which keeps a user's untracked nested allowlist; see item 5 |
| The code halves of C4 (warn or refuse from a copy: the manager's call), K28 | `installer-hooks-json-robustness`, items 3 and 4 |
| K20's hook half | `codex-agents-block-refresh`, item 5 |
| K29's matcher (Monitor, PowerShell; a contract change) | `owner-deferred/mcp-tools-guard-matcher`, item 3 |

**Rejected, with the reason:**

- S-b1 — the production questions' observability topic. It repeats pass 2's reject
  spec:b4-production-questions: they widen the round without changing a stop.
- S-b2 — `gate: manual` beside `gate: owner`. It repeats pass 2's reject spec:b4-gate-manual:
  the board's own vocabulary for a person's action, within D6's intent.
- S-b3 — the docs lead with `install_plugin.py --codex`. It is not a different install:
  `--codex` adds the Codex links to the same Claude install, and D1's bare line stays
  documented (OPERATOR.md, harness/README.md).
- S-b4 — CREW.md's field record and LOOPS.md §6. Both rest on approved decisions: A3 cites
  the field record as its reason, and §6 serves M7 and M9.
- T2 — two "is KEEL on" rules. install_guard's narrower switch is by design (D4; the crew
  plan's Open question 17), and the two are documented apart.
- T3 — repeated `harness == "codex"` switches. It repeats pass 2's std:smells reject.
- T4 — `guard(raw, harness)` never reads `harness`. The module docstring says so on purpose:
  the call has the same shape for both harnesses.
- T5 — `layer_status`'s tuples are DESIGN's recorded contract behind approved P-C;
  install_plugin's report parse is a refactor for later.
- T6 — small duplications. Real, but each change would re-run the suites and mutation proofs
  for no change in behavior; folded into a later refactor.
- T8 — the name `one`, and ROLE_NEXT's `keel:helm`. It repeats std:smells (short names), and
  `keel:helm` is the skill's name, which the slash command `/keel:helm` invokes.

**Fixed by the lead in fix round 4:** C9 (PROVE-2's coverage sentence corrected, dated),
S-c2's note at PROVE-2's Spec section, C17 (the crew plan's decisions 9 and 12 point at
what superseded them), C5's half in HARNESS-PROBES (its preamble names P14's exception).
C10 is closed by a new handoff at the PROVE pass 4 stop.
