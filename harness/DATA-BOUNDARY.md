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
path; a plain word counts only when it is secret-shaped and a file by that name exists
where the command runs, so `git config` and `grep secret` pass while `cat id_rsa` beside
a real key does not. A gitignored file named by its bare name (`cat dump.sql`) is
therefore not checked, while `./dump.sql` is.
A command may also use a project's own tool folders, `.venv/bin/`, `venv/bin/` and
`node_modules/.bin/`, though they are gitignored. That is how a project runs its own
checks. The Read, Edit and Write tools stay strict there, and secret-shaped names stay
blocked everywhere:

- **Anything the project's own `.gitignore` would exclude, inside a git repository**
  (the limits are under "What this does not cover"). If it's not meant to be committed,
  it's not meant to be read into an agent's context or copied somewhere else either, by
  default.
- **Anything shaped like a secret, whether or not it's gitignored.** `.env*` (except
  `.env.example` / `.sample` / `.template`), `*credential*`, `*password*`, `*.pem`,
  `*.key`, SSH private keys, `.npmrc`/`.pypirc`/`.netrc`, anything under `.aws/`,
  `.kube/`, `.ssh/`, `.gnupg/`, `.config/gcloud/`, Terraform state, service-account JSON,
  GPG files, wallet files. Full list and exact patterns are in the hook source — read it
  before trusting it, the list is short enough to review in a minute.

This is deliberately biased toward false positives. A blocked read that turns out to be
fine costs one override. A secret that reaches a model's context or a tool's output
because the pattern list missed it costs a great deal more.

## Wiring it in — with the KEEL plugin (v1.1)

Nothing to wire by hand. The plugin's PreToolUse hook (`plugin-hooks.json`) runs
`hooks/keel_hook.py guard`, which hands every Read, Edit, MultiEdit, Write, NotebookEdit,
Glob, Grep and Bash call to this guard, unchanged, **in projects where KEEL is switched
on**: an entry named exactly `.keel` or `keel-factory` in the project's folder, or in a
folder above it inside the same git repository (outside git, the session's folder only).
The exact rule is in [`README.md`](README.md). Elsewhere it allows at once without
evaluating anything; set `KEEL_GUARD=always` to arm it in every project. The matcher
names MultiEdit, but no run has yet shown a MultiEdit call reaching it (Missing
evidence). Proven live on 2026-10-18
([`HARNESS-PROBES.md`](../keel/framework/HARNESS-PROBES.md), L1, L2 and L8): a headless
session's Read of `.env` was blocked where `.keel/` existed and went through where it did
not (L1, L2), and the hook fires on subagent tool calls too, `Explore` included, which
does not load `CLAUDE.md` (L8).

For Codex, `install_plugin.py --codex-hooks` merges the same hook, passing
`--harness codex`, into `$CODEX_HOME/hooks.json`, else `~/.codex/hooks.json`, with
matcher `Bash|apply_patch`. Codex runs it only after you trust it in `/hooks`, and no
Codex session has yet been seen blocking (Missing evidence).
`install_plugin.py --codex-hooks` writes machine-wide hooks that run the kit it was run
from: run it from the master (or through a linked `keel-factory/`), never from a copy
inside a project. In Codex every file read is a shell command, so the guard sees it only
as Bash and covers it only through its Bash heuristic: a blocked probe shows the hook is
wired, not that reads are covered. Codex lists no dedicated read tool (Inferred,
[`CAPABILITIES.md`](../keel/framework/CAPABILITIES.md), "File reads"); what the
heuristic misses is under "What this does not cover".

If you also ran `install_guard.py` (below), both hooks run on a call in a
`keel-factory/` project, and a block from either one wins. Both run the guard of the kit
they were installed from, the master's when installed as below; only the plugin's also
guards the allowlist (below). The machine-wide hook is optional with the plugin:
`install_guard.py --remove` takes it out.

## Wiring it in by hand (Claude Code, no plugin)

Add to the project's `.claude/settings.local.json` (or `~/.claude/settings.json` for a
machine-wide default), never to the shared `.claude/settings.json`. The command holds
this machine's absolute path, and where that path is missing the guard's `python3` exits
2, which blocks every call the guard matches ("Unwire before you remove", below). The
form that disarms itself instead is `install_guard.py`'s, or the one under "Unwire
before you remove". Use [`settings.hooks.json`](settings.hooks.json) — it wires this
hook alongside the other three; merge its `hooks` block in and replace every
`/ABSOLUTE/PATH/TO/` with the real absolute path to the kit root, the folder that holds
`harness/` (each template path already ends in `harness/hooks/…`).

