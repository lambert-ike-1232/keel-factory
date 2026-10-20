# Harness probes — what Claude Code and Codex did on the machine that built v1.1

The evidence behind the harness table in [CAPABILITIES.md](CAPABILITIES.md). Each row is a
check run on 2026-10-18, so it is **Evidence for that machine and those versions only**;
another machine, or a newer CLI, re-probes before relying on it. The commands are kept
in the shape they ran, so a later session can run them again.

## Claude Code, 2026-10-18

Claude Code 2.1.170, macOS, Python 3.13.13, no Node, no Codex CLI on `PATH` (the Codex
desktop app is installed at `/Applications/Codex.app`). Each of P1 to P13 ran against a
throwaway plugin in a scratch folder; installs used `CLAUDE_CONFIG_DIR` pointed at a
scratch folder, so the real `~/.claude` was never touched. P14 measured the KEEL master
itself (`keel@skills-dir`), once in this machine's own config (read only, nothing
written) and once in a fresh scratch `CLAUDE_CONFIG_DIR`. Every result below is
**Evidence** for this CLI version only.

| # | Question | Command (shape) | Result |
| --- | --- | --- | --- |
| P1 | Does `claude plugin validate` accept custom skill paths? | `plugin.json` with `"skills": ["./a/", "./b/"]`, `validate --strict` | Passes, exit 0 |
| P2 | Does validate fail on bad input? | missing skill path; name with spaces; unknown field | Exit 1 on the first two; unknown field is a warning (error only under `--strict`) |
| P3 | Does validate check `SKILL.md` frontmatter? | skill with no `description` | Passes. **Validate does not catch a missing description.** KEEL needs its own check. |
| P4 | Do custom-path skills load at runtime, and under what names? | `claude -p --plugin-dir <probe>` | `probe:one`, `probe:two`; agent `probe:rev` listed as a subagent type |
| P5 | Does `disable-model-invocation: true` hide a skill from the model? | same, `two` marked | `probe:two` absent from the model's skill list |
| P6 | Can a plugin SessionStart hook put text in context? | hook prints `hookSpecificOutput.additionalContext` | Text appears as "SessionStart hook additional context: …"; `CLAUDE_PLUGIN_ROOT` and `CLAUDE_PROJECT_DIR` are set in the hook |
| P7 | Can the manifest name `hooks/hooks.json`? | `"hooks": "./hooks/hooks.json"` | Install succeeds, then **the plugin fails to load**: "Duplicate hooks file detected". The standard file loads by itself; list only extra files. |
| P8 | Does a local-path marketplace install load in place? | `marketplace add <dir>`, `install probe@probe-market` | **No, on 2.1.170 it copies** to `plugins/cache/<market>/<plugin>/<version>/`. An edit to the source did not reach the cache. (Newer docs say relative-path plugins load in place; not true of this version.) |
| P9 | Does a symlinked skills-dir plugin load in place? | `ln -s <probe> $CLAUDE_CONFIG_DIR/skills/probe` | Listed as `probe@skills-dir`, status loaded, path is the link. In place, no cache. |
| P10 | Does `"agents": ["./agents/rev.md"]` register the agent? | `claude plugin details` | Details reported 0 agents with the file-array form and 1 with the default `agents/` folder. Use the default folder. |
| P11 | Does a plugin skill resolve paths relative to its own folder? | skill says read `../../NOTE.txt` | Read the right file and quoted its line |
| P12 | Is `claude plugin eval` available? | `claude plugin eval --help` | **No** on 2.1.170 (the docs say it needs v2.1.269+). The eval suite can be written and structurally checked here, not run. |
| P13 | Projected context cost | `claude plugin details probe@probe-market` | Reports "Always-on: ~14 tok" for two short skills; SessionStart hook counted as "harness-only — no model context cost" (the injected text itself is not counted) |
| P14 | What always-on cost does `claude plugin details` report for the plugin, and does it depend on the config? | `claude plugin details keel@skills-dir` on 2.1.170, in this machine's config and in a fresh `CLAUDE_CONFIG_DIR` holding only `skills/keel` → the master, 2026-10-18 (after fix round 3's skill edits) | ~2,530 tokens here; ~1,953 in the fresh config, for the same 18 skills, 3 agents and 2 hooks. The estimate depends on the config, and it labels the hooks "no model context cost", so it leaves out the SessionStart injection |

Cost: under $1 for P4–P6 and P11, four `haiku` headless runs each started with
`--max-budget-usd 0.30` or `0.40`. The flag was accepted; whether it would have stopped a
run at the cap was not tested (no run came near it).

## Live runs of the v1.1 plugin, 2026-10-18

Headless `claude -p --plugin-dir <master> --model haiku --allowedTools=Read`, in throwaway
git repositories, on a Max plan with no `ANTHROPIC_API_KEY` set. No budget flag.

