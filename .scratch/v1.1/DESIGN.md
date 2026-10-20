# Design: KEEL v1.1 — harness conformance

Phase 3, STANDARD, checkpoint mode (not a blocking stop). Signatures and seams only.
Inherits `CONTRACT.md` D1–D11 as approved 2026-10-18.
*Updated 2026-10-18 after PROVE pass 1:* also the contract's Amendments section (A1–A7
approved; P-A to P-H proposed, awaiting the manager). §1, §2, §3, §6.2 and §6.4 now
describe the code as it stands.
*Updated 2026-10-18, fix round 3:* the manager approved P-A and P-C to P-H as written and
P-B as an explicit exception, after PROVE pass 2, and fix round 3 changed them (the
contract's F3-1 to F3-9). §1, §2 and §3 describe the code as phase A of fix round 3
landed it.
*Corrected 2026-10-19, fix round 4:* the first note's "P-A to P-H proposed, awaiting the
manager" was true when written; the manager approved all eight on 2026-10-18, at the
PROVE pass 2 report (P-B as an explicit exception), as the second note says. Awaiting
the manager then, and approved as written on 2026-10-20 (the crew plan's Open question
21): fix round 3's rewordings F3-1, F3-2, F3-4 and F3-6, and fix round 4's F4-8, with
F3-3; F3-7's reading of D7 was approved 2026-10-19 ([CONTRACT.md](CONTRACT.md),
"Approved at the PROVE pass 4 report" and "Approved at the PROVE pass 3 report").
*Updated 2026-10-19, fix round 4:* §2's `keel_hook.py` entry and §3's guard row describe
the hook as phase A of fix round 4 landed it: the bounded role read and the guard's
single fail-closed `try` (K30, the contract's F4-1), the patch reader (K31, F4-2), and
the operator note's `<ops>` (K25).

## 1. The shape

*Updated 2026-10-18 after PROVE pass 1.* *Updated 2026-10-18, fix round 3: the
machine-wide guard installer and the release script are in the tree.*

One master folder is both the Claude Code plugin and the source of the Codex skill links.
One hook script with two entry points (subcommands) and one shared marker test, used by
both harnesses:

```text
KEEL-FACTORY/
├── .claude-plugin/plugin.json        # name keel; skills = keel/skills, keel/capabilities and
│                                     #   twelve named skills-board/claude/<name> (A1)
├── .claude-plugin/marketplace.json   # marketplace keel-factory → plugin keel, source "./"
├── agents/prove-{standards,spec,gate}.md
├── evals/<case>/{prompt.md,graders/*.md}
├── CLAUDE.md                         # the short always-on layer (one source)
└── harness/
    ├── plugin-hooks.json             # Claude Code: SessionStart + PreToolUse → keel_hook.py
    ├── settings.hooks.codex.json     # Codex template: keel_hook.py (--harness codex),
    │                                 #   block-no-verify
    ├── hooks/keel_hook.py            # `session` and `guard`, `--harness claude|codex`
    ├── hooks/test_keel_hook.py
    ├── install_plugin.py             # links: ~/.claude/skills/keel, ~/.agents/skills/<skill>;
    │                                 #   --with-docs: the four diataxis-* skills, opt-in (A1);
    │                                 #   --codex-hooks: KEEL's hooks into Codex's hooks.json
    ├── test_install_plugin.py
    ├── install_guard.py              # machine-wide fallback: a PreToolUse entry in
    │                                 #   ~/.claude/settings.json, this master's guard
    ├── test_install_guard.py
    ├── make_release.py               # cuts and proves a release from main; README-FIRST
    ├── test_make_release.py
    ├── check_kit.py                  # KEEL's own instrument; its lists come from the installer
    └── test_check_kit.py
```

## 2. Signatures

*Updated 2026-10-18 after PROVE pass 1: written from the code as it stands.*
*Updated 2026-10-18, fix round 3: `keel_hook.py`'s kit-folder test, import rule and
upgrade note (F3-1, F3-3); `install_guard.py` and README-FIRST added (F3-5, F3-8);
`install_plugin.py`'s taken-name warning and backup rule (N43, N44).*
*Updated 2026-10-19, fix round 4: `keel_hook.py`'s `read_payload`, `role_of`, `marker`,
`keel_state`, `patch_paths`, `guard_payloads` and `guard`, and the operator note in
`session_text` (K30, K31, K25).*

### `harness/hooks/keel_hook.py`

```python
LAYER_MARK = "<!-- KEEL always-on layer -->"   # read by check_kit.py with ast
IMPORT_LINE = re.compile(r"^@(?:\./)?keel-factory/CLAUDE\.md[ \t]*$", re.MULTILINE)
    # an import line, alone on its line; a prose mention of the path is not one
@dataclass
class KeelState:
    root: Path                    # the folder that switched KEEL on
    role: str                     # "owner" | "operator" | "not recorded" | "kit"
    layer_root: Path | None       # a worktree's own root, when the marker is in
                                  #   its main checkout
def read_payload(raw: str) -> dict | None
    # the hook's JSON; {} for empty input; None for anything unreadable, input nested
    # deep enough to raise RecursionError included
def project_start(payload: dict | None) -> Path
    # CLAUDE_PROJECT_DIR, else payload["cwd"], else the working directory
def role_of(keel_dir: Path) -> str
    # "owner" or "operator" from keel.json, else "not recorded"; a bounded read that
    # never hangs or raises: opened with ROLE_OPEN (read-only, without waiting on a pipe
    # or a device where the system allows), then read only when fstat says S_ISREG and
    # the size is within ROLE_CAP (64 KiB). Any oddity (a pipe, a device, a link to one,
    # a file past the cap, JSON nested too deep) is "not recorded", and KEEL stays on
def kit_root() -> Path            # CLAUDE_PLUGIN_ROOT if set, else this file's ../..
def git_root(start: Path) -> Path | None
    # nearest folder at or above start holding .git (a folder, or a worktree's file)
def main_worktree(top: Path) -> Path | None
    # a linked worktree's main checkout (its gitdir holds commondir); None for a submodule
def master_checkout(kit: Path) -> bool
    # the kit root is the master's own git checkout: a .git folder, or a linked worktree;
    # a copy (the documented rsync leaves .git out) or a submodule-vendored kit is not
def has_entry(folder: Path, name: str) -> bool
    # an entry named exactly `name` (os.listdir), a folder or a link to one
def marker(folder: Path, kit: Path, seen: list[Path]) -> KeelState | None
    # .keel/ first (role from .keel/keel.json); then keel-factory/ (role "kit"),
    # unless it is the kit root itself and master_checkout(kit): a link or a copy
    # switches on. Residuals, both failing closed (on, role "kit"): a master that is
    # a worktree of a bare repository; a tarball master renamed keel-factory, seen
    # from its parent. Each entry found goes into `seen` before anything in it is read
def keel_state(start: Path, seen: list[Path] | None = None) -> KeelState | None
    # the six-step rule in the module docstring: off at or inside the kit root;
    # inside git, start → git root, nearest first; outside git, start only;
    # never $HOME or /; a linked worktree then checks its main checkout
    # (layer_root = the worktree), unless that is $HOME, / or inside the kit.
    # Every .keel or keel-factory entry met on the way, its main checkout's
    # included, is added to `seen` when one is given
def instruction_files(root: Path, harness: str) -> list[tuple[str, str]]
    # codex: AGENTS.md; claude: CLAUDE.md, CLAUDE.local.md, .claude/CLAUDE.md,
    # plus AGENTS.md when one of them imports @AGENTS.md
def layer_import(folder: Path) -> bool
    # folder/keel-factory/CLAUDE.md exists and holds LAYER_MARK
def carries_layer(text: str, harness: str, folder: Path) -> bool
    # the mark; or, under claude only, an IMPORT_LINE and layer_import(folder), where
    # folder is the importing file's own folder (.claude/ for .claude/CLAUDE.md)
def layer_status(root: Path, harness: str) -> tuple[str, str]
    # ("v1.0", file) for KEEL's v1.0 copy; ("carries", "") when a file carries_layer;
    # else ("", ""). A prose mention, a dangling import, or an import of a file
    # without the mark never counts: the worst case is the layer twice
def upgrade_note(name: str, harness: str, root: Path) -> str
    # one line for a v1.0 copy: under claude, the import @keel-factory/CLAUDE.md
    # only when layer_import holds; otherwise delete KEEL's v1.0 text (this hook
    # then supplies the layer) or replace it with v1.1's CLAUDE.md. Codex never
    # gets the import
def session_text(state: KeelState, kit: Path, harness: str = "claude") -> str
    # the header, three lines: where KEEL is on and the role; the kit root and how to
    # read keel-factory/ paths; ROLE_NEXT[role], the role's routing line (for "kit":
    # "The kit is at `keel-factory/` (a link or a copy)."; for "operator": follow
    # OPERATOR.md, then the operator note, "Notes go in `<ops>`: `keel-factory/.ops/`
    # where the project holds a `keel-factory/`, else `.keel/ops/`."). Then the kit's
    # CLAUDE.md body; header only when the layer is carried; header + upgrade_note
    # for a v1.0 copy
def patch_paths(text: str) -> list[str]
    # every path a patch's headers name (Add File, Update File, Delete File, Move to).
    # Headers are read from stripped lines, as Codex's parser trims them, wherever they
    # sit: a superset of what Codex applies. The frame lines (Begin Patch, End Patch,
    # End of File, matched exactly once stripped) and `*** Environment ID` pass, and a
    # space-led line inside an Update File or Move to hunk is file context. Any other
    # line that starts with *** once stripped raises ValueError, so the guard blocks
def guard_payloads(raw: str, payload: dict) -> list[str]
    # list-shaped command → joined string; a patch (apply_patch by tool name, or
    # another tool's command that starts with "*** Begin Patch") → one
    # {"tool_name": "Write", "cwd": …, "tool_input": {"file_path": p}} per path from
    # patch_paths, plus the call as it stands when the patch names no file or the tool
    # is not apply_patch (a shell runs that text as a command); anything else → [raw]
def touches_allowlist(one: str) -> bool
    # a Write|Edit|MultiEdit|NotebookEdit of a path ending in .keel/data-boundary-allow
    # (case ignored, links followed), or any command containing data-boundary-allow
def guard(raw: str, harness: str = "claude") -> int
    # one try around all of it: read_payload, keel_state (collecting `seen`),
    # load_guard and the checks. Where KEEL is off, and not under KEEL_GUARD=always,
    # exit 0 before anything is evaluated. Otherwise, per payload, the allowlist block
    # first (KEEL_DATA_BOUNDARY_OVERRIDE does not lift it), then the unchanged guard.
    # On any error, the `seen` rule: a marker met means an error blocks (so does
    # KEEL_GUARD=always); an error before any marker allows, so a folder where KEEL is
    # off is never touched
def parse_args(argv: list[str]) -> tuple[str, str] | None
    # session|guard [--harness claude|codex]; None → the usage on stderr, exit 1
def main(argv: list[str]) -> int
```

Outputs: `session` prints `{"hookSpecificOutput": {"hookEventName": "SessionStart",
"additionalContext": …}}` (both harnesses accept it) or nothing. `guard` exits 0 silently
or 2 with a non-empty reason on stderr (Codex ignores exit 2 with empty stderr). Only
`session` reads `--harness`; `guard` behaves the same for both values.

### HELM's Codex block in a project's `AGENTS.md` (D3)

In Codex owner mode, when the project's `AGENTS.md` has no line
`<!-- KEEL always-on layer -->`, HELM (step 4) adds this once, creating the file if
needed. Operator mode never edits the package's `AGENTS.md`.
*Updated 2026-10-19, fix round 4 (the contract's F4-6):* step 4 now opens "If
`AGENTS.md` holds KEEL's v1.0 text (it says
`This project was started from KEEL FACTORY.`), add no block: offer MANUAL §11's
choice, replacing that text with the block (recommended, so the layer loads once) or
deleting it and relying on the hook, and change the file only on the owner's yes."

```text
<!-- KEEL always-on layer -->        ← the kit's CLAUDE.md as it stands, from its own first line
…the rest of the kit's CLAUDE.md…
Kit root for this block: the project's `keel-factory/` if it has one, else three folders
above the real folder of the `keel:helm` skill (resolve its link first).
<!-- end KEEL always-on layer -->
```

`keel_hook.py session --harness codex` then finds the mark in `AGENTS.md` and injects the
header only.

### `harness/install_plugin.py`

```text
install_plugin.py                        # Claude Code: ~/.claude/skills/keel → master
install_plugin.py --with-docs            # + ~/.claude/skills/diataxis-* → skills-board/claude/
install_plugin.py --codex                # + one link per skill (OWN + BOARD) in
                                         #   ~/.agents/skills/
install_plugin.py --codex --with-docs    # + the four diataxis skills' Codex copies
install_plugin.py --codex-hooks          # merge KEEL's SessionStart + PreToolUse
                                         #   (Bash|apply_patch) into <codex home>/hooks.json;
                                         #   alone, it links nothing
install_plugin.py --remove [same flags]  # unlink only its own links; drop only hook entries
                                         #   naming keel_hook.py
--claude-home / --agents-home / --codex-home   # retarget, for the self-test
```

`<codex home>` is `--codex-home`, else `$CODEX_HOME`, else `~/.codex`; the path written
is printed. Each hook command passes `--harness codex`, carries the shell-quoted absolute
path of `keel_hook.py`, and exits 0 if that file is gone. The original `hooks.json` is
saved once as `hooks.json.before-keel`. Refuses to touch a path that exists and is not
its own link. Never deletes a folder. A link the system will not make (on Windows, links
need Developer Mode or an administrator shell) is a refusal with the reason, and so is a
`hooks.json` or backup that cannot be written, naming the path; a refusal exits 1.
*Updated 2026-10-18, fix round 3:* `--codex` skips a taken name and leaves it untouched;
for KEEL's own six it also prints a warning that `$keel:<name>` will not work in Codex
until the name is free (N43). `--codex-hooks` saves `hooks.json.before-keel` only when
the file held no KEEL entry yet, so the backup is always the user's own original (N44).

### `harness/install_guard.py`

*Added 2026-10-18, fix round 3 (F3-5).*

```text
install_guard.py                 # add KEEL's PreToolUse entry to ~/.claude/settings.json
install_guard.py --remove        # take out only KEEL's entries, older forms included
--settings FILE                  # another settings file, for the self-test
```

```python
MASTER = Path(__file__).resolve().parent.parent   # the copy the script is run from
GUARD = MASTER / "harness" / "hooks" / "data-boundary-guard.py"
COMMAND = ('ls -1 "$CLAUDE_PROJECT_DIR" 2>/dev/null | grep -qxF keel-factory || exit 0; '
           f'g={shlex.quote(str(GUARD))}; [ -f "$g" ] || exit 0; exec python3 "$g"')
    # the exact-name switch, then this master's guard by its absolute, shell-quoted
    # path, never the project's copy; a moved master disarms it until a re-run
MATCHER = "Read|Edit|Write|NotebookEdit|Glob|Grep|Bash"   # no MultiEdit (F3-6)
OLD_MARKER = "$CLAUDE_PROJECT_DIR/keel-factory/harness/hooks/data-boundary-guard.py"
SWITCH = "grep -qxF keel-factory"
GUARD_END = "harness/hooks/data-boundary-guard.py"
def is_keel_command(command: object) -> bool
    # OLD_MARKER in it (v1.0's form and the early v1.1 build's, which ran the project's
    # copy), or SWITCH and GUARD_END both in it (this form, from any master);
    # a hand-wired bare guard is not KEEL's entry
def is_keel(entry: dict) -> bool                # any of the entry's hooks is KEEL's
def load(path: Path) -> dict | None             # {} when absent; None when not shaped
                                                #   the way Claude Code writes it
def main() -> int
```

Install: with no KEEL entry it appends `{"matcher": MATCHER, "hooks": [{"type": "command",
"command": COMMAND}]}`; a KEEL entry holding another command (an older form, or another
master's) gets COMMAND in place ("updated KEEL's guard to the current command"), so a
re-run upgrades and repoints it at this master; a current entry changes nothing. Before
an install or an update writes, the original is saved once as
`settings.json.before-keel-guard`. `--remove` drops every KEEL entry, and the
`PreToolUse` and `hooks` keys when they are left empty. It prints key names only, never
values. A file not shaped the way Claude Code writes it is left untouched, exit 1.
Residual: the master's guard still honors a project's own `.keel/data-boundary-allow`
(N33).

### README-FIRST (`harness/make_release.py`)

*Added 2026-10-18, fix round 3 (F3-8).*

`make_release.py` releases `VERSION` as tag `v<version>`; among the checks it makes before
writing anything, the master must be on `main` (`RELEASE_BRANCH`) with a clean tree. The
README-FIRST.txt it writes gives
four command lines, in this order, each run from the release folder:

```text
shasum -a 256 -c SHA256SUMS                                      # every line must say OK
git clone --branch main "$PWD/KEEL-FACTORY-<tag>.bundle" ~/GitProjects/KEEL-FACTORY
git -C ~/GitProjects/KEEL-FACTORY describe --tags     (must print <tag>)
mkdir -p ~/GitProjects && tar -xzf KEEL-FACTORY-<tag>.tar.gz -C ~/GitProjects  # no git
```

`~/GitProjects/KEEL-FACTORY` is an example: the user's own local path, never the drive.
`--branch main` puts the clone on `main`, where a bundle clone would otherwise take
whichever branch sits at HEAD's commit, so MANUAL's upgrade pull works; a detached
`git checkout <tag>` would strand it.

### `harness/check_kit.py`

`check_kit.py [--root DIR]` → exit 0 clean, 1 with every finding named under its rule id:
`source`, `manifest`, `hooks`, `marketplace`, `skill`, `skill-set`, `skill-path`,
`listing-budget`, `codex`, `agent`, `eval`, `always-on`, `release`, `link` (14; the
docstring defines each). `OWN`, `BOARD` and `DOCS` come from
`<root>/harness/install_plugin.py` and `LAYER_MARK` from
`<root>/harness/hooks/keel_hook.py`, read with `ast` as top-level literals: no code in
them runs, and `--root` checks a copy against its own installer and hook. One function per
rule, each adding findings, so the self-test can break one rule at a time. It writes
nothing in the kit; the `always-on` rule runs the session hook on a temporary folder.

## 3. Seams and the tests at each

*Updated 2026-10-18 after PROVE pass 1.* *Updated 2026-10-18, fix round 3: the marker
and session rows, and the install_guard and README-FIRST rows.* *Updated 2026-10-19, fix
round 4: the guard row (K30, K31).*

| Seam | Test |
| --- | --- |
| marker → armed or dormant | `test_keel_hook.py`: temp repos with `.keel/`, `keel-factory/`, neither, a nested subfolder, `KEEL_GUARD=always`; exact names (a sibling `KEEL-FACTORY`, `.KEEL`), a non-git start, `$HOME`, the kit root, a worktree, a submodule; the master's own git checkout named `keel-factory`, dormant (`test_kit_own_folder_named_keel_factory_is_dormant`); a copied kit with hooks wired from the copy, on and blocking (`test_copied_kit_with_hooks_from_the_copy_switches_on`) |
| guard wrapper → unchanged guard | same file: `.env` read blocked only where KEEL is on; Codex `apply_patch` touching `.env` blocked, touching `src/a.py` whose text mentions `.env` allowed; list-shaped command joined; unreadable JSON blocked in a KEEL project, allowed where KEEL is off; a write, patch or command naming `.keel/data-boundary-allow` blocked, even under the override, and a Read of it allowed; a role file nested 20,000 deep, one byte past `ROLE_CAP`, a named pipe or a link to `/dev/zero` leaves KEEL on, the role not recorded and the guard blocking, and input nested too deep is blocked where KEEL is on and ignored where it is off (`Hostile`); in process, an error after a `.keel`, `keel-factory` or main-checkout marker blocks and one before any marker allows (`InProcess`); a padded header after a hunk, an unreadable `***` line and another tool's command that starts as a patch are blocked or checked as they stand, while the frame and context lines pass (`CodexPatches`) |
| session text → context | same file: emitted only where KEEL is on; size ≤ 7,000; header-only when the project already carries KEEL, counted per harness; an import line counts only when it resolves to a file holding the mark (`@./` too, and from `.claude/` for `.claude/CLAUDE.md`), while a prose mention, a dangling import and an import of a file without the mark inject the layer; a v1.0 copy gets the upgrade note, which offers the import only when it resolves |
| plugin manifest → Claude Code loader | `claude plugin validate .claude-plugin/plugin.json` (exit 0, only the root-`CLAUDE.md` warning; `validate --strict .` checks only the marketplace) and `claude plugin details` (Evidence per run) |
| plugin → live session | headless `claude -p --plugin-dir` in a throwaway repo: `keel:helm` listed, context present, `.env` read blocked |
| Codex links → Codex loader | `codex debug prompt-input` with a scratch `CODEX_HOME` |
| the whole kit → well formed | `check_kit.py`, proven to fail on one broken copy per rule |
| installer → filesystem | `test_install_plugin.py` against temp homes, including a scratch Codex home for `--codex-hooks` |
| install_guard → `settings.json` | `test_install_guard.py` against temp settings files: every other setting kept and the original saved; a re-run changes nothing; an older or another master's entry updated in place; `--remove` takes out only KEEL's entries; a hand-wired bare guard is not KEEL's entry, so install adds KEEL's beside it and `--remove` leaves it; the installed command equals OPERATOR.md's block after its placeholder is substituted; run in temp projects, it arms only for an exact `keel-factory`, never runs the project's copy, and the master's guard blocks `.env` while the project's copy would allow it |
| README-FIRST → a restored master | `test_make_release.py`: `test_readme_first_restores_onto_main_at_the_tag` follows the text word for word and requires HEAD on `main` and `describe` printing the tag; `test_readme_first_without_git_untars_off_the_drive` restores `VERSION` from the archive; neither writes on the drive |

## 4. Depth check

`keel_hook.py` is the one deep module: a small interface (two subcommands) over marker
discovery, two harness payload shapes and the guard. Everything else is data (manifests,
agent files, eval cases, prose). No new abstraction is introduced for one caller.

## 5. Test plan

Red first at each seam: write `test_keel_hook.py` before `keel_hook.py`, watch it fail
on import, then make it pass. `check_kit.py` and `install_plugin.py` the same way. Each
new self-test is proven to fail against deliberately broken copies (Rule 6b), the way the
v1.0 suites were.

## 6. Least-confident decisions

1. **Codex hook trust and matcher names on 0.138.** The docs are for 0.163; this binary is
   older. Until a Codex session shows the guard blocking, the Codex guard is *Missing
   evidence*. A live probe needs a Codex model call, which the manager has not yet
   approved.
2. **Skill-list budget.** *Updated 2026-10-18 after PROVE pass 1.* The plugin loads 18
   skills, whose names and descriptions come to 7,038 characters by `check_kit.py`'s
   count; the four Diataxis skills would add 1,105, giving 8,143, over the 8,000 that
   `check_kit.py` holds the listing to. Both harnesses budget their skill listing (each
   one's caps and overflow behavior:
   [CAPABILITIES.md](../../keel/framework/CAPABILITIES.md)), so the same 18 load under
   both, as the plugin under Claude Code and as links under Codex: one listing size to
   keep within bounds, not two. `--with-docs` adds the four under both harnesses; under
   Claude Code they are linked into `~/.claude/skills/` as standalone skills, outside the
   plugin. Shortening KEEL's six helps; the vendored ones can't be edited.
3. **SessionStart text in Claude Code after `/compact`.** The docs say SessionStart fires
   with source `compact`; not probed here.
4. **A subagent in a KEEL project.** Hooks fire on subagent tool calls (Inferred from the
   docs); Explore agents skip `CLAUDE.md`, so the injected rule may not reach them and the
   guard is their only data boundary. CREW's brief must carry the rule.
   *Updated 2026-10-18 after PROVE pass 1:* the hook half is now Evidence. In live run L8
   ([HARNESS-PROBES.md](../../keel/framework/HARNESS-PROBES.md)), a `general-purpose`
   and an `Explore` subagent in a `.keel/` project each had a Read of `.env` blocked by
   the plugin's hook. Whether the injected rule reaches them is still not probed.
5. **Removing `disable-model-invocation` from `keel`.** It lets the model start KEEL by
   itself. The description says "not for trivial tweaks", and HELM's trivial branch still
   comes first.
