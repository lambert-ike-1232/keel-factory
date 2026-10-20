# CAPABILITIES — what the agent can physically do, and the rule that the framework never asks for more

The hardest failure mode for a framework like this is not asking too little. It is asking
for something the agent **cannot actually do**, and getting a confident fabrication back
instead of a refusal. A skill that says "ensure the deployment is healthy" to an agent
with no access to the deployment does not produce a healthy deployment; it produces a
sentence that says it did. The whole evidence discipline exists to prevent exactly that,
and it starts here: **every action the framework asks for must map to a real affordance
the agent has in the environment it is running in.**

> **The grounding rule.** A skill, phase, or doctrine may only instruct an action that
> some actual tool can carry out. If a step cannot be executed by a real affordance, it is
> not a step — it is a wish, and it gets rewritten into something that can be done, or
> handed to the human as a gate. "Do X" where no tool does X is a bug in the framework,
> not an instruction to the agent.

## The affordance classes an AI coding agent actually has

These are the *kinds* of thing an agent in this class can do. The exact tool names differ
by host (Claude Code, Codex, Cursor, …), but the classes are stable, and the framework is
written against the classes, not one host's names. **Check what is actually present in the
session before relying on it** — the roster below is the superset, not a guarantee.

| Affordance | What it enables | The framework work it backs |
|---|---|---|
| **Read files** | Comprehension of anything on disk | RECON mapping, resume, reading `docs/` and the board |
| **Search / grep / glob** (e.g. ripgrep) | Finding symbols, usages, patterns at scale | "what does the code say," crossing joins, convention-reading |
| **Explore (read-only subagent)** | Breadth-first codebase survey without burning main context | RECON, "find where X is," broad lookups |
| **Write / edit files** | Authoring code, docs, artifacts | every phase's output; board tasks; the slices themselves |
| **Run commands (terminal)** | Build, test, run, measure, verify — the only affordance that produces **Evidence** | PROVE's gate, arming checks, the board validators, cost measurement, spikes |
| **Web search + fetch** | Learning external knowledge from authoritative sources | the deep-research sense (`../capabilities/deep-research/`) |
| **Subagents (parallel, clean-context)** | Independent review; parallel investigation; work that must not share context with its author | PROVE's three-axis review; parallel research; CREW's lanes (`../skills/crew/`) |
| **Isolated checkouts (git worktrees)** | A separate working copy per worker, so parallel edits cannot touch each other's files | CREW's `worktree` lanes. Needs git; in Claude Code, `isolation: "worktree"` on a subagent. Not a fence by itself (`CREW.md` §9) |
| **Continuing a worker / agent messaging** | Following up with a worker that keeps its context; agents on a shared task list | CREW's back-brief. Claude Code's agent teams are experimental and off by default, so check before relying on them |
| **Perception (via an external tool like REA)** | Seeing systems with no readable source | the reverse-engineering sense (`../capabilities/reverse-engineering/`) |
| **Scheduled / background execution** | Work that continues without a prompt each cycle | LOOPS.md loops — under its seven guardrails, never unbounded |
| **Tool-call hooks (host-dependent)** | Enforcing a rule at the moment of action | the harness (`../../harness/`) — see the honesty note below |
| **Put a file in front of the user** | Hand over a report/artifact across devices | status reports, RECON maps, review findings |

## The rule of mapping need → affordance

When a discipline needs something done, route it to the affordance that actually delivers
it, and prefer the one that produces the strongest evidence:

- **"Is it true?"** → *run the command.* Reading the code tells you what it should do;
  running it is the only thing that produces Evidence (Rule 2). A claim that was only read
  is `Inferred` at best.
- **"What does the world know?"** → *the deep-research sense*, authoritative sources,
  triangulated — not a guess dressed as fact.
- **"What is this opaque thing doing?"** → *the perception sense*, under its authorization
  gate — not a guess about a binary.
- **"Is this review independent?"** → *a clean-context subagent*, because an agent
  reviewing its own fresh output inflates, structurally. Same-context "review" is not
  independent and the framework does not pretend it is.
- **"Can this run without a human each cycle?"** → *scheduled/background execution*, but
  only with LOOPS.md's stop condition, cost ceiling, and escalation trigger in place.

## What each harness offers on this machine (checked 2026-10-18)

The classes above say what kind of thing an agent can do. This section says what two real
harnesses do, need by need, so other KEEL documents can point here instead of restating
it. It covers Claude Code 2.1.170 and Codex CLI 0.138.0-alpha.7 (the binary inside the
Codex desktop app, not on `PATH`), as found on the machine that built KEEL v1.1.

