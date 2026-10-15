# Data boundary

Two layers, doing two different jobs. Neither one alone is the answer.

1. **A hard block** (`hooks/data-boundary-guard.py`, and its Node original
   `hooks/data-boundary-guard.js`) — stops a tool call before it runs.
   Enforced in code, same posture as `block-no-verify.js` and `config-protection.js`:
   default-deny, and the only way past it requires a human to do something deliberate.
2. **A standing question the agent asks itself** (below, and in `../CLAUDE.md`) — before
   even attempting something invasive, not just when it happens to trip the hook.

Layer 1 exists because layer 2 is prose, and prose does not fail a build (KEEL Rule 6d —
the exact finding `ECC-CROSSREF.md` makes about KEEL itself, applied here). An agent
under pressure to finish a task can talk itself past a written guideline. It cannot talk
itself past `exit 2`.

## What the hook blocks, by default, with no configuration

Checked against every `Read` / `Edit` / `Write` / `NotebookEdit` call exactly (structured
`file_path`), every `Glob` / `Grep` call's target path exactly, and every `Bash` command
on a best-effort basis (a plain tokenizer, not a shell parser — treat this as a backstop,
not a guarantee). In a command, a word with a slash or a leading dot is checked as a
path; a plain word counts only when a file by that name exists where the command runs,
so `git config` and `grep secret` pass while `cat id_rsa` beside a real key does not.
A command may also use a project's own tool folders, `.venv/bin/`, `venv/bin/` and
`node_modules/.bin/`, though they are gitignored. That is how a project runs its own
checks. The Read, Edit and Write tools stay strict there, and secret-shaped names stay
blocked everywhere:

- **Anything the project's own `.gitignore` would exclude.** If it's not meant to be
  committed, it's not meant to be read into an agent's context or copied somewhere else
  either, by default.
- **Anything shaped like a secret, whether or not it's gitignored.** `.env*` (except
  `.env.example` / `.sample` / `.template`), `*credential*`, `*password*`, `*.pem`,
  `*.key`, SSH private keys, `.npmrc`/`.pypirc`/`.netrc`, anything under `.aws/`,
  `.kube/`, `.ssh/`, `.gnupg/`, `.config/gcloud/`, Terraform state, service-account JSON,
  GPG files, wallet files. Full list and exact patterns are in the hook source — read it
  before trusting it, the list is short enough to review in a minute.

This is deliberately biased toward false positives. A blocked read that turns out to be
fine costs one override. A secret that reaches a model's context or a tool's output
because the pattern list missed it costs a great deal more.

## Wiring it in (Claude Code)

Add to the project's `.claude/settings.json` (or `~/.claude/settings.json` for a
machine-wide default). Use [`settings.hooks.json`](settings.hooks.json) — it wires this
hook alongside the other three; merge its `hooks` block in and replace the
`/ABSOLUTE/PATH/TO/` placeholders with the real path to `harness/hooks/`.

**The default is the Python version, because it is the one that has run.** On
2026-10-15 the self-test for `data-boundary-guard.py` (`hooks/test_data_boundary_guard.py`,
27 tests, with a real `git init` repository for the gitignore cases) passed. Fifteen
deliberately broken copies of it each failed that suite, and the armed check below
blocked and allowed as required. It needs only Python 3's standard library, and both
settings templates wire it.

`data-boundary-guard.js` is the Node original: same patterns, allowlist, override, and
message. It has never been executed — the machine this factory is built on has no Node —
and it differs in two ways, both read from its source:

- It keeps only the first 1 MiB of its input, so a Write or Edit whose JSON is larger
  fails to parse and is allowed without its path being checked.
- Its Bash rule treats every word that matches a secret pattern as a path. The Python
  version's narrower rule, above, was the framework owner's call on 2026-10-14.
- It blocks commands that use a project's gitignored tool folders, so it would stop an
  operator from running a Python project's own tests. The Python version allows those
  folders in commands, again at the owner's call, on 2026-10-15. A trial on a real
  project hit exactly this.

The Python version also blocks input it cannot parse, and any error of its own, instead
of allowing. The reasons are in its docstring.

**Why the interpreter matters.** Claude Code treats any hook exit other than 0 or 2 as a
non-blocking error and lets the tool call go ahead, and a hook whose interpreter is missing
exits 127. A guard wired as `node …/data-boundary-guard.js` on a machine without Node
therefore blocks nothing: the call proceeds with only a hook-error notice. Wire the `.js`
only on a machine with Node, and only after its own armed check. Whichever you wire, it is
not armed until the checklist below has passed on that machine at least once;
`harness/README.md` has the same check for the other three hooks.

