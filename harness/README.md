# Harness — curated from ECC, plus one guard authored for this factory

Source: *ECC — Everything Claude Code*, Affaan Mustafa, `github.com/affaan-m/ECC`, MIT
licensed (full text in `LICENSE-ECC.txt`). The full project — 286 skills, ~40 hooks,
agents, rules, plugins — was downloaded to `~/Downloads/ECC-main`. **Nothing here is a
full mirror of that.** This folder holds only what
[`../keel/framework/ECC-CROSSREF.md`](../keel/framework/ECC-CROSSREF.md) already read,
evaluated, and named as an adoption candidate — three hook scripts that are wired and
tested in ECC itself, twelve `SKILL.md` write-ups the cross-reference cites directly, and
one hook (`data-boundary-guard.js`, now with a Python version, `data-boundary-guard.py`)
written for this factory because ECC does not ship anything that plays this role.
If you want to browse past this curated set, the source is the Downloads copy or the
GitHub repo, not a copy pasted in here without having read it first.

## hooks/ — mechanism, not prose

These are the three hooks `ECC-CROSSREF.md` §4.1 and §4.8 call out as genuine enforcement
(as opposed to a written guideline an agent can talk itself past):

- **`block-no-verify.js`** — blocks `git commit --no-verify` and
  `-c core.hooksPath=` tricks. This is the mechanism behind KEEL's proposed Rule 6e (gate
  immutability): a gate the agent can route around is not a weaker gate, it's a gate
  whose green result means nothing.
- **`config-protection.js`** — refuses to let the agent edit protected lint/format
  config files at all, rather than trusting it not to loosen them under pressure.
- **`cost-tracker.js`** — records token/cost data per run. Ships with a named failure
  worth reading before you trust any cost pipeline: an earlier version silently produced
  2,340 zero-filled rows over 52 days because it expected fields that weren't there. The
  fix embedded in this version is the reason it's worth taking as-is rather than
  rewriting from scratch — see the comment at the top of the file.
- **`data-boundary-guard.py`** and its Node original **`data-boundary-guard.js`** —
  **not from ECC.** Unlike the three ECC hooks and the Node original, the Python version
  has been executed: its self-test and armed check (2026-10-14), and live through
  `keel_hook.py` under the plugin
  ([`HARNESS-PROBES.md`](../keel/framework/HARNESS-PROBES.md), L1–L8). Written for this
  factory to block reading, editing, or writing any path a project's `.gitignore`
  excludes (inside a git repository; `DATA-BOUNDARY.md` has the limits), or any path
  shaped like a secret or credential, by default — because the production-system use
  case this factory is meant for cannot depend on a human remembering to protect every
  sensitive path by hand. Default-deny; the only way past it is a deliberate, human-made
  override. Full detail, the exact patterns it matches, and —
  importantly — **how to verify it actually blocks before trusting it**, in
  [`DATA-BOUNDARY.md`](DATA-BOUNDARY.md).

## The plugin's two hooks — `keel_hook.py`, `plugin-hooks.json`, `settings.hooks.codex.json`

Authored for this factory in v1.1. One script, two subcommands, used by both harnesses:
`keel_hook.py session [--harness claude|codex]` and `keel_hook.py guard [--harness
claude|codex]`. The default is `claude`; Codex's hook commands, the installer's and the
template's, pass `--harness codex`. Only `session` acts on it; `guard` behaves the same
for both.