- **Evidence**: a probe or a live run on this machine produced it. The IDs P1–P14, X1–X10,
  L1–L8 are in [HARNESS-PROBES.md](HARNESS-PROBES.md), with the commands.
- **Inferred**: documentation or an extracted system prompt says it, or a probe only read
  bundled text. The docs describe newer builds (Claude Code up to about 2.1.29x, Codex
  0.163), so an Inferred row may not hold on these versions.
- **Missing evidence**: nothing was observed.

Doc URLs were read on 2026-10-18. An "extracted system prompt" is a captured prompt of the
named build, cited by file and line. The captured prompts do not ship with the kit: they
were read, as untrusted data, from a local folder outside it on the machine that built
v1.1, so their file and line citations cannot be followed from the kit. The KEEL master's
working notes summarize them with the same citations (in `.scratch/v1.1/research/`:
`research-codex-prompts.md` and `research-claude-code-prompts.md`); linked kits leave
that folder out.
Every row that rests on a captured prompt stays Inferred. A newer version can change any
row; re-probe before a decision rests on an Inferred row.

### Claude Code 2.1.170

| Need | What it does here | Label | Source |
| --- | --- | --- | --- |
| Skills listed to the model | Name and description per skill; the body loads on use. Plugin skills are namespaced `keel:<name>`: the master loads 18 (P14); 17 are listed, because `commit` is hidden (P5's flag); L1, run before `keel` was unhidden, saw 16 | Evidence | P4, P14; L1 for the 16; the 17 listed is Inferred from P5 and the skills' frontmatter |
| Description cap and listing budget | Each description, with `when_to_use`, is cut at 1,536 characters. The listing gets about 1% of the context window. On overflow every name stays and descriptions are dropped, least-invoked skills first | Inferred | [skills docs](https://code.claude.com/docs/en/skills#skill-descriptions-are-cut-short) |
| Hide a skill from the model | `disable-model-invocation: true` removes it from the model's list | Evidence | P5 |
| Install once, live | `--plugin-dir <master>` and a symlink in `~/.claude/skills/` both load the master in place, with no copy | Evidence | P9, L1 |
| Pinned install | A marketplace install from a local path copies to `plugins/cache/…`; source edits do not reach the copy. The docs say local-path plugins load in place; not on this version | Evidence | P8 |
| Plugin agents | The default `agents/` folder registers `<plugin>:<name>` subagent types. The manifest's `agents` file array registered none, though the docs accept it | Evidence | P4, P10 |
| Plugin validation | `claude plugin validate` fails a missing path or a bad name, warns on an unknown field, and passes a skill with no `description` | Evidence | P2, P3 |
| Always-on context from a plugin | A plugin cannot ship `CLAUDE.md`: one at the plugin root is not loaded, and validate warns | Inferred | [plugin manifest reference](https://code.claude.com/docs/en/plugins-reference#standard-layout) |
| SessionStart context | A plugin SessionStart hook's `additionalContext` reaches the model. In a repo without `.keel/`, KEEL's hook injected nothing | Evidence | P6, L1, L2 |
| Long SessionStart text | Over 10,000 characters is written to a file; the model gets the path and a preview | Inferred | [hooks docs](https://code.claude.com/docs/en/hooks) |
| Import through a linked kit | `@keel-factory/CLAUDE.md` through a linked `keel-factory/` resolves outside the project, which the docs treat as an external import: the user is asked once, and if they decline, imports stay off and the dialog does not return. KEEL's session hook then gives only its header ([harness README](../../harness/README.md)), so the layer, data-boundary rule included, would be missing. Not run here; the probe is an owner-gated follow-on | Inferred | [memory docs](https://code.claude.com/docs/en/memory), read 2026-10-19 |
| Who does not get `CLAUDE.md` | Built-in Explore and Plan subagents start without it; other subagents load it | Inferred | [subagents docs](https://code.claude.com/docs/en/sub-agents) |
| Fresh context for a reviewer | Plugin agents `keel:prove-*` ran as subagents in their own contexts, with their own tool calls, and found what the builder's same-context review missed | Evidence | L5 |
| Block a tool call | A plugin PreToolUse hook, the data-boundary guard, blocked a Read of `.env` where `.keel/` exists and let it through where it does not | Evidence | L1, L2 |
| When a hook fails | Exit 2 blocks. Any other exit, a crash, a timeout or bad JSON lets the call through. `onFailure: "block"` needs 2.1.295 or later, so here a hook cannot be set to fail closed; the script has to fail closed itself | Inferred | [hooks docs](https://code.claude.com/docs/en/hooks) |
| When new wiring arms | A hook written into a settings file mid-session may load only after the user opens `/hooks` or restarts: the settings watcher covers only folders that held a settings file when the session started. The model cannot open `/hooks` itself, and the desktop app has no `/hooks` dialog, so there only a restart arms it. A plugin installed mid-session loads from the next session; whether opening `/hooks` loads it sooner is Missing evidence. Until a probe there comes back blocked, strict policy stands | Inferred | extracted Claude Code skill text (snapshot near 2.1.301), `skills/update-config/SKILL.md:362`; extracted desktop app prompt, `claude-code-desktop-fable-5.1.md:115`; not probed on 2.1.170 |
| Hooks in subagents | The plugin's PreToolUse hook fires on subagent tool calls, `Explore` included: both subagents' Read of `.env` came back blocked. The docs add `agent_id` to the hook input; the trace does not record the input, so that part was not observed | Evidence | L8; [hooks docs](https://code.claude.com/docs/en/hooks) for `agent_id` (Inferred) |
| Tools outside the guard's matcher | Claude Code's Monitor tool, and PowerShell on Windows, run shell commands that the matcher does not name, so the guard never sees them (Inferred from the matcher). MCP tools are not matched either. 2.1.170 offers Monitor and DesignSync, and no PowerShell on this Mac | Inferred | the matcher in [`plugin-hooks.json`](../../harness/plugin-hooks.json); L8 for the tool list (Evidence) |
| Structured question | AskUserQuestion: 1–4 questions, 2–4 options each, "Other" added; not given to subagents. In a headless `-p` run on 2.1.170 the tool is offered but fails ("Answer questions?"), and the agent falls back to a numbered text round | Evidence | L3, L4 (headless); [subagents docs](https://code.claude.com/docs/en/sub-agents) for the limits (Inferred) |
| Headless run | `claude -p` runs a session with no human and exits | Evidence | P4, L1 |
| Cost cap | `--max-budget-usd` was accepted. Per the docs it works in print mode only, checks a client-side estimate, and spend can pass it; subagent enforcement needs 2.1.217 or later. Stopping at the cap was never tested. `--max-turns` limits the agentic turns in print mode and exits with an error at the limit; not run here | Inferred | P4–P6, P11 (flag accepted); [CLI reference](https://code.claude.com/docs/en/cli-reference) |
| Keep a turn from ending | A Stop hook can refuse to let a turn end (exit 2, or `decision: "block"` with a reason), and the agent keeps working. After eight such continuations in a row the next block is overridden and the turn ends; the count resets whenever a tool is called, and `CLAUDE_CODE_STOP_HOOK_BLOCK_CAP` raises it. Not run here | Inferred | [hooks docs](https://code.claude.com/docs/en/hooks) (Stop input) |
| Recurring work | CronCreate and `/loop` tasks belong to the session, fire only while it is open and idle, and recurring ones expire after 7 days. Durable schedules are cloud routines, desktop scheduled tasks or GitHub Actions | Inferred | [scheduled tasks docs](https://code.claude.com/docs/en/scheduled-tasks) |
| Plugin evals | `claude plugin eval` does not exist here; the docs require 2.1.269 or later | Evidence | P12; [plugin evals docs](https://code.claude.com/docs/en/plugin-evals) |
| Context cost estimate | `claude plugin details` reports an always-on token estimate; SessionStart text is not counted in it. The estimate depends on the config: ~1,953 tokens in a fresh config, ~2,530 in the build machine's | Evidence | P13, P14 |

### Codex CLI 0.138.0-alpha.7

| Need | What it does here | Label | Source |
| --- | --- | --- | --- |
| Skills listed to the model | Skills in `.agents/skills/` appear as name, description and `SKILL.md` path; the body is not in the prompt. A linked skill whose real folder sits under a `.claude-plugin/plugin.json` is named after that plugin: KEEL's links list as `keel:helm` and so on, called `$keel:helm`. A skill whose metadata sets `allow_implicit_invocation: false` (`commit`) is not listed | Evidence | X2, X9 |
| Description cap and listing budget | Each description is cut at 1,024 characters. The catalog gets about 2% of the context window, or 8,000 characters if the window is unknown. Over the cap, descriptions are shortened first, then skills are left out with a warning | Inferred | [skills docs](https://learn.chatgpt.com/docs/build-skills); `openai/codex` source at `rust-v0.163.0` |
| Install once, live | Symlinked skill folders are followed, and `~/.agents/skills/` is read whatever `CODEX_HOME` says. Whether an edit shows up without a restart was not tested | Evidence | X3, X5 |
| Pinned install | Plugins install as cached copies, refreshed by a version cachebuster and a reinstall. Read from the 0.138 bundled plugin spec, not run | Inferred | X6 |
| Always-on context | A root `AGENTS.md` is injected verbatim | Evidence | X4 |
| `AGENTS.md` size | Combined content is capped at 32 KiB (`project_doc_max_bytes`); past it, files are left out. `CLAUDE.md` is read only if named in `project_doc_fallback_filenames` | Inferred | [AGENTS.md docs](https://learn.chatgpt.com/docs/agent-configuration/agents-md) |
| SessionStart context | A SessionStart hook's stdout or `additionalContext` becomes developer context. Not observed on 0.138 | Inferred | [hooks docs](https://learn.chatgpt.com/docs/hooks) |
| Hooks present | `hooks` is on. Hooks need persisted trust, which `codex exec --dangerously-bypass-hook-trust` skips for one run | Evidence | X1, X7 |
| Block a tool call | Not observed: no Codex model call has run with the guard wired in | Missing evidence | none yet; L1 covers Claude Code only |
| File reads | In Codex every file read is a shell command, so the guard sees it only as Bash and covers it only through its Bash heuristic: a blocked probe shows the hook is wired, not that reads are covered. The docs' list of tools PreToolUse sees has no dedicated read tool | Inferred | [hooks docs](https://learn.chatgpt.com/docs/hooks); what the heuristic misses is in [`DATA-BOUNDARY.md`](../../harness/DATA-BOUNDARY.md) |
| Hook semantics | Exit 2 blocks only with a non-empty stderr; any other failure, a timeout or an `ask` decision lets the call through. Project hooks load only in trusted projects, and each definition must be trusted in `/hooks`. `apply_patch` arrives as patch text in `tool_input.command`, with no `file_path` | Inferred | [hooks docs](https://learn.chatgpt.com/docs/hooks); `openai/codex` source at `rust-v0.163.0` |
| Hooks inside a plugin | The 0.138 bundled spec says validation rejects a `hooks` manifest field. The 0.163 docs accept one for manually installed plugins, and the removed `plugin_hooks` flag fits either reading. Trust the bundled spec for 0.138 until a plugin's hook is seen to run | Inferred | X6, X1; [plugins docs](https://learn.chatgpt.com/docs/plugins) |
| Structured question | `request_user_input` works only in Plan mode; the flag that would allow it in Default mode is off. Not available in `codex exec` | Inferred | X1 (flag off); extracted Codex system prompt, `gpt-6.1-sol.md:494-516`; `openai/codex` source at `rust-v0.163.0` |
| Checkpoint's up-front round | In Plan mode the round runs as `request_user_input` questions with options. In Default mode there is no choice prompt, and KEEL asks one question per turn as a sentence that names the pick, so the round takes as many turns as it has questions (about eight topics, [TIERS.md](TIERS.md) "Stop modes"). No Codex trial has run one | Inferred | the Structured question row; extracted Codex system prompt, `gpt-6.1-sol.md:494-516`; `DOCTRINE.md` §2 |
| Fresh-context reviewer | Multi-agent v1 is on, v2 off. v1 `spawn_agent` starts with only its prompt unless `fork_context: true`. The v1 prompt spawns only when the user explicitly asks; the docs also let `AGENTS.md` or a skill ask. Trust the v1 prompt for 0.138. Claude plugin `agents/` are not loaded as Codex subagents | Inferred | X1; extracted Codex 0.140.0-alpha.2 system prompt, `codex-full.md:1279-1281`; [subagents docs](https://learn.chatgpt.com/docs/agent-configuration/subagents) |
| Headless run | `codex exec` exists, with `--sandbox`, `-C` and `--add-dir` | Evidence | X7 |
| Approvals in a headless run | `codex exec` forces `approval_policy = never`; an action that needs approval fails | Inferred | [non-interactive docs](https://learn.chatgpt.com/docs/non-interactive-mode); `openai/codex` source at `rust-v0.163.0` |
| Default sandbox | The rendered prompt shows `sandbox_mode` as `read-only`; escalation asks via `sandbox_permissions: "require_escalated"` with a justification | Evidence | X8 |
| Cost cap on a headless run | No spend or turn cap for `codex exec` was seen | Missing evidence | X7 lists none |
| Token ceiling on a goal | `goals` is on; `create_goal` takes an optional `token_budget`. A goal may be set `blocked` (`update_goal`) only after the same blocker held for 3 consecutive goal turns, automatic continuations included | Inferred | X1; extracted Codex 0.140.0-alpha.2 system prompt, `codex-full.md:518-600`; extracted Codex system prompt, `gpt-6.1-sol.md:741-891` (the blocked rule) |
| Recurring work | The desktop app has automations under `$CODEX_HOME/automations/`: `heartbeat` re-wakes a thread, `cron` runs a job. Nothing for CLI 0.138 was observed | Inferred | extracted Codex 0.140.0-alpha.2 system prompt, `codex-full.md:627` |
| Plugin evals | `codex plugin --help` on 0.138 lists `add`, `list`, `marketplace` and `remove`, no eval command. The 0.163 docs and source show none either | Evidence | X10; [plugins docs](https://learn.chatgpt.com/docs/plugins) and `openai/codex` source at `rust-v0.163.0` for 0.163 (Inferred) |

### Windows: untested

Every row above was checked on macOS. Nothing in KEEL has run on Windows (Missing
evidence, 2026-10-18). Read from the scripts, these points would bite there (Inferred):

- `../../harness/install_plugin.py` and `../../harness/link_kit.py` make symlinks, which
  Windows creates only with Developer Mode on or from an administrator shell.
- Every KEEL hook command is POSIX `sh` that runs `python3`
  (`../../harness/plugin-hooks.json` and the Codex hook commands). A Windows machine may
  have no `python3`, or only the Microsoft Store stub.
- A missing `python3` exits 127 (Evidence on this Mac: `env PATH=/nonexistent-keel-probe
  /bin/sh -c 'exec python3 -c 1'` printed "exec: python3: not found", exit 127). Both
  harnesses read any exit but 2 as an allow ("When a hook fails", "Hook semantics"), so
  the guard would let every call through and the session hook would inject no layer,
  without a word.
- The Claude Code PreToolUse matcher in `plugin-hooks.json` names no PowerShell tool, so a
  PowerShell call on Windows would not reach the guard (raised by PROVE's completeness
  critic, COMPLETENESS-12).

### Re-checking a row

- Claude Code: `claude -p --plugin-dir <dir>` shows skills, hooks and injected context;
  `claude plugin validate` and `claude plugin details` check a manifest and its context
  cost; `claude plugin eval --help` shows whether evals exist.
- Codex: `codex features list` shows the flags; `codex debug prompt-input` renders what the
  model sees without a model call; `codex exec --help` lists the headless flags. Moving
  "Block a tool call" off Missing evidence takes a real `codex exec` run in a trusted
  project with the hook trusted.

Record each new result in [HARNESS-PROBES.md](HARNESS-PROBES.md) under a new ID, then
update the row here.

## Honesty about this environment — a worked example of the rule

This is not abstract. On the machine where this factory was last built:

- **Python 3.13, git 2.50, ripgrep 14 are present** → the task-board validators and index
  generator actually run. Tested, both directions: clean board exits 0, a board with a
  dangling reference exits 1 with the finding named. That layer is **Evidence-grade
  functional**, not prose.
- **Node.js is absent** → the harness hooks (`block-no-verify.js`, `config-protection.js`,
  `data-boundary-guard.js`, `cost-tracker.js`) **cannot execute here.** The grounding rule
  forbids pretending otherwise. So on a Node-less machine the harness enforcement is
  `Missing evidence`, and the framework says so rather than implying a backstop that isn't
  running. Two honest remedies: install Node where the hooks are needed, or port the
  critical hook to Python, which *is* present. The second is done: the data-boundary
  guard's Python version (`../../harness/hooks/data-boundary-guard.py`) was executed and
  proven in both directions here on 2026-10-14. The other three hooks remain Node-only
  and unexecuted, so they stay `Missing evidence`.

That is the rule doing its job: the framework states what actually runs, flags what does
not, and never asks the agent to rely on a capability the environment does not provide.

## When a needed affordance is genuinely absent

Do not fabricate the result, and do not silently skip the step. Instead:

1. **Name the gap** — "this step needs X; X is not available in this session."
2. **Offer the real alternatives** — a different affordance that gets partway, a human
   gate for the part only a person can do, or installing/enabling the missing tool.
3. **Label the consequence honestly** — what stays `Missing evidence` because the check
   could not run. A gate that cannot run is `FAIL`/`PARTIAL`, never a silent `PASS`.

This is the same posture the data-boundary rule takes when a harness has no hooks: state
the limitation once, plainly, and operate within what is actually there.
