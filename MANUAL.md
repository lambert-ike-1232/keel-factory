# KEEL FACTORY — the manual

Read this when you've lost track. It covers everything from a blank machine to a
finished job, in order. Every other document in this folder goes deeper into one piece;
this one tells you which piece you need and what to type.

Version 1.1.0 (see `VERSION`). Last revised 2026-10-19.

---

## The short version

If you only remember one thing, remember this. Install once per machine (section 3):

```bash
python3 "$KEEL/harness/install_plugin.py" --codex
```

`$KEEL` is the master's folder (section 3, step 2). For Codex, `--codex` gives the skills
only: Codex's guard and session hook need `--codex --codex-hooks` and your approval of
both of KEEL's hooks in Codex's `/hooks`, and no Codex session has yet been seen blocking
(Missing evidence).

Then, in any project, start Claude Code or Codex **inside the project folder** and say:

```text
Use KEEL: <what you want>.
```

That one line covers your own idea, a codebase to take to production grade, and a job in
someone else's package; `START-PROMPTS.md` has the table of what to say after the colon.
KEEL switches itself on in that project by creating `.keel/` (section 3 says exactly
where KEEL counts as on), and from then on every Claude Code session there starts
oriented. In your own project, commit `.keel/keel.json` by name with the work. In
someone else's package, read `.keel/ops/debrief.md` when it's done, then delete `.keel/`.

The v1.0 way, linking the kit into the project (`link_kit.py`, section 4), still works
and needs no plugin.

---

## 1. What this is

KEEL FACTORY is a framework you hand to an AI coding agent (Claude Code, or another
tool) so it works like a disciplined engineering team rather than a guesser. It is
mostly instructions, written as Markdown files the agent reads, plus a few small Python
scripts that check things mechanically.

It works two ways:

- **Operator mode.** You drop it into someone else's package (a codebase, or a bundle
  of material with its own instructions). The agent reads the package's instructions,
  does the job, proves it worked, tells you what it did, and leaves nothing behind but
  the work.
- **Owner mode.** It becomes the framework for a project of your own. The agent walks
  the project through five phases, from figuring out what to build to proving it's done,
  and stops where the stop mode says: by default one question round, one approval of
  BRIEF and CONTRACT together, and the final PROVE report (section 7).

---

## 2. What's in the folder