**The default is the Python version, because it is the one that has run.** On 2026-10-15
the self-test for `data-boundary-guard.py` (`hooks/test_data_boundary_guard.py`,
27 tests, with a real `git init` repository for the gitignore cases) passed. Fifteen
deliberately broken copies of it each failed that suite, and the armed check below
blocked and allowed as required. It needs only Python 3's standard library, and both
settings templates wire it.

`data-boundary-guard.js` is the Node original: same patterns, allowlist, override, and
message. It has never been executed — the machine this factory is built on has no Node —
and it differs in three ways, all read from its source:

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
non-blocking error and lets the tool call go ahead, and a hook whose interpreter is
missing exits 127. A guard wired as `node …/data-boundary-guard.js` on a machine
without Node therefore blocks nothing: the call proceeds with only a hook-error notice.
Wire the `.js` only on a machine with Node, and only after its own armed check.
Whichever you wire, it is not armed until the checklist below has passed on that
machine at least once; `harness/README.md` has the same check for the other three
hooks.

**Unwire before you remove.** `python3` exits 2 when the script it is asked to run does
not exist, and Claude Code reads exit 2 as a block. So a wired guard whose file has gone —
`keel-factory/` deleted, or a branch switched away from the one that holds it — refuses
every tool call it matches. Remove the hook entry first, or wire it in the form
`../OPERATOR.md` uses. That form first checks that the project holds an entry named
exactly `keel-factory` (macOS ignores letter case in names), then that the master's
guard script is there, before running it. So it disarms itself once `keel-factory/` is
gone. A `git clean -fd` or `git stash -u` does the same mid-session where `keel-factory/`
or `.keel/` is untracked, for every KEEL hook (`../OPERATOR.md`, §3). Here
`/ABSOLUTE/PATH/TO` stands for the master's path, the folder that holds `harness/`:

```sh
ls -1 "$CLAUDE_PROJECT_DIR" 2>/dev/null | grep -qxF keel-factory || exit 0; g='/ABSOLUTE/PATH/TO/harness/hooks/data-boundary-guard.py'; [ -f "$g" ] || exit 0; exec python3 "$g"
```

`install_guard.py` writes exactly this command into `~/.claude/settings.json`, with the
master it was run from filled in, shell-quoted. The project's `keel-factory` entry is
only the switch. `install_guard.py`'s hook, installed from the master, never runs a
project's own code, so the guard of a committed copy is not the one it enforces: the
master's is. Installed from a copy, it would run that copy's guard in every
`keel-factory/` project, so run `install_guard.py` from the master or through a link to
it; Codex's hooks follow the same rule (above). If the master moves, the hook disarms
until the script is run again. A re-run also updates an entry an older version wrote, in
place, and repoints it at the master's guard; those entries ran the project's copy. In
that form the hook can live machine-wide: inert in any project without `keel-factory/`,
and armed in every one that has it. It covers only `keel-factory/` projects, not the
plugin's `.keel/` (the plugin's own hook covers those), and it runs the guard directly,
so it has none of `keel_hook.py`'s allowlist protection (below). Two facts make
machine-wide the better home on this machine. Git here ignores
`.claude/settings.local.json` globally (`~/.config/git/ignore`). And an armed guard
blocks gitignored paths, so it would stop an agent from removing its own local wiring.

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