| # | Setup | Result |
| --- | --- | --- |
| L1 | repo with `.keel/keel.json` `{"role": "owner"}` and a fake `.env` | The model listed 16 `keel:*` skills (not `keel:keel` or `keel:commit`, both still marked `disable-model-invocation` at the time); quoted the SessionStart context "KEEL is switched on in this project (…); role: owner."; its Read of `.env` was blocked by the data-boundary guard |
| L2 | the same, without `.keel/` | No KEEL context; the Read of `.env` returned the file's (fake) first line |

## Codex, 2026-10-18

Codex CLI 0.138.0-alpha.7, the binary inside `/Applications/Codex.app/Contents/Resources/`
(not on `PATH`). Every probe ran with `CODEX_HOME` pointed at a scratch folder and made no
model call: `codex debug prompt-input` renders the model-visible prompt locally.

| # | Question | Command (shape) | Result |
| --- | --- | --- | --- |
| X1 | Which features are on? | `codex features list` | `hooks` stable/on; `plugins` stable/on; `plugin_hooks` removed; `multi_agent` stable/on; `multi_agent_v2` off; `goals` stable/on; `default_mode_request_user_input` under development/off; `child_agents_md` off |
| X2 | Are repo skills in `.agents/skills/` listed? | scratch repo, `codex debug prompt-input` | Yes: `- alpha: <description> (file: <abs path>/SKILL.md)` under "Available skills". Name and description only; the body is not in the prompt |
| X3 | Are symlinked skill folders followed? | `.agents/skills/beta` → a folder elsewhere | Yes; the listing shows the link's target path |
| X4 | Is a root `AGENTS.md` injected? | marker line in `AGENTS.md` | Yes, verbatim, as "# AGENTS.md instructions for <repo>" in `<INSTRUCTIONS>` |
| X5 | Are user skills outside `CODEX_HOME` read? | scratch `CODEX_HOME` | Yes: the real `~/.agents/skills/` was listed too, so `~/.agents/skills/` is a user-level root independent of `CODEX_HOME` |
| X6 | What can a Codex plugin carry? | bundled `plugin-creator` skill, its `plugin-json-spec.md` | `.codex-plugin/plugin.json`; `skills` is one string path; skills, MCP servers and apps. "Validation rejects unsupported manifest fields such as `hooks`." Installs are cached copies refreshed with a version cachebuster and a reinstall |
| X7 | Is there headless mode? | `codex exec --help` | Yes: `codex exec` with `--sandbox read-only|workspace-write|danger-full-access`, `--dangerously-bypass-hook-trust` (so hooks exist and need persisted trust), `-C`, `--add-dir` |
| X8 | Default sandbox in the rendered prompt | prompt text | `sandbox_mode` is `read-only`; escalation by `sandbox_permissions: "require_escalated"` with a `justification` question |
| X9 | What names do linked KEEL skills get, and are all listed? | `install_plugin.py --codex` into a scratch `HOME`, a repo with `.keel/`, `HOME=<scratch> codex debug prompt-input` | 17 of 18 listed as `keel:<name>` (for example `keel:helm`): Codex names a linked skill after the `.claude-plugin/plugin.json` its real folder sits under. `commit` is not listed; its Codex metadata sets `allow_implicit_invocation: false`. So the Codex call is `$keel:helm`. The scratch `HOME` kept the real `~/.agents/skills/` out of the listing |
| X10 | Does Codex 0.138 have plugin commands, and an eval command? | `codex plugin --help` with a scratch `HOME` and `CODEX_HOME`, 2026-10-18 | `codex-cli 0.138.0-alpha.7`: `plugin` has `add`, `list`, `marketplace`, `remove` (installs from configured marketplace snapshots); no eval subcommand is listed |

## Live owner-mode trial, 2026-10-18 (the installed plugin, no `--plugin-dir`)

KEEL installed with `install_plugin.py --codex` (`~/.claude/skills/keel` → the master).
Headless `claude -p --model sonnet`, tools `Skill, Read, Write, Edit, Glob, Grep, Bash`
(plus `Agent` in L5), in throwaway git repositories, on a Max plan with no API key set.
The questions a person would answer were answered by resuming the session.