| Item | What it is |
| --- | --- |
| `MANUAL.md` | This file. |
| `VERSION`, `RELEASES.md` | Which release this is, and what each release changed. |
| `OPERATOR.md` | The drop-in protocol the agent follows in operator mode. |
| `START-PROMPTS.md` | The one opening line, `Use KEEL: …`, and what to say after it; plus the v1.0 prompts to paste with a linked kit, for owner and operator mode. |
| `README.md` | What's inside, where it came from, privacy and security notes. |
| `QUICKSTART.md` | The owner-mode setup steps, written out by hand. |
| `ARCHITECTURE.md` | How all the pieces fit together. Read this if the rest stops making sense. |
| `CLAUDE.md` | The always-on layer the agent works under. Where KEEL is on, the plugin's session hook injects it and HELM reads it at switch-on; in Codex it comes through the Codex hooks or the block HELM adds to an owner project's `AGENTS.md`; with a linked kit, the project's `CLAUDE.md` copies or imports it. |
| `.claude-plugin/` | `plugin.json` (the plugin manifest) and `marketplace.json` (the marketplace entry): what makes this folder the `keel` plugin. |
| `agents/` | The three PROVE reviewers (`prove-standards`, `prove-spec`, `prove-gate`) as plugin agents. |
| `evals/` | The eval suite that scores KEEL against plain Claude Code (`claude plugin eval`). |
| `keel/framework/` | The rules and disciplines: the five phases, RECON, CREW, LOOPS, the doctrine, and more. |
| `keel/skills/` | KEEL's own skills: `helm` (routes every session), `keel` (the five phases), `keel-prove` (proves "done"), `crew` (several agents at once). |
| `keel/skills-board/` | 16 skills by Miguel Hernandez: the task board, interviewing, handoff and resume, commit, spike, docs upkeep. Claude and Codex versions. |
| `keel/capabilities/` | The two "senses": `deep-research` (find out what the agent doesn't know) and `reverse-engineering` (look inside binaries and running systems, authorized targets only). |
| `keel/templates/` | Blank documents the phases fill in (BRIEF, RECON, DESIGN, ...). |
| `harness/` | The safety layer: the data-boundary guard (`hooks/data-boundary-guard.py`), KEEL's own hook (`hooks/keel_hook.py`, wired by `plugin-hooks.json`: the session layer, and the guard where KEEL is on), three other hooks that need Node.js, and their docs. Also the scripts `install_plugin.py` (install KEEL on a machine), `link_kit.py` (link the kit into a project), `install_guard.py` (the guard alone, without the plugin), `check_kit.py` (check the kit after editing it) and `make_release.py` (cut a versioned release). |
| `.scratch/handoff.md` | Notes for the next session that develops the framework itself. Never copied into a project. |

---

## 3. Setting up a machine — once per computer

On a new machine, start from a release (section 11 says what's in one):

1. **Restore the master** wherever you keep projects, for example your Git projects
   folder. `<version>` below is the release you are restoring, such as `1.1.0`. From the
   release folder on the SSD:

   ```bash
   cd /Volumes/S-USB/KEEL-FACTORY-releases/v<version>   # wherever the release folder is
   shasum -a 256 -c SHA256SUMS                         # every line must say OK
   git clone --branch main "$PWD/KEEL-FACTORY-v<version>.bundle" ~/GitProjects/KEEL-FACTORY
   git -C ~/GitProjects/KEEL-FACTORY describe --tags   # must print v<version>
   ```

   The release folder's `README-FIRST.txt` holds the same commands, checksum check first,
   and the no-git route below. Use your own local path for `~/GitProjects/KEEL-FACTORY`,
   never the drive. Releases are cut from `main`
   (section 11), and `--branch main` puts the clone on `main` at the release: without it,
   git can pick another branch that sits at the same commit, such as a just-merged work
   branch. Stay on `main`: section 11's upgrade pulls into it.

   The bundle is one file that carries the whole history and the version tags. Use it
   rather than copying the folder: the SSD is exFAT, which drops file permissions, and
   git would then report changed files. No git?
   `mkdir -p ~/GitProjects && tar -xzf KEEL-FACTORY-v<version>.tar.gz -C ~/GitProjects`
   makes `~/GitProjects/KEEL-FACTORY/` and writes nothing on the drive.

   Nothing after this step needs the drive: work from the restored master, never from
   the drive itself. If macOS won't let the app read the drive, turn on Removable
   Volumes for Visual Studio Code (or Terminal) in System Settings → Privacy & Security →
   Files and Folders.

2. **Tell your shell where the master lives.** Every command in this manual uses
   `"$KEEL"`:

   ```bash
   echo 'export KEEL="$HOME/GitProjects/KEEL-FACTORY"' >> ~/.zshrc   # your real path
   source ~/.zshrc
   ```

   On the machine where this was built, `KEEL` is `~/Documents/KEEL-FACTORY`.

3. **Check the tools.** `python3 --version` must work (3.8 or newer; built and tested on
   3.13). `git` is needed for releases and most real work. Node.js is optional: only the
   three ECC hooks need it; the data-boundary guard and KEEL's own hook run on Python.

4. **Install KEEL for Claude Code and Codex.** One command, which only makes links to
   the master, so editing the master updates every project at the next session:

   ```bash
   python3 "$KEEL/harness/install_plugin.py" --codex
   ```

   - Claude Code then lists KEEL's skills as `keel:helm`, `keel:keel`, ... in every
     project, and its guard and session layer work only where KEEL is switched on
     (below). Start a new session to pick it up. There the guard has been seen blocking,
     in subagents too, and idle in a project without `.keel/`
     (`keel/framework/HARNESS-PROBES.md`, L1, L8 and L2).
   - Codex lists the same skills as `keel:helm`, ...; call one with `$keel:helm`. That is
     all `--codex` gives Codex: no guard and no session hook. A later Codex session then
     gets the always-on layer only from the block HELM adds to your own project's
     `AGENTS.md`, or when it calls `$keel:helm` (Inferred from HELM's steps, not seen in
     Codex).
   - For Codex's guard and session hook, run
     `python3 "$KEEL/harness/install_plugin.py" --codex --codex-hooks`. It merges KEEL's
     two hooks into `hooks.json` in the Codex home (`$CODEX_HOME` when that is set, else
     `~/.codex`) and prints the path it wrote. The master's path in each hook command is
     shell-quoted, so spaces in it are fine. Then open Codex, run `/hooks` and trust both
     of KEEL's hooks: Codex runs a hook only after you do. No Codex session has yet been
     seen blocking (Missing evidence), so treat KEEL's rule in Codex as policy alone until
     you have seen HELM's guard probe come back blocked there. Even then, the rule stays
     the main protection. In Codex every file read is a shell command, so the guard sees
     it only as Bash and covers it only through its Bash heuristic: a blocked probe shows
     the hook is wired, not that reads are covered.
   - `--remove` (with the same flags) takes out only the links and hook entries it made.
   - Prefer pinned releases to a live link? Instead run
     `claude plugin marketplace add "$KEEL"` and
     `claude plugin install keel@keel-factory`, and
     `claude plugin update keel@keel-factory` after each release. Use one or the other:
     the marketplace install wins over the link.

   **Where KEEL switches on.** In a git repository, KEEL is on when the session's folder,
   or any folder above it up to the top of the repository, holds an entry named exactly
   `.keel` (a folder) or `keel-factory` (a linked or copied kit). The nearest one wins,
   and a git worktree also counts its main checkout. Outside git, only the session's own
   folder counts. The names must match exactly, capitals included: macOS ignores letter
   case, so a folder named `KEEL-FACTORY` does not count. A `.keel` or `keel-factory` in
   your home folder or in `/` never counts, and KEEL is never on in the kit's own folder:
   a session started in `$KEEL` or anywhere inside it stays off. Only the master's own git
   checkout (the folder KEEL's hooks run from, when it holds a `.git` folder or is a
   linked worktree) never switches on the folder that holds it, even when it is named
   `keel-factory`. A linked `keel-factory/`, or a copy made with section 4's copy command
   (which leaves `.git` out), switches KEEL on, even when KEEL's hooks run from that copy;
   a copy that keeps `.git` stays dormant when its own hooks run (section 4). Everywhere
   else the plugin's hooks do nothing.

   **Without the plugin** (older Claude Code, or you prefer the v1.0 wiring), install the
   data-boundary guard machine-wide instead. With the plugin installed it is optional:
   the plugin's hook already arms in projects that hold `keel-factory/`, and in `.keel/`
   ones too. The guard stops the agent reading secrets (`.env` files, keys, credentials)
   and anything gitignored (inside a git repository: section 10), and this wiring arms
   only when the session's project folder itself holds an entry named exactly
   `keel-factory`; a `.keel/` alone does not arm it:

   ```bash
   python3 "$KEEL/harness/install_guard.py"
   ```

   The `keel-factory` entry is only the switch. The hook then runs the guard of the
   master you ran the script from, by its absolute path, never the project's own copy,
   so a package cannot ship a guard that lets everything through. Run the script from
   the master or through a link to it. If the master moves, the hook disarms until you
   run the script again. It keeps everything already in `~/.claude/settings.json`, saves
   the original once as `settings.json.before-keel-guard`, and changes nothing if run
   twice. Re-running it repoints, in place, an entry from an older version (those ran the
   project's copy) or from a master elsewhere. `--remove` takes it out again. This wiring
   runs the guard alone: unlike KEEL's hook, it does not block the direct ways an agent
   could write `.keel/data-boundary-allow`.

5. **Prove it all works on this machine.** Each must end in OK:

   ```bash
   cd "$KEEL"
   python3 harness/hooks/test_data_boundary_guard.py
   python3 harness/hooks/test_keel_hook.py
   python3 harness/test_link_kit.py
   python3 harness/test_install_guard.py
   python3 harness/test_install_plugin.py
   python3 harness/test_check_kit.py
   python3 harness/test_make_release.py
   python3 harness/check_kit.py
   (cd keel/skills/crew && python3 scripts/test_check_lanes.py)
   ```

---

## 4. Linked, not copied — how the kit gets into a project

There is only one real copy of the framework: the master, at `$KEEL` (section 3).
Under the plugin a project gets no kit at all, only its own `.keel/`. Without the plugin,
a project gets a `keel-factory/` folder that holds **links** to the master, not copies,
plus one real folder of its own, `keel-factory/.ops/`, for that project's notes. So:

- you update the framework in one place, and every linked project sees the change at
  once;
- a project's notes stay in that project, never in the master;
- removing the kit from a project deletes only the links; the master is never touched.

```bash
python3 "$KEEL/harness/link_kit.py" /path/to/project            # link it in
python3 "$KEEL/harness/link_kit.py" /path/to/project --remove   # take it out
```

Always take it out with `--remove`, never by hand. `rm -rf keel-factory/` with a trailing
slash can follow a link and delete what it points at. The script refuses to touch any
`keel-factory/` it didn't make, so an old full copy is safe from it. It refuses its own
links too once the master has moved; section 10 ("You moved the master") clears them.

The links point at this machine. For a project that must carry its own copy, because it's
committed to a shared repo or worked on from another computer, use a full copy instead:

```bash
rsync -a --exclude '.git/' --exclude '.scratch/' --exclude '__pycache__/' \
  --exclude '.DS_Store' "$KEEL/" /path/to/project/keel-factory/
```

A copied project keeps the version it was copied from. A copy made with the rsync above
(no `.git`) switches KEEL on; a copy that keeps `.git` (a `git clone`, `cp -R` or a Finder
copy) counts as a master's own checkout and stays dormant when its own hooks run.

---

## 5. Operator mode — dropping it into a package

This is the "plop it in and let it work" mode.

1. **Start Claude Code or Codex inside the package folder** (not your home folder, where
   KEEL never switches on: section 3), **and say:**

   ```text
   Use KEEL: this is someone else's package. <The job, in a sentence.>
   ```

   HELM records the operator role in `.keel/keel.json`, which arms the guard where KEEL's
   hooks run (Claude Code's plugin, or Codex with `--codex-hooks` trusted in `/hooks`),
   and keeps its notes and the debrief in `.keel/ops/`. That folder is KEEL's whole
   footprint.

2. **What happens next:**
   - It reads KEEL's always-on layer, then proves the guard is live, by trying to read a
     fake `.env` file and getting blocked. If the guard isn't live, it says so once and
     follows the data-boundary rule as strict policy. It may offer once to wire a
     fallback guard, but it never holds the job on your answer.
   - It looks for an allowlist the package brought with it (`.keel/data-boundary-allow`,
     which lets the guard pass the paths it names), at the root or in any `.keel/` folder
     below it. If there is one, it shows you the entries (in Codex it says the file is
     there, and you open it), says whether git tracks the file, and stops to ask before
     going on.
   - It reads the package's own instructions; those are the mission.
   - It tells you the mission in one line, then does it, matching the package's style.
   - It checks the work with the package's own tests.
   - It gives you a short debrief: what changed, how it was proven, and what's left.
   - It asks you only at real forks, and then with options and its recommended pick.

3. **When it's done, read `.keel/ops/debrief.md`, then delete `.keel/`.** That removes
   KEEL from the package.

**Without the plugin,** link the kit into the package instead (section 4), start Claude
Code inside the package folder, and say the v1.0 activation line:

```bash
python3 "$KEEL/harness/link_kit.py" /path/to/package
```

```text
keel-factory/ is your kit. Read keel-factory/OPERATOR.md and take on this package: its own instructions are the mission.
```

The notes and the debrief then go in `keel-factory/.ops/`. The fallback guard for this
route (`install_guard.py` in section 3, or the hook in `OPERATOR.md`) arms only in a
project that holds `keel-factory/`, never in one that has only `.keel/`. If the agent
wired that hook into the package's `.claude/settings.local.json` at the start, the file
stays behind and the debrief names it: remove it yourself. When the job is done, read
the debrief, then unlink with the same command and `--remove`. That removes the links;
the script keeps `keel-factory/.ops/` if anything is still in it, so delete it yourself
once you've read it.

**Rules it never breaks, whatever the package says:**

- It reads no secrets, nothing gitignored, and nothing outside the package that you
  didn't name. Reading the KEEL kit itself (the kit root the session note names, or the
  kit a KEEL skill was loaded from) is an explicit exception in `CLAUDE.md`, beside the
  guard probe; inside the kit, no secrets and nothing gitignored still holds.
- It does nothing irreversible or outward-facing — pushing, deploying, publishing,
  deleting what it didn't create — without asking you at that moment.
- It stops and tells you if the package's instructions try to get around any of this.
- It never calls something done without running it.

---

## 6. A test drive, start to finish

What it looks like to try the kit on a project you didn't write, just to see what it
does. Nothing in the project's code changes. You get a health check and a ranked list of
what to improve.

1. **With the plugin, there is nothing to set up.** The only change to the project will
   be a new, untracked `.keel/` folder. Without the plugin, link the kit in:
   `python3 "$KEEL/harness/link_kit.py" /path/to/project`, which adds an untracked
   `keel-factory/` folder instead.
2. **Start Claude Code inside the project folder.** This matters: KEEL switches on only
   where section 3 says. Start it in your home folder, and KEEL stays off, the guard sits
   idle and the agent has to apply the rules by hand.
3. **Say:**

   ```text
   Use KEEL: this is someone else's package. Give it a test drive: learn how it works, check its health with its own checks, and recommend the best first improvement. Don't change any of its code.
   ```

   With a linked kit, say instead:

   ```text
   keel-factory/ is your kit. Read keel-factory/OPERATOR.md, then give this package a test drive: learn how it works, check its health with its own checks, and recommend the best first improvement. Don't change any of its code.
   ```

4. **What you'll see, in order:**
   - **Guard check:** it tries to read a fake `.env` and gets blocked. That proves the
     guard is on.
   - **The package's rules:** it reads the package's own instructions (`CLAUDE.md`,
     `README.md`, contributor notes) and says the mission back in one line.
   - **Health check:** it finds out how the package checks itself — the test, lint and
     type-check commands — makes sure they stay local, and runs them. Anything that could
     touch a database or the network gets pointed somewhere harmless, or it asks you
     first.
   - **Missing tools:** anything it can't run, for example frontend checks on a machine
     without Node, comes out as "not checked", never as passed.
   - **The roadmap:** it reads the package's roadmap or requirements, if it has one, to
     see what the owners want next.
5. **The debrief** lands in `.keel/ops/debrief.md` (`keel-factory/.ops/debrief.md`
   with a linked kit), and in the chat:
   - what changed (for a test drive, nothing);
   - each check's real result, labeled Evidence, Inferred or Missing evidence;
   - what it noticed;
   - a ranked list with one recommended first pick;
   - what it deliberately didn't do.
6. **Clean up:** delete `.keel/` when you're done with the debrief. With a linked kit,
   unlink: `python3 "$KEEL/harness/link_kit.py" /path/to/project --remove`. The links
   go, and `keel-factory/.ops/` stays so you can keep the debrief. Delete that folder
   when you're done with it.
7. **Want it to act on the recommendation?** Keep `.keel/` (or link the kit in again)
   and say "Do the first item on the debrief." It will follow the package's own way of
   working (its branches, its test style, its review rules), and it won't push anything.

---

## 7. Owner mode — your own project

1. **With the plugin installed** (section 3), open the project and say
   `Use KEEL: <your idea or description>`. Nothing is copied in; HELM records
   `.keel/keel.json` and starts. Commit `.keel/keel.json` by name with your project,
   never `.keel/` as a whole, and never gitignore `.keel/` (section 10).
2. **Without it,** link the kit into the project (section 4) and paste a starter prompt
   from `START-PROMPTS.md`. It sets the project up without overwriting anything already
   there; an existing `CLAUDE.md` gets one import line rather than being replaced.
3. **From then on, just talk to it.** Every new session starts with HELM, which works
   out where the project stands and what to do next.

**How often it stops** is the stop mode, recorded in `docs/STATE.md`:

| Mode | It waits for you at | Default for |
| --- | --- | --- |
| checkpoint | one question round up front, one approval of BRIEF and CONTRACT together, and the final PROVE report | SPRINT and STANDARD |
| supervised | every phase the tier stops at | PLATFORM |
| unattended | the up-front approval, then nothing until the PROVE report; needs `LOOPS.md`'s fields | only when you ask |

Every mode still stops for the safety rules, a decision it can't settle from what you
approved, a check it can't fix in three tries, or the cost ceiling.

What the agent walks through:

| Step | What happens | You get |
| --- | --- | --- |
| RECON (existing systems only) | It learns the system and its conventions before proposing anything. | `docs/RECON.md`, and a ranked list of improvements with a recommended first pick |
| BRIEF | What are we building, for whom, and what it is guessing. It asks questions, each with options and a pick. | `docs/BRIEF.md` |
| CONTRACT | What must be true for this to count as done. | `docs/CONTRACT.md`, `docs/ACCEPTANCE.md` |
| DESIGN | The shapes, with no implementations yet. | `docs/DESIGN.md`, including the decisions it's least sure of |
| SLICE | Thin working slices, each tracked as a task on the board. | Working code, and tasks in `.scratch/task_board/` |
| PROVE | An independent review, with the checks actually run. | An honest status: verified, unverified, or only specified |

At each stop it asks: "Approve `<PHASE>`, or what should change?" In checkpoint mode
the first stop is "Approve BRIEF and CONTRACT, or what should change?"

---

## 8. Coming back after a break

- **To a project:** open a session and say anything. HELM reads the project's state and
  tells you where things stand before doing anything. If a handoff was left, say
  "resume the handoff".
- **Mid-session and running out of room:** say "write a handoff". It writes everything
  the next session needs to a file, and the next session picks up from it.
- **To developing the framework itself:** open the master folder and say "Read
  `.scratch/handoff.md` and resume from it."

---

## Things you can say to it

| Say | It will |
| --- | --- |
| "Use KEEL: <anything>" | Work out whose project this is, switch KEEL on, and route: brief, RECON, an operator job, or resume. |
| "Stop at every phase" / "Don't stop until PROVE" | Switch the stop mode to supervised / checkpoint, recorded in `docs/STATE.md`. |
| The operator activation line (`OPERATOR.md`) | Read the package's instructions and take the mission from them. |
| "Give this a test drive" | Check the package's health and recommend improvements, without changing any code (section 6). |
| "Do the first item on the debrief" | Do it the package's way, prove it with the package's tests, and tell you what changed. |
| "What's the state of this?" | Reconstruct where the project stands before doing anything. |
| "Write a handoff" | Save everything the next session needs, before you stop or run out of room. |
| "Resume the handoff" | Check the project still matches the handoff, then pick up from it. |
| "Prove it's done" | Run `keel-prove`: an independent review with the checks actually run. |
| "Split this across agents" | Run `crew`: separate lanes, no two agents writing the same file. |

---

## 9. The kit — what each piece is for

| Piece | Reach for it when |
| --- | --- |
| `helm` | Every session start. It decides what kind of situation this is, and hands off. |
| `keel` | Building something through the five phases. |
| `keel-prove` | You need to know something is really done, by running the checks. |
| RECON | Taking on an existing system you don't know yet. |
| `crew` | Splitting work across several agents without them editing the same files. |
| `deep-research` | A decision depends on knowledge the agent doesn't have. |
| `reverse-engineering` | Part of the target has no readable source. Authorized targets only, and read-only first. |
| task board (`task-board-init`, `to-task`, `focused-implementation`, `orchestrate-implementation`, `task-board-triage`) | Tracking many tasks, or work that outlasts one session. |
| `handoff` / `resume-handoff` | Ending a session cleanly, and picking it back up. |
| `spike` | A question only a throwaway prototype can answer. |
| `keel:prove-standards`, `keel:prove-spec`, `keel:prove-gate` | `keel-prove`'s reviewers, each in a fresh context. Above SPRINT it spawns all three; at SPRINT it spawns Standards and Spec, the builder may run the gate's commands itself, and the report says so. You don't call them yourself. |
| data-boundary guard | On wherever KEEL is switched on (section 3). It blocks secrets and gitignored files (inside a git repository: section 10). In Claude Code it has been seen blocking, in subagents too (`keel/framework/HARNESS-PROBES.md`, L1 and L8). In Codex it runs only with `--codex-hooks` and your trust in `/hooks`, and has not yet been seen blocking (Missing evidence). In Codex every file read is a shell command, so the guard sees it only as Bash and covers it only through its Bash heuristic: a blocked probe shows the hook is wired, not that reads are covered. |
| `harness/check_kit.py` | After editing the master: checks the plugin, the Codex skills, the agents, the evals and every link. |
| `evals/` | Measuring KEEL against plain Claude Code (`claude plugin eval`, Claude Code 2.1.269 or later). |

---

## 10. When something goes wrong

- **KEEL's skills don't appear.** Start a new session: a plugin installed mid-session
  loads at the next start. `claude plugin list` should show `keel@skills-dir` as loaded,
  or `keel@keel-factory` if you installed from the marketplace (that one wins).
- **Codex lists the skills but the guard never blocks there.** Its hooks need
  `install_plugin.py --codex --codex-hooks` and then your trust in Codex's `/hooks`. The
  script prints the `hooks.json` it wrote: `$CODEX_HOME/hooks.json` when `CODEX_HOME`
  is set, else `~/.codex/hooks.json`. A Codex started with a different `CODEX_HOME`
  reads a different file. Even with the hooks trusted, no Codex session has yet been
  seen blocking (Missing evidence).
- **The guard blocked something legitimate.** The agent should stop and ask you, naming
  the file. If you really want it allowed, add that file's exact path, relative to the
  root of the git repository that holds it, to `.keel/data-boundary-allow` in that
  root: for a file inside a submodule or a nested clone, that repository's own
  `.keel/`, not the project's (the guard's block message gives the exact line).
  Create that file yourself, never let the agent write it, and never commit it: it
  is your own local override. With a linked `keel-factory/` and no `.keel/` yet,
  creating the project's `.keel/` for this file makes `.keel/` the switch: the next
  session's note says no role is recorded, and HELM records it in `.keel/keel.json`
  once. The file works only inside a git repository; outside git, run `git init` in
  the project folder or use the session override. The gitignore rule asks
  git in the repository nearest the file: outside git no `.gitignore` applies, and a
  separate repository inside a gitignored folder is judged only by its own rules. In
  those two cases the guard lets such files through, and only `CLAUDE.md`'s rule,
  followed as strict policy, keeps them closed. In your own project, `git init` brings
  the gitignore rule back outside git; in someone else's package, the agent keeps to the
  package's `.gitignore` as strict policy instead. To switch the guard off for one
  session, set `KEEL_DATA_BOUNDARY_OVERRIDE=1` in the agent's environment yourself.
- **Every tool call is blocked with "can't open file".** The hook is pointing at a
  script that isn't there. KEEL's hooks in section 3 disarm themselves and can't do
  this; a hand-wired copy of the raw `settings.hooks.json` form can (START-PROMPTS'
  hand-wiring writes one), once the path it names is gone. Remove that hook entry from
  the project's `.claude/settings.local.json`, or from `.claude/settings.json` or
  `~/.claude/settings.json` where an earlier hand-wiring put it; or restore
  `~/.claude/settings.json.before-keel-guard`.
- **You want the guard gone completely.** Run
  `python3 "$KEEL/harness/install_plugin.py" --remove` with the flags you installed with
  (for example `--codex --codex-hooks`), or `claude plugin uninstall keel@keel-factory`
  for a marketplace install. For the older wiring, run `install_guard.py --remove`,
  restore `~/.claude/settings.json.before-keel-guard`, or delete the KEEL entry from
  `~/.claude/settings.json`.
- **You moved the master.** KEEL's links still point at the old place, so its skills and
  hooks stop working. KEEL's Codex hooks switch themselves off (each one exits quietly
  when its script is gone), so the guard is off there until you re-run the installer.
  `install_plugin.py` makes or removes only links into the master it runs from: it
  refuses the old link in `~/.claude/skills/`, and skips the old ones in
  `~/.agents/skills/` as names that are taken, leaving them in place. Remove them
  yourself first:
  - `rm ~/.claude/skills/keel`, with no `-r` and no trailing slash.
  - KEEL's other dangling links: in `~/.agents/skills/`, and in `~/.claude/skills/` if
    you installed with `--with-docs`. This lists every dangling link in both folders and
    shows where each one points:
    `find -L ~/.claude/skills ~/.agents/skills -maxdepth 1 -type l -exec ls -l {} +`.
    `rm` each one that points into the old master.

  Then point `KEEL` at the new place (section 3, step 2) and re-run `install_plugin.py`
  with the flags you installed with. With `--codex-hooks`, the re-run points KEEL's hooks
  in `hooks.json` at the new place; trust both again in Codex's `/hooks`, because Codex
  pins its trust to the exact hook definition (Inferred from Codex's hooks
  documentation, read 2026-10-18). For the older wiring, run `install_guard.py` again
  (section 3). Each project you linked with `link_kit.py` still points at the old place
  too, and `link_kit.py` from the new place refuses it, with or without `--remove`
  ("holds real files"). In that project's folder, remove only the old links, which
  keeps `keel-factory/.ops/` and your notes:
  `find keel-factory -maxdepth 1 -type l -exec rm {} +`. Then link it again (section 4).
- **"Node isn't installed".** Only the three ECC hooks need it, and they're optional.
  The guard runs on Python.
- **KEEL can't read its own files.** Something gitignores `.keel/`, `keel-factory/`,
  `.scratch/` or `docs/`. Don't gitignore those; the guard blocks gitignored paths. HELM
  warns when the repository ignores `.keel/keel.json`. To find the rule, run
  `git check-ignore -v .keel/keel.json` (or name the file it can't read): it prints the
  ignore file, the line number and the pattern. In your own project, remove that line. In
  someone else's package, leave it: the agent tells you, and if it can't write the
  debrief's copy, it gives you the debrief in the chat.
- **The guard didn't block the fake `.env` probe.** Either KEEL is not on where the
  session started (outside the project, or in your home folder, `/` or the kit's own
  folder, where KEEL never switches on: section 3), or, in Codex, KEEL's hooks are not
  installed or not trusted (above). Close the session and start a new one inside the
  project folder.
- **Claude Code asks to allow external imports, in a project with a linked kit.** The
  project's `CLAUDE.md` line `@keel-factory/CLAUDE.md` resolves, through the link, to the
  master's `CLAUDE.md`, outside the project, so Claude Code asks once whether to allow
  external imports. If you decline, imports stay off and the dialog does not come back
  (Inferred from Claude Code's memory documentation, read 2026-10-19; no KEEL run has
  seen the dialog yet). The session then starts with neither KEEL's layer nor its
  data-boundary rule: the import is their only source, since the plugin's session hook,
  too, leaves the layer to an import that resolves. Approve the dialog when it appears.
  Under the plugin you can instead delete the import line, and that is the fix once you
  have declined: the session hook then supplies the layer itself. Without the plugin,
  approve it, or, once declined, copy the kit's `CLAUDE.md` text into the project's
  `CLAUDE.md`.
- **KEEL went quiet mid-session, or its notes vanished.** `git clean -fd` or `-fdx` (any
  clean with `-d`) removes an untracked `.keel/` or `keel-factory/` folder, and plain
  `git clean -f` removes a `keel-factory` that is a single link; `git stash -u` or
  `--all` removes both. That switches KEEL off with no message (the guard stops blocking)
  and deletes `.keel/ops/` or `keel-factory/.ops/`: the notes, the board and the debrief.
  A stash brings them back with `git stash pop`; a clean does not. When a clean is needed
  (some packages' build or release steps call for one), what the agent does depends on
  whose project it is. In someone else's package, it asks you first, then runs
  `git clean -fd -e .keel -e keel-factory`, adding `-x` only if you ask, and it stashes
  with plain `git stash`, never `-u` or `--all` (`OPERATOR.md`, section 3). In your own
  project, it stops before a clean, as it does before anything irreversible, but nothing
  yet tells it to keep KEEL's folders out: ask for those `-e` flags yourself, and don't
  let it run `git stash -u` or `--all` while `.keel/` or `keel-factory/` is untracked.
- **A whole-project check such as `mypy .` behaves strangely, or stops with "errors
  prevented further checking".** It may have walked into `keel-factory/`. Run it with
  the kit excluded, for example `mypy . --exclude '^keel-factory/'`. The agent is told to
  do this, but it's worth knowing.
- **The agent wants to read something inside `.venv/` or `node_modules/`.** Commands may
  use a project's own tool folders (`.venv/bin/`, `venv/bin/`, `node_modules/.bin/`), so
  it can run the project's tests. Reading other files in those gitignored folders stays
  blocked, as does anything secret-shaped. If it truly needs one, it asks you, naming the
  file.
- **`git status` shows `.keel/` or `keel-factory/` as untracked.** That's expected. In
  your own project, commit `.keel/keel.json` with the work. Never commit
  `.keel/data-boundary-allow`: it is your own local override. Stage `.keel/keel.json` by
  name, never `.keel/` as a whole. In someone else's package, leave `.keel/` uncommitted
  and delete it after the debrief. Never commit a linked `keel-factory/`: its links point
  at this machine.
- **The rules feel like too much ceremony.** Operator mode cuts everything except the
  safety rules. In owner mode, the tier decides how many stops you get: SPRINT has
  almost none.

---

## 11. Releases and versions

The master is a git repository, and what travels between machines is a **release**.
This is v1.1.0. Its version is in `VERSION`, and what each release contains is in
`RELEASES.md`.

**What a release folder holds** (`KEEL-FACTORY-releases/v<version>/`, next to the
master):

| File | What it's for |
| --- | --- |
| `KEEL-FACTORY-v<version>.bundle` | The whole repository in one file. Restore with `git clone` (section 3). |
| `KEEL-FACTORY-v<version>.tar.gz` | The same files without git history, for a machine without git. |
| `MANUAL-v<version>.md` | This manual, readable straight off the drive. |
| `README-FIRST.txt` | The restore commands, checksum check first, in four lines. |
| `SHA256SUMS` | Checksums. `shasum -a 256 -c SHA256SUMS` checks the files arrived intact. |

**To cut the next release,** on whichever machine you've been working. Releases are cut
from `main`, after merging:

1. Commit your changes on your branch: `cd "$KEEL" && git add -A && git commit -m "..."`.
2. Bump `VERSION`. Use the last number for fixes (1.0.1), the middle one for additions
   (1.1.0), and the first for changes that break how you use it (2.0.0).
3. Add a `## v<version>` section to `RELEASES.md`, saying what changed and how you know
   it works. Commit both.
4. Merge your branch into `main` and check `main` out, for example
   `git switch main && git merge <your-branch>`.
5. Run `python3 "$KEEL/harness/make_release.py"`. Before writing anything, it refuses if
   HEAD is not on `main`, anything is uncommitted, or the notes are missing. It then
   tags the commit, writes the release folder, clones it fresh, and runs every self-test
   from the clone. It only says "proven" if all of that passes.
6. Copy the release folder to the SSD, in Finder or with
   `cp -R "$KEEL/../KEEL-FACTORY-releases/v<version>" /Volumes/S-USB/KEEL-FACTORY-releases/`.

**To take a release onto a machine that already has an older one,** with the master on
`main`, as section 3 leaves it:

1. Pull the release into `main`:

   ```bash
   cd "$KEEL"
   git pull /Volumes/S-USB/KEEL-FACTORY-releases/v<version>/KEEL-FACTORY-v<version>.bundle main --tags
   ```

   Linked projects see the new version at once, and the plugin at the next session.
2. A project whose `CLAUDE.md` is v1.0's copy of the layer (it says "This project was
   started from KEEL FACTORY.") needs one change. Until it is made, the session hook adds
   no second layer on top of it, and its one-line note says which of these fits:
   - With a linked `keel-factory/` in the project, or a copy of v1.1 or later, replace
     v1.0's copy with the line `@keel-factory/CLAUDE.md`.
   - Under the plugin, with no `keel-factory/`, that line imports nothing. Delete KEEL's
     v1.0 text instead (the session hook then supplies the layer), or replace it with
     v1.1's `CLAUDE.md`.
   - In Codex, an `AGENTS.md` holding v1.0's copy gets the replacement, never the
     import: the kit's `CLAUDE.md` as one block that opens with its mark line. HELM
     offers deleting v1.0's copy and relying on the hook instead only where its guard
     probe came back blocked (KEEL's Codex hooks wired and trusted); otherwise it offers
     only the replacement.

   A project holding a copied v1.0 `keel-factory/` re-copies it with section 4's rsync,
   or replaces it with a link (`link_kit.py`); until then its import carries v1.0's
   layer beside the hook's v1.1 layer. The session hook gives no note for this case. To
   link it, move the old copy aside first, since `link_kit.py` refuses a `keel-factory/`
   that holds real files; after linking, move the notes from the old copy's `.ops/` into
   the new `keel-factory/.ops/`.

---

## 12. Where it came from

- **KEEL:** the original v1.1 is at `~/Documents/FRAMEWORK/`. This folder grew from it.
- **Miguel Hernandez's Skills:** copied in full into `keel/skills-board/`.
- **ECC** (`~/Downloads/ECC-main`) and **REA** (`~/Downloads/rea-main`): cited, not
  copied. Only the pieces the framework uses are in `harness/`. REA is reached through
  `keel/capabilities/reverse-engineering/`, and needs its own install.

The full detail is in `README.md` and in the cross-reference documents under
`keel/framework/`.
