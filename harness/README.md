# Harness — curated from ECC, plus one guard authored for this factory

Source: *ECC — Everything Claude Code*, Affaan Mustafa, `github.com/affaan-m/ECC`, MIT
licensed (full text in `LICENSE-ECC.txt`). The full project — 286 skills, ~40 hooks,
agents, rules, plugins — was downloaded to `~/Downloads/ECC-main`. **Nothing here is a
full mirror of that.** This folder holds only what
[`../keel/framework/ECC-CROSSREF.md`](../keel/framework/ECC-CROSSREF.md) already read,
evaluated, and named as an adoption candidate — three hook scripts that are wired and
tested in ECC itself, twelve `SKILL.md` write-ups the cross-reference cites directly, and
one hook (`data-boundary-guard.js`, now with a Python version, `data-boundary-guard.py`)
written for this factory because ECC does not ship anything that plays this role. If you want to browse past this curated set, the source is
the Downloads copy or the GitHub repo, not a copy pasted in here without having read it
first.

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
  **not from ECC.** The Python version is the only hook here that has actually been
  executed (its self-test and armed check, 2026-10-14). Written for this factory to block
  reading, editing, or writing any path a project's `.gitignore` excludes, or any path
  shaped like a secret or credential, by default — because the production-system use case
  this factory is meant for cannot depend on a human remembering to protect every
  sensitive path by hand. Default-deny; the only way past it is a deliberate, human-made
  override. Full detail, the exact patterns it matches, and — importantly — **how to
  verify it actually blocks before trusting it**, in [`DATA-BOUNDARY.md`](DATA-BOUNDARY.md).

## Linking the kit into a project — `link_kit.py`

`python3 harness/link_kit.py <project>` gives a project a `keel-factory/` folder of
symbolic links to this master, plus a real `.ops/` for that project's notes. `--remove`
deletes only the links. It refuses to touch any `keel-factory/` it didn't make, such as an
old full copy. Self-test: `python3 harness/test_link_kit.py`.

## Setting up a machine and cutting releases

- `python3 harness/install_guard.py` installs the self-disarming data-boundary guard into
  `~/.claude/settings.json`, keeping everything else in the file. `--remove` takes it out
  again. Self-test: `python3 harness/test_install_guard.py`.
- `python3 harness/make_release.py` cuts the release named in `VERSION`. It writes a git
  bundle, an archive, the manual and checksums, then proves the release by cloning it
  fresh and running every self-test from the clone.

## Wiring — `settings.hooks.json`

All four are written directly against Claude Code's native `PreToolUse`/`Stop` hook
contract (not ECC's `run-with-flags.js`/`hooks.json` dispatcher — that layer wasn't
copied in). [`settings.hooks.json`](settings.hooks.json) is the ready-to-use wiring:
merge its `hooks` block into the project's `.claude/settings.json`
(or `.claude/settings.local.json` to keep it personal rather than committed), replacing
every `/ABSOLUTE/PATH/TO/` with the real path to this `harness/hooks/` directory. Copying
the `.js` files alone does not activate them — this file is what does. On a machine
without Node, a `node …` hook command exits 127, which Claude Code treats as a
non-blocking error, so the call goes ahead. That is why the templates wire the
data-boundary guard's Python version (`DATA-BOUNDARY.md`).

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