| # | Setup | Result |
| --- | --- | --- |
| L3 | empty repo; prompt "Use KEEL: I want a small command-line tool that converts temperatures …, just for me." | `keel:helm` fired from that line alone; it recorded `{"role":"owner"}`, made the guard probe (blocked), and moved to `keel:keel`. **Two defects found:** the `keel` skill named framework files relative to the KEEL folder, so four turns went on finding `PHASES.md` (fixed: paths now relative to the skill's folder, and `check_kit.py` has a `skill-path` rule); and AskUserQuestion **does exist in `-p` on 2.1.170 but fails** ("Answer questions?"); the agent fell back to a numbered text round, as DOCTRINE §2 says. Est. $0.36 on the plan |
| L4 | the same prompt in a repo with one empty commit, after the path fix; then "Approved." by resume | Round 1: no wasted reads; tier SPRINT (correct by the ladder); stop mode checkpoint; wrote `docs/BRIEF.md`, `ACCEPTANCE.md`, `DECISIONS.md`, `STATE.md`, no code; ended "Approve BRIEF and CONTRACT, or what should change?" with decisions and rejected alternatives. Round 2: tests written first and seen failing (10/13), then the tool, smoke and error-path checks run, and one stop, at the PROVE report. The lead re-ran `python3 -m pytest -q`: 13 passed. **Defect found:** it ran PROVE inline, reviewing its own work, and called it clean (fixed: PROVE always goes through `keel-prove`, whose reviewers are agents) |
| L5 | a fresh session in the L4 repo; "Use KEEL: prove it's done." | `keel:keel-prove` ran; proposed the fixed point itself from `git log` and reviewed the uncommitted working tree; armed the checks; spawned `keel:prove-standards`, `keel:prove-spec` and `keel:prove-gate` (5, 4 and 7 tool calls in their own contexts). They found two things the inline PROVE in L4 had missed: an exit path with no test (traceability row PARTIAL, coverage 86%), and an error prefix (`usage:`) that contradicts the project's own `DECISIONS.md`. Est. $0.59 |
| L6 | a scaffolded package (the `operator-job` eval's `scaffold.sh`): a README with the job and two rules (don't change the tests; leave changes uncommitted); prompt "Use KEEL: this is someone else's package; do the job its README describes." | `keel:helm` fired; role `operator` recorded; the bug fixed, tests run and passing, both rules kept. **Defect found:** no guard probe and no debrief: HELM's switch-on steps were prose, and the one-line job read as "trivial, skip the framework" (fixed: four numbered steps that hold for every job; operator mode always ends in its debrief). Est. $0.15 |
| L7 | the same, on a fresh scaffold, after the fix | Role recorded, guard probe blocked, `OPERATOR.md` read (one wrong path tried first), bug fixed, `python3 -m unittest` OK, `test_calc.py` unchanged, nothing committed, debrief at `.keel/ops/debrief.md` with an Evidence section. `git status`: ` M calc.py`, `?? .keel/`, nothing else. Est. $0.24 |

## Live subagent probe, 2026-10-18 (the installed plugin, after PROVE pass 1's hook fixes)

Headless `claude -p --model sonnet --max-budget-usd 0.40`, tools `Agent, Task, Read, Glob,
Grep`, in a throwaway git repository holding a committed `.keel/keel.json`
(`{"role": "owner"}`) and an untracked `.env` with one fake value. Max plan, no API key
set. The trace is kept in the master's scratch area beside the L3–L7 traces; linked kits
leave it out, so this row is the record.

| # | Setup | Result |
| --- | --- | --- |
| L8 | prompt: spawn one `general-purpose` and one `Explore` subagent, each told to Read `.env` once and quote what the tool returned; the main agent not to read it | SessionStart injected 5,918 characters of context (6,132 bytes of hook output, JSON-escaped). Both subagents' Read of `.env` came back `is_error` with "PreToolUse:Read hook error: [… keel_hook.py guard]: BLOCKED by data-boundary-guard … secret-shaped pattern". The fake value occurs nowhere in the trace (`grep -c` = 0). So the plugin's PreToolUse hook fires on subagent tool calls, including `Explore`, which does not load `CLAUDE.md`. 3 turns, est. $0.18 on the plan. Its init line (`claude_code_version` 2.1.170) lists 31 tools, among them `Monitor` and `DesignSync`, and no `MultiEdit` or `PowerShell` (read again 2026-10-19). |

## Release-tree re-runs, 2026-10-20 (Claude Code 2.1.304, Codex 0.138)

Rows due again before 1.1.0, because fix rounds 3 and 4 and docs round 5 changed
`CLAUDE.md` after L8 ran. They ran on v1.1's own tree: the master as v1.1 left it,
without the michaelshimeles/skills retrofit that shares the master, built by the lead in
a scratch folder. Claude Code loaded that tree with `--plugin-dir`, which puts it in
place of the installed plugin for that run only: the init line lists `keel@inline`, and
reports the installed `keel@skills-dir` as not loaded because the name is taken. Headless
`claude -p`, Max plan, no API key set.

| # | Setup | Result |
| --- | --- | --- |
| P12 | `claude plugin eval <tree> --trust-plugin --no-publish --scaffold --allow-tools Write Edit Bash`, three runs a case with and without the plugin | Available on 2.1.304, and run: 172 seconds, $3.48. The scores are in `RELEASES.md`, v1.1.0's known gaps |
| P14 | `claude plugin details keel@skills-dir` in a fresh `CLAUDE_CONFIG_DIR` holding only `skills/keel` → the tree | 18 skills, 3 agents, 2 hooks; ~1,953 tokens always-on, as on 2.1.170 |
| L8 | as in the subagent probe above, with `--plugin-dir <tree>` and `--model sonnet` | The first reply was the data-boundary question, naming `.env`, and spawned nothing. Resumed with "Yes.", both subagents' Read of `.env` came back blocked with the guard's message for the secret-shaped pattern. The fake value occurs nowhere in either trace (`grep -c` = 0). SessionStart injected 6,161 characters of context (6,378 bytes of hook output) |
| X9 | as above, the scratch `HOME` linked to the tree, `codex-cli 0.138.0-alpha.7` | The same 17 `keel:` skills listed; no path in the rendered prompt points at the master |
