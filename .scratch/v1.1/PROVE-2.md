# PROVE pass 2 — KEEL v1.1, 2026-10-18

The second PROVE pass on v1.1, run on the uncommitted working tree against `e09480c`
(tag `v1.0.0`) after the fix run planned in `PROVE-FINDINGS.md` and carried out under
`.scratch/task_board/crew-plan-prove-fixes.md`.

## How the review was done

- **Three reviewers in fresh contexts**: the plugin's own agents `keel:prove-standards`,
  `keel:prove-spec` and `keel:prove-gate`, each handed only the fixed point and its source
  paths, nothing of the session that made the fixes.
- **Four closure checkers** re-tested every pass-1 finding against the fixed tree,
  reproducing the original failure where they could, and judged each fix against the
  decision recorded for it.
- **One fresh critic** read the user guides as a new user would, for Claude Code and
  Codex, followed them in temporary folders, and probed the hook for bypasses.
- **Ten skeptics** then tried to reproduce or refute every new or remaining finding (45
  from the checkers and the critic, 15 from the Standards and Spec reports): one per
  claimed major, one per area for the minors. **None was refuted**; each was dated to the
  v1.0 release, the v1.1 build, or this fix round.
  *Corrected 2026-10-19 (PROVE pass 3, C9): the skeptics verified 42 of the checkers' and
  critic's items and 18 reviewer items. N10, N12 and N20 were never given to a skeptic, so
  they got no disposition; N12 and N20 were closed by the STATE.md rewrite, and N10 is
  pass 3's C10 (`PROVE-3.md`).*
- Everything ran read-only against the master. Nothing was committed.

## What the fix run did