- **`keel_hook.py session`** (SessionStart) injects KEEL's always-on layer, the root
  `CLAUDE.md`, with a header naming the kit root and the project's role. It gives only
  the header when the project's own instruction files, as this harness loads them,
  already carry the layer. For Codex that is an `AGENTS.md` holding the mark
  `<!-- KEEL always-on layer -->`. For Claude Code it is a `CLAUDE.md`, `CLAUDE.local.md`
  or `.claude/CLAUDE.md` that holds the mark, or an import line `@keel-factory/CLAUDE.md`
  (or `@./keel-factory/CLAUDE.md`) that resolves, from that file's own folder, to a file
  holding the mark; and an `AGENTS.md` only when one of those imports `@AGENTS.md`. A
  prose mention of the path, or an import with nothing to import, never counts, so the
  worst case is the layer twice, never none. An import line inside a fenced code block
  still counts (a follow-on). A v1.0 copy of `CLAUDE.md` (it says "This project was
  started from KEEL FACTORY.") gets the header and a one-line upgrade note instead of a
  second layer. The note offers the import `@keel-factory/CLAUDE.md` only when
  `keel-factory/CLAUDE.md` exists beside that file and holds the mark. Otherwise it says
  to delete KEEL's v1.0 text from that file (the hook then supplies the layer), or to
  replace it with v1.1's `CLAUDE.md`. Codex's note never offers the import.
- **`keel_hook.py guard`** (PreToolUse) hands the call to the unchanged
  `data-boundary-guard.py`, after turning a Codex `apply_patch` (patch text, no file path)
  into one path check per file the patch names. It also guards the guard's allowlist,
  `.keel/data-boundary-allow`, which only the user edits, by blocking the direct ways of
  writing it: a Write, Edit, MultiEdit or NotebookEdit of that file, a Codex patch naming
  it, and any shell command containing `data-boundary-allow`, even under
  `KEEL_DATA_BOUNDARY_OVERRIDE=1`; a Read of it is allowed. It is a tripwire, not a lock:
  the match is on paths and command text, so a rename, a variable or a script gets past
  it (`DATA-BOUNDARY.md`, "What this does not cover"). Only `keel_hook.py` has this block.
  The bare wirings (`install_guard.py`, `settings.hooks.json`, `OPERATOR.md`'s fallback
  hook) run `data-boundary-guard.py` directly and do not. The guard honors a
  `.keel/data-boundary-allow` at the nearest git root of each path, so a submodule or a
  nested clone can bring its own; HELM's switch-on check lists every `.keel/` folder
  below the root as well. The details are in `DATA-BOUNDARY.md`, "What this does not
  cover".
- **Both do nothing unless KEEL is switched on** in the project. `KEEL_GUARD=always` arms
  the guard everywhere; it never switches the session layer on. The rule, which the other
  documents point to here:
  - The start is `CLAUDE_PROJECT_DIR` when the harness sets it (Claude Code does), else
    the `cwd` in the hook's input (Codex sends one), else the working directory.
  - The git root is the nearest folder at or above the start that holds `.git`, a folder
    or a worktree's file.
  - Inside git, KEEL is on when a folder from the start up to and including the git root
    holds an entry named exactly `.keel` (a folder) or exactly `keel-factory` (a folder or
    a link to one); the nearest wins. Names are compared exactly, from a listing of the
    folder, because macOS ignores letter case: `KEEL-FACTORY` is not a marker. A linked
    git worktree also checks its main checkout's root; a submodule does not.
  - Outside git, only the start folder counts.
  - Never on: a start at or inside the kit root; a marker in `$HOME` or `/`; a
    `keel-factory` entry that is the kit root itself when the kit root is the master's
    own git checkout (it holds a `.git` folder, or a linked worktree's `.git` file whose
    gitdir holds `commondir`); a worktree whose main checkout is the kit. A copy made
    with MANUAL §4's rsync (no `.git`) switches KEEL on; a copy that keeps `.git` (a
    `git clone`, `cp -R` or a Finder copy) counts as a master's own checkout and stays
    dormant when its own hooks run. A submodule-vendored kit or a link switches KEEL on
    too; each gives role kit. Two rare cases also switch on, failing closed: a master
    that is a worktree of a bare repository, and a master restored from the archive
    without `.git` and renamed to lowercase `keel-factory`, each seen from the folder
    that holds it.
  - Role: `.keel/keel.json` gives owner or operator, anything else "not recorded"; a
    `keel-factory` entry gives "kit".