Those checks run the guard script directly, so they pass even when the wiring is wrong.
A hook command with a doubled path (`…/keel-factory/harness/hooks/harness/hooks/…`)
either disarms itself and allows everything, in the `[ -f "$g" ] || exit 0` forms, or
fails to start, in the raw `python3 <path>` form. And a wiring can be dormant in one
project while armed in another. So also run **the wired command itself**, the way the
harness does, in the real project, with a Read of `keel-armed-check/.env`, the path
HELM's probe uses. That path does not exist, so nothing is read and no fake `.env` is
needed. `P` is the project's root. `HOOKS` is the file you wired:
`~/.claude/settings.json`, the project's `.claude/settings.json` or
`.claude/settings.local.json`, `$CODEX_HOME/hooks.json` (else `~/.codex/hooks.json`), or
`harness/plugin-hooks.json`. `R` is the kit root, set only for `plugin-hooks.json`, whose
command needs `CLAUDE_PLUGIN_ROOT`; for every other file leave it empty, so that an
inherited `CLAUDE_PLUGIN_ROOT` cannot make a dormant wiring look armed. The recipe takes
the first PreToolUse entry whose command names `keel_hook.py` or `data-boundary-guard`,
prints that entry's matcher, then runs its command:

```bash
P=/absolute/path/to/the/project; HOOKS=~/.claude/settings.json; R=
C=$(mktemp)
python3 -c 'import json, sys
d = json.load(open(sys.argv[1]))
e, h = next((e, h) for e in d["hooks"]["PreToolUse"] for h in e["hooks"]
            if "keel_hook.py" in h["command"] or "data-boundary-guard" in h["command"])
print("matcher:", e.get("matcher"), file=sys.stderr)
print(h["command"])' "$HOOKS" > "$C"
printf '{"cwd":"%s","tool_name":"Read","tool_input":{"file_path":"%s/keel-armed-check/.env"}}' "$P" "$P" \
  | (cd "$P" && env -u CLAUDE_PLUGIN_ROOT ${R:+"CLAUDE_PLUGIN_ROOT=$R"} CLAUDE_PROJECT_DIR="$P" sh -c "$(cat "$C")"); echo "exit=$?"; rm -f "$C"
# must print the matcher, then a "BLOCKED by data-boundary-guard" reason, AND exit=2
```

The printed matcher must name Read and Bash for Claude Code (the plugin's
`Read|Edit|MultiEdit|Write|NotebookEdit|Glob|Grep|Bash`, or the bare wirings' same set
without MultiEdit), or be `Bash|apply_patch` for Codex. The check sends a Read whatever
the matcher says, so only reading the printed matcher catches a misspelled or narrow one.
Exit 2 alone is not enough: the raw form with a wrong path also exits 2, with python3's
"can't open file" and no BLOCKED reason. Exit 0 means the wiring is not armed in this
project. That is by design for `install_guard.py`'s command in a project that holds only
`.keel/`, since it arms only where `keel-factory` is; there, the plugin's hook is the one
to check. The user runs this check. Copying a command out of a hooks file means reading
that file, which may be gitignored (an armed guard then blocks it), outside the project,
or holding keys. An agent runs it only after asking the data-boundary question for that
file, or puts the exact command it wrote there itself into `"$C"`.

On 2026-10-19 this recipe, as printed here, was run under both zsh and sh, in temp git
projects, with temp homes and `--settings` files only (Evidence). Each of these printed
its matcher, then the BLOCKED reason, and exited 2:

- `plugin-hooks.json`, with `R` the kit root, in a `.keel/` project, a linked-kit
  project and a project holding an rsync copy of the kit;
- `install_guard.py`'s command, installed from the master, in a linked-kit project;
- the Codex command `install_plugin.py --codex-hooks` writes from the master, in a
  `.keel/` project;
- the Codex command written from an rsync copy made with the documented command, in that
  copy's own project, which holds no `.keel/`. That is an armed-check case, not an
  install to copy: run from a copy, `--codex-hooks` writes machine-wide hooks that run
  that copy (above);
- both templates with the kit root filled in.