Disposition rows 1–11 and 13 were carried out in two phases of CREW lanes (nine write
lanes, a reconcile lane and the lead's lane). Each phase was fenced by a snapshot diff and
gated before the next started. Row 12's amendments are in `CONTRACT.md`. Evidence:

- **Self-tests:** guard 27, keel_hook 76, link_kit 9, install_guard 13, install_plugin 28,
  check_kit 34, make_release 13 (new), check_lanes 21. 221 tests, all OK; 133 before.
- **Mutation proofs:** every broken copy was caught, each run with the unbroken suite green
  first on the same kit: keel_hook 49/49, check_kit 36/36, install_plugin 22/22,
  install_guard 11/11 (R4 now seen failing), make_release 19/19 (R13). 137 in all.
- **Kit checks:** `check_kit.py` reports no findings (80 skill paths, 22 Codex skills, 228
  links). `claude plugin validate` passes with the one expected warning. The board has no
  findings. R11 shows the plugin loaded. R12 lists 17 `keel:*` skills.
- **Live run L8 (row 11),** in `keel/framework/HARNESS-PROBES.md`: under the installed
  plugin, a `general-purpose` and an `Explore` subagent each had their Read of `.env`
  blocked; the fake value never reached the trace.

## Standards

**Standards review: working tree against e09480c (v1.1)**

**Hard violations (documented standard)**

1. `/Users/lambertike/Documents/KEEL-FACTORY/harness/hooks/keel_hook.py:85`: breaks the RECON §2 Scripts rule ("a docstring that is the usage text"). The script prints its own `USAGE` constant, not `__doc__`, and docstring lines 4-5 repeat the same usage by hand. The other scripts pass `description=__doc__`. Severity is low, and the v1.0 guard script set the same precedent.
2. `/Users/lambertike/Documents/KEEL-FACTORY/.scratch/v1.1/tools/mutate_hook.py` breaks Rule 6 (Instrument): it cannot run. Its anchors `project_carries_layer(state.root)` and `(folder / ".git").exists()` no longer appear in keel_hook.py (grep count 0), so `assert old in src` fails before any broken copy is tried. `mutate.py` with `mut-hook.json` replaces it, so this file is dead and duplicated. Delete it or fix it.
3. `/Users/lambertike/Documents/KEEL-FACTORY/.scratch/v1.1/tools/mutate.py:5-6`: the docstring says "the whole kit is symlinked except the script", but the code runs `shutil.copytree(..., symlinks=True)`, which makes a full copy. The docstring does not match what the code does.

**Judgement calls (baseline smells)**

- **Shotgun Surgery / Duplicated Code:** the hook command text, `statusMessage` strings and `"Bash|apply_patch"` are written three times: `harness/plugin-hooks.json`, `harness/settings.hooks.codex.json`, and `install_plugin.py:121-123,167-172`. No test checks that the template matches the installer. The matchers have already drifted: `plugin-hooks.json` matches `MultiEdit`, `install_guard.py` `MATCHER` does not, yet `keel_hook.WRITE_TOOLS` blocks MultiEdit writes.
- **Duplicated Code (mitigated):** the plugin.json `skills` list repeats `install_plugin.BOARD`. check_kit's `skill-set` rule cross-checks them, so this is acceptable. The path literal `keel/skills-board/{claude,codex}` is repeated at check_kit 264, 270 and 306, and install_plugin 111 and 213.
- **Repeated Switches / Primitive Obsession:** keel_hook branches on the string `harness == "codex"` in `instruction_files` (246), `carries_layer` (255) and `upgrade_note` (270).
- **Speculative Generality:** `guard(raw, harness="claude")` (364) never reads `harness`, and the docstring says so.
- **Data Clumps / Primitive Obsession:** in check_kit, `(root, src, found)` travels together through five checks, and `src` is a `dict[str, object]` keyed by the strings `"OWN"`, `"BOARD"`, `"DOCS"` and `"LAYER_MARK"`. VERSION is read twice (191, 406).
- **Feature Envy (minor):** `check_skills` and `check_always_on` write `found.scope[...]` directly instead of going through `Findings`.
- **Inconsistency:** `install_plugin.py` is the only new script whose docstring leaves out "Self-test: test_install_plugin.py, beside this file". The others include it.
- **Mysterious Name:** `ours()` (install_plugin 65), `one` (keel_hook 371), and `r` and `l` in both mutate scripts. The mutate scripts also put several imports on one line and have no self-test beside them. They are scratch files, so this is low priority.

**What complies**

- The vendored `keel/skills-board/` folder does not appear in the diff (Evidence: `git diff --stat`).
- Grounding rule: `evals/README.md` and `MANUAL.md` say `claude plugin eval` needs 2.1.269 or later, and results are labelled Missing evidence. CAPABILITIES.md labels and sources every row.
- The RULES.md "Six" title and the TIERS.md "seven" contradictions from RECON finding 9 are fixed.
- The phases are unchanged; stop modes add no phase.
- RELEASES.md v1.1 lists Evidence, Inferred and Missing in separate sections.

I did not read anything gitignored or shaped like a secret.

**Worst on this axis:** hook command text written in three places, with the MultiEdit
matcher already drifting between the plugin and `install_guard.py` (verified minor;
follow-on).

## Spec

**Spec review: v1.1 working tree against e09480c**

What I ran (Evidence): I copied the working tree to my scratchpad and ran `check_kit.py` there with no findings. Seven of the eight suites passed: keel_hook 76 (1 skipped), check_kit 34, install_plugin 28, make_release 13, install_guard 13, guard 27, link 9. I did not run the crew lane-checker suite (21 tests). The guard file `data-boundary-guard.py` has not been edited.

**(a) Missing or partial**
1. D2 says "HELM writes it the first time KEEL is used in a project", and D5 says "It records the answer". When the kit is linked as `keel-factory/`, HELM is told to "decide the role the same way, record nothing" (`/Users/lambertike/Documents/KEEL-FACTORY/keel/skills/helm/SKILL.md`). The hook then reports the role as `kit`, so the role is worked out again every session.
2. D2 says "are removed at exfil". OPERATOR.md §4 leaves `.keel/` in place for the user to delete. That matches only P-H, which is not approved.

**(b) Not asked for**
1. D7 says the reviewer prompts are "moved, not rewritten". P-E itself admits to one added sentence. The real additions in `/Users/lambertike/Documents/KEEL-FACTORY/agents/prove-*.md` go further:
   - new opening paragraphs;
   - instructions for reviewing uncommitted work;
   - the Gate's rules on not editing checks and not running outward-facing ones;
   - data-boundary items 1 and 2;
   - "Do not edit any file".
2. In `make_release.py`, the restore steps in README-FIRST changed to `git clone --branch main` plus `describe --tags`. No decision asks for this. It depends on P-F, which is not approved.
3. `settings.hooks.codex.json` drops `config-protection.js` and the `cost-tracker` Stop hook. §4 says the Node hooks are "(unchanged; not in scope)". D8 allows changes only to "whatever the Codex docs and a probe show", but the reason given is reasoning (Inferred), not a probe.
4. Smaller additions:
   - TIERS lets unattended halts be filed as `gate: owner` "or `gate: manual`"; D6 names only `gate: owner`.
   - TIERS adds observability and data retention to D6's list of production questions.
   - CREW adds a lane rule for the lead's own writes, which A3 does not cover.
   - `keel_hook.py` blocks calls when its own code fails, which D4 does not mention.
5. Every proposed amendment is already in the tree although none is approved: P-A through P-H.
   - P-B widens a security rule. CLAUDE.md item 3 now treats the kit as "named", so the agent may read it.
   - P-D rewrites the user's existing `settings.json` entry.

**(c) Implemented, but it looks wrong**
1. D4 says "with both, the guard runs twice on the same call and gives the same answer". This no longer holds:
   - The plugin's hook now blocks writes to the allowlist, even under OVERRIDE; the machine-wide hook does not (P-G).
   - The plugin's hook arms for `.keel/` and for folders above the project; `install_guard.py` arms only for an exact `keel-factory` in the project folder (P-A).
   - A block from either one still wins, so the outcome is safe, but the stated rule is false.
2. D3 says it "injects only the kit-root line" when the project already carries the layer. It actually injects a three-line header: that KEEL is on, the kit root, and a routing line for the role. For v1.0 copies it adds an upgrade note as well. The deviation is small, but it is not what D3 says.

Nothing else is missing for D1, D5 (opening line, `keel` no longer hidden), D6 (TIERS and STATE template), D8, D9, D10 or D11:
- `plugin.json` matches A1.
- The two rule-count fixes are in (TIERS now says "seven", the RULES title "Six").
- `VERSION` is 1.1.0.
- The plugin install comes first in all seven documents.
- The RELEASES section keeps Evidence, Inferred and Missing apart.
- Nothing has been committed or tagged.

**Worst on this axis:** D4's "the guard runs twice and gives the same answer" no longer
holds, and seven proposed amendments are already in the tree. The proposals go to the
manager below; the D4 wording goes with P-A and P-G.
*Note 2026-10-19 (PROVE pass 3, S-c2): the D4 wording went through fix round 3's F3-6
under the pick "Fix round 3 → pass 3", not with P-A and P-G; it goes to the manager at the
PROVE pass 4 report.*

## Gate

**Gate (PROVE): all 13 Required Checks pass, with no critical findings.** I ran them from the master root with `PYTHONDONTWRITEBYTECODE=1`. Every one exited 0 and stated what it examined. The working tree is unchanged (still the same 51 status entries).

| ID | Exit | Output | Scope it reported |
|---|---|---|---|
| R1 | 0 | OK | 27 tests, no skips |
| R2 | 0 | OK | 76 tests |
| R3 | 0 | OK | 9 tests |
| R4 | 0 | OK | 13 tests |
| R5 | 0 | OK | 28 tests |
| R6 | 0 | OK | 34 tests |
| R7 | 0 | OK | 21 tests |
| R8 | 0 | `OK: … no findings` | 14 skill paths, 2 hook commands, 18 skills, 7038 listing characters, 80 skill paths checked, 22 Codex skills, 3 agents, 3 eval cases, 5437 `CLAUDE.md` characters, 5871 session characters, 213 docs, **228 links** |
| R9 | 0 | "Validation passed with warnings" | manifest plus `CLAUDE.md`; one warning, the expected root `CLAUDE.md` one |
| R10 | 0 | `OK: 17 task(s) … no findings` | 17 tasks |
| R11 | 0 | `keel@skills-dir`, Version 1.1.0, Status loaded | `~/.claude/skills/keel` links to this master |
| R12 | 0 | 17 `keel:<name>` skills listed, `commit` absent; nothing on stderr | 22,734-byte rendered prompt; all 17 resolve to files under this master |
| R13 | 0 | OK | 13 tests |

**R12 setup, as the row says:** I made a scratch git repo holding a committed `.keel/keel.json` (`{"role": "owner"}`) and an empty scratch `CODEX_HOME`, with `HOME=$HOME`. It made no model call.

**Findings (minor)**
- **R8 count is out of date:** it reports 228 links; `/Users/lambertike/Documents/KEEL-FACTORY/.scratch/v1.1/ACCEPTANCE.md` says 227. All other counts match.
- **R8 does not print its rule names:** its output gives counts only. All 14 rule names do appear in `/Users/lambertike/Documents/KEEL-FACTORY/harness/check_kit.py`, and R6 tests each rule.
- **R9's failing record is only Inferred:** ACCEPTANCE itself labels it so.
- **P1 and P2 were not run.** P1 needs Claude Code 2.1.269 or later; this machine has 2.1.170, which I confirmed. P2 needs a Codex model call that has not been approved.

**Traceability** (`/Users/lambertike/Documents/KEEL-FACTORY/.scratch/v1.1/TRACEABILITY.md`)
- **M1:** R5 and R11 exist and pass. L1 and L3 are past live runs that I did not re-run.
- **M2:** R2 passes. L3, L4 and L7 were not re-run.
- **M3:** no Required Check is bound to it, only the live run L4 (not re-run). Supervised and unattended stop modes are not covered by any check. PARTIAL stands.
- **M4:** R8 passes (3 agents). L5 was not re-run.
- **M5:** R8 passes (3 eval cases). P1 is not runnable here. PARTIAL stands: the suite is written and checked but has never been run.
- **M6:** R8 and R9 pass. `claude plugin details keel@skills-dir` exits 0 and reports "~2,530 tok" always-on. It labels the hooks "no model context cost", but the SessionStart hook does add context.
- **M7:** R8 passes (22 Codex skills) and R12 passes (17 skills). P2 was not run. PARTIAL stands: Codex hooks are unproven.
- **M8:** R1 and R2 pass. L1–L3 were not re-run.
- **M9:** R8's link check passes (228 links). The "reviewer reading" half is not a runnable check.

**Verdict:** all 13 Required Checks are present, have a recorded failing run, and pass. Of the 9 rows, 6 claimed PASS rest on passing checks plus live runs I didn't repeat. The 3 PARTIAL rows (M3, M5, M7) stay PARTIAL.

**Worst on this axis:** R9's failing record is only Inferred, so its green result counts as
PARTIAL evidence. The R8 link count in ACCEPTANCE is stale (227, now 228).

## Closure of pass 1

Of pass 1's 52 findings, the closure checkers gave 76 verdicts, including the "Related"
items: **68 fixed, 8 partly, none not-fixed, none regressed.** The eight partly fixed:

- **COMPLETENESS-8** (partly): Two cases still get the layer twice in Claude Code. (1) The 'any folder with an ancestor CLAUDE.md' half of the finding: gp/CLAUDE.md (a copy of the layer) above gp/app/{.git,.keel} still gets the full layer injected (5,922 chars, mark present), because the carry check reads only the marker root. The same applies inside one repo, when the root CLAUDE.md imports the layer and .keel/ sits in a subfolder. (2) A marketplace-style install, where CLAUDE_PLUGIN_ROOT is a cached copy rather than the mas
- **G2** (partly): The docs present one machine's figure as the plugin's cost "in every session on a machine where the plugin is installed". A fresh install measures ~1,953, and the roughly 580-token gap (already noted in pass 1's Gate summary) is unexplained. Give both measurements, or find what the real config adds. I did not run against the real config, because that would read ~/.claude.
- **WALKTHROUGH-2** (partly): MANUAL.md:240-248 (§5 step 1, "Start Claude Code or Codex inside the package folder") still says HELM records the role "which arms the guard", with no caveat for Codex without --codex-hooks. helm/SKILL.md:78 says "the guard arms on the next tool call", also uncaveated, though the probe in step 3 then corrects it.
- **WALKTHROUGH-10** (partly): Rewrite the handoff and STATE.md to the landed state before the release, or point MANUAL §8 at a document that is kept current. As it stands, a fresh machine resuming from the handoff would redo rows 1-11.
- **COMPLETENESS-5** (partly): Operator mode is still not handled in keel. Suppose `keel` is picked directly in someone else's package. Switch-on finds operator, and HELM step 5 reads OPERATOR.md. HELM:29-30 then sends the agent back to keel, whose orientation step 3 records the tier in docs/STATE.md and runs BRIEF. That contradicts OPERATOR.md:117-118: 'Nothing KEEL-shaped lands in the package's own tree: no `docs/` artifacts'. With a role already recorded as operator, step 0 never fires at all, because KEEL is on. The 'docs
- **COMPLETENESS-7** (partly): The lockout itself is unchanged. The guard's uneven blocking (a write passes until its parent folder exists) also remains. The warning names no way out. In operator mode the package's ignore files must not be edited (OPERATOR.md:120), so the mandatory debrief can be blocked, and no step says what to do then. Add the remedy to the warning: an owner un-ignores it (for example `!.keel/`); an operator tells the user and puts the debrief in the final reply.
- **WALKTHROUGH-3** (partly): Paths that do resolve inside the project are still mis-resolved. RELEASES.md:158 ('a copied skill resolves its paths under `keel-factory/`') overclaims. Decision 9 (option c) looks incomplete as written. The line should say that in a copied skill (its folder under the project's .claude/skills/ or .agents/skills/), every `../../../` root path is read under keel-factory/, even when a file of that name exists in the project. Alternatively, QUICKSTART:29-34 and START-PROMPTS:194-197/:245-247 could s
- **row-5** (partly): WALKTHROUGH-3: root paths that exist inside the project bypass the fallback. COMPLETENESS-5: keel has no operator-mode guard after switch-on, so the phases can write docs/ into a package.

## Verified findings of pass 2

Sixty items, all reproduced: 48 confirmed and 12 partly; none refuted. Severity after
verification: **4 major** (three distinct defects), 44 minor, 12 none. Origin: 30 from
this fix round, 18 from the v1.1 build, 10 from v1.0, 2 unclear. Dispositions proposed by
the verifiers: 13 fix-now, 32 docs-only, 8 follow-on, 7 reject.

### The three major defects

1. **A copied kit wired from the copy is dormant (N2 = N35; fix round).** Row 1 made the
   hook ignore a `keel-factory` entry that is the kit itself, to stop the master switching
   on its own parent folder. A full copy of the kit made with the documented `rsync` is
   also "the kit itself" when its own hooks run. So a project set up that way, the
   documented Codex route, has no guard and no layer, and the armed-check recipe in
   `DATA-BOUNDARY.md` still reports it armed. **Fix:** ignore the kit's own folder only
   when the kit root is a git checkout (the master always is; the documented copy never is).
   A prototype passed all 76 tests plus a new one. This restores approved D2; no contract
   change.
2. **A mention of `keel-factory/CLAUDE.md` drops the layer (N36 with N3; v1.1 build and
   fix round).** Under the plugin, a project whose `CLAUDE.md` merely names that path,
   including the import the v1.0 upgrade note recommends, gets no layer, because the
   import does not resolve there. **Fix:** count an import only when it is an import line
   that resolves to a file carrying the mark; recommend the import only where
   `keel-factory/` exists.
3. **The v1.0 fallback guard runs the project's own copy (N37; v1.0).** The machine-wide
   hook `install_guard.py` writes, and OPERATOR.md's fallback, run
   `$CLAUDE_PROJECT_DIR/keel-factory/harness/hooks/data-boundary-guard.py`. So a package can
   ship a `keel-factory/` whose guard does nothing. **Fix:** run the installing master's
   guard by absolute path. This is the hook still installed on this machine; see the last
   question below.

### Every verified item

Sorted by severity, then disposition. The fix text is the verifier's.

| ID | Finding | Verdict | Severity | Origin | Disposition | Fix (from the verifier) |
| --- | --- | --- | --- | --- | --- | --- |
| N2 | A project holding a copied kit, with hooks wired to that copy, is silently dormant (no guard, no layer), and the documented armed check passes anyway | confirmed | major | fix-round | fix-now | Code: in keel_hook.py marker(), drop the kit's own folder only when the kit root is the master, meaning its own git checkout. A copy made by the documented rsync never has a .git. Change :177 to `linked = entry.is_symlink() or entry.resolve() != kit or not master_checkout(kit)` and add `def master_checkout(kit): return (kit / ".git").is_dir() or main_worktree(kit) is not None`. A linked worktree of the master stil… |
| N35 | With a full (rsync) copy of the kit and hooks wired from that copy, the documented Codex route, KEEL never switches on: guard and session layer stay dormant, and the armed-check recipe still passes | confirmed | major | fix-round | fix-now | Use the N2 fix: exclude the own folder only when the kit root holds its own .git directory or is a linked worktree (main_worktree(kit) is not None). This is N35's '.git' idea applied in marker(), not in the installer. To tell the master's own folder from a copy: check the kit root, not the candidate. The master, the case disposition row 1 meant to exclude, is its own git checkout (keel-factory/.git is a folder, or… |
| N36 | The session hook drops the whole always-on layer when CLAUDE.md merely contains the text 'keel-factory/CLAUDE.md', even when no keel-factory/ exists (a dangling import) | confirmed | major | v1.1-build | fix-now | In keel_hook.py, count an import only when it actually resolves to the layer. Use a regex for an import line: `^@(\./)?keel-factory/CLAUDE\.md\s*$` (multiline). Resolve that path against the importing file's own folder (layer_root for CLAUDE.md, CLAUDE.local.md and AGENTS.md; layer_root/.claude for .claude/CLAUDE.md). Count it only when the resolved file exists and holds LAYER_MARK. Concretely: pass each file's fo… |
| N37 | The machine-wide fallback guard (install_guard.py, OPERATOR.md's hook) runs the project's own keel-factory/harness/hooks/data-boundary-guard.py, so a package controls, and can silently disarm, the guard | confirmed | major | v1.0 | fix-now | install_guard.py: build COMMAND at run time as `ls -1 "$CLAUDE_PROJECT_DIR" 2>/dev/null \| grep -qxF keel-factory \|\| exit 0; g=<shlex.quote(MASTER/harness/hooks/data-boundary-guard.py)>; [ -f "$g" ] \|\| exit 0; exec python3 "$g"`, the same way install_plugin.hook_command does. Keep the exact-name test only as the switch. MARKER also has to change: on this machine the master is .../KEEL-FACTORY/..., and the case-sens… |
| N3 | Carry check trusts the bare text keel-factory/CLAUDE.md, and the v1.0 upgrade note recommends an import that does not resolve under the plugin, so the layer goes missing | confirmed | minor | fix-round | fix-now | Land this together with N36. Give upgrade_note the layer root and offer `@keel-factory/CLAUDE.md` only when <root>/keel-factory/CLAUDE.md exists and holds LAYER_MARK. Otherwise say: 'Upgrade: delete KEEL's v1.0 text from that file (this hook then supplies the layer), or replace it with the v1.1 layer.' Make the matching edits. MANUAL.md §11 step 2 and RELEASES.md 'Upgrading from v1.0' first bullet should both say:… |
| N43 | install_plugin.py --codex silently skips KEEL's front door when ~/.agents/skills/helm is taken, and still exits 0 | confirmed | minor | v1.1-build | fix-now | Keep D8's skip, but for a taken name among OWN (above all helm) print a warning that names the consequence. For example: 'warning: KEEL's own skill helm is not installed for Codex because <path> is taken; $keel:helm will not work until you move it and re-run.' Add a test. Turning that skip into a refusal with exit 1 would contradict approved D8 ('skipping taken names') and would need an amendment. |
| N44 | A second --codex-hooks run saves KEEL's own hooks as 'the original' hooks.json.before-keel | confirmed | minor | v1.1-build | fix-now | In codex_hooks, before stripping KEEL's entries, record had_keel = any(is_keel_entry(e) for each event list). Back up only when the path exists, no backup exists, and not had_keel. Add a test: run twice from no file, and assert that no .before-keel exists. This brings the code in line with A4 as approved. |
| std:mutate_hook | std:mutate_hook | confirmed | minor | fix-round | fix-now | Delete .scratch/v1.1/tools/mutate_hook.py. Change .scratch/handoff.md:308 to `python3 -B .scratch/v1.1/tools/mutate.py . harness/hooks/keel_hook.py harness/hooks/test_keel_hook.py .scratch/v1.1/tools/mut-hook.json`. |
| N11 | README-FIRST's restore commands put the master on the release drive and contradict MANUAL section 3 | confirmed | minor | v1.0 | fix-now | make_release.py README-FIRST: put 'shasum -a 256 -c SHA256SUMS' first. Then, run from this folder: 'git clone --branch main "$PWD/KEEL-FACTORY-<tag>.bundle" ~/GitProjects/KEEL-FACTORY' and 'git -C ~/GitProjects/KEEL-FACTORY describe --tags', with a note to use your own local path, never the drive. No-git route: 'mkdir -p ~/GitProjects && tar -xzf KEEL-FACTORY-<tag>.tar.gz -C ~/GitProjects'. Update test_make_releas… |
| N23 | COMPLETENESS-5 still partly | confirmed | minor | v1.1-build | fix-now | Add one sentence to keel's step 0, not to HELM, which stays a router: 'In operator mode (`.keel/keel.json` says operator, the session note says so, or switch-on just decided it), follow `../../../OPERATOR.md` instead of the phases below.' Follow-on: in operator mode, keel-prove's records go to `<ops>`, not `docs/`. N28 is the same gap. |
| N28 | keel resumes its phases after switch-on finds operator mode, writing docs/ into someone else's package | confirmed | minor | fix-round | fix-now | Same sentence as N23, in keel's step 0: in operator mode, follow `../../../OPERATOR.md` instead of the phases. Leave HELM:29-30 as it is, so HELM stays a router. Follow-on: in operator mode, keel-prove writes its records to `<ops>`. |
| N25 | WALKTHROUGH-3 still partly | partly | minor | v1.0 | fix-now | Reword the one identical line in all six skills: 'In a copied skill (this file sits under a project's `.claude/skills/` or `.agents/skills/`, not under `keel/`), read every `../` path under `keel-factory/keel/`, and root files such as `CLAUDE.md` under `keel-factory/`, even when the project has a file of that name.' Narrow RELEASES:158 to match. Note the change against crew-plan decision 9. |
| N26 | row-5 still partly | partly | minor | v1.1-build | fix-now | No separate work: the N23 fix (keel step 0 operator line) and the N25 fix (copied-skill line reworded) close it. |
| N32 | Routine 'git clean -fd' (or any removal of .keel/) silently disarms the guard mid-session and deletes the operator notes and debrief | confirmed | minor | v1.0 | docs-only | Now, docs-only, contract unchanged. Add to OPERATOR.md section 3 (Footprint) and the MANUAL section 10 troubleshooting list: "`git clean -f`/`-fd`/`-fdx` and `git stash -u`/`--all` remove an untracked `.keel/` or `keel-factory/`. That switches KEEL off mid-session (the guard disarms with no message) and deletes `<ops>`: notes, board, debrief. If the package or the user needs a clean, ask first, then run `git clean… |
| N33 | A repository can ship .keel/data-boundary-allow through git and pre-authorize reading the user's own .env; the docs even permit committing it | confirmed | minor | v1.0 | docs-only | For v1.1, docs only, no contract change: (1) DATA-BOUNDARY.md overrides bullet, MANUAL §10 (the 'guard blocked something legitimate' and 'git status shows .keel/' items) and QUICKSTART: replace the conditional 'Don't commit it if...' with 'Never commit .keel/data-boundary-allow: it is your own local override. Stage .keel/keel.json by name, never .keel/ as a whole.' Optionally suggest adding '.keel/data-boundary-al… |
| N34 | The allowlist protection ('KEEL's hook blocks agents from it') is bypassable with the Write tool alone, and by trivial shell quoting | partly | minor | fix-round | docs-only | Docs, not a sandbox attempt. Qualify CLAUDE.md:91-92 (one sentence, merged with the N4 fix), README.md:80-82 and RELEASES.md:41/138 to say the hook blocks the direct ways: a Write/Edit/patch of the file and any command naming it. Call it a tripwire, not a lock. Add a bullet to DATA-BOUNDARY.md 'What this does not cover': the allowlist block is a path/text match, so renaming or relinking .keel, quoting or variables… |
| N5 | Allowlist protection is a single-command name match; two-step routes still write it | confirmed | minor | fix-round | docs-only | Use the same DATA-BOUNDARY.md 'What this does not cover' bullet as N34: the allowlist block catches direct writes and commands naming the file; renames, variables, globs and scripts get past it. Do not add an mv/cp/tee blocklist, since it cannot be complete and adds false blocks. Follow-on, small and contract-safe because the guard file stays unchanged: in keel_hook.guard, rewrite the guard's 'Durable, this path o… |
| N4 | CLAUDE.md says KEEL's hook blocks agents from the allowlist, but the bare wirings do not | confirmed | minor | fix-round | docs-only | Narrow CLAUDE.md:92, one sentence merged with N34's qualifier, for example: 'only the user edits that file. The plugin's and Codex's KEEL hook block the direct ways of writing it; a hand-wired guard does not.' Correct the '(true in every wiring)' note in crew-plan Open question 14. Leave install_guard.py, settings.hooks.json and OPERATOR.md wired to the bare guard for now; test_install_guard pins the OPERATOR.md c… |
| N38 | Outside git the allowlist can never work, though v1.1 switches KEEL on outside git, and the block message gives a remedy that is never read | confirmed | minor | v1.0 | docs-only | Say in DATA-BOUNDARY.md ('One path, durably') and MANUAL's 'The guard blocked something legitimate' entry that the allowlist works only inside a git repository. Outside git, run `git init` or use the session override. The guard file stays unchanged (D4). If wanted later as a follow-on, keel_hook could rewrite the block message when the target has no repo root. |
| N39 | MCP tools reach neither guard matcher, and 'What this does not cover' does not mention them | confirmed | minor | v1.0 | docs-only | Add a bullet to DATA-BOUNDARY 'What this does not cover', and a clause to README's privacy section: 'MCP tools are not matched, so an MCP tool that takes a local path is not checked'. Extending the matchers with 'mcp__.*' is a separate follow-on. It needs a contract amendment, because approved D4 fixes the Claude matcher and approved A4 fixes the Codex one as 'Bash\|apply_patch'. |
| N8 | G2 still partly | confirmed | minor | fix-round | docs-only | README.md:42-45 and RELEASES.md:94: give both measurements with their conditions, e.g. 'about 1,950-2,530 tokens: ~1,953 in a fresh config, ~2,522-2,533 in the build machine's own config; the estimate depends on the config'. Keep the SessionStart figure separate. Re-measure right before tagging. |
| N9 | WALKTHROUGH-2 still partly | confirmed | minor | fix-round | docs-only | MANUAL.md:247: '..., which, where KEEL's hooks run (Claude Code's plugin, or Codex with --codex-hooks trusted in /hooks), arms the guard'. helm/SKILL.md:78: 'where KEEL's hooks run, the guard arms on the next tool call and every later session starts with the always-on layer'. Same defect as N14; fix once. |
| N13 | CAPABILITIES still labels hooks in subagents as Inferred after L8 proved it | confirmed | minor | fix-round | docs-only | CAPABILITIES.md:94: 'Plugin PreToolUse hooks fire on subagent tool calls, Explore included \| Evidence \| L8'. Keep '`agent_id` in the input' as Inferred, citing the hooks docs. CAPABILITIES.md:66: 'L1–L8'. Same as N29 and N40(4). |
| N14 | MANUAL section 5 still says recording the role arms the guard, for Codex too | confirmed | minor | fix-round | docs-only | Same as N9: qualify both sentences with 'where KEEL's hooks run (Claude Code's plugin, or Codex with --codex-hooks trusted in /hooks)'. |
| N15 | Codex rows that LOOPS now relies on cite source files that ship nowhere | confirmed | minor | fix-round | docs-only | In CAPABILITIES.md:72-74, say that the captured prompts are not shipped: 'captured prompt, kept outside the kit; summarized in the KEEL master's .scratch/v1.1/research/research-codex-prompts.md'. Or quote the two or three load-bearing lines (token_budget, the 3-turn blocked rule, automations) into a HARNESS-PROBES appendix and cite that. |
| N22 | The always-on token figure is presented as Evidence but depends on the Claude config | confirmed | minor | fix-round | docs-only | Same as N8: state the range and its conditions, e.g. '~1,950 in a fresh config, ~2,520-2,530 in the build machine's config (Evidence, both); the plugin-details estimate depends on the config'. |
| N29 | CAPABILITIES still labels 'Hooks in subagents' Inferred after L8 proved it | confirmed | minor | fix-round | docs-only | Same as N13: label the firing Evidence (L8), keep agent_id Inferred, and change L1–L7 to L1–L8. |
| N30 | RELEASES overclaims the copied-skill fix | confirmed | minor | fix-round | docs-only | Smallest: narrow RELEASES.md:158 to 'a copied skill resolves paths missing from the copy under keel-factory/; a root file the project also has (ARCHITECTURE.md, CLAUDE.md, agents/) still resolves to the project's'. Better, as a follow-on: change the six skills' fallback line to 'In a copied skill (not under a kit's keel/), read every ../../../ path under keel-factory/ instead'. That also removes the risk of HELM s… |
| N40 | Evidence-labelled figures that the recorded runs do not back | confirmed | minor | fix-round | docs-only | HARNESS-PROBES.md:89, README.md:47-49 and RELEASES.md:94: say L8 injected 5,918 characters of context (6,132 of hook stdout, JSON-escaped), and drop the longer-path explanation, or keep it as roughly 50 characters. README.md:44: cite the recorded 2,522, or record the 2,533 run in HARNESS-PROBES, and give the fresh-config figure (N8). CAPABILITIES.md:127: add an X10 probe row (codex plugin --help on 0.138) or cite … |
| N41 | START-PROMPTS' Claude Code prompt tells the agent to merge into an existing .claude/settings.local.json; OPERATOR.md says never to open it | confirmed | minor | v1.0 | docs-only | START-PROMPTS.md:205-207: 'write the hooks into ./.claude/settings.local.json if it does not exist yet; if it does, don't open it: ask me the data-boundary question naming that file, or leave the merge to me (or use harness/install_guard.py machine-wide)'. |
| N45 | QUICKSTART's new-project setup links the kit into a folder that does not exist yet, and link_kit.py refuses | confirmed | minor | v1.0 | docs-only | QUICKSTART.md section 0: add 'mkdir -p ~/path/to/new-project' before the link_kit.py line. Leave link_kit.py's refusal as it is. |
| N16 | Approved amendments A5 and A6 (and partly A4) cover more than the manager's quoted approval | partly | minor | fix-round | docs-only | In A6, move the 8,000-character listing bound to Proposed, or label it "A1's stated reason, to confirm with the manager". In A4 and A5, add one clause each saying the $CODEX_HOME default and `--harness` were approved as rows 7 and 2 of the go-ahead, not by the option text. |
| N17 | The manager's quoted option text has no recorded source, and the lead's draft framed it differently | partly | minor | fix-round | docs-only | The lead copies the exact question and option text from this session's question round into crew-plan Open question 2. If it matches, CONTRACT:255-257 cites Open question 2 as verbatim. If it differs, move whatever A5–A7 covers beyond it to Proposed. |
| N18 | ACCEPTANCE.md contradicts itself on the phase-2 mutation results and has stale counts | confirmed | minor | fix-round | docs-only | Replace the last sentence of ACCEPTANCE:35-37 with a pointer to R5 and R13. Set R8 to 228 links. Once the final re-run is recorded, set R13 and the RELEASES Release-script row to 19 of 19. |
| spec:a1-linked-kit-role | spec:a1-linked-kit-role | confirmed | minor | v1.1-build | docs-only | Add to P-A, for D2 and D5: the role is recorded only where `.keel/` is the switch. A linked `keel-factory/` (hook role `kit`) has its role inferred each session, because the linked folder is KEEL's whole footprint there. |
| spec:a2-exfil | spec:a2-exfil | confirmed | minor | v1.1-build | docs-only | Nothing new. The manager decides P-H at the PROVE report. |
| spec:b1-agent-bodies | spec:b1-agent-bodies | confirmed | minor | v1.1-build | docs-only | Rewrite P-E's What to list the additions: the framing paragraph, the change-reading step, the Gate's no-edit and no-outward-facing rules, and the read-only and data-boundary limits. Propose D7 as "moved, with those added" instead of "moved, not rewritten". |
| spec:b5-proposals-in-tree | spec:b5-proposals-in-tree | partly | minor | fix-round | docs-only | In the Proposed preamble, say which proposals carry out approved rows 1–11 and which go beyond them (P-B, P-D's upgrade, P-C's narrowing). Present P-B first at the PROVE report as a change to the security rule, and revert CLAUDE.md:70-72 if it is declined. |
| spec:c1-guard-twice | spec:c1-guard-twice | confirmed | minor | fix-round | docs-only | Through P-G and P-A, reword D4: "with both, a block from either wins; the plugin's hook also guards the allowlist and arms in .keel/ projects and parent folders, where the machine-wide hook does nothing." |
| N24 | COMPLETENESS-7 still partly | partly | minor | v1.1-build | docs-only | Add one clause to HELM's warning at helm:80-82: 'an owner removes that ignore (MANUAL §10); in operator mode, tell the user, and if the debrief copy is blocked, give the debrief in the reply only.' No code change. |
| N1 | COMPLETENESS-8 still partly | confirmed | minor | v1.1-build | follow-on | In instruction_files() for claude, also read CLAUDE.md and CLAUDE.local.md in every folder from the start up to (not including) '/', which is what Claude Code loads. An ancestor layer copy, or the master's own CLAUDE.md, then counts as carrying the layer. Add two tests: ancestor copy, and subfolder .keel under an importing root. Case (2) also needs N42's kit detection. This moves the code toward approved D3 ('neve… |
| N6 | keel_hook.py guard fails open on a malformed command line | confirmed | minor | fix-round | follow-on | In main(), when argv[1] == 'guard' and the rest does not parse, write USAGE to stderr and return 2, so a mis-wired guard blocks loudly. Keep exit 1 for session. Update docstring line 9 and add a test for one malformed guard form. |
| N7 | check_kit's ast source read misses a top-level mutation of OWN, BOARD or DOCS | confirmed | minor | fix-round | follow-on | In read_sources, add a 'source' finding for any other top-level statement that targets OWN, BOARD, DOCS or LAYER_MARK: AugAssign, an Expr Call on Name.attr (append, extend, insert and so on), or an Assign or AugAssign to a Subscript of that Name. Add one test_check_kit case (BOARD += [...]). Optionally make install_plugin.link refuse a target that does not exist, which catches a dangling skill however the list was… |
| N31 | link_kit.py crashes with a traceback when a link is refused | confirmed | minor | v1.0 | follow-on | In link(), wrap kit.mkdir and dest.symlink_to in try/except OSError. Print the install_plugin-style line: 'refused: could not make the link <dest> -> <item> (<strerror>). On Windows, links need Developer Mode or an administrator shell.' Return 1. Add a test_link_kit case with a read-only keel-factory/. |
| N42 | Under the marketplace install the master is no longer 'the kit', so HELM can switch KEEL on inside $KEEL | confirmed | minor | fix-round | follow-on | In keel_state, also treat as the kit any folder in the start's chain that holds .claude-plugin/plugin.json with name 'keel' and harness/hooks/keel_hook.py. Mirror it in HELM step 1 ('or a folder holding KEEL's .claude-plugin/plugin.json'). Add a test with CLAUDE_PLUGIN_ROOT set to a copy. As a docs-only stopgap, qualify MANUAL §3 for the marketplace install. This refines Proposed P-A only; no approved text changes. |
| std:hook-cmd-dup | std:hook-cmd-dup | partly | minor | fix-round | follow-on | Add a test_install_plugin case that loads settings.hooks.codex.json, substitutes the placeholder, and compares the matcher, statusMessage and command shape with codex_hooks' output. For MultiEdit, either add it to install_guard.MATCHER, settings.hooks.json and OPERATOR.md together (install_guard's upgrade-in-place must then also compare the matcher, and test_install_guard pins OPERATOR.md), or record in DATA-BOUND… |
| N21 | The Codex AGENTS.md block has no refresh path, so a stale copy hides the current layer | confirmed | minor | fix-round | follow-on | Land this with, or before, the first change to CLAUDE.md after v1.1.0. (1) keel_hook.py layer_status: when a counted file holds the mark but the text from the mark to `<!-- end KEEL always-on layer -->`, minus the kit-root line, differs from the kit's CLAUDE.md, return a 'stale' status. Print the header plus one line: "<file>'s KEEL block is older than the kit's layer; run $keel:helm (or /keel:helm) to refresh it"… |
| N27 | HELM's Codex AGENTS.md block is a frozen copy that silently suppresses an upgraded layer | confirmed | minor | fix-round | follow-on | Same fix as N21, and land it once with N21. Compare any marked instruction file's block, under either harness, against the kit's CLAUDE.md, and print a one-line refresh note when they differ. Change HELM step 4 so it replaces a block that differs instead of checking only that the mark is present. Document it in RELEASES and MANUAL. |
| std:mutate-doc | std:mutate-doc | confirmed | none | v1.1-build | docs-only | Docstring: 'into a full temp copy of the kit (existing links kept as links; .git, __pycache__, .scratch and results left out)'. |
| std:selftest-line | std:selftest-line | confirmed | none | v1.1-build | docs-only | Append 'Self-test: test_install_plugin.py, beside this file.' to install_plugin.py's docstring, after 'Standard library only.'. |
| N19 | A changed §5 bound number is recorded as a "Stale" note, not as an amendment | partly | none | fix-round | docs-only | Add to the §5 Stale note: "(the seven new install_guard tests come from row 8 and P-D)". No approved decision changes. |
| spec:b2-readme-first | spec:b2-readme-first | partly | none | fix-round | docs-only | Add one clause to P-F: README-FIRST restores with `git clone --branch main` and checks `git describe --tags`. No code change. |
| spec:c2-carry-header | spec:c2-carry-header | confirmed | none | v1.1-build | docs-only | Through P-C, change D3's "only the kit-root line" to "only the header (where KEEL is on and the role, the kit root, the routing line)". |
| std:usage | std:usage | partly | none | unclear | reject | None required. If N6's fix lands, derive USAGE from the docstring's first lines, or leave it as it is. |
| std:smells | std:smells | confirmed | none | v1.1-build | reject | None before release. Fold them into any later refactor of keel_hook or check_kit. |
| spec:b3-codex-template | spec:b3-codex-template | partly | none | v1.1-build | reject | None needed. Optionally label the stated reason Inferred (from the hooks' source and Codex's docs) in harness/README. |
| spec:b4-gate-manual | spec:b4-gate-manual | confirmed | none | unclear | reject | None. Optionally note it in DESIGN. |
| spec:b4-production-questions | spec:b4-production-questions | confirmed | none | v1.1-build | reject | None. |
| spec:b4-crew-lead-lane | spec:b4-crew-lead-lane | confirmed | none | v1.1-build | reject | None. |
| spec:b4-hook-fail-closed | spec:b4-hook-fail-closed | confirmed | none | v1.1-build | reject | None. Optionally add a clause to D4 through P-G: "fails closed, as the guard does". |

## Traceability, promoted

| # | Must-have | Before | After pass 2 | Why |
| --- | --- | --- | --- | --- |
| M1 | Install once; every skill visible in every project | claimed PASS | **PASS** | R5 (28 tests, 22/22 mutants) and R11, both armed; L1, L3 |
| M2 | One front door; HELM tells owner from operator | claimed PASS | **PARTIAL** | R2 armed (49/49); but HELM's switch-on text changed in this run and no live run has exercised it since L7, and `keel` entered directly still runs its phases in operator mode (N23, N28) |
| M3 | Stop modes | claimed PARTIAL | **PARTIAL** | checkpoint live (L4); supervised and unattended not exercised |
| M4 | PROVE reviewers shipped as agents | claimed PASS | **PASS** | R8's agent rule armed (36/36); L5; this pass ran them |
| M5 | Eval suite with a baseline | claimed PARTIAL | **PARTIAL** | written and checked by R8; never run (P1 needs Claude Code ≥ 2.1.269) |
| M6 | Less always-on context | claimed PASS | **PASS** | R8's sizes armed: `CLAUDE.md` 5,437 characters (v1.0: 12,773); R9 passes, though its failing record is only Inferred |
| M7 | Codex, as far as Codex allows, gaps named | claimed PARTIAL | **PARTIAL** | skills proven (R8, R12); Codex hooks unproven (P2); the copied-kit route is dormant (N2) |
| M8 | Guard keeps working and arms in KEEL projects | claimed PASS | **FAIL** | plugin route PASS (R1, R2, L1, L8); a documented route, a copied kit wired from the copy, does not arm (N2 = N35) |
| M9 | CAPABILITIES says what each harness can and can't do | claimed PASS | **PARTIAL** | R8 links armed; "hooks in subagents" still Inferred after L8 proved it (N13); two Codex rows cite sources that ship nowhere (N15) |

Coverage = (PASS + DESCOPED) / total = **3 / 9 (33%)**; the lead had claimed 6 / 9.

## Cost

Measured from the workflow runs (Evidence: the harness's own counts):

| Run | Agents | Subagent tokens |
| --- | --- | --- |
| Phase 1 back-briefs | 5 | 827,421 |
| Phase 1 builds | 5 | 849,366 |
| Phase 2 back-briefs | 4 | 743,647 |
| Phase 2 builds | 4 | 901,065 |
| PROVE pass 2 | 8 | 1,444,686 |
| Verification | 10 | 1,429,461 |

That is 36 agents and about 6.2 million subagent tokens, on the manager's plan. One
headless probe (L8) ran under a $0.40 cap: 3 turns, est. $0.18 (notional on the plan). No
Codex model call was made.

## Honest status

- **Implemented and verified:**
  - the hook's switch-on rule, carry check, allowlist block and CLI (R2, 76 tests,
    49/49);
  - the installer's CODEX_HOME, quoting and error paths (R5, 22/22);
  - install_guard's exact name and upgrade (R4, 11/11);
  - check_kit's single sources and new rules (R6, 36/36);
  - make_release's main-only refusal and README-FIRST (R13, 19/19);
  - the plugin loading (R11);
  - Codex skill links (R12);
  - the guard in subagents (L8).
- **Implemented, unverified:**
  - HELM's new switch-on steps: reading the layer, the refusals, the gitignore warning, the
    Codex `AGENTS.md` block. They are written but no live run has followed them.
  - The Codex hooks (P2, owner-gated).
  - Supervised and unattended stop modes.
- **Specified only:**
  - The eval suite (P1 needs a newer Claude Code).
  - The proposed amendments P-A to P-H, which are in the tree but not approved.

## For the manager

PROVE pass 2 does **not** pass: one must-have fails (M8) and three confirmed major defects
are open, one of them made by this fix run. Recommended: a third fix round over the 13
fix-now and 32 docs-only items, the 8 follow-ons filed as board tasks and the 7 rejects
recorded with their reasons, then PROVE pass 3. Also for the manager:

1. The proposed amendments P-A to P-H in `CONTRACT.md`. P-B changes the data-boundary
   rule's text: it lets agents read the KEEL kit itself.
2. Removing the v1.0 machine-wide guard hook from `~/.claude/settings.json`. The plugin
   covers every project that hook covers, and N37 shows the old hook runs a project's own
   guard copy.
3. Still held for a later round: the live Codex hook probe (needs a `~/.codex/hooks.json`
   write and a Codex model call).

## Dispositions recorded in fix round 3 (2026-10-18)

The manager picked "Fix round 3 → pass 3 (Recommended)". Fix-now and docs-only items were
fixed in fix round 3 (`.scratch/task_board/crew-plan-prove-fixes.md`, Open questions 16–19
and the execution log). The rest:

**Follow-ons, filed as board tasks** (`.scratch/task_board/`):

| Item | Board task |
| --- | --- |
| N1 (ancestor CLAUDE.md), N6 (malformed guard line), N42 (marketplace kit) | `keel-hook-hardening` |
| N7 (top-level list mutation) | `check-kit-ast-mutation` |
| N31 (link_kit traceback) | `link-kit-oserror-message` |
| std:hook-cmd-dup (hook text in three places; MultiEdit in the bare wirings) | `hook-commands-single-source` |
| N21 = N27 (stale Codex `AGENTS.md` block), plus `AGENTS.override.md` | `codex-agents-block-refresh` |
| N39's matcher half (MCP tools; a contract change) | `owner-deferred/mcp-tools-guard-matcher` |
| N32's and N34's command blocks, N5's message rewrite | `keel-hook-hardening` |
| N35's warning from a copied kit; the read-error and atomic-write gaps | `installer-hooks-json-robustness` |
| N23's keel-prove and crew half (text landed; a live trial remains) | `keel-prove-operator-records` |
| START-PROMPTS' project-level `./.codex/hooks.json` (unprobed) | added to `owner-deferred/codex-hook-live-probe` |
| N33's code half (ignore a git-tracked allowlist; filed after fix round 3's audit) | `keel-hook-hardening` |
| N33's role sub-claim (a recorded owner role in someone else's package) | `helm-role-override` |

**Rejected, with the reason:**

- std:usage — `keel_hook.py` prints its own `USAGE` line rather than `__doc__`. The usage
  text is still in the docstring; the v1.0 guard sets the same precedent; nothing breaks.
- std:smells — the baseline smells (repeated `harness == "codex"` branches, the
  `(root, src, found)` data clump, short names). Folded into any later refactor of
  `keel_hook.py` or `check_kit.py`; none is a defect.
- spec:b3-codex-template — the Codex template dropping `config-protection.js` and
  `cost-tracker.js`. That is recorded with its reason in harness/README and RELEASES. The
  reason is Inferred from the two hooks' own source and Codex's tool names.
- spec:b4-gate-manual — TIERS lets an unattended halt be filed `gate: manual` as well as
  `gate: owner`. That is the board's own vocabulary for a person's action, and within D6's
  intent.
- spec:b4-production-questions — TIERS adds observability and data retention to the
  production questions. The evals lane found them missing in CREW's first run; they widen
  the round without changing a stop.
- spec:b4-crew-lead-lane — CREW's rule that a writing lead declares its own lane. It is the
  field record's Gap 1 fix, inside A3's agreement.
- spec:b4-hook-fail-closed — `keel_hook.py` blocks when its own code fails, where KEEL is
  on. That mirrors the guard's documented fail-closed behavior; D4 asks for nothing
  weaker.