**Unwire before you remove.** `python3` exits 2 when the script it is asked to run does
not exist, and Claude Code reads exit 2 as a block. So a wired guard whose file has gone —
`keel-factory/` deleted, or a branch switched away from the one that holds it — refuses
every tool call it matches. Remove the hook entry first, or wire it in the form
`../OPERATOR.md` uses, which tests for the script before running it and so disarms
itself once `keel-factory/` is gone:
`g="$CLAUDE_PROJECT_DIR/keel-factory/harness/hooks/data-boundary-guard.py"; [ -f "$g" ] || exit 0; exec python3 "$g"`.
In that form it can also live machine-wide in `~/.claude/settings.json`: inert in any
project without `keel-factory/`, and armed in every one that has it. Two facts make that
the better home on this machine. Git here ignores `.claude/settings.local.json`
globally (`~/.config/git/ignore`). And an armed guard blocks gitignored paths, so it
would stop an agent from removing its own local wiring.

## Prove it before trusting it (KEEL Rule 6b, applied to this hook specifically)

A check nobody has watched fail is unproven — a silent no-op and a working block look
identical from the outside. Before this hook guards anything real:

```bash
echo '{"tool_input":{"file_path":"/path/to/some/.env"}}' | python3 harness/hooks/data-boundary-guard.py; echo "exit=$?"
# must print a BLOCKED reason and exit=2

echo '{"tool_input":{"file_path":"/path/to/some/normal/file.md"}}' | python3 harness/hooks/data-boundary-guard.py; echo "exit=$?"
# must exit=0 with no output on stderr

python3 harness/hooks/test_data_boundary_guard.py
# the full self-test: every rule, the allowlist, the override, and the fail-closed cases
```

For the Node original, run the same two commands with
`node harness/hooks/data-boundary-guard.js` in place of the `python3` invocation.

If either result is wrong, the hook is not armed — fix it before depending on it, not
after.

## Deliberate overrides — both leave a trail, neither is available by accident

- **One path, durably:** add the exact path (relative to the repo root) to
  `.keel/data-boundary-allow`, one per line. This file has to be created by a human. Do
  not let an agent create or edit it on your behalf — that would just move the same
  problem one layer up. Don't commit it if the paths in it would themselves reveal
  something about what's sensitive in the repo.
- **Everything, this session only:** a human sets `KEEL_DATA_BOUNDARY_OVERRIDE=1` in the
  actual environment the agent's tool calls run in. Nothing in this factory ever sets
  this for you.

## The question the agent should ask before it gets this far

The hook is the backstop. The first line of defense is not attempting the access without
asking. `../CLAUDE.md` states the standing rule; the shape of the question is:

> This would require reading/copying/sending `<exact path>`, which is
> `<gitignored / shaped like a credential / outside the project entirely>`. Do you want
> me to proceed with this specific access?

Not a generic "is it okay if I look around" — name the exact path and the exact reason it
tripped the boundary, every time. A vague confirmation given once at the start of a
session does not cover this; this question gets asked again for each new sensitive path,
because a yes to the task is not a yes to this.

## What this does not cover

- **Exfiltration once data is already in context.** The guard stops a sensitive file from
  being *read*. It does nothing to stop an agent that already read something sensitive
  from pasting it into a `curl` command, a commit message, or a file written somewhere
  else. That is a prompt-level discipline problem (`CLAUDE.md`'s job), not a tool-call
  pattern-matching problem.
- **Bash coverage is heuristic.** A sufficiently indirect command (reading through a
  wrapper script, an interpreter's `-c` flag, a base64-encoded path) can evade the
  tokenizer, and a plain word counts as a path only when it names an existing file, so a
  command that creates a new secret-shaped file from a bare name is not caught. Treat the
  Bash coverage as a speed bump, and the Read/Edit/Write/NotebookEdit coverage — which
  matches a structured field, not parsed text — as the actual guarantee.
- **Anything outside this project's working tree**, unless it happens to match the
  secret-pattern list regardless of location. It is not a general filesystem sandbox.
- **Files inside a searched directory.** A Glob or Grep aimed at a directory is checked as
  that directory, not file by file, so a secret-shaped file inside it that is not
  gitignored can still surface in the results.
- **Symlinks.** A path is judged as written. A link with an innocent name that points at a
  secret is not followed. Both gaps apply to both implementations.