- **Wiring.** Claude Code: the plugin carries it in `plugin-hooks.json` (PreToolUse
  matcher `Read|Edit|MultiEdit|Write|NotebookEdit|Glob|Grep|Bash`), nothing to wire.
  Codex: `install_plugin.py --codex-hooks` merges the same two hooks into `hooks.json` in
  the Codex home (`$CODEX_HOME` when it is set, else `~/.codex`) and prints the path it
  wrote. `install_plugin.py --codex-hooks` writes machine-wide hooks that run the kit it
  was run from: run it from the master (or through a linked `keel-factory/`), never from
  a copy inside a project. Each command holds that kit's absolute, shell-quoted path.
  Codex runs them only after you trust them in `/hooks`, and no Codex session has yet
  been seen blocking with them (Missing evidence;
  [`../keel/framework/CAPABILITIES.md`](../keel/framework/CAPABILITIES.md)).
  `settings.hooks.codex.json` is the template for wiring by hand: its
  `/ABSOLUTE/PATH/TO/` stands for the kit root, the folder that holds `harness/`.
- **Two ECC hooks left the Codex template in v1.1.** It no longer wires
  `config-protection.js` (it reads `tool_input.file_path`, and Codex edits through
  `apply_patch`) or `cost-tracker.js` (it parses Claude Code transcripts). Both stay in
  `settings.hooks.json` for Claude Code.
- **Failing closed is the script's job.** Claude Code 2.1.170 treats a hook that crashes,
  times out or exits with anything but 0 or 2 as an allow (a setting to fail closed,
  `onFailure: "block"`, arrives in 2.1.295), and Codex does the same. So `keel_hook.py`
  catches its own errors and blocks where KEEL is on. A missing `python3`, which never
  starts the script, and a hook timeout still fail open. Two routes reach the timeout.
  One is a command with tens of thousands of path-shaped words (`DATA-BOUNDARY.md`,
  "What this does not cover"; K36). The other is a file KEEL reads that is linked to a
  device or a pipe. An allowlist linked that way stalls every guarded call in its
  repository, and a linked instruction file such as `CLAUDE.md` stalls the session hook
  (Evidence: links to `/dev/zero` and to a FIFO ran past test limits of 1 s and 3 s,
  PROVE pass 4, 2026-10-19; what happens at the real timeout is Inferred). Both stalls
  last until the fix filed as `keel-hook-hardening` item 9 on KEEL's board lands. See
  "When a hook fails" in
  [`../keel/framework/CAPABILITIES.md`](../keel/framework/CAPABILITIES.md).
- Self-test: `python3 harness/hooks/test_keel_hook.py` (108 tests; 93 deliberately broken
  copies of the script each failed it, after the unbroken script passed).

## Installing and checking the kit — `install_plugin.py`, `check_kit.py`

- `python3 harness/install_plugin.py` links this master into `~/.claude/skills/keel`,
  which Claude Code loads in place as the plugin `keel@skills-dir`. `--codex` links each
  skill into `~/.agents/skills/`, skipping a name already taken there, and warns when the
  skipped name is one of KEEL's own six (`$keel:helm` then does not work in Codex until
  the name is free); `--codex-hooks` adds the Codex hooks (above);
  `--with-docs` adds the four Diataxis skills; `--remove` takes out only what it made.
  Self-test: `python3 harness/test_install_plugin.py`.
- `python3 harness/check_kit.py` checks what `claude plugin validate` does not. It reads
  the skill lists from `install_plugin.py` and the always-on mark from `keel_hook.py`
  with `ast`, running no code (rule `source`), and checks that the plugin's skill folders
  are exactly the installer's (`skill-set`). Then: every skill's name and description
  against both harnesses' caps, the skill paths in KEEL's own skills, the Codex skill set
  (all 22 that `--codex --with-docs` links) and its metadata, the agents, the eval cases,
  the always-on sizes, the release record, and every relative link. Self-test:
  `python3 harness/test_check_kit.py`.

