# KEEL FACTORY — the manual

Read this when you've lost track. It covers everything from a blank machine to a
finished job, in order. Every other document in this folder goes deeper into one piece;
this one tells you which piece you need and what to type.

Version 1.0.0 (see `VERSION`). Last revised 2026-10-15.

---

## The short version

If you only remember one thing, remember this. Setup is once per machine (section 3).
Then, for every project:

```bash
python3 "$KEEL/harness/link_kit.py" /path/to/project
```

Start Claude Code **inside that project folder**, and say:

```text
keel-factory/ is your kit. Read keel-factory/OPERATOR.md and take on this package: its own instructions are the mission.
```

When it's done, read its debrief, then unlink:

```bash
python3 "$KEEL/harness/link_kit.py" /path/to/project --remove
```

---

## 1. What this is

KEEL FACTORY is a framework you hand to an AI coding agent (Claude Code, or another
tool) so it works like a disciplined engineering team rather than a guesser. It is
mostly instructions, written as Markdown files the agent reads, plus a few small Python
scripts that check things mechanically.

It works two ways:

- **Operator mode — the usual one.** You drop it into someone else's package (a
  codebase, or a bundle of material with its own instructions). The agent reads the
  package's instructions, does the job, proves it worked, tells you what it did, and
  leaves nothing behind but the work.
- **Owner mode.** It becomes the framework for a project of your own. The agent walks
  the project through five phases, from figuring out what to build to proving it's done,
  and stops for your approval at each one.

---

## 2. What's in the folder