Each of these printed only its matcher and exited 0, as it must: `plugin-hooks.json`
with `R` left empty, also with `CLAUDE_PLUGIN_ROOT` set in the calling environment; a
project with no marker, for the plugin's, `install_guard.py`'s and the Codex command; and
`install_guard.py`'s command in a `.keel/`-only project, by design. With the doubled
path, the Codex template printed only its matcher and exited 0, and the raw form exited 2
with "can't open file" and no BLOCKED reason, so the check failed both, as it must. The
matchers printed were the plugin's, the bare wirings' set without MultiEdit, and
`Bash|apply_patch` for both Codex commands. A hooks file whose first PreToolUse entry was
another hook (`true # my-safeguard`) still had KEEL's entry checked. A misspelled matcher
(`Raed|Bsah`) still blocked and exited 2, printed as written: only reading it catches it.

If any result is wrong, the hook is not armed — fix it before depending on it, not
after.

## Deliberate overrides — both leave a trail, neither is available by accident

- **One path, durably:** add the exact path, relative to its git root, to
  `.keel/data-boundary-allow` at that root, one per line. It works only inside a git
  repository: the guard looks for the file at the nearest git root above each path (a
  submodule's or nested clone's own), so outside git it is never read. There, run
  `git init`, or use the session override below. This file has to be created and edited
  by a human. Do not let an agent create or edit it on your behalf — that would just move
  the same problem one layer up. Where KEEL is switched on, KEEL's hook (`keel_hook.py`:
  the plugin's, or Codex's with `--codex-hooks`) blocks the direct ways of writing it: a
  write, an edit, a Codex patch, or any shell command naming it, even under the override
  below; a Read of it is allowed. It is a tripwire, not a lock (see "What this does not
  cover"). The bare wirings, which run this guard directly, do not have that block.
  Never commit `.keel/data-boundary-allow`: it is your own local override, and the guard
  honors it in every clone that has it. Stage `.keel/keel.json` by name, never `.keel/`
  as a whole.
- **Everything, this session only:** a human sets `KEEL_DATA_BOUNDARY_OVERRIDE=1` in the
  actual environment the agent's tool calls run in. Nothing in this factory ever sets
  this for you.

## The question the agent should ask before it gets this far

The hook is the backstop. The first line of defense is not attempting the access without
asking. `../CLAUDE.md` states the standing rule; the shape of the question is:

> This would require reading/copying/sending `<exact path>`, which is
> `<gitignored / shaped like a credential / outside the project entirely>`. Do you want
> me to proceed with this specific access?

`../CLAUDE.md` names two exceptions that need no question. The guard probe, a Read of
`keel-armed-check/.env`, a path that does not exist, reads nothing. Reading the KEEL kit
itself (the kit root the session note names, or the kit a KEEL skill was loaded from) is
the other; the gitignore and secret rules still apply inside it.

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
- **Bash coverage is heuristic.** The tokenizer splits a command on whitespace only, so a
  name touching shell punctuation passes (`cat .env;`, `cat <.env`, `cat .env|head`). A
  plain word counts as a path only when it is secret-shaped and names an existing file,
  so a gitignored file given by its bare name (`cat dump.sql`) passes, and so does a
  command that creates a new secret-shaped file from a bare name. Recursive searches
  (`grep -r … .`) pass too, and so does a sufficiently indirect command (reading through
  a wrapper script, an interpreter's `-c` flag, a base64-encoded path). Each command
  shown here exited 0 through `keel_hook.py guard --harness codex` on 2026-10-19
  (Evidence). The guard also runs one `git check-ignore` per path-shaped word, about
  21 ms each on the machine that built KEEL (Evidence, 2026-10-19). So a command holding
  tens of thousands of them can outlast the hook's timeout, 600 s by Claude Code's
  documented default ([hooks docs](https://code.claude.com/docs/en/hooks), read
  2026-10-19; 2.1.170's own default is unprobed), and a timed-out hook lets the call
  through (Inferred; "When a hook fails" in
  [`CAPABILITIES.md`](../keel/framework/CAPABILITIES.md)). Under Codex this heuristic is
  the only read coverage (above). Treat the Bash coverage as a speed bump, and the
  Read/Edit/Write/NotebookEdit coverage — which matches a structured field, not parsed
  text — as the actual guarantee.
- **Anything outside this project's working tree**, unless it happens to match the
  secret-pattern list regardless of location. It is not a general filesystem sandbox.
- **Gitignore outside git, and in a nested repository.** The gitignore rule asks git in
  the repository nearest the file: outside git no `.gitignore` applies, and a separate
  repository inside a gitignored folder is judged only by its own rules. Outside git
  only the secret-shaped rule applies; in a nested repository, that rule and the nested
  repository's own `.gitignore` do. HELM's probe tests only the secret rule, so it
  reports the guard live in both layouts. Run `git init` in a package folder that is not
  a repository, or treat its `.gitignore` as strict policy (`../CLAUDE.md`).
- **Files inside a searched directory.** A Glob or Grep aimed at a directory is checked as
  that directory, not file by file, so a secret-shaped file inside it that is not
  gitignored can still surface in the results.
- **Symlinks.** A path is judged as written. A link with an innocent name that points at a
  secret is not followed. Both gaps apply to both implementations.
- **The allowlist block is a tripwire, not a lock.** `keel_hook.py` matches paths and
  command text, so it catches a direct write and any command naming the file. Renaming or
  relinking `.keel`, quoting or variables in the name, globs, copies and scripts get past
  it. Removing `.keel/` or `keel-factory/` switches the guard off altogether. And the
  harness's own settings, `.claude/settings*.json` (an `env` block, `disableAllHooks`,
  `enabledPlugins`), are not protected: only `CLAUDE.md`'s rule on changing security
  tooling covers them.
- **An allowlist that came with the repository.** The guard honors a
  `.keel/data-boundary-allow` at the nearest git root of each path, so a submodule or a
  nested clone can bring its own; HELM's switch-on check lists the `.keel/` folders below
  the root (not through linked folders) as well. Committed or not, the file is honored,
  so a clone of a repo that commits one starts with those paths open. HELM's switch-on
  and `../OPERATOR.md`'s infil show the root's to the user, saying when git tracks it,
  and list the rest with `find . -path ./keel-factory -prune -o -name .keel -print` (it
  never names the file, so KEEL's hook allows it, unless `.keel/` or `keel-factory` is
  gitignored; then HELM's step 3(d) applies). Each `.keel/` found below the root is
  handled like the root's. In operator mode they stop to ask. The listing does not
  follow a linked folder: a nested repository reached through a link to a folder outside
  the project is not listed, though the guard honors its allowlist, since it finds that
  repository's `.git` through the link. `find -L` is no fix, because it walks every
  linked folder, wherever the link points. The guard itself does not check where the
  file came from; making it ignore a committed one is a follow-on.
- **MCP tools.** Neither matcher names them: the plugin's is
  `Read|Edit|MultiEdit|Write|NotebookEdit|Glob|Grep|Bash` and Codex's is
  `Bash|apply_patch`. So an MCP tool that takes a local path is not checked (Inferred from
  the matchers; not run live). Adding `mcp__.*` to the matchers is a follow-on that needs
  a contract amendment.
- **Monitor, PowerShell and other unmatched tools.** Claude Code's Monitor tool, and
  PowerShell on Windows, run shell commands that the matcher does not name, so the guard
  never sees them (Inferred from the matcher). So `Monitor(command: "cat .env")`, or a
  `tail -f` of a gitignored log, is never checked. Claude Code 2.1.170 offers Monitor
  (Evidence: L8 in [`HARNESS-PROBES.md`](../keel/framework/HARNESS-PROBES.md)), and
  PowerShell is under "Windows: untested" in
  [`CAPABILITIES.md`](../keel/framework/CAPABILITIES.md). DesignSync, in the same tool
  list, uploads local files named in `files[].localPath` after a plan you approve
  (Inferred from its schema). It is not matched either, and even if it were, the guard
  reads only top-level `file_path`, `file`, `path`, `notebook_path` and `command`.
  Widening the matcher belongs to the MCP tools' follow-on, and it is a contract change
  too.