## Linking the kit into a project — `link_kit.py`

`python3 harness/link_kit.py <project>` gives a project a `keel-factory/` folder of
symbolic links to this master, plus a real `.ops/` for that project's notes. `--remove`
deletes only the links. It refuses to touch any `keel-factory/` it didn't make, such as an
old full copy. Self-test: `python3 harness/test_link_kit.py`.

## Setting up a machine and cutting releases

- `python3 harness/install_guard.py` installs the self-disarming data-boundary guard into
  `~/.claude/settings.json`, keeping everything else in the file. It is optional with the
  plugin, whose own hook guards every project where KEEL is on. It arms only in projects
  holding an entry named exactly `keel-factory`, not under the plugin's `.keel/`. That
  entry is only the switch: installed from the master, the hook runs the master's own
  guard, by its absolute, shell-quoted path, never the project's copy, so a package cannot
  ship a guard that lets everything through. Installed from a copy, it would run that
  copy's guard in every `keel-factory/` project, so run it from the master or through a
  link to it; if the master moves, the hook disarms until the script is run again. Running
  it again also updates an entry an older version wrote, in place, repointing it at the
  master's guard (those entries ran the project's copy). `--remove` takes it out again.
  Self-test: `python3 harness/test_install_guard.py`.
- `python3 harness/make_release.py` cuts the release named in `VERSION`. It refuses
  unless the current branch is `main`, before writing anything. It writes a git bundle,
  an archive, the manual and checksums, then proves the release by cloning it fresh and
  running every self-test from the clone. Its README-FIRST clones with `--branch main`.
  Self-test: `python3 harness/test_make_release.py`, in temporary git repositories only.

## Wiring — `settings.hooks.json`

All four are written directly against Claude Code's native `PreToolUse`/`Stop` hook
contract (not ECC's `run-with-flags.js`/`hooks.json` dispatcher — that layer wasn't
copied in). [`settings.hooks.json`](settings.hooks.json) is the ready-to-use wiring:
merge its `hooks` block into the project's `.claude/settings.local.json` or
`~/.claude/settings.json`, never the shared `.claude/settings.json`, replacing every
`/ABSOLUTE/PATH/TO/` with the real absolute path to the kit root, the folder that holds
`harness/` (each template path already ends in `harness/hooks/…`). The commands then
hold this machine's absolute path, and where that path is missing the guard's `python3`
exits 2, which blocks every call the guard matches (`DATA-BOUNDARY.md`). The form that
disarms itself instead is `install_guard.py`'s (above). Copying the `.js` files alone
does not activate them — this file is what does. On a machine without Node, a `node …`
hook command exits 127, which Claude Code treats as a non-blocking error, so the call
goes ahead. That is why the templates wire the data-boundary guard's Python version
(`DATA-BOUNDARY.md`).

## Safety review — what these four hooks can and can't touch

Done because this factory is meant to be safe to point at a production codebase without
a human re-auditing it first. All four:

- **Require only Node built-ins** (`fs`, `os`, `path`, `child_process`) — verified by
  grepping every `require(` in `hooks/*.js`. No npm dependencies, no supply-chain surface,
  nothing pulled in from the network.
- **Make no network calls** — no `http`, `https`, `net`, `dns`, `fetch`, or subprocess
  that reaches outside the local machine, anywhere in any of the four files.
- **Never read file contents**, only file paths, a shell command string, or (for
  `cost-tracker.js`) numeric token counts and a model name pulled from the transcript.
  None of the four can put your actual source code into a log, a network request, or
  anywhere else it wasn't already.