| Item | What it is |
| --- | --- |
| `MANUAL.md` | This file. |
| `VERSION`, `RELEASES.md` | Which release this is, and what each release changed. |
| `OPERATOR.md` | The drop-in protocol the agent follows in operator mode. |
| `START-PROMPTS.md` | The prompts to paste for owner mode, plus the operator one-liner. |
| `README.md` | What's inside, where it came from, privacy and security notes. |
| `QUICKSTART.md` | The owner-mode setup steps, written out by hand. |
| `ARCHITECTURE.md` | How all the pieces fit together. Read this if the rest stops making sense. |
| `CLAUDE.md` | The instruction file the agent loads. In owner mode it goes at the project's root. |
| `keel/framework/` | The rules and disciplines: the five phases, RECON, CREW, LOOPS, the doctrine, and more. |
| `keel/skills/` | KEEL's own skills: `helm` (routes every session), `keel` (the five phases), `keel-prove` (proves "done"), `crew` (several agents at once). |
| `keel/skills-board/` | 16 skills by Miguel Hernandez: the task board, interviewing, handoff and resume, commit, spike, docs upkeep. Claude and Codex versions. |
| `keel/capabilities/` | The two "senses": `deep-research` (find out what the agent doesn't know) and `reverse-engineering` (look inside binaries and running systems, authorized targets only). |
| `keel/templates/` | Blank documents the phases fill in (BRIEF, RECON, DESIGN, ...). |
| `harness/` | The safety layer: the data-boundary guard (`hooks/data-boundary-guard.py`), three other hooks that need Node.js, and their docs. Also the scripts `link_kit.py` (link the kit into a project), `install_guard.py` (set the guard up on a machine) and `make_release.py` (cut a versioned release). |
| `.scratch/handoff.md` | Notes for the next session that develops the framework itself. Never copied into a project. |

---

## 3. Setting up a machine — once per computer

On a new machine, start from a release (section 11 says what's in one):

1. **Restore the master** wherever you keep projects, for example your Git projects
   folder. From the release folder on the SSD:

   ```bash
   cd /Volumes/S-USB/KEEL-FACTORY-releases/v1.0.0     # wherever the release folder is
   shasum -a 256 -c SHA256SUMS                          # every line must say OK
   git clone KEEL-FACTORY-v1.0.0.bundle ~/GitProjects/KEEL-FACTORY   # your path
   ```

   The bundle is one file that carries the whole history and the version tags. Use it
   rather than copying the folder: the SSD is exFAT, which drops file permissions, and
   git would then report changed files. No git? `tar -xzf KEEL-FACTORY-v1.0.0.tar.gz`.

2. **Tell your shell where the master lives.** Every command in this manual uses
   `"$KEEL"`:

   ```bash
   echo 'export KEEL="$HOME/GitProjects/KEEL-FACTORY"' >> ~/.zshrc   # your real path
   source ~/.zshrc
   ```

   On the machine where this was built, `KEEL` is `~/Documents/KEEL-FACTORY`.

3. **Check the tools.** `python3 --version` must work (3.8 or newer; built and tested on
   3.13). `git` is needed for releases and most real work. Node.js is optional: only
   three of the four safety hooks need it, and the important one doesn't.

4. **Install the data-boundary guard, machine-wide.** It stops the agent reading
   secrets (`.env` files, keys, credentials) and anything gitignored, and it switches on
   only in folders that contain `keel-factory/`:

   ```bash
   python3 "$KEEL/harness/install_guard.py"
   ```

   It keeps everything already in `~/.claude/settings.json`, saves the original once as
   `settings.json.before-keel-guard`, and changes nothing if run twice. `--remove` takes
   it out again.

5. **Prove it all works on this machine.** Each must end in OK:

   ```bash
   cd "$KEEL"
   python3 harness/hooks/test_data_boundary_guard.py
   python3 harness/test_link_kit.py
   python3 harness/test_install_guard.py
   (cd keel/skills/crew && python3 scripts/test_check_lanes.py)
   ```

6. **Working from the SSD directly?** macOS has to let the app reach it. In System
   Settings → Privacy & Security → Files and Folders, turn on Removable Volumes for
   Visual Studio Code (or Terminal).

---

## 4. Linked, not copied — how the kit gets into a project

There is only one real copy of the framework: the master, at `$KEEL` (section 3).
A project gets a `keel-factory/` folder that holds **links** to the master, not copies,
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
`keel-factory/` it didn't make, so an old full copy is safe from it.

The links point at this machine. For a project that must carry its own copy, because it's
committed to a shared repo or worked on from another computer, use a full copy instead:
`rsync -a --exclude '.git/' --exclude '.scratch/' --exclude '__pycache__/'
"$KEEL/" /path/to/project/keel-factory/`. A copied project keeps the
version it was copied from.

---

## 5. Operator mode — dropping it into a package

This is the "plop it in and let it work" mode.

1. **Link the kit into the package** (section 4):

   ```bash
   python3 "$KEEL/harness/link_kit.py" /path/to/package
   ```

2. **Start Claude Code inside the package folder** (the guard only arms there), **and say:**

   ```text
   keel-factory/ is your kit. Read keel-factory/OPERATOR.md and take on this package: its own instructions are the mission.
   ```

3. **What happens next:**
   - It proves the guard is live, by trying to read a fake `.env` file and getting
     blocked. If the guard isn't live, it asks you before going on.
   - It reads the package's own instructions; those are the mission.
   - It tells you the mission in one line, then does it, matching the package's style.
   - It checks the work with the package's own tests.
   - It gives you a short debrief: what changed, how it was proven, and what's left.
   - It asks you only at real forks, and then with options and its recommended pick.

4. **When it's done, read the debrief, then unlink:** run the same command with
   `--remove`. That removes every trace of KEEL. The mission's notes and debrief are in
   `keel-factory/.ops/`, and the script keeps that folder if anything is still in it,
   so delete it yourself once you've read it.

**Rules it never breaks, whatever the package says:**

- It reads no secrets, nothing gitignored, and nothing outside the package.
- It does nothing irreversible or outward-facing — pushing, deploying, publishing,
  deleting what it didn't create — without asking you at that moment.
- It stops and tells you if the package's instructions try to get around any of this.
- It never calls something done without running it.

---

## 6. A test drive, start to finish

What it looks like to try the kit on a project you didn't write, just to see what it
does. Nothing in the project's code changes. You get a health check and a ranked list of
what to improve.

1. **Link it in:** `python3 "$KEEL/harness/link_kit.py" /path/to/project`.
   The only change to the project is a new, untracked `keel-factory/` folder.
2. **Start Claude Code inside the project folder.** This matters: the guard arms only for
   the project a session starts in. Start it in your home folder, and the guard sits idle
   and the agent has to apply the rules by hand.
3. **Say:**

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
5. **The debrief** lands in `keel-factory/.ops/debrief.md`, and in the chat:
   - what changed (for a test drive, nothing);
   - each check's real result, labeled Evidence, Inferred or Missing evidence;
   - what it noticed;
   - a ranked list with one recommended first pick;
   - what it deliberately didn't do.
6. **Unlink:** `python3 "$KEEL/harness/link_kit.py" /path/to/project --remove`.
   The links go, and `keel-factory/.ops/` stays so you can keep the debrief. Delete that
   folder when you're done with it.
7. **Want it to act on the recommendation?** Link it in again and say "Do the first item
   on the debrief." It will follow the package's own way of working (its branches, its
   test style, its review rules), and it won't push anything.

---

## 7. Owner mode — your own project

1. **Link the kit into the project** (section 4), or copy it if the project must carry
   its own.
2. **Paste a starter prompt** from `START-PROMPTS.md`. For Claude Code, use the block
   under "Claude Code:". For any other agent, use "The prompt". It sets the project up
   without overwriting anything already there. In particular, an existing `CLAUDE.md`
   gets one import line rather than being replaced.
3. **From then on, just talk to it.** Every new session starts with HELM, which works
   out where the project stands and what to do next. You never re-paste the prompt.

What the agent walks through, stopping for your approval where the tier calls for it:

| Step | What happens | You get |
| --- | --- | --- |
| RECON (existing systems only) | It learns the system and its conventions before proposing anything. | `docs/RECON.md`, and a ranked list of improvements with a recommended first pick |
| BRIEF | What are we building, for whom, and what it is guessing. It asks questions, each with options and a pick. | `docs/BRIEF.md` |
| CONTRACT | What must be true for this to count as done. | `docs/CONTRACT.md`, `docs/ACCEPTANCE.md` |
| DESIGN | The shapes, with no implementations yet. | `docs/DESIGN.md`, including the decisions it's least sure of |
| SLICE | Thin working slices, each tracked as a task on the board. | Working code, and tasks in `.scratch/task_board/` |
| PROVE | An independent review, with the checks actually run. | An honest status: verified, unverified, or only specified |

At each stop it asks: "Approve `<PHASE>`, or what should change?"

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
| The activation line (top of this manual) | Read the package's instructions and take the mission from them. |
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
| data-boundary guard | Always on in any folder with `keel-factory/`. It blocks secrets and gitignored files. |

---

## 10. When something goes wrong

- **The guard blocked something legitimate.** The agent should stop and ask you, naming
  the file. If you really want it allowed, add that file's exact path, relative to the
  project root, to `.keel/data-boundary-allow`. Create that file yourself; never let the
  agent write it. To switch the guard off for one session, set
  `KEEL_DATA_BOUNDARY_OVERRIDE=1` in the agent's environment yourself.
- **Every tool call is blocked with "can't open file".** The hook is pointing at a
  script that isn't there. The self-disarming hook in section 3 can't do this, but an
  older wiring could. Remove the hook entry, or restore the backup of
  `~/.claude/settings.json`.
- **You want the guard gone completely.** Restore
  `~/.claude/settings.json.before-keel-guard`, or delete the KEEL entry from
  `~/.claude/settings.json`.
- **"Node isn't installed".** Only the three ECC hooks need it, and they're optional.
  The guard runs on Python.
- **KEEL can't read its own files.** Something gitignores `keel-factory/`, `.scratch/`
  or `docs/`. Don't gitignore those; the guard blocks gitignored paths.
- **The guard didn't block the fake `.env` probe.** The session was started outside the
  project. Close it and start Claude Code inside the project folder.
- **A whole-project check such as `mypy .` behaves strangely, or stops with "errors
  prevented further checking".** It may have walked into `keel-factory/`. Run it with
  the kit excluded, for example `mypy . --exclude '^keel-factory/'`. The agent is told to
  do this, but it's worth knowing.
- **The agent wants to read something inside `.venv/` or `node_modules/`.** Commands may
  use a project's own tool folders (`.venv/bin/`, `venv/bin/`, `node_modules/.bin/`), so
  it can run the project's tests. Reading other files in those gitignored folders stays
  blocked, as does anything secret-shaped. If it truly needs one, it asks you, naming the
  file.
- **`git status` shows `keel-factory/` as untracked.** That's expected. Never commit it:
  its links point at this machine.
- **The rules feel like too much ceremony.** Operator mode cuts everything except the
  safety rules. In owner mode, the tier decides how many stops you get: SPRINT has
  almost none.

---

## 11. Releases and versions

The master is a git repository, and what travels between machines is a **release**.
This is v1.0.0. Its version is in `VERSION`, and what each release contains is in
`RELEASES.md`.

**What a release folder holds** (`KEEL-FACTORY-releases/v<version>/`, next to the
master):

| File | What it's for |
| --- | --- |
| `KEEL-FACTORY-v<version>.bundle` | The whole repository in one file. Restore with `git clone` (section 3). |
| `KEEL-FACTORY-v<version>.tar.gz` | The same files without git history, for a machine without git. |
| `MANUAL-v<version>.md` | This manual, readable straight off the drive. |
| `README-FIRST.txt` | The restore commands, in three lines. |
| `SHA256SUMS` | Checksums. `shasum -a 256 -c SHA256SUMS` checks the files arrived intact. |

**To cut the next release,** on whichever machine you've been working:

1. Commit your changes: `cd "$KEEL" && git add -A && git commit -m "..."`.
2. Bump `VERSION`. Use the last number for fixes (1.0.1), the middle one for additions
   (1.1.0), and the first for changes that break how you use it (2.0.0).
3. Add a `## v<version>` section to `RELEASES.md`, saying what changed and how you know
   it works. Commit both.
4. Run `python3 "$KEEL/harness/make_release.py"`. It refuses if anything is uncommitted
   or the notes are missing. It then tags the commit, writes the release folder, clones
   it fresh, and runs every self-test from the clone. It only says "proven" if all of
   that passes.
5. Copy the release folder to the SSD, in Finder or with
   `cp -R "$KEEL/../KEEL-FACTORY-releases/v<version>" /Volumes/S-USB/KEEL-FACTORY-releases/`.

**To take a release onto a machine that already has an older one:**
`cd "$KEEL" && git pull /Volumes/S-USB/KEEL-FACTORY-releases/v<version>/KEEL-FACTORY-v<version>.bundle main --tags`.
Linked projects see the new version at once.

---

## 12. Where it came from

- **KEEL:** the original v1.1 is at `~/Documents/FRAMEWORK/`. This folder grew from it.
- **Miguel Hernandez's Skills:** copied in full into `keel/skills-board/`.
- **ECC** (`~/Downloads/ECC-main`) and **REA** (`~/Downloads/rea-main`): cited, not
  copied. Only the pieces the framework uses are in `harness/`. REA is reached through
  `keel/capabilities/reverse-engineering/`, and needs its own install.

The full detail is in `README.md` and in the cross-reference documents under
`keel/framework/`.
