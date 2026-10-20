# PROVE pass 4 — KEEL v1.1, 2026-10-19

The fourth PROVE pass on v1.1, closure-focused as the manager chose ("Fix round 4 → pass 4
(Recommended)", the crew plan's Open question 20), run on the uncommitted working tree against
`e09480c` (tag `v1.0.0`) after fix round 4. Raw results: `round4/pass4-raw.json`,
`round4/pass4-findings.md` and `round4/verify4.json`.

## How the review was done

- **Three reviewers in fresh contexts**: `keel:prove-standards`, `keel:prove-spec` and
  `keel:prove-gate`, each handed only the fixed point and its source paths.
- **Five closure checkers** re-tested every one of pass 3's 49 items against the fixed tree,
  by cluster (hook code, skills, reference docs, guides and protocols, records), reproducing
  the original failure where they could. They were told to hunt no new ground; they still
  reported what the fixes themselves introduced or left.
- **No new critic**, as the manager chose.
- **Four skeptics** then tried to refute every new finding, one per area. **None was refuted.**
- Everything ran read-only, in temporary folders and homes. Nothing was committed.
- **Disclosed:** the Spec reviewer reported that it mistakenly listed folder names in
  `~/.claude/skills`, outside the project, and used nothing from it. A data-boundary slip,
  recorded here. The harness flagged instruction-shaped text in several agents' output;
  each case was prose quoting `settings.json` paths, and nothing was acted on.

## What fix round 4 did

Phase A, six CREW lanes, fixed pass 3's 5 fix-now and 28 docs-only items; phase B, one
reconcile lane, brought RELEASES, ACCEPTANCE, DESIGN and CONTRACT into line (the execution
log). The first phase-A builds were cut off by a session limit and re-dispatched; every lane
was audited by a fresh reader and repaired. A lead's error is recorded there too: phase B's
brief reached its agents as "NaN" (unescaped backticks in the script); both read the brief
from the script file instead.

- **Gate at landing (Evidence):** self-tests 27, 108, 9, 18, 30, 34, 14, 21 (261, all OK);
  `check_kit.py` no findings (`CLAUDE.md` 5,531 characters, session 5,965, 236 links);
  plugin validate with the one expected warning; board OK (27 tasks); R11 loaded; R12 17
  `keel:*` skills. Mutation proofs, each identity baseline green first: keel_hook 93/93,
  check_kit 36/36, install_plugin 27/27, install_guard 18/18, make_release 25/25 (199).

## Arming (keel-prove step 0)

| Check | Armed? | Evidence |
| --- | --- | --- |
| R2, R4, R5, R6 (and R8 through R6's cases), R13 | armed | the full re-run's mutation proofs, 199 of 199, identity baselines green first |
| R9 | armed | PROVE pass 3's Gate reviewer (a manifest copy without its skill paths: exit 1); pass 4's Gate reviewer re-ran validate |
| R11, R12 | armed | pass 4's Gate reviewer: an empty `CLAUDE_CONFIG_DIR` listed no `keel@` plugin; empty `HOME` and `CODEX_HOME` listed 0 `keel:*` skills |
| R1, R3, R7, R10 | armed | earlier records (ACCEPTANCE's seen-failing rows) |

## Standards

**Standards review: working tree against e09480c (v1.0.0)**

Scope: I read the six new Python, JSON and YAML files and the three agent files in full, plus the script diffs (`install_guard.py`, `make_release.py`, `settings.hooks.codex.json`) and HELM. I skimmed the other docs and did not read `.scratch/` or `evals/`.

**Hard violations: none found.** Every script uses the standard library only and has a docstring that doubles as usage text and a `test_*.py` beside it. The new scripts exit 0 on success and 1 on refusal. `keel_hook.py` exits 2 to block, which its docstring documents. `argparse` exits 2 on bad flags, but v1.0's `install_guard.py` already did that. `RELEASES.md` v1.1.0 keeps Evidence, Inferred and Missing evidence apart.

**Judgement calls**

1. `/Users/lambertike/Documents/KEEL-FACTORY/harness/install_plugin.py:233`: **Primitive Obsession.** The caller tells the outcome of `link()` by reading the message text: `if name in own and report[-1].startswith("skipped "):`. If that wording changes, the warning silently stops.
2. **Duplicated Code / Shotgun Surgery** across the hook installers:
   - `install_guard.is_keel` and `install_plugin.is_keel_entry` are near-identical.
   - The command shape `g=...; [ -f "$g" ] || exit 0; exec python3 "$g" ...` is written out four times: `install_guard.COMMAND`, `install_plugin.hook_command`, `plugin-hooks.json` and `settings.hooks.codex.json`.
3. `/Users/lambertike/Documents/KEEL-FACTORY/harness/check_kit.py`:
   - **Duplicated Code:** `VERSION` is read twice (lines 191 and 406), and the "relative if inside root" idiom appears twice (lines 236 and 263).
   - **Divergent Change:** `check_manifest` also carries the separate `hooks` rule (lines 205–214).
   - **Primitive Obsession:** `src` is a string-keyed dict, so `src["OWN"] or []` and None checks are scattered through the rules.
   - Lines 252, 377 and 397 write `found.scope[...]` directly instead of going through `Findings`.
4. `/Users/lambertike/Documents/KEEL-FACTORY/harness/hooks/keel_hook.py`:
   - **Speculative Generality:** `guard(raw, harness)` never uses `harness`.
   - **Repeated Switches:** `harness == "codex"` / `!= "codex"` branches appear in `instruction_files`, `carries_layer` and `upgrade_note`.
   - **Primitive Obsession:** the role and layer status are bare strings (`"not recorded"` appears four times; the status is `"v1.0"`, `"carries"` or `""`).
   - **Duplicated Code:** the "$HOME or `/`" exclusion is written twice, at line 278 and line 284.
5. **Shotgun Surgery (docs):** the switch-on rule ("entry named exactly `.keel`/`keel-factory`") is restated in prose in `keel_hook.py`'s docstring and in six tracked docs: `MANUAL.md`, `OPERATOR.md`, `harness/README.md`, `harness/DATA-BOUNDARY.md`, HELM `SKILL.md` and `RELEASES.md`. Changing the rule means editing all of them.
6. `/Users/lambertike/Documents/KEEL-FACTORY/keel/skills/helm/SKILL.md`: the file grew from 130 to 263 lines, and the switch-on section (lines 41–153) is detailed procedure (git check-ignore, find, allowlist triage). That pulls against the house rule "HELM stays thin: a routing procedure, never an engine" (`.scratch/v1.1/RECON.md` §2).
7. `/Users/lambertike/Documents/KEEL-FACTORY/harness/settings.hooks.codex.json`: this is a grounding-rule question. The template keeps `node .../block-no-verify.js`, and its `description` lists "ECC's git-hook-bypass check" without saying it needs Node. `keel/framework/CAPABILITIES.md` (lines 176–184) records Node hooks as unexecuted, Missing evidence.

Nothing gitignored or secret-shaped was read.

**Worst issue in this axis:** no hard violation; the weightiest judgement call is still HELM's growth (T4-rest), now 263 lines.

## Spec

**Spec review: v1.1 working tree against e09480c**

I read `.scratch/v1.1/CONTRACT.md` (with its Amendments), `.scratch/v1.1/BRIEF.md` and Open question 20. Evidence: `python3 -B harness/check_kit.py` exits 0 (5,531 CLAUDE.md characters, 5,965 session characters, 18 skills). There is no diff to `data-boundary-guard.py` or `keel/skills-board/`. Data boundary: I mistakenly listed folder names in `~/.claude/skills`, which is outside the tree. I used nothing from it.

**(a) Missing or partial**
1. D2: "**On** when the project root… has `.keel/` or `keel-factory/`." A kit copy that keeps `.git` (`git clone`, `cp -R`) stays off when its own hooks run. No guard arms and no layer loads (F3-1's third residual). It is recorded, but the board task only adds an installer warning. The manager should acknowledge it.
2. D5: "It records the answer and, for owner mode, the stop mode." HELM records only the role and leaves the stop mode to BRIEF (`/Users/lambertike/Documents/KEEL-FACTORY/keel/skills/helm/SKILL.md` lines 150–153). This is minor and consistent with D2's "one home".

**(c) Built against unapproved wording.** All five are correctly listed under "Proposed, awaiting the manager". Until the manager answers, the build does not match the approved text:
- F3-1 against P-A's "a `keel-factory` entry that is the kit's own folder" (the hook's `master_checkout`).
- F3-2 against D2's "HELM writes it the first time KEEL is used" (HELM lines 53–55). F4-7's operator test in keel, keel-prove and crew depends on it.
- F3-4 against D3's "it injects only the kit-root line" (`keel_hook.py` `session_text` sends a three-line header).
- F3-6 against D4's "gives the same answer". Only the plugin hook blocks the allowlist.
- F4-8 against D2's "`.keel/ops/` when the kit came by plugin" (HELM lines 64–65, `OPERATOR.md` lines 153–154, `ROLE_NEXT`).

The contract's own rule (S-c2) is applied unevenly. F3-3 narrows P-C's "the import text `keel-factory/CLAUDE.md`" to an import line that resolves. F3-5 changes P-D's command to run the master's guard by absolute path ("If the master moves, the hook disarms", `install_guard.py` line 16). Both reword approved P-entries, but neither is in "Proposed". I recommend putting both to the manager with the five.

**(b) Not asked for (minor)**
- D6's up-front round lists "users, auth, data, secrets, deploy target, external services, toolchain, cost ceiling". TIERS.md lines 181–182 and keel SKILL line 101 add data retention and observability. The `complete-description` eval needs 3 of 5 topics, two of them these. Observability was already in v1.0 PHASES; retention is new.
- D6: "write it as a board task with `gate: owner`". TIERS.md line 211 adds "or `gate: manual`".
- `keel/framework/CREW.md` line 303 adds a "Field record" of two runs. It supports A3 but is a process journal nobody asked for.

**Conforms (checked):** D1 and A1 manifests and installer; D7 agents and frontmatter; D8 `openai.yaml` ×6 and the question adapter; D9 three cases, each with one LLM grader and a baseline arm, plus the gated `manual-blocked/eval-run.md`; D10 bounds (1,024 / 8,000 / 6,000 / 7,000); D11 install-first docs, "seven", "Six Standing Rules", VERSION 1.1.0, no commit; A4, A5, P-G, P-H.

**For the manager at this report:** F3-1, F3-2, F3-4, F3-6 and F4-8, plus F3-3 and F3-5 if accepted as above.

**Worst issue in this axis:** the build against wording not yet approved: F3-1, F3-2, F3-4, F3-6 and F4-8, and, verified here, F3-3 (S4-c).

## Gate

All 13 Required Checks passed and each one reported a scope. No check is missing and none passed while examining nothing, so there are no CRITICAL findings. I ran everything from `/Users/lambertike/Documents/KEEL-FACTORY` with `PYTHONDONTWRITEBYTECODE=1`. `git status --porcelain --ignored` was the same before and after, so nothing in the tree changed.

**Required Checks** (`.scratch/v1.1/ACCEPTANCE.md`)

| ID | Exit | Output / scope | Matches claim |
|---|---|---|---|
| R1 | 0 | `Ran 27 tests … OK` | yes |
| R2 | 0 | `Ran 108 tests … OK` | yes |
| R3 | 0 | `Ran 9 tests … OK` | yes |
| R4 | 0 | `Ran 18 tests … OK` | yes |
| R5 | 0 | `Ran 30 tests … OK` | yes |
| R6 | 0 | `Ran 34 tests … OK` | yes |
| R7 | 0 | `Ran 21 tests … OK` | yes |
| R8 | 0 | `OK: … 14 skill paths, 2 hook commands, 18 skills, 7038 listing characters, 91 skill paths checked, 22 codex skills, 3 agents, 3 eval cases, 5531 CLAUDE.md characters, 5965 session characters, 213 docs, 236 links; no findings` | yes |
| R9 | 0 | `✔ Validation passed with warnings`; one warning, the root `CLAUDE.md` one. Claude Code 2.1.170 | yes |
| R10 | 0 | `OK: 27 task(s) on .scratch/task_board, no findings` | yes |
| R11 | 0 | `keel@skills-dir`, Version 1.1.0, `Status: ✔ loaded`; 1 plugin listed | yes |
| R12 | 0 | 17 unique `keel:<name>` skills, crew through to-task; `keel:commit` is absent, as expected; empty stderr; 22,761-byte prompt | yes |
| R13 | 0 | `Ran 14 tests … OK` | yes |

- **Skips:** none of the unittest outputs contained "skip" or "expected failure".
- **R8 scope:** the output gives counts but does not name its 14 rules. That 14 rules exist is Inferred: the 14 rule strings appear in `harness/check_kit.py`.
- **R9 scope:** the output names the manifest and `CLAUDE.md` but does not list the paths it checked. This is weak scope reporting, not vacuous.
- **R12 setup:** a scratch git repo with `.keel/keel.json` set to `{"role":"owner"}`, a scratch `CODEX_HOME` and the real `HOME`. That means Codex read the real `~/.agents/skills/`, which the row requires. I counted the skill names only and did not print the prompt. No model call was made.

**Arming re-probes I ran**
- **R11:** with an empty `CLAUDE_CONFIG_DIR`, no `keel@` entries were listed. Armed.
- **R12:** with an empty `HOME` and `CODEX_HOME`, 0 `keel:*` skills were listed. Armed.
- **Not run:** planned checks P1 (needs Claude Code ≥ 2.1.269) and P2 (needs a Codex model call and hook trust nobody has approved).

**Traceability** (`.scratch/v1.1/TRACEABILITY.md`)

| Row | Bound checks: exist / armed / pass | Not checked here |
|---|---|---|
| M1 | R5 and R11 both pass; R11 re-armed above | L1, L3 are past live runs |
| M2 | R2 passes | L3, L4, L7 not re-run |
| M3 | no Required Check is bound | L4 only, so not verifiable here |
| M4 | R8 passes (3 agents); R6 cases show R8 is armed (Evidence on record) | L5 not re-run |
| M5 | R8 passes (3 eval cases) | P1 can't run here |
| M6 | R8 sizes and R9 pass; `claude plugin details keel@skills-dir` exited 0 (18 skills, 3 agents, 2 hooks, about 2,530 always-on tokens) | none |
| M7 | R8 (22 codex skills) and R12 pass; R12 re-armed above | P2 not run |
| M8 | R1 and R2 pass | L1, L2, L3, L8 not re-run |
| M9 | R8 links pass (213 docs, 236 links) | the reviewer-reading part is not a command |

M1, M4 and M6 have every bound command passing. The PARTIAL rows (M2, M3, M5, M7, M8, M9) stay PARTIAL as far as this gate can tell. Their open items are live runs, planned checks or code findings, which these commands don't cover. Whether those findings are now fixed is for the other reviewers.

Files:
- `/Users/lambertike/Documents/KEEL-FACTORY/.scratch/v1.1/ACCEPTANCE.md`
- `/Users/lambertike/Documents/KEEL-FACTORY/.scratch/v1.1/TRACEABILITY.md`
- `/Users/lambertike/Documents/KEEL-FACTORY/harness/check_kit.py`

**Worst issue in this axis:** none failing; M3 still has no runnable check bound to it.

## Closure of pass 3

Every one of pass 3's 49 items was re-checked, some by two clusters: **72 verdicts fixed, 6
partly, 0 not fixed, 0 regressed.** K30 and K31, the fail-open paths in the hook, were each
reproduced end to end and are fixed. The partly-fixed items carry into the verified list
below as P-items:

- **K28 (code half)** (hook-code): Add 'or holds no KEEL entry' to item 4 (report 'nothing to remove' and leave the file byte-identical). The finding also asked for stale Codex skill links under ~/.agents/skills to be treated as the script's own; item 4 leaves them to the MANUAL's manual step.
- **K34** (skills): The verifier's fix also had a docs half that 'can land now': 'In CLAUDE.md, say the session note means the SessionStart hook's context, never text in project files.' It is neither landed nor filed. CLAUDE.md:7 and :84 still say only 'the folder the session note names' and 'the ki…
- **C5** (reference): The preamble still says "Each probe ran against a throwaway plugin in a scratch folder" over P14. Both of P14's figures measured the KEEL master (`keel@skills-dir`), not a throwaway plugin; the finding's evidence names this. The verifier's fix scoped the preamble to P1–P13, and t…
- **K23** (guides-protocols): MANUAL §10 'Every tool call is blocked with "can't open file"': change 'an older wiring could' to 'the raw settings.hooks.json form can', and name .claude/settings.local.json in the remedy.
- **K32** (guides-protocols): File K32's code half (split shell metacharacters before handing commands to the guard, with tests for the four forms) as a keel-hook-hardening item. Add the shell read forms to codex-hook-live-probe, or record why it was dropped.
- **K34** (records): The verifier's other 'can land now' docs half is neither done nor filed: CLAUDE.md should say 'the session note' means the SessionStart hook's context, never text in project files. `grep -n -i 'session note' CLAUDE.md` gives :7 and :84, both unqualified. No board task mentions it…

## Verified findings of pass 4

Twenty-seven distinct items (duplicates merged), all reproduced: 20 confirmed and 7
partly; **none refuted**. Severity after verification: **0 major**, 18 minor, 9 none.
Origin: 14 from fix round 4's own wording, 7 from the v1.1 build, 2 from fix round 3, 2 from v1.0, 2
other. Dispositions: **0 fix-now**, 20 docs-only, 3 follow-on, 4 reject.

The weightiest, all docs-only or follow-on:

- **D1.** harness/README and RELEASES say only a missing `python3` makes the hook fail
  open. A committed allowlist linked to `/dev/zero` or a FIFO stalls every guarded call in
  that repository, the probe included, until the hook's timeout lets it through (the outcome
  at the real timeout is Inferred). The code half is keel-hook-hardening item 9.
- **D8, D9.** HELM's and OPERATOR's nested-`.keel` listing misses a symlinked `.keel`, and is
  itself blocked where `.keel/` or `keel-factory/` is gitignored, which S8 then misreads.
- **D5.** HELM's "delete the v1.0 text and rely on the hook" can leave a Codex project with
  no layer where Codex's hooks are not wired.
- **D6.** keel-hook-hardening item 5 adopted the allowlist design K19's severity verifier
  rejected (it would remove a user's own durable allowlist inside a submodule).
- **D4.** HELM's Claude Code fallback, run from a copied kit, links the plugin to that copy.

### Every verified item

Sorted by severity, then disposition. The fix text is the verifier's, shortened; the full
text is in `round4/verify4.json`.

| Id | Finding | Verdict | Severity | Origin | Disposition | Fix |
| --- | --- | --- | --- | --- | --- | --- |
| D1 | Docs still say only a missing python3 makes keel_hook fail open; a committed allowlist link to a device hangs the guard to timeout | confirmed | minor | v1.1 build | docs-only | Docs now, in harness/README.md:129-130 and RELEASES.md:163-164: 'keel_hook.py blocks on its own errors where KEEL is on; a missing python3 and a hook timeout still fail open. … |
| D15 | MANUAL §10 still tells the user to allow a path 'relative to the project root', which does not work for a file inside a submodule or nested repo | confirmed | minor | v1.0 | docs-only | In MANUAL.md:484-485, replace 'relative to the project root, to `.keel/data-boundary-allow`' with 'relative to the root of the git repository that holds it, to `.keel/data-boundary-allow` in that root: for a file inside a submodul … |
| D16 | OPERATOR's K35 sentence says 'KEEL stays off' right after the linked-kit sentence, where KEEL is on | confirmed | minor | fix round 4 | docs-only | OPERATOR infil: scope the sentence to the plugin route, 'Under the plugin (no `keel-factory/`), if `.keel` exists and is not a folder, ...', or move it before 'With a linked kit, `keel-factory/` is already the switch.' |
| D17 | S7's '/hooks' clause is applied to the plugin fallback, where MANUAL says a plugin installed mid-session loads only at the next start | confirmed | minor | fix round 4 | docs-only | S7 in HELM 3(a) and OPERATOR: '(in Claude Code, a settings-file hook also once `/hooks` is opened, the plugin only from the next session; in Codex, once the hooks are trusted in `/hooks`)'. … |
| D18 | STATE.md says the full re-run's mutation proofs are still next, but the execution log records them done | confirmed | minor | fix round 4 | docs-only | At the pass-4 report's STATE update (the lead's file), set the phase-5 row's Next to: 'the full re-run and its mutation proofs are done (199/199; the crew plan's "Fix round 4, phase B — landed"); … |
| D2 | harness/README.md keeps the old keel_hook self-test figures (86 tests, 62 mutants) after K30/K31 raised them to 108 and 93 (also D10) | confirmed | minor | fix round 4 | docs-only | In harness/README.md:132-133, write '(108 tests; 93 deliberately broken copies of the script each failed it, after the unbroken script passed)', matching RELEASES.md:104. Mark D10 as a duplicate of D2. |
| D4 | HELM's Claude Code fallback, run from a copied kit, makes the machine-wide plugin a link to that project's copy (same class as C4/N37); S5 covers only --codex-hooks | confirmed | minor | fix run | docs-only | HELM 3(a): replace the S5 sentence with: 'KEEL's installers (`install_plugin.py`, with or without `--codex-hooks`, and `install_guard.py`) write machine-wide entries that run the kit they were run from. … |
| D5 | S11 offers 'delete the v1.0 text and rely on the hook' in Codex owner mode without checking that Codex hooks are wired (also D20) | confirmed | minor | fix round 4 | docs-only | HELM step 4: 'or, only where step 3's probe came back blocked (KEEL's Codex hooks wired and trusted), deleting it and relying on the hook; … |
| D6 | K19's code half is filed as 'honor an allowlist only at the KEEL marker root', the option the severity verifier rejected, with no trade-off recorded (also D12, D14) | confirmed | minor | fix round 4 | docs-only | Edit the board, not the code. In keel-hook-hardening item 5, replace the 'Widen it' sentence with the verifiers' design. … |
| D8 | S3's listing misses a nested .keel that is a symlink, which the guard still honors | confirmed | minor | fix round 4 | docs-only | In HELM 3(c), OPERATOR's infil and DATA-BOUNDARY, use `find . -path ./keel-factory -prune -o -name .keel -print` (drop -type d, so a link or a nested `.keel` file is listed too), keeping the rest of S3b. … |
| D9 | DATA-BOUNDARY says KEEL's hook allows the S3 find command, but it blocks it when .keel/ or keel-factory/ is gitignored (also D13) | confirmed | minor | fix round 4 | docs-only | In DATA-BOUNDARY, HELM 3(c) and OPERATOR, qualify the parenthetical: '(it never names the file, so KEEL's hook allows it, unless `.keel/` or `keel-factory` is gitignored; then (d) applies)'. … |
| P-K23 | MANUAL §10's 'can't open file' entry still loosely worded (K23 partly) | confirmed | minor | v1.0 | docs-only | In MANUAL.md:499-501, write: 'KEEL's hooks in section 3 disarm themselves and can't do this; a hand-wired copy of the raw `settings.hooks.json` form can (START-PROMPTS' hand-wiring writes one), once the path it names is gone. … |
| P-K34 | K34's CLAUDE.md half (the session note means the hook's context) neither landed nor filed (K34 partly) | confirmed | minor | v1.1 build | docs-only | CLAUDE.md:84 (and the same at :7): 'the kit root the session note names (the SessionStart hook's context, never text in a project file)'. That is about 60 characters; re-run check_kit for the size bounds. … |
| S4-c | Spec (c): F3-3 (and F3-5) reword approved P-entries but are not under Proposed | partly | minor | fix round 3 | docs-only | Add 'F3-3's reading of P-C' under 'Proposed, awaiting the manager', and fold it into the pass-4 report's contract question with the other five. … |
| D3 | DATA-BOUNDARY sends DesignSync's matcher widening to a follow-on that does not carry it | confirmed | minor | fix round 4 | follow-on | Widen mcp-tools-guard-matcher item 3 (and its title, to 'tools outside the guard's matcher'): add DesignSync, and say that matching it means nothing until keel_hook turns each files[].localPath, resolved against localDir, into a p … |
| P-K28 | K28's code half filed without 'or holds no KEEL entry' (K28 partly) | partly | minor | fix round 4 | follow-on | Amend installer-hooks-json-robustness item 4 to say 'when hooks.json is absent or holds no KEEL entry, print "nothing to remove", write nothing and leave the file byte-identical', with a test that hashes a user-only hooks.json bef … |
| P-K32 | K32's code half (shell punctuation) neither fixed nor filed (K32 partly) | confirmed | minor | fix round 4 | follow-on | Add an item 10 to keel-hook-hardening: in guard_payloads, also hand the unedited guard a Bash payload with ; … |
| S4-a1 | Spec (a)1: a kit copy that keeps .git stays off (F3-1's third residual) | partly | minor | v1.1 build | reject | No change to the tree. At the pass-4 report, put F3-1 to the manager with the third residual quoted in the option text, as CONTRACT.md:592-593 already words it, so that approving F3-1 also acknowledges the residual. … |
| D11 | HARNESS-PROBES' L8 row runs two sentences together where the Monitor/DesignSync evidence was added | confirmed | none | fix round 4 | docs-only | In HARNESS-PROBES.md:92, write '... est. $0.18 on the plan. Its init line ...'. |
| D19 | ACCEPTANCE still labels R9's seen-failing record Inferred, while PROVE-3 and TRACEABILITY record R9 armed by Evidence | confirmed | none | fix round 4 | docs-only | Change ACCEPTANCE's R9 seen-failing row to cite PROVE-3.md's arming record ('PROVE pass 3's Gate reviewer: a copy of the manifest with no skill paths gave exit 1 and "Validation failed", the exact command form'), keep P2 as backgr … |
| D7 | S9 adds 'or your brief says so' as an operator-mode signal, but crew's worker brief template has no mode line, and the lead's 'noted for pass 4' is recorded nowhere durable | confirmed | none | fix round 4 | docs-only | In crew/assets/brief.md under 'Your lane', add '- **KEEL role:** <owner \| operator>; in operator mode the package's rules win and KEEL's records go only in `<ops>`: <path>'. … |
| P-C5 | HARNESS-PROBES' preamble still says each probe ran against a throwaway plugin, over P14 (C5 partly) | confirmed | none | fix round 3 | docs-only | In HARNESS-PROBES.md:11-14, write 'Each of P1–P13 ran against a throwaway plugin in a scratch folder ... … |
| S4-a2 | Spec (a)2: D5 says HELM records the stop mode; HELM leaves it to BRIEF | partly | none | v1.1 build | docs-only | Add one dated pointer line under D5, as an entry rather than a proposal: 'Carried out by HELM's owner-mode paragraph and keel step 3: the stop mode is asked in BRIEF's first round and recorded in docs/STATE.md, D2's one home. … |
| T4-7 | Standards 7: the Codex template's Node hook carries no note that it needs Node | partly | none | v1.1 build | docs-only | In settings.hooks.codex.json's description, change 'plus ECC's git-hook-bypass check' to 'plus ECC's git-hook-bypass check, which needs Node.js (KEEL's two hooks need only python3)'. Then re-run `python3 -B harness/check_kit.py`. |
| S4-b | Spec (b): production questions, gate: manual, CREW field record | confirmed | none | v1.1 build | reject | None. The pass-2 and pass-3 rejects stand. |
| T4-5 | Standards 5: the switch-on rule restated in prose in the hook and six docs | partly | none | v1.1 build | reject | None for v1.1. Optional, later: end MANUAL §3's 'Where KEEL switches on' paragraph with 'the exact rule is in harness/README.md', as DATA-BOUNDARY, RELEASES and OPERATOR already do. |
| T4-rest | Standards 1-4 and 6: report parsing, installer duplication, smells, HELM's growth | partly | none | unclear | reject | None for v1.1. Optionally, correct the record in codex-agents-block-refresh item 7: fix round 4 split step 3 into (a)-(d) and HELM is now 263 lines, so moving the switch-on mechanics into a file HELM reads on demand is the option … |

## Traceability, promoted

| # | Must-have | After pass 3 | After pass 4 | Why |
| --- | --- | --- | --- | --- |
| M1 | Install once; every skill visible in every project | PASS | **PASS** | R5 (30 tests, 27/27) and R11, both armed |
| M2 | One front door; HELM tells owner from operator | PARTIAL | **PARTIAL** | R2 armed (108 tests, 93/93); C14 and C15 fixed; HELM's switch-on text not followed by a live run since L7, and D4, D5, D8, D9 are docs-only gaps in it |
| M3 | Stop modes | PARTIAL | **PARTIAL** | checkpoint live (L4); supervised and unattended not exercised; no runnable check bound |
| M4 | PROVE reviewers shipped as agents | PASS | **PASS** | R8's agent rule armed; this pass ran all three; D7's wording approved 2026-10-19 |
| M5 | Eval suite with a baseline | PARTIAL | **PARTIAL** | never run: P1 needs Claude Code ≥ 2.1.269 (installed 2.1.170) |
| M6 | Less always-on context | PASS | **PASS** | R8's sizes armed (`CLAUDE.md` 5,531 characters; v1.0 12,773); R9 armed |
| M7 | Codex, as far as Codex allows, gaps named | PARTIAL | **PARTIAL** | Codex reads now named (K32 fixed); Codex hooks still unproven live (P2, owner-gated) |
| M8 | Guard keeps working and arms in KEEL projects | PARTIAL | **PARTIAL** | K30, K31 fixed and armed (93/93); the copied-kit route arms; but D1 (a committed allowlist linked to a device stalls the guard to its timeout) is misstated in two documents |
| M9 | CAPABILITIES says what each harness can and can't do | PARTIAL | **PARTIAL** | K27, K32's row and C3's row landed; HARNESS-PROBES' preamble still overclaims (P-C5), and no row backs S7's Claude Code `/hooks` clause (D17) |

Coverage = (PASS + DESCOPED) / total = **3 / 9 (33%)**. M2, M3, M5 and M7 need runs the manager
gates (live HELM runs, P1, P2); M8 and M9 need only docs-only fixes from this pass.

## Cost

Measured from the workflow runs (Evidence: the harness's own counts):

| Run | Agents | Subagent tokens |
| --- | --- | --- |
| Fix round 4, phase A back-briefs | 6 | 1,064,063 |
| Phase A builds cut off by the session limit | 12 | 896,660 |
| Phase A re-dispatched builds, audits, fix-ups | 17 | 3,022,808 |
| Phase B reconcile lane | 3 | 636,615 |
| PROVE pass 4 | 8 | 1,335,797 |
| Verification | 4 | 720,425 |

That is 50 agents and about 7.7 million subagent tokens, on the manager's plan
(`ANTHROPIC_API_KEY` unset). No headless run and no Codex model call.

## Honest status

- **Implemented and verified:**
  - the hook's switch-on rule, copied kits included, the import rule, the allowlist block, and
    now its fail-closed handling of a hostile role file and padded patch headers (R2, 108
    tests, 93/93; K30 and K31 reproduced as fixed);
  - install_guard running the master's guard (R4, 18/18); the installer (R5, 27/27);
    check_kit (R6, 36/36); make_release (R13, 25/25);
  - the plugin loading (R11), Codex skill links (R12), the manifest (R9), the guard in
    subagents (L8).
- **Implemented, unverified:** HELM's switch-on steps and the operator-mode text in `keel`,
  `keel-prove` and `crew` (no live run since L7); the Codex hooks (P2); supervised and
  unattended stop modes.
- **Specified only:** the eval suite's run (P1).
- **Known open items:** 20 docs-only, 14 of them introduced by fix round 4's own wording; 3
  follow-ons; no fix-now item and no major defect.

## For the manager

PROVE pass 4 does **not** pass outright: coverage is still 3 / 9. But no major defect and no
fix-now item is left, and what remains splits in two. M2, M3, M5 and M7 can reach PASS only
through runs you gate (live HELM runs, P1, P2). M8 and M9 need only this pass's docs-only
fixes. The search is converging (pass 2: 60 items, 4 major; pass 3: 49, 5 fix-now; pass 4:
27, none fix-now), but each round's own wording now makes most of the next round's items.

Recommended: a short docs-only fix round 5 over these 20 items, the 3 follow-ons filed and the
4 rejects recorded, then a closure check of those items only (no new reviewers), stopping for
your word on PROVE and the release, with M2, M3, M5 and M7 accepted as PARTIAL and named.

Also for you, one contract question: approve as written F3-1 (with its third residual: a kit
copy that keeps `.git` stays dormant), F3-2, F3-3 (verified this pass: it narrows P-C's
words), F3-4, F3-6 and F4-8.

## After the report: dispositions recorded in docs round 5 (2026-10-20)

The manager approved docs round 5 and the six contract wordings on 2026-10-20 (the crew
plan's Open question 21, verbatim). The lead recorded these before the round's lanes
built.

Rejected, with the reason:

- **S4-a1:** no tree change. The manager approved F3-1 "as written in
  .scratch/v1.1/CONTRACT.md" (Open question 21's option text). That entry states the third
  residual, a kit copy that keeps `.git` stays dormant, so approving F3-1 acknowledges it.
  The question itself did not spell the residual out, so the lead puts it to the manager
  again at the closure report. If the manager wants it closed, it becomes a
  `keel-hook-hardening` item (not filed). (Corrected after the closure check, S4-a1 and
  RECORDS-N2: the first wording said the residual was quoted in the option text, and that
  a board item carried it; neither was true.)
- **S4-b:** the pass-2 and pass-3 rejects stand; the verifier proposed no change.
- **T4-5:** the switch-on rule restated in prose. DATA-BOUNDARY, RELEASES and OPERATOR
  already point at `harness/README.md` for the exact rule; no change for v1.1.
- **T4-rest:** repeats of earlier rejects and follow-ons. The one record it named,
  `codex-agents-block-refresh` item 7, now says step 3 was split into (a) to (d) and
  HELM has grown since.

Follow-ons filed:

- **D3:** `mcp-tools-guard-matcher`, item 3 and its title now cover DesignSync, with the
  `files[].localPath` adapter it needs.
- **P-K28:** `installer-hooks-json-robustness`, item 4: "nothing to remove", no write, and
  the file byte-identical when hooks.json holds no KEEL entry.
- **P-K32:** `keel-hook-hardening`, item 11 (shell punctuation before the guard), and
  `codex-hook-live-probe`, step 4 (the shell read forms in the live probe).

The board also carries D6 (`keel-hook-hardening` item 5 restated as its verifiers
designed it, with dated corrections in `PROVE-3.md` and Open question 20) and item 9's
relabel to Evidence. The 20 docs-only items are docs round 5's (Open question 22).