- `cost-tracker.js` originally pulled in ECC's general-purpose `lib/utils.js` (669 lines)
  and, transitively, a multi-harness config-file-driven path resolver
  (`lib/agent-data-home.js`, `lib/path-safety.js`) — none of which were copied in, so the
  hook would have crashed on first use. **Fixed**: the three functions it actually needs
  are inlined directly in the file (~15 lines), so its entire filesystem footprint —
  writes one line to `~/.claude/metrics/costs.jsonl`, reads only the transcript path
  Claude Code hands it — is auditable in a single read, with nothing hidden behind an
  import.

The Python version of the data-boundary guard was checked the same way: it imports only
the standard library (`json`, `os`, `re`, `subprocess`, `sys`, verified by grepping its
imports), makes no network calls, and reads the contents of exactly one file, the
human-made allowlist.

**What this review does not establish:** the `.js` files still have not been executed —
this machine has no Node.js installed, so this was static review (reading every line,
checking every `require`), not a test run. That is `PARTIAL` evidence under KEEL's own
Evidence Rule, not `PASS`. Run the armed-check below on a machine with Node before
trusting any of this against a real system.

## Prove each hook actually works before trusting it (Rule 6b)

```bash
H=/ABSOLUTE/PATH/TO/harness/hooks

# block-no-verify.js — must block, exit 2
echo '{"tool_input":{"command":"git commit --no-verify -m x"}}' | node "$H/block-no-verify.js"; echo "exit=$?"
# and must allow a normal commit, exit 0
echo '{"tool_input":{"command":"git commit -m x"}}' | node "$H/block-no-verify.js"; echo "exit=$?"

# config-protection.js — must block an existing config, exit 2
touch /tmp/.eslintrc.js
echo '{"tool_input":{"file_path":"/tmp/.eslintrc.js"}}' | node "$H/config-protection.js"; echo "exit=$?"

# data-boundary-guard (.py and .js) — see harness/DATA-BOUNDARY.md for its own armed check

# cost-tracker.js — must exit 0 and append one line to ~/.claude/metrics/costs.jsonl
echo '{"session_id":"test","transcript_path":"/nonexistent"}' | node "$H/cost-tracker.js"; echo "exit=$?"
tail -1 ~/.claude/metrics/costs.jsonl
```

If any result doesn't match what's described, the hook is not armed — fix it before
relying on it in a real project, not after.

## skills/ — the write-ups behind the rest of the cross-reference

Reference material, prose-only, exactly as cited in `ECC-CROSSREF.md` §4 and §5:

| Skill | Cited for |
|---|---|
| `loop-design-check` | Reconciliation-beats-assertion; the Goodhart antibody (§4.2) |
| `autonomous-loops` | Independent reviewer design; the LAND / merge-queue-with-eviction gap (§4.5, §4.6) |
| `continuous-learning-v2` | The parked cross-project Learning Rule and its promotion threshold (§4.3) |
| `rules-distill` | The governance loop for turning a candidate into a rule (§4.3) |
| `skill-comply` | Measuring whether a rule is actually followed under a competing prompt (§4.4) |
| `strategic-compact` | Window-scaled compaction threshold — the correction to KEEL's old fixed ~150k number (§4.7) |
| `recursive-decision-ledger` | Upgrading DESIGN's least-confident list into a decaying, append-only ledger (§4.9) |
| `delivery-gate` | The enforcement-vs-methodology trade-off stated explicitly; the rationalization-language detector (§4.10, §5) |
| `santa-method` | Fresh-reviewer-each-round, and why a single reviewer's blind spot is the failure mode independence exists to catch (§4.5) |
| `council-multi-model` | The honesty rule for claiming provider diversity — never claim it if the fallback silently used the same model (§4.5) |
| `gateguard` | Source for "LLM self-evaluation doesn't work," contradicting `agent-self-evaluation` (§3) |
| `context-budget` | The standing token tax of loaded tool schemas and skill frontmatter, independent of conversation growth (§4.7) |

Read these as ECC's own words, not KEEL's restatement of them — `ECC-CROSSREF.md` is the
analysis; these files are the primary source it was built from.
