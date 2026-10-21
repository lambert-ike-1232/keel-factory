# Contract: KEEL v1.1 — harness conformance

Phase 2 of KEEL, at STANDARD, run in checkpoint mode: this document and `BRIEF.md` are
approved together, once. Every line is a decision. Each decision cites the probe
(`keel/framework/HARNESS-PROBES.md`, P = Claude Code, X = Codex) or source it rests on; a decision resting only on
documentation is marked *Inferred* until a probe confirms it here.

---

## 1. Production build contract

| | |
| --- | --- |
| **Runtime** | Python 3.8+ standard library for every script (built and tested on 3.13.13). No Node. |
| **Harnesses** | Claude Code ≥ 2.1.170 (tested here). Codex CLI 0.138 (tested here, binary in the Codex app). |
| **Distribution** | One master folder, a git repo. Claude Code: the master *is* the plugin. Codex: per-skill links into `~/.agents/skills/`. The `link_kit.py` kit stays as the fallback and for operator drops. |
| **Primary interface** | `/keel:helm …` in Claude Code, `$keel:helm …` in Codex, or plain words ("use KEEL: …"). |
| **Secrets policy** | KEEL holds none. The guard keeps the agent away from a project's secrets. |

## 2. What each harness really offers — the facts this contract stands on

| Need | Claude Code 2.1.170 | Codex 0.138 |
| --- | --- | --- |
| Skills listed by name + description, body on demand | Yes (P4) | Yes (X2) |
| Install once, live from the master | Symlink `~/.claude/skills/keel` → master: a skills-dir plugin, loaded in place (P9) | Symlink each skill into `~/.agents/skills/` (X3, X5) |
| Pinned, versioned install | Marketplace install copies to a cache (P8) | Plugin install copies to a cache with a cachebuster (X6) |
| Namespaced names | `keel:helm` (P4) | Only inside a Codex plugin (`plugin:skill`); plain skills are bare names |
| Always-on context without `CLAUDE.md` | Plugin SessionStart hook `additionalContext` (P6) | `AGENTS.md` (X4); hooks exist (X1, X7) but not in plugins (X6) |
| Block a tool call | Plugin PreToolUse hook, exit 2 (docs; probed in S1) | Hooks with persisted trust (X7); the matcher's tool names are not yet probed → *Inferred* |
| Structured multiple-choice question | AskUserQuestion, 1–4 questions × 2–4 options, interactive only (docs) | `request_user_input` in Plan mode only by default (X1; prompts) |
| Fresh-context reviewer | Plugin `agents/*.md`, called as `keel:<name>` (P4, P10) | `spawn_agent` with no forked history; v1 spawns only on an explicit user request (prompts) |
| Headless run with a cost cap | `claude -p --max-budget-usd` | `codex exec`; goals carry a `token_budget` (prompts) |
| Plugin evals | `claude plugin eval` needs ≥ 2.1.269 → not here (P12) | none found |

*Stale 2026-10-19: the "Namespaced names" row's Codex cell. Probe X9
([HARNESS-PROBES.md](../../keel/framework/HARNESS-PROBES.md), "Codex, 2026-10-18") shows
that Codex names a linked skill whose real folder sits under a
`.claude-plugin/plugin.json` after that plugin. So KEEL's links list as `keel:helm`:
`$keel:helm` in Codex (`$helm` where the skills were copied into `.agents/skills/`), as
§1 says. A copied skill's bare name rests on X2: Evidence for a plain repo skill,
Inferred for KEEL's own copied skills. The current table is
[CAPABILITIES.md](../../keel/framework/CAPABILITIES.md)'s (D11). No decision changes.*

## 3. Decisions

### D1 — Claude Code packaging

*Amended 2026-10-18: see Amendments, A1.*

- `.claude-plugin/plugin.json` at the master root: `name` `keel`, `version` equal to
  `VERSION`, `skills` = `./keel/skills/`, `./keel/capabilities/`,
  `./keel/skills-board/claude/`, `hooks` = `./harness/plugin-hooks.json` (not
  `hooks/hooks.json`, P7). Agents in the default `agents/` folder at the root (P10).
- `.claude-plugin/marketplace.json`: marketplace `keel-factory`, one plugin, source `./`.
- Default install: `python3 "$KEEL/harness/install_plugin.py"` makes
  `~/.claude/skills/keel` a link to the master and refuses to touch anything it didn't
  make; `--remove` unlinks only. Pinned alternative:
  `claude plugin marketplace add "$KEEL"` then `claude plugin install keel@keel-factory`.
  Pick one: an installed marketplace plugin of the same name wins over the skills-dir
  one (seen in the P8–P10 runs).

### D2 — What switches KEEL on in a project

*Amended 2026-10-18, approved after PROVE pass 2: see Amendments, P-A and P-H; changed in
fix round 3: F3-1 and F3-2.*
*2026-10-19: F3-1's and F3-2's rewordings go to the manager again; see "Proposed,
awaiting the manager".*
*2026-10-19, fix round 4: F4-5 and F4-7 carry it out; F4-8 rewords where operator notes
go and is proposed; see "Amendments — 2026-10-19, fix round 4" and "Proposed, awaiting
the manager".*
*2026-10-20: F3-1's, F3-2's and F4-8's readings approved as written; see "Approved at the
PROVE pass 4 report".*

- **On** when the project root, or a folder above it inside the same repo, has `.keel/`
  or `keel-factory/`. Otherwise KEEL is dormant there: its skills are listed, nothing is
  injected, the guard does not arm.
- `.keel/keel.json` records one thing: `{"role": "owner"}` or `{"role": "operator"}`.
  HELM writes it the first time KEEL is used in a project. Tier and stop mode live in
  `docs/STATE.md`, their one home.
- Operator notes go in `.keel/ops/` when the kit came by plugin, `keel-factory/.ops/`
  when it was linked. Both are KEEL's whole footprint and are removed at exfil.

### D3 — Always-on context

*Amended 2026-10-18: see Amendments, A2 and A5; approved after PROVE pass 2: P-B (as an
explicit exception) and P-C; changed in fix round 3: F3-3 and F3-4; A2's and A5's
records corrected: C5 and C1.*
*2026-10-19: F3-4's rewording goes to the manager again; see "Proposed, awaiting the
manager".*
*2026-10-19, fix round 4: F4-6 carries it out (no Codex block on top of a v1.0
`AGENTS.md`); see "Amendments — 2026-10-19, fix round 4".*
*2026-10-20: F3-4's reading approved as written, and F3-3's reading of P-C with it; see
"Approved at the PROVE pass 4 report".*

- The master's `CLAUDE.md` is rewritten as the short always-on layer: operator gate,
  HELM pointer, suggest-don't-ask-blind, the data-boundary rule in full, one-line
  tripwires. Target ≤ 6,000 characters (was 12,856).
- The plugin's SessionStart hook (`harness/hooks/keel_session.py`) injects that same
  file, prefixed with the kit root and the project's role, in projects where KEEL is on,
  and only there. If the project's own `CLAUDE.md` already imports or copies it, it
  injects only the kit-root line. One source, never two copies in context.
- Codex: the same text goes into the project's `AGENTS.md` (owner mode) as a fenced
  KEEL block HELM adds once; Codex has no import.

### D4 — The guard under the plugin

*Amended 2026-10-18: see Amendments, A5; approved after PROVE pass 2: P-D and P-G; changed
in fix round 3: F3-5, F3-6 and F3-9; A5's record corrected: C1.*
*2026-10-19: F3-6's rewording goes to the manager again; see "Proposed, awaiting the
manager".*
*2026-10-19, fix round 4: F4-1 and F4-2 carry it out (the hook's two fail-open paths
closed); see "Amendments — 2026-10-19, fix round 4".*
*2026-10-20: F3-6's reading approved as written; see "Approved at the PROVE pass 4
report".*

- `harness/plugin-hooks.json` runs `harness/hooks/keel_guard.py` on
  `Read|Edit|Write|NotebookEdit|Glob|Grep|Bash`. The wrapper exits 0 at once where KEEL
  is off, and otherwise hands stdin to the unchanged `data-boundary-guard.py`. The guard
  itself is not edited; its 27-test self-test must stay green.
- `KEEL_GUARD=always` arms it everywhere for a user who wants that.
- The existing machine-wide hook from `install_guard.py` keeps working; with both, the
  guard runs twice on the same call and gives the same answer.

### D5 — One front door

*Amended 2026-10-18, approved after PROVE pass 2: see Amendments, P-A (where HELM writes
`.keel/`); changed in fix round 3: F3-2.*
*2026-10-19: F3-2's rewording goes to the manager again; see "Proposed, awaiting the
manager".*
*2026-10-19, fix round 4: F4-3, F4-4, F4-5 and F4-7 carry it out (HELM's switch-on and
the operator test); see "Amendments — 2026-10-19, fix round 4".*
*2026-10-20: F3-2's reading approved as written; see "Approved at the PROVE pass 4
report".*
*2026-10-20, docs round 5 (S4-a2), an entry, not a proposal: Carried out by HELM's
owner-mode paragraph and keel step 3: the stop mode is asked in BRIEF's first round and
recorded in docs/STATE.md, D2's one home. HELM writes no docs/ file, because its routing
branch 1 reads docs/STATE.md as a project already under way.*
*2026-10-20, docs round 6 (RECORDS-N3): S4-a2's reading stays inside D5's meaning
under S-c2: the stop mode is still asked once and recorded for owner mode, in D2's one
home; only the step that writes it moves from HELM to the keel skill HELM routes to.
PROVE-4's "Every verified item" table named it an entry, in the report the manager
answered.*

- HELM's description names its triggers plainly ("use KEEL", "/keel:helm", any session in
  a project where KEEL is on). `keel` loses `disable-model-invocation`, so HELM can route
  to it (P5 showed the flag hides a skill from the model).
- HELM gains a first step: *is KEEL on here, and in what role?* It reads `.keel/keel.json`;
  if absent it infers owner vs operator from the evidence (the package has its own
  instructions → operator) and asks once, with options and a pick, only when it can't
  tell. It records the answer and, for owner mode, the stop mode.
- One opening line replaces three: "Use KEEL: <what you want>". The operator line and the
  test-drive line become things you say *after* it, not separate front doors.

### D6 — Stop modes

*Amended 2026-10-18: see Amendments, A3.*
*2026-10-20, docs round 6 (sprint-checkpoint-stops): approved by the manager at the
closure report, answer "Up-front round (Recommended)" (the crew plan's Open question 23).
At SPRINT the up-front round is BRIEF's one question, asked in the same message as the
approval of BRIEF and CONTRACT, and supervised mode stops at the same two places (that
message, then the PROVE report). `TIERS.md`, the `keel` skill and `PHASES.md` say so
from 1.1.1.*

Added to `TIERS.md` as a second dial beside the tier. The tier sets how heavy each phase
is; the mode sets which stops wait for you. The phases never change.

| Mode | Waits for you at | Runs on its own |
| --- | --- | --- |
| **supervised** | every stop the tier lists (today's behavior) | nothing between stops |
| **checkpoint** | one up-front round (BRIEF questions plus the production questions: users, auth, data, secrets, deploy target, external services, toolchain, cost ceiling), one approval of BRIEF + CONTRACT together, and the PROVE report | DESIGN, SLICE, and the PROVE review |
| **unattended** | the same up-front approval, then nothing until the PROVE report | everything after the approval, inside `LOOPS.md`'s seven fields |

- Checkpoint and unattended still halt for: the data boundary; any irreversible or
  outward-facing action; a decision BRIEF and CONTRACT don't settle and that changes the
  outcome; a check still failing after three honest attempts; a finding that breaks the
  approved CONTRACT; the cost ceiling.
- Unattended has nobody to ask, so a halt there means: write it as a board task with
  `gate: owner`, carry on with work that doesn't depend on it, and stop at the PROVE
  report. It needs the `LOOPS.md` fields recorded in `STATE.md` first.
- Default: checkpoint at SPRINT and STANDARD, supervised at PLATFORM. → question round.

### D7 — PROVE reviewers as agents

*Amended 2026-10-18, approved after PROVE pass 2: see Amendments, P-E; fix round 3's
F3-7 proposes a rewording, awaiting the manager.*
*2026-10-19: F3-7's reading approved; see "Approved at the PROVE pass 3 report".*

- `agents/prove-standards.md`, `agents/prove-spec.md`, `agents/prove-gate.md`, called as
  `keel:prove-standards` and so on. Their bodies are the review prompts `keel-prove`
  holds today, moved, not rewritten. Tools: `Read, Grep, Glob, Bash`. No `hooks`,
  `mcpServers` or `permissionMode` (ignored for plugin agents, per docs).
- `keel-prove` names the agents, and tells any other harness to brief a fresh-context
  sub-agent with the body of the same file. In Codex: `spawn_agent` without forked
  history; asking for `keel-prove` is the explicit request Codex's multi-agent v1 needs.

### D8 — Codex track

*Amended 2026-10-18: see Amendments, A4; its record corrected in fix round 3: C1.*

- `harness/install_plugin.py --codex` links each KEEL skill, using the `codex/` variants of
  the vendored ones, into `~/.agents/skills/`, skipping taken names, and `--remove` unlinks
  only what it made.
- KEEL's own six skills get `agents/openai.yaml` (display name, short description,
  `allow_implicit_invocation: true`), matching the vendored Codex copies.
- The question adapter (DOCTRINE §2, `CLAUDE.md`): in Codex Default mode, where the
  structured question tool is absent and multiple-choice text is discouraged by Codex's own
  prompt, ask one question in a sentence that states the recommended pick and its
  alternatives, or run the interview round in Plan mode, where `request_user_input` takes
  options and a recommended first choice.
- Hooks: `harness/settings.hooks.codex.json` is corrected to whatever the Codex docs and a
  probe show. Until a probe shows the guard blocking inside Codex, the Codex guard is
  *Missing evidence* and the rule runs as policy, said once per session.

### D9 — Evals

- `evals/` at the root, three cases in the documented format: a vague idea, a complete
  description, an operator job. Graders: deterministic first (skill invoked, no code
  written before approval, files that must exist), one LLM criterion each. Baseline arm
  on.
- They can't run on 2.1.170. `check_kit.py` checks their structure; running them is a
  manual gate (`gate: manual`) for a machine with ≥ 2.1.269.

### D10 — KEEL's own instrument

*Amended 2026-10-18: see Amendments, A6; approved after PROVE pass 2: P-F; changed in fix
round 3: F3-8; A6's record corrected: C2.*

- `harness/check_kit.py` with `harness/test_check_kit.py`, standard library only. It
  checks the plugin manifest and marketplace, every skill on the plugin's paths (name
  equals folder, description present, ≤ 1,536 characters, no duplicate names), the agents,
  the hooks file and every script it names, the eval cases' keys, the Codex link set, the
  always-on sizes, `VERSION` against `plugin.json`, and that relative links resolve.
- `make_release.py` runs it and the new self-tests along with the old four.

### D11 — Documents

*Amended 2026-10-18, approved after PROVE pass 2: see Amendments, P-F; changed in fix
round 3: F3-8.*

- `CAPABILITIES.md` gains a dated harness table (§2 above, kept current with probe IDs).
- `README`, `QUICKSTART`, `MANUAL`, `START-PROMPTS`, `ARCHITECTURE`, `OPERATOR`,
  `harness/README` describe the plugin install first and the linked kit as the fallback.
- Fix: `TIERS.md` "these six" lists seven; `RULES.md` title says five rules, defines six.
- `VERSION` 1.1.0 and a `RELEASES.md` section with Evidence / Inferred / Missing kept
  apart. No tag and no commit without the manager's word.

## 4. Toolchain (Rule 6a)

| Requirement | Version | Needed by | Status |
| --- | --- | --- | --- |
| python3 | 3.13.13 | every script and self-test | present |
| git | 2.50.1 | repo, release, lane checker | present |
| claude | 2.1.170 | `plugin validate`, `plugin details`, `-p` probes | present |
| codex | 0.138.0-alpha.7 | `debug prompt-input`, `features list` | present (app bundle path) |
| claude ≥ 2.1.269 | — | `claude plugin eval` | **MISSING** → evals stay a manual gate |
| node | — | the three ECC hooks | **MISSING** (unchanged; not in scope) |

## 5. Bound numbers (Rule 6d)

*Amended 2026-10-18: see Amendments, A6; its record corrected in fix round 3: C2 and C4.*

| Figure | Value | Asserted by |
| --- | --- | --- |
| Always-on `CLAUDE.md` size | ≤ 6,000 chars | `check_kit.py` |
| SessionStart injection | ≤ 7,000 chars | `check_kit.py`, running the hook on a temp project |
| Skill description length | ≤ 1,536 chars each | `check_kit.py` |
| Old self-tests | 63 tests (27 + 9 + 6 + 21), all pass | the four suites |
| `plugin.json` version | equals `VERSION` | `check_kit.py` |
| Live-trial spend | ≤ the ceiling the manager picks | `--max-budget-usd` on each run |

*Stale 2026-10-18: `test_install_guard.py` now has 13 tests (the seven new install_guard
tests come from row 8 and P-D), so the old four suites total 70 (27 + 9 + 13 + 21);
`ACCEPTANCE.md` holds the measured counts. Fix round 3, 2026-10-18: 18 tests (five more,
from N37), so the old four suites total 75 (27 + 9 + 18 + 21), all passing; see C4.*

## 6. Cost budget

| | |
| --- | --- |
| Unit of work | one headless verification run |
| Unit ceiling | $0.40 for probes; the trial ceiling is the manager's pick |
| Measured so far | four probes, under $1 total (Evidence: each ran with a $0.30–0.40 cap) |

## 7. Human review gates

The manager decides: the default stop mode, the guard's scope, the live-trial budget,
installing on this machine, committing and tagging. Everything else above is decided
here from the probes.

## Goals

Make KEEL load the way its harnesses load things, cost less context, stop where the
manager chose, and be honest per harness about what is enforced.

## Non-goals

New phases, rules or tiers; edits to `keel/skills-board/`; Node hooks; a heuristic
"done"-claim Stop hook; a Codex plugin package (its installs are cached copies and can't
carry hooks; the links are live and proven, so they come first).

## Amendments — 2026-10-18, after PROVE pass 1

PROVE pass 1 ([PROVE-FINDINGS.md](PROVE-FINDINGS.md)) found decisions made outside the
sections above and figures the code no longer matches. Sections D1–D11 and §1–§7 stay as
approved; each decision amended here, or proposed for amendment, carries a pointer line
under its heading.

**The manager's approval, 2026-10-18, verbatim.** To "Which contract amendments should I
write in as recommended?" the manager ticked "D1: Diataxis opt-in,D3: guard-probe
exception,D6: crew checkpoint OK,D8: keep --codex-hooks". The option text said
"Wording-only fixes (one keel_hook.py, the 1,024 cap, non-strict validate) come along
with these." The go-ahead for the fixes was "Yes, rows 1–11 → pass 2 (Recommended)".
Evidence: the lead's record in
[crew-plan-prove-fixes.md](../task_board/crew-plan-prove-fixes.md), Open questions 1
and 2 (the option text as the lead quoted it in the records lane's brief).

### Approved

**A1 — D1, the plugin's skills (closes P2).** `skills` = `./keel/skills/`,
`./keel/capabilities/` and twelve named `./keel/skills-board/claude/<name>` skills:
commit, focused-implementation, handoff, orchestrate-implementation, post-creation-audit,
resume-handoff, spike, task-board-init, task-board-triage, task-interview, to-follow-on,
to-task. The four `diataxis-*` skills are opt-in through `install_plugin.py --with-docs`,
which links them under both harnesses, to keep the skill listing under `check_kit.py`'s
8,000-character budget. Evidence: `.claude-plugin/plugin.json` lists those twelve, and
`check_kit.py`'s `skill-set` rule holds it to the installer's `BOARD`; `check_kit.py`
reports 7,038 listing characters for the 18 skills loaded, and the four docs skills add
1,105 by its own count (names plus descriptions, 1,089, plus 4 per skill), which gives
8,143. Manager's pick: "D1: Diataxis opt-in".

**A2 — D3, the guard-probe exception (closes P6).** The always-on layer carries the
data-boundary rule in full, plus one named exception: the guard probe, a Read of the
nonexistent `keel-armed-check/.env`, made only to see the guard block it. HELM's
switch-on (`keel/skills/helm/SKILL.md`, step 3) and OPERATOR.md's infil require it. The
conflict between the rule and the probe was found by reading the two texts (Inferred),
not from an observed refusal. Evidence: `CLAUDE.md`, Data boundary section, "The one
exception is the guard probe". Manager's pick: "D3: guard-probe exception".

**A3 — D6, CREW's dispatch agreement in checkpoint mode (closes P9).** In checkpoint
mode the agreement CREW's step 4 waits for is the BRIEF + CONTRACT approval plus the
manager's own words allowing agents, quoted in the plan. A lane decision those approvals
do not settle still halts. This amendment says nothing about unattended mode. Evidence:
`keel/skills/crew/SKILL.md` §4; the reason is `keel/framework/CREW.md`, Field record,
Gap 2. Manager's pick: "D6: crew checkpoint OK".

**A4 — D8, `--codex-hooks` (closes P7).** `install_plugin.py --codex-hooks` merges KEEL's
SessionStart and PreToolUse (matcher `Bash|apply_patch`) entries into Codex's
`hooks.json`: in `$CODEX_HOME` when it is set, else in `~/.codex`, and `--codex-home`
overrides both. It keeps every other hook, backs the original up once as
`hooks.json.before-keel`, and `--remove` takes out only entries whose command names
`keel_hook.py`. Codex runs the hooks only after the user trusts them in `/hooks`.
Running it on a real machine needs the manager's own yes (`STATE.md`: writing Codex's
`hooks.json` "needs its own yes"). Evidence: `harness/install_plugin.py` and the hooks
cases in `harness/test_install_plugin.py`. Manager's pick: "D8: keep --codex-hooks".

Wording only, approved with A1–A4 (the three the option text named):

**A5 — D3 and D4, one hook script (closes P11).** Where D3 names
`harness/hooks/keel_session.py` and D4 names `harness/hooks/keel_guard.py`, read one
script, `harness/hooks/keel_hook.py`, with `session` and `guard` subcommands and
`--harness claude|codex`. Its `guard` adapts Codex `apply_patch` (each file the patch
names is checked as a path) and list-shaped commands (joined into a string) before
handing each call to the unchanged `data-boundary-guard.py`. Evidence:
`harness/plugin-hooks.json` runs `keel_hook.py session` and `keel_hook.py guard`;
neither `keel_session.py` nor `keel_guard.py` exists in `harness/hooks/`.

*2026-10-19, fix round 4: F4-2 carries it out (every header a Codex patch names, padded
or not, is checked as a path); see "Amendments — 2026-10-19, fix round 4".*

**A6 — §5 and D10, the description cap and the listing bound (closes P12b).** A skill
description is at most 1,024 characters, Codex's cap and the stricter of the two
harnesses' (both caps: [CAPABILITIES.md](../../keel/framework/CAPABILITIES.md), the
harness tables). The skill listing, names plus descriptions of the plugin's skills, is
at most 8,000 characters. Both are asserted by `check_kit.py` (`DESC_MAX`,
`LISTING_MAX`; rules `skill` and `listing-budget`). Evidence: `harness/check_kit.py`.

*2026-10-19: the 8,000-character listing bound approved by the manager; see "Approved at
the PROVE pass 3 report".*

**A7 — BRIEF's done criterion (closes P3).** "`claude plugin validate --strict` passes"
becomes "`claude plugin validate .claude-plugin/plugin.json` exits 0 with only the
expected root-CLAUDE.md warning (strict fails on that warning by design)". The root
`CLAUDE.md` is the always-on layer the session hook reads, so the warning stays.
Evidence: PROVE-FINDINGS, P3 (strict exits 1 on that warning; non-strict exits 0);
`ACCEPTANCE.md` R9 already uses the non-strict form.

**Implemented as approved, no amendment.** D3's Codex block (P1): in Codex owner mode
HELM adds the kit's `CLAUDE.md` to the project's `AGENTS.md` once (step 4), between the
mark and `<!-- end KEEL always-on layer -->`, with one portable kit-root line. Its exact
form is in `DESIGN.md` §2. Two more of HELM's switch-on steps serve approved D3 and D5 as
written, with no amendment: it reads the kit's `CLAUDE.md` at switch-on, so the first session
carries the layer (COMPLETENESS-1), and it warns when `.keel/keel.json` is gitignored and
tells an owner to commit it (COMPLETENESS-7).

#### Approved after PROVE pass 2, 2026-10-18

The manager's picks at the PROVE pass 2 report, verbatim, with each question and option
text in [crew-plan-prove-fixes.md](../task_board/crew-plan-prove-fixes.md), Open question
16: "Make it an explicit exception" for P-B, and "All as written (Recommended)" for P-A
and P-C to P-H, whose option text was "Each is written up in CONTRACT.md 'Proposed,
awaiting the manager' with its reason; all conform to what rows 1–11 asked for." Each
was decided during the fix run (the crew plan's Open questions) and went to the manager
as proposed. P-A and P-C to P-H keep their proposed text word for word; P-B is written
in its approved form, its proposed text kept as history. Fix round 3's changes to them
are not written into these texts: each is a dated entry in the next section (F3-1 to
F3-9), with a pointer line under the entry it changes.

Which of them carry out the approved fix rows (spec:b5). The go-ahead "Yes, rows 1–11 →
pass 2 (Recommended)" approved rows 1–11 of the disposition table in
[PROVE-FINDINGS.md](PROVE-FINDINGS.md). Carrying out those rows: P-A (rows 1 and 4), P-C
(row 2, narrowed), P-E (rows 5 and 9), P-F (rows 6 and 10), P-G (row 3), and P-D's
exact-name test (row 8). Going beyond them: P-B (COMPLETENESS-15, which no row names; it
changes the data-boundary rule's text, and PROVE-2's "For the manager", item 1, put it to
the manager as that); P-D's in-place upgrade of an older entry; P-C's narrowing of row 2
(a lone `AGENTS.md` does not count under Claude Code); and P-H, row 12's exfil sentence,
which needed the manager's re-approval. The option text says all of them "conform to what
rows 1–11 asked for"; for P-D's upgrade, P-C's narrowing and P-H (row 12, not one of rows
1–11) that is not exact, but each entry's own text, approved as written, says what it does
(P-C: "narrower than the PROVE plan's row 2"; P-D: "re-running it upgrades an older KEEL
entry in place"; P-H: "it records unchanged v1.0 behavior").

**P-A — D2 and D5, the switch-on rule made exact (closes P10, WALKTHROUGH-1,
COMPLETENESS-2, COMPLETENESS-3, COMPLETENESS-8).** What: KEEL is on when a folder from the
start up to and including the git root holds an entry named exactly `.keel` (a folder) or
exactly `keel-factory` (a folder or a link to one); the nearest wins. Outside git, only
the start folder counts. Never on: a start at or inside the kit root; a marker in `$HOME`
or `/`; a `keel-factory` entry that is the kit's own folder. A linked worktree also checks
its main checkout; a submodule does not. HELM applies the same bounds when it writes
`.keel/keel.json`: it refuses `$HOME`, `/` and anywhere inside the kit root. Why: D2's
"inside the same repo" was built as a case-insensitive walk with no bound outside git, so
a non-git folder beside a master named `KEEL-FACTORY` switched on (P10, WALKTHROUGH-1), a
`~/.keel/` switched on every non-git folder under home (COMPLETENESS-3), a worktree of a
KEEL project was off (COMPLETENESS-2), and a project inside the master got the layer twice
(COMPLETENESS-8, Inferred from Claude Code loading ancestor `CLAUDE.md` files). Evidence:
`harness/hooks/keel_hook.py`, the module docstring's six-step rule, and its tests in
`test_keel_hook.py`. Recommend: approve; it is what "inside the same repo" meant, made
exact. Alternative: keep D2's wording and treat the refinements as design (`DESIGN.md`
§2).

*Manager's pick: "All as written (Recommended)". Changed in fix round 3: F3-1 (the
master's own git checkout) and F3-2 (where the role is recorded); D4 is reworded through
it in F3-6.*
*2026-10-20: F3-1's reading approved as written, with its third residual; see "Approved
at the PROVE pass 4 report".*

**P-B — D3, reading the KEEL kit: a second named exception (closes COMPLETENESS-15).**
Approved form. What: `CLAUDE.md`'s item 3 keeps its approved wording, "Anything outside
this project's working tree that the task did not explicitly name.", and a second named
exception follows the guard probe's. `CLAUDE.md` now reads: "Two exceptions need no
question. The **guard probe**: a Read of `keel-armed-check/.env`, a path that does not
exist, made only to see the guard block it (HELM's switch-on, OPERATOR.md's infil); it
reads nothing. And **reading the KEEL kit itself**: the kit root the session note names,
or the kit a KEEL skill was loaded from; items 1 and 2 still apply inside it." Why, as
proposed: under the plugin the kit is outside the project, so the rule as written forbade
the framework reads the live runs made. Evidence: `CLAUDE.md`, Data boundary section
(item 3 at line 69, the exceptions at lines 80–84, read 2026-10-18).

*Manager's pick: "Make it an explicit exception", whose text was "Reword it as a second
named exception beside the guard probe, not a reading of item 3." Not picked: "Approve as
clarification (Recommended)", "Reject and revert". The proposed text, declined in that
form, is kept below as history only.*

> **P-B — D3, data-boundary item 3 and the kit (closes COMPLETENESS-15).** What:
> `CLAUDE.md`'s item 3 now says the KEEL kit itself counts as named by the task (the kit
> root the session note names, or the kit a KEEL skill was loaded from), so reading it is
> allowed; items 1 and 2 still apply. Why: under the plugin the kit is outside the project,
> so the rule as written forbade the framework reads the live runs made (the L4a and L7
> traces read the kit under `~/.claude/skills/keel/`). Recommend: approve, as a
> clarification of what the task names. Alternative: a second named exception beside the
> guard probe.

**P-C — D3, which project files already carry the layer (closes COMPLETENESS-4, P5).**
What: the session hook asks per harness. Codex counts only `AGENTS.md` holding the mark.
Claude Code counts `CLAUDE.md`, `CLAUDE.local.md` and `.claude/CLAUDE.md` holding the mark
or the import text `keel-factory/CLAUDE.md`, and `AGENTS.md` only through an
`@AGENTS.md` import from one of them. A v1.0 copy (it says "This project was started from
KEEL FACTORY.") gets the header and a one-line upgrade note instead of a second layer.
Why: the check ignored which harness asked, so the layer was dropped (COMPLETENESS-4),
and a v1.0 copy got the layer twice (P5). This is narrower than the PROVE plan's row 2,
which counted a lone `AGENTS.md`: KEEL's research says Claude Code does not read one
(Inferred, not probed). The worst case is the layer twice, never missing. Evidence:
`keel_hook.py` `instruction_files` and `layer_status`. Recommend: approve. Alternative:
row 2's wording, whose worst case, if the research holds, is the layer missing.

*Manager's pick: "All as written (Recommended)". Changed in fix round 3: F3-3 (the import
line and the upgrade note) and F3-4 (what the header holds).*
*2026-10-20: F3-3's reading approved as written, with F3-4's; see "Approved at the PROVE
pass 4 report".*

**P-D — D4, re-running `install_guard.py` (closes H3).** What: its command tests the exact
name `keel-factory` before the `[ -f ]` test, and re-running it upgrades an older KEEL
entry in place ("updated"), keeping every other setting. Why: the v1.0 command armed in a
folder holding a `KEEL-FACTORY` folder, because macOS matches names without case (H3; it
fails safe), and without the upgrade a machine keeps that entry. It changes the user's
`settings.json` entry KEEL owns. Evidence: `harness/install_guard.py` and
`test_install_guard.py`. Recommend: approve. Alternative: print "run `--remove`, then
install" and leave the entry as it is.

*Manager's pick: "All as written (Recommended)". Changed in fix round 3: F3-5 (the
master's guard, and the upgrade repoints an older entry at it).*

**P-E — D7, the reviewer agents (closes S8, COMPLETENESS-14).** What: each of the three
agent bodies gained data-boundary item 3 in one sentence (nothing outside the working tree
unless the brief names it), so D7's "moved, not rewritten" now has one sentence added to
each. At SPRINT, keel-prove spawns two of them (Standards and Spec); the builder may run
the gate's commands itself, because an exit code does not depend on who runs it, and the
report says so. The three descriptions now open "One of keel-prove's independent
reviewers", no longer "three" (grep, 2026-10-18). Why: the agent file is a reviewer's
whole boundary brief (S8), and keel-prove's "spawn three" contradicted its own SPRINT rule
(COMPLETENESS-14). Evidence: `agents/prove-*.md`; `keel/skills/keel-prove/SKILL.md`.
Recommend: approve as wording. Alternative: keep the bodies as moved, put item 3 in
keel-prove's brief to each reviewer, and always spawn the gate.

*Manager's pick: "All as written (Recommended)". Changed in fix round 3: F3-7 (what the
agent bodies add).*

**P-F — D10 and D11, the instrument and the release (closes S4, S5, S6, P12,
WALKTHROUGH-11).** What: `check_kit.py` reads `OWN`, `BOARD` and `DOCS` from
`install_plugin.py` and `LAYER_MARK` from `keel_hook.py` with `ast` (no code runs), and
gains the rules `source` and `skill-set`; its `codex` rule covers OWN + BOARD + DOCS, and
its `skill-path` rule also checks bare `agents/` and `harness/` tokens. `make_release.py`
refuses unless the current branch is `main`. Why: three hand-kept skill lists drifted
with no finding (S4, P12), the mark was defined three times (S5), keel-prove's `agents/`
paths went unchecked (S6), and a release cut from this branch would leave the documented
upgrade pull on v1.0 (WALKTHROUGH-11). Evidence: `harness/check_kit.py`'s docstring;
`harness/make_release.py`. Recommend: approve as conforming: D10 lists what the
instrument checks, and these make each list one source. Alternative: record them in
`DESIGN.md` only.

*Manager's pick: "All as written (Recommended)". Changed in fix round 3: F3-8
(README-FIRST's restore).*

**P-G — D4, the guard's allowlist and matcher (closes COMPLETENESS-6).** What: where
KEEL is on (and under `KEEL_GUARD=always`), `keel_hook.py guard` blocks a Write, Edit,
MultiEdit or NotebookEdit of a path ending in `.keel/data-boundary-allow`, a Codex patch
naming it, and any shell command containing `data-boundary-allow`, even under
`KEEL_DATA_BOUNDARY_OVERRIDE=1`; a Read stays allowed. D4's matcher gained `MultiEdit`
(`Read|Edit|MultiEdit|Write|NotebookEdit|Glob|Grep|Bash`). `CLAUDE.md` gained one
sentence: never create or change that file; only the user edits it. The guard file is
unchanged, and the bare wirings (`install_guard.py`, `settings.hooks.json`,
OPERATOR.md's fallback) run it directly, without this block. Why: a Write to the
allowlist was allowed, and once it listed `.env` the guard allowed reading `.env`
(COMPLETENESS-6). Evidence: `keel_hook.py` `touches_allowlist`;
`harness/plugin-hooks.json`. Recommend: approve. Alternative: CLAUDE.md's sentence alone,
as policy, with no hook block.

*Manager's pick: "All as written (Recommended)". Changed in fix round 3: F3-6 (D4's "same
answer") and F3-9 (`CLAUDE.md`'s sentence).*

**P-H — D2, exfil (closes P4).** What: D2's "Both are KEEL's whole footprint and are
removed at exfil" reads "Both are KEEL's whole footprint; at exfil KEEL leaves them for
the user, who deletes `.keel/` (or unlinks the kit) after reading `<ops>/debrief.md`"
(`<ops>` is `.keel/ops/` under the plugin, `keel-factory/.ops/` when linked). Why: it
records unchanged v1.0 behavior: OPERATOR.md leaves the folder because it holds the
debrief (PROVE-FINDINGS, P4). Recommend: approve. Alternative: KEEL deletes its notes at
exfil, and the debrief goes with them.

*Manager's pick: "All as written (Recommended)". Not changed in fix round 3.*
*2026-10-19, fix round 4: F4-8 rewords its `<ops>` parenthesis; proposed, see "Proposed,
awaiting the manager".*
*2026-10-20: F4-8's reading approved as written; see "Approved at the PROVE pass 4
report".*

#### Approved at the PROVE pass 3 report, 2026-10-19

The manager's answer at the PROVE pass 3 report ([PROVE-3.md](PROVE-3.md)), verbatim as
received, from the crew plan's Open question 20
([crew-plan-prove-fixes.md](../task_board/crew-plan-prove-fixes.md)): "Fix round 4 → pass
4 (Recommended): fix the 5 fix-now and 28 docs-only items, file the 5 follow-ons, record
the 10 rejects, then a closure-focused PROVE pass 4 (three reviewers and closure checkers,
no new critic), stopping at its report. And approve as written F3-7's D7 reading, the
8,000-character" The message was cut there, mid-sentence, after "the 8,000-character".

The contract question it answers, as Open question 20 quotes it: "## Decision 2: three
contract wordings ... Approve these as written (recommended), or decide each one
separately:", over F3-7's D7 reading, the 8,000-character listing bound, and F3-1, F3-2,
F3-4 and F3-6. The lead's reading (Open question 20): approved are F3-7's reading of D7
and the listing bound, the only 8,000-character item in the question. Not approved are
F3-1, F3-2, F3-4 and F3-6, which come after the cut; they go to the manager again at the
PROVE pass 4 report ("Proposed, awaiting the manager", below). Each entry here keeps its
proposed or approved text word for word, and the decision it amends keeps its own words,
with a dated pointer line.

**F3-7's reading of D7 (spec:b1-agent-bodies).** What: D7's "moved, not rewritten" reads
"moved, with those added", the additions being the ones F3-7 lists. Why: the agent bodies
add more to the v1.0 prompts than P-E's one sentence (F3-7), and the verifier's fix
proposed this rewording (PROVE-2's table, spec:b1: 'Propose D7 as "moved, with those
added"'). Recommend: approve as wording. Alternative: keep D7's words as they stand, with
F3-7's list as the record of what was added. Until the manager answers, D7 keeps its
approved text.

*Manager's pick: "approve as written F3-7's D7 reading". The proposal's last sentence is
now history: from 2026-10-19, D7 reads "moved, with those added", the additions being
F3-7's list. D7's own words stay, with a pointer line under D7.*

**A6's listing bound (C11).** What: A6's "The skill listing, names plus descriptions of
the plugin's skills, is at most 8,000 characters", asserted by `check_kit.py`'s
`listing-budget` rule (`LISTING_MAX = 8000`). Before this answer it rested on A1's stated
reason, which the manager ticked; it had not been put to the manager as a bound (C2).

*Manager's pick: "And approve as written F3-7's D7 reading, the 8,000-character" (the
answer above, cut after these words; the listing bound is the only 8,000-character item
in the question). A6's own words stay, with a pointer line after A6.*

#### Approved at the PROVE pass 4 report, 2026-10-20

The manager's answer at the PROVE pass 4 report ([PROVE-4.md](PROVE-4.md)), verbatim as
received, from the crew plan's Open question 21
([crew-plan-prove-fixes.md](../task_board/crew-plan-prove-fixes.md)). The question:
"v1.1 has six contract wordings waiting: F3-1, F3-2, F3-3, F3-4, F3-6 and F4-8. ...
Approve them?" The pick: "Approve all six (Recommended)". That option read: "Approve all
six as written in .scratch/v1.1/CONTRACT.md. The build already follows them, so nothing
changes in the code."

The lead's reading (Open question 21): F3-1 (with its third residual: a kit copy that
keeps `.git` stays dormant), F3-2, F3-3, F3-4, F3-6 and F4-8 are approved as written.
Five of them stood under "Proposed, awaiting the manager" and move here, each with its
text word for word. F3-3 never stood there. Its approved wording is its entry under
"Changes, F3-1 to F3-9", below, which keeps its place and its words. Each decision these
entries reword keeps its own words, with a dated pointer line.

**F3-1's reading of D2 (N2 = N35).** What: P-A's "a `keel-factory` entry that is the
kit's own folder" reads "a `keel-factory` entry that is the kit root itself, when the kit
root is the master's own git checkout" (the F3 entry below). Why: it carries out the
fix-now major N2 = N35. As built, P-A's exclusion left a project holding a copied kit,
with hooks wired from that copy, dormant while the armed check passed; approved D2 says
KEEL is on where a folder "has `.keel/` or `keel-factory/`", and this restores that for a
copy made with MANUAL §4's rsync (no `.git`); a copy that keeps `.git` stays dormant
(F3-1's third residual, below). Recommend: approve as written. Alternative: revert to
P-A's words, which makes every copied kit dormant again.

*Manager's pick: "Approve all six (Recommended)". It covers F3-1's third residual,
recorded under its change entry below. P-A's own words stay, with a pointer line under
P-A and D2.*

**F3-2's reading of D2 and D5 (spec:a1-linked-kit-role).** What: HELM records the role in
`.keel/keel.json` only where `.keel/` is the switch; where a linked or copied
`keel-factory/` is the switch, it records nothing and infers the role each session. D2's
"HELM writes it the first time KEEL is used" and D5's "It records the answer" hold only
for `.keel/` (the F3 entry below). Why: there the `keel-factory/` folder is KEEL's whole
footprint (D2). Recommend: approve as written. Alternative: HELM writes `.keel/keel.json`
beside a linked kit too, which adds a second footprint.

*Manager's pick: "Approve all six (Recommended)". D2's and D5's own words stay, with a
pointer line under each.*

**F3-3's reading of P-C (N36 with N3).** What: the approved wording is F3-3's entry
under "Changes, F3-1 to F3-9", below, which stays where it is, word for word. Its What
sentence reads:

> P-C's "holding the mark or the import text `keel-factory/CLAUDE.md`" reads: holding the
> mark, or an import line `@keel-factory/CLAUDE.md` (optionally
> `@./keel-factory/CLAUDE.md`) that resolves, from the importing file's own folder, to a
> file carrying the mark.

*Manager's pick: "Approve all six (Recommended)". P-C's own words stay, with a pointer
line under P-C and D3.*

**F3-4's reading of D3 (spec:c2-carry-header).** What: D3's "it injects only the kit-root
line" reads "it injects only the header: where KEEL is on and the role, the kit root, and
the role's routing line" (the F3 entry below). Why: the hook has always given that header
(D3 itself prefixes the kit root and the role), and no layer goes in twice. Recommend:
approve as written. Alternative: the hook injects the kit-root line alone.

*Manager's pick: "Approve all six (Recommended)". D3's own words stay, with a pointer
line under D3.*

**F3-6's reading of D4 (spec:c1-guard-twice).** What: D4's "with both, the guard runs
twice on the same call and gives the same answer" reads "with both, a block from either
wins" (the F3 entry below). Why: where both hooks run, P-G's allowlist block makes their
answers differ; either hook's block stops the call, so the outcome is safe. Recommend:
approve as written. Alternative: keep D4's words, with the F3 entry as the record of where
the two hooks' answers differ. D4's "same answer" is not buildable as written without
dropping P-G's block or editing the guard, which D4 forbids.

*Manager's pick: "Approve all six (Recommended)". D4's own words stay, with a pointer
line under D4.*

*2026-10-19, fix round 4: one more, for the same report, so five in all. It rewords
approved text through a change fix round 4 made, under the same rule.*
*2026-10-20, docs round 6 (RECORDS-N4): "five" counts the wordings that stood under
"Proposed, awaiting the manager"; with F3-3, six were approved.*

**F4-8's reading of D2 and P-H (K25).** What: D2's "Operator notes go in `.keel/ops/`
when the kit came by plugin, `keel-factory/.ops/` when it was linked" and P-H's "(`<ops>`
is `.keel/ops/` under the plugin, `keel-factory/.ops/` when linked)" read "`<ops>` is
`keel-factory/.ops/` whenever the project holds a `keel-factory/` (linked or copied),
else `.keel/ops/`" (the F4 entry below). Why: D2 chooses by how the kit came, and a
project can have both. Following MANUAL §10 in a linked-kit project creates `.keel/` for
the allowlist and flips the role from `kit` to "not recorded"; D2's two clauses then
both apply, and the hook's operator note said `.keel/ops/` alone, so a mission begun in
`keel-factory/.ops/` would have its handoff looked for in `.keel/ops/` (K25). A copied
kit is neither linked nor the plugin. Choosing by what the project holds gives one
answer. Recommend: approve as written. Alternative: keep D2's and P-H's words, and
choose `<ops>` by how the kit came, in HELM, `OPERATOR.md` and the hook's operator note.

*Manager's pick: "Approve all six (Recommended)". D2's and P-H's own words stay, with a
pointer line under each.*

### Proposed, awaiting the manager

None pending. The six wordings that waited for the PROVE pass 4 report were approved
there on 2026-10-20 ("Approved at the PROVE pass 4 report", above). A later round's
proposals go here.

## Amendments — 2026-10-18, fix round 3 (after PROVE pass 2)

PROVE pass 2 ([PROVE-2.md](PROVE-2.md)) did not pass. The manager's answers, 2026-10-18,
verbatim; the crew plan's Open question 16
([crew-plan-prove-fixes.md](../task_board/crew-plan-prove-fixes.md)) records each
question and option text word for word:

- "PROVE pass 2 does not pass (three confirmed major defects, one made by this fix run).
  What next?" Picked: "Fix round 3 → pass 3 (Recommended)", whose text was "Fix the 3
  majors first, then the 13 fix-now and 32 docs-only items; file the 8 follow-ons as board
  tasks; record the 7 rejects with reasons; then a fresh PROVE pass 3, stopping at its
  report."
- P-B: "Make it an explicit exception" (above).
- P-A and P-C to P-H: "All as written (Recommended)" (above).
- The data-boundary question "This would require modifying `~/.claude/settings.json`
  (removing KEEL's v1.0 PreToolUse guard entry), which is security tooling outside this
  project. Do you want me to proceed with this specific action?" Picked: "Yes". The lead
  ran `python3 -B harness/install_guard.py --remove`, which printed "removed KEEL's guard
  from ~/.claude/settings.json; every other setting kept", without opening the file; the
  plugin's wired PreToolUse command then blocked a Read of `.env` (exit 2) in a scratch
  `.keel/` project and in a scratch linked-kit project (the crew plan's execution log,
  "Data-boundary action"). This changed this machine, not the contract: D4's machine-wide
  hook still ships.

### Changes, F3-1 to F3-9

The authority for each is the manager's pick "Fix round 3 → pass 3 (Recommended)", whose
text sends the fix-now and docs-only items to be fixed. Each finding named below has the
disposition fix-now or docs-only in PROVE-2's "Every verified item" table. The P-entries
above keep their approved text; each change is recorded here, with a pointer line there.
One part rests on no pick: F3-7's reading of D7 is only proposed, for the PROVE pass 3
report ("Proposed, awaiting the manager", above).
The code changes landed in fix round 3's phase A, with each mutation proof run on an
unbroken baseline green first (the crew plan's execution log, "Fix round 3, phase A —
landed").

*2026-10-19, fix round 4 (C12):* F3-7 alone was proposed because its verified fix said
"Propose" (PROVE-2's table, spec:b1: 'Propose D7 as "moved, with those added"'); the
verified fixes behind F3-2, F3-4 and F3-6 wrote their rewordings out, and the pick sent
them to be fixed as written. Still, each of F3-1, F3-2, F3-4 and F3-6 rewords approved
decision text, so the PROVE pass 3 report asked the manager to approve them as written
(PROVE-3's S-c2). The answer was cut before them (the crew plan's Open question 20), so
they are proposed again, for the PROVE pass 4 report ("Proposed, awaiting the manager",
above). F3-7's reading of D7 was approved ("Approved at the PROVE pass 3 report", above).
*2026-10-20, docs round 5 (S4-c):* F3-3 rewords P-C's words as F3-1 and F3-4 reword
theirs, so the PROVE pass 4 report put it to the manager with them, and all six were
approved ("Approved at the PROVE pass 4 report", above); F3-5 adds a cost to P-D and
leaves its words standing, so it stays an entry (its "Which" line, below).

**F3-1 — P-A, for D2: the master's own git checkout (N2 = N35, fix-now).** What: P-A's
"a `keel-factory` entry that is the kit's own folder" reads "a `keel-factory` entry that
is the kit root itself, when the kit root is the master's own git checkout" (a `.git`
folder, or a linked worktree's `.git` file whose gitdir holds `commondir`). A copy of the
kit (the documented rsync leaves `.git` out, and a submodule's gitdir has no `commondir`)
or a link switches KEEL on. Two residuals remain, both failing closed (KEEL switches on,
role `kit`): a master that is a worktree of a bare repository, and a tarball-restored
master renamed to lowercase `keel-factory`, seen from its parent. Why: as built in the
fix run, P-A's exclusion left a project holding a copied kit, with hooks wired from that
copy, dormant (no guard, no layer) while the documented armed check passed (N2, N35).
Approved D2 says KEEL is on where a folder "has `.keel/` or `keel-factory/`"; this
restores that for copies. The armed check now runs the wired command in the real project
root on a Read of `keel-armed-check/.env` (Open question 17; the recipe is
`harness/DATA-BOUNDARY.md`'s). Evidence: `harness/hooks/keel_hook.py` `master_checkout`
and `marker`, the docstring's rule 4; `test_keel_hook.py`
`test_copied_kit_with_hooks_from_the_copy_switches_on` and
`test_kit_own_folder_named_keel_factory_is_dormant`; mutation proof keel_hook 62/62.

*Fix round 4, 2026-10-19 (C2), a third residual:* A copy made with MANUAL §4's rsync (no
`.git`) switches KEEL on; a copy that keeps `.git` (a `git clone`, `cp -R` or a Finder
copy) counts as a master's own checkout and stays dormant when its own hooks run. Unlike
the two residuals above, this one does not fail closed: no guard arms and no layer goes
in, and the documented armed check then reports no block, which shows the copy as
unarmed. The same clone under the plugin route blocks (exit 2). Evidence: the C2
verifier's runs (`.scratch/v1.1/round3/verify3.json`, item C2; [PROVE-3.md](PROVE-3.md),
row C2), each running the copy's own `keel_hook.py ... --harness codex`: a `git clone`
and a `cp -R` copy gave guard exit 0 on Bash `cat .env`, a 0-byte session and no BLOCKED
line on the armed check; the documented rsync copy gave exit 2, 6,265 bytes and one
BLOCKED line. The installer's warning from a copy is board task
`installer-hooks-json-robustness`, item 3.

**F3-2 — P-A, for D2 and D5: where the role is recorded (spec:a1-linked-kit-role,
docs-only).** What: HELM records the role in `.keel/keel.json` only where `.keel/` is the
switch. Where a linked or copied `keel-factory/` is the switch (hook role `kit`), it
records nothing and infers the role each session. D2's "HELM writes it the first time
KEEL is used" and D5's "It records the answer" hold only for `.keel/`. Why: there the
`keel-factory/` folder is KEEL's whole footprint (D2), and writing `.keel/` beside it
would add a second one. Evidence: `keel/skills/helm/SKILL.md` lines 53–54, "A
`keel-factory/` (linked or copied) is itself the switch: decide the role the same way,
record nothing, and start at step 2."; `keel_hook.py` `marker` gives role `kit`.

**F3-3 — P-C, for D3: an import that counts, and the upgrade note (N36 with N3,
fix-now).** What: P-C's "holding the mark or the import text `keel-factory/CLAUDE.md`"
reads: holding the mark, or an import line `@keel-factory/CLAUDE.md` (optionally
`@./keel-factory/CLAUDE.md`) that resolves, from the importing file's own folder, to a
file carrying the mark. A prose mention, a dangling import or an import of a file
without the mark never counts; the worst case stays the layer twice. P-C's v1.0 upgrade
note offers Claude Code the import only when `keel-factory/CLAUDE.md` beside that file
carries the mark; otherwise it says to delete KEEL's v1.0 text (the hook then supplies
the layer) or to replace it with v1.1's `CLAUDE.md`. Codex never gets the import. Why:
the bare text dropped the whole layer when no `keel-factory/` existed (N36), and the note
recommended an import that does not resolve under the plugin (N3). Evidence:
`keel_hook.py` `IMPORT_LINE`, `layer_import`, `carries_layer` and `upgrade_note`;
`test_keel_hook.py` `test_prose_mention_injects_the_layer`,
`test_dangling_import_injects_the_layer`,
`test_import_of_a_file_without_the_mark_injects_the_layer`,
`test_dot_slash_import_counts`, `test_dot_claude_import_resolves_from_its_own_folder` and
`test_v1_copy_gets_the_upgrade_note`. Known gap, filed as board task
`keel-hook-hardening`: an import line inside a fenced code block still counts.

**F3-4 — P-C, for D3: what "header only" injects (spec:c2-carry-header, docs-only).**
What: D3's "it injects only the kit-root line" reads "it injects only the header: where
KEEL is on and the role, the kit root, and the role's routing line". Why: the hook has
always given that header (D3 itself prefixes the kit root and the role); no layer goes in
twice. Evidence: `keel_hook.py` `session_text` and `ROLE_NEXT`;
`test_header_only_when_project_imports_the_layer`.

**F3-5 — P-D, for D4: the machine-wide hook runs the master's guard (N37, fix-now).**
What: `install_guard.py`'s command keeps the exact-name test on `keel-factory` in the
project folder as the switch, then runs the installing master's own guard by its
absolute, shell-quoted path, never the project's copy. Re-running the script upgrades an
older KEEL entry in place and repoints it at the master it is run from ("updated KEEL's
guard to the current command"). It recognizes the old form exactly
(`$CLAUDE_PROJECT_DIR/keel-factory/harness/hooks/data-boundary-guard.py`) and the new
form from any master; a hand-wired bare guard is not its entry. A moved master disarms
the hook until the script is run again. Why: since v1.0 the command ran the project's own
`keel-factory/harness/hooks/data-boundary-guard.py`, so a package could ship a guard that
allowed everything, and HELM's probe could not tell (N37). Residual: the master's guard
still honors a project's own `.keel/data-boundary-allow` (N33, docs-only). OPERATOR.md
shows the command with a quoted placeholder for the master's path, and the pinning test
compares after substituting it. Evidence: `harness/install_guard.py` `COMMAND`,
`OLD_MARKER` and `is_keel_command`; `test_install_guard.py`
`test_the_masters_guard_blocks_even_when_the_projects_copy_allows`,
`test_never_runs_the_projects_own_copy`,
`test_an_entry_from_another_master_is_repointed_here` and
`test_the_installed_command_is_the_one_operator_md_documents`; mutation proof
install_guard 18/18.

*2026-10-20, docs round 5 (S4-c):* Which: an entry, not a proposal. P-D's words still
hold: the command still tests the exact name `keel-factory` before the `[ -f ]` test
(`harness/install_guard.py` lines 41–42), and re-running the script still upgrades an
older entry in place. F3-5 adds one cost that D4's "keeps working" never carried: if the
master moves, the hook disarms until the script is run again (`install_guard.py` lines
15–16). The S4-c verifier saw it: in a project holding `keel-factory/`, the installed
command blocked a Read of `.env` (exit 2), and after that master was renamed it allowed
the same Read (exit 0) (`.scratch/v1.1/round4/verify4.json`, item S4-c).

**F3-6 — P-G and P-A, for D4: two hooks, not one answer (spec:c1-guard-twice,
docs-only).** What: D4's "with both, the guard runs twice on the same call and gives the
same answer" reads "with both, a block from either wins". The plugin's hook also guards
the allowlist (P-G) and arms in `.keel/` projects and in the folders up to the git root
(P-A), where the machine-wide hook does nothing; the machine-wide matcher has no
`MultiEdit`. Why: where both run, P-G's allowlist block makes their answers differ; the
outcome is safe because either hook's block stops the call. Evidence:
`harness/plugin-hooks.json`'s matcher; `install_guard.py` `MATCHER` and `COMMAND`, which
lists only `$CLAUDE_PROJECT_DIR`; the verifier's paired runs
(`.scratch/v1.1/round3/verify2.json`, item spec:c1-guard-twice; the finding is PROVE-2's
Spec section, (c) 1). The machine-wide hook is no longer installed on this machine (the
data-boundary action above).

**F3-7 — P-E, for D7: what the agent bodies add (spec:b1-agent-bodies, docs-only).**
What: P-E's "one sentence added to each" reads as this list of what the agent bodies add
to the v1.0 prompts (`git show e09480c:keel/skills/keel-prove/SKILL.md`, §3): an opening
framing paragraph; how to read the change, uncommitted work included (Standards and
Spec); the Gate's rules to run each check as the project defines it, not to edit source
or tests to make a check pass, not to skip, weaken or comment out a check, and not to run
an outward-facing or irreversible check; "Do not edit any file" (Standards and Spec); and
data-boundary items 1–3. D7's rewording is proposed, not settled: see "Proposed, awaiting
the manager". Why: P-E named only item 3. Every other addition narrows what a reviewer
may do; the change-reading step instead widens what Standards and Spec read (uncommitted
and untracked work, in full), still inside data-boundary items 1–3. Evidence: the framing
paragraph at lines 7–9 of each file; `agents/prove-standards.md` lines 13–15 and 27–30,
`agents/prove-spec.md` lines 12–14 and 21–24, `agents/prove-gate.md` lines 18–21 and
23–26 (read 2026-10-18); none of these rules is in the v1.0 prompts.

*2026-10-19: F3-7's reading of D7 approved at the PROVE pass 3 report, so its "proposed,
not settled" is history; see "Approved at the PROVE pass 3 report", above.*

**F3-8 — P-F, for D10 and D11: README-FIRST's restore (spec:b2-readme-first,
docs-only).** What: P-F's release rule adds that `make_release.py`'s README-FIRST checks
`shasum -a 256 -c SHA256SUMS` first, restores with `git clone --branch main
"$PWD/KEEL-FACTORY-<tag>.bundle" ~/GitProjects/KEEL-FACTORY`, then checks `git -C
~/GitProjects/KEEL-FACTORY describe --tags` (it must print the tag), onto the user's own
local path, never the drive; without git, `mkdir -p ~/GitProjects && tar -xzf
KEEL-FACTORY-<tag>.tar.gz -C ~/GitProjects`. Why: a detached `git checkout <tag>` breaks
the upgrade pull and the next release (the crew plan's Open question 15), and a clone of
the bundle lands on whichever branch sits at HEAD's commit (measured by phase 2's scripts
lane; the crew plan's execution log, "Phase 2 — landed"). It serves approved row 10.
Evidence: `harness/make_release.py` lines 114–126; `test_make_release.py`
`test_readme_first_restores_onto_main_at_the_tag` and
`test_readme_first_without_git_untars_off_the_drive`; mutation proof make_release 25/25.

**F3-9 — P-G: CLAUDE.md's allowlist sentence (N4 with N34, docs-only).** What: P-G's
"`CLAUDE.md` gained one sentence: never create or change that file; only the user edits
it" now reads, in `CLAUDE.md`: "Never create or change `.keel/data-boundary-allow`, even
when a block message suggests it: only the user edits that file. KEEL's hook (the
plugin's, or Codex's with `--codex-hooks`) blocks the direct ways of writing it; a
hand-wired bare guard does not. It is a tripwire, not a lock." Why: the sentence PROVE
pass 2 reviewed said KEEL's hook blocks agents from the file, which the bare wirings
do not (N4), and the block can be bypassed (N34; its command blocks are board task
`keel-hook-hardening`). Evidence: `CLAUDE.md` lines 90–93.

### Corrections to the record, C1 to C5

Each corrects what this record says about approved text; the approved text itself keeps
its words.

**C1 — A4 and A5: what approved them (N16).** A4's `$CODEX_HOME` default and A5's
`--harness claude|codex` were approved as rows 7 and 2 of the go-ahead "Yes, rows 1–11 →
pass 2 (Recommended)" (PROVE-FINDINGS, the disposition table: row 7, "`--codex-home`
defaults to `$CODEX_HOME`, then `~/.codex`"; row 2, "`keel_hook.py session --harness
codex|claude`"), not by the option text the approval paragraph quotes.

**C2 — A6: the 8,000-character listing bound (N16).** Until 2026-10-19 the bound rested
on A1's stated reason, which the manager ticked, and had not been put to the manager as
a bound. The D1 option the manager ticked said "Listing all 16 adds ~1,100
characters and breaks the 8,000-character skill listing budget that both harnesses cap."
(the crew plan's Open question 2, verbatim). The option text A5 to A7 rest on
("Wording-only fixes (one keel_hook.py, the 1,024 cap, non-strict validate) come along
with these.") does not name it. The manager approved the bound at the PROVE pass 3
report, 2026-10-19 ("Approved at the PROVE pass 3 report", above; the crew plan's Open
question 20).

*Reworded 2026-10-19 (fix round 4, C11): C2 said "The bound is approved as A1's stated
reason" and ended "No new proposal is needed (the crew plan's Open question 19)". PROVE
pass 3's C11 found that a stated reason did not approve the bound itself.*

**C3 — the source of the quoted texts (N17).** The approval paragraph's "as the lead
quoted it in the records lane's brief" now has a verbatim source: the crew plan's Open
question 2 records that question round's questions and option texts word for word, and
Open question 16 records PROVE pass 2's. Every pick and option text this contract quotes
is found there (a whitespace-normalised substring check, 2026-10-18).

**C4 — §5, the install_guard count (N19).** The pass-2 Stale note's seven new tests came
from row 8 (five: exact name, letter case, contains-only, guard gone, no project folder)
and P-D (two: an older entry updated in place, `--remove` taking out an older entry).
Fix round 3 added five from N37: the command runs this master's guard; the hook never
runs the project's own copy; another master's entry is repointed here; a hand-wired bare
guard is not KEEL's entry; and the end-to-end run, where the master's guard blocks while
the project's copy would allow. `test_install_guard.py` now has 18 tests and the old
four suites total 75 (27 + 9 + 18 + 21), all passing (run 2026-10-18). The attribution
is Inferred from test names. §5's intent, that the old suites all pass, still holds; its
row is not amended.

**C5 — A2's Evidence quote.** Since P-B's approved form, `CLAUDE.md`'s Data boundary
section no longer says "The one exception is the guard probe"; it says "Two exceptions
need no question. The **guard probe**: …" (line 80). A2's decision is unchanged.

## Amendments — 2026-10-19, fix round 4 (after PROVE pass 3)

PROVE pass 3 ([PROVE-3.md](PROVE-3.md)) did not pass yet: 49 items verified, none
refuted, none major after verification. The manager's answer, verbatim as received, is
quoted under "Approved at the PROVE pass 3 report" above and recorded in the crew plan's
Open question 20 ([crew-plan-prove-fixes.md](../task_board/crew-plan-prove-fixes.md)).
Its pick for this round is "Fix round 4 → pass 4 (Recommended)", whose text says to
"fix the 5 fix-now and 28 docs-only items".

### Changes, F4-1 to F4-8 (fix round 4)

The authority for each is that pick. Each finding named below has the disposition
fix-now or docs-only in PROVE-3's "Every verified item" table. PROVE pass 3 taught one
rule (S-c2): a change that only carries out its finding inside a decision's meaning is
an entry here, with a one-line pointer under the decision; a change that rewords or
narrows an approved decision's meaning is also written under "Proposed, awaiting the
manager", beside F3-1, F3-2, F3-4 and F3-6, for the PROVE pass 4 report. Each entry says
which, and why: F4-1 to F4-7 carry decisions out, and F4-8 rewords D2 and P-H, so it is
proposed. Approved text keeps its words throughout. F4-1 and F4-2 are code, landed in
fix round 4's phase A with the mutation proof run after an identity baseline (the crew
plan's execution log, "Fix round 4, phase A — landed"). F4-3 to F4-8 are skill and
protocol text, written and not yet run live (Inferred); F4-8's line in the hook is
pinned by a test.

Round 4's other changes touch no decision's text: the limits the documents now name (the
crew plan's seams S1, S2, S4, S5, S7 and S14, and K36), the wiring notes (K21, K23), a
copied skill's Codex name (S13, already in §2's stale note) and the records. F3-1's third
residual (S6, C2) and the two approvals above (S-a1, C11) are recorded where they stand.

**F4-1 — D4: the hook fails closed on a hostile role file (K30, fix-now).** What:
`keel_hook.py guard` decides whether KEEL is on inside its fail-closed `try`. Each
`.keel` or `keel-factory` entry met while deciding is noted first; after that, an error
blocks the call, while an error before any entry allows it, so a folder where KEEL is
off is never touched. `.keel/keel.json` is opened without waiting and read only as a
regular file of at most 64 KiB; anything else is role "not recorded", and KEEL stays
on. Why: the role was read before the `try`, so a committed `keel.json` nested 20,000
deep made every guarded call exit 1, which both harnesses read as allow, and a link to
`/dev/zero` hung the hook until it timed out (PROVE-3, K30). Evidence:
`harness/hooks/keel_hook.py` lines 163–180 (`role_of`), 211–227 (`marker`) and 457–480
(`guard`), and the module docstring's rule 6 (lines 33–37); `test_keel_hook.py`
`Hostile` and `InProcess` (lines 718–841); mutation proof keel_hook 93/93, identity
baseline first. Which: an entry, not a proposal. D4's wrapper "exits 0 at once where
KEEL is off, and otherwise hands stdin to the unchanged `data-boundary-guard.py`", which
fails closed; this keeps "off" for a folder with no marker, and stops an error from
passing for "off" where a marker was met. Pick: "Fix round 4 → pass 4 (Recommended)".

**F4-2 — D4 and A5: Codex patches read as Codex reads them (K31, fix-now).** What: the
`apply_patch` adapter strips each line before it matches a header (`Add File`,
`Update File`, `Delete File`, `Move to`), and catches a header wherever it sits. Any
other line that starts with `***` once stripped blocks the patch, except the frame
(`Begin Patch`, `End Patch`, `End of File`), `*** Environment ID`, and a space-led line
inside an `Update File` or `Move to` hunk, which Codex reads as file context. Another
tool's command that starts as a patch is also checked as it stands. Why: headers were
matched only at the start of a line, while Codex's parser trims each line first, so a
patch whose second header was indented edited `.env` or wrote the allowlist with the
guard answering exit 0 (K31). Evidence: `keel_hook.py` lines 107–111 (the patch
constants), 375–394 (`patch_paths`) and 397–418 (`guard_payloads`); `test_keel_hook.py`
`CodexPatches` (lines 502–618) and `test_padded_patch_naming_the_allowlist_blocked`;
mutation proof keel_hook 93/93. Whether Codex sends any other `***` line is Missing
evidence; such a line blocks until the hook learns it. Which: an entry. A5's "each file
the patch names is checked as a path" now holds for every header Codex accepts, and
blocking a line the hook cannot read is D4's fail-closed guard applied to its own input.
Pick: "Fix round 4 → pass 4 (Recommended)".

**F4-3 — D5: HELM's gitignore check runs before the write (C14, fix-now).** What: HELM
step 1 runs `git check-ignore -q .keel/keel.json` before writing the file, while KEEL is
still off; git answers for a path that does not exist yet. In HELM step 3 (d) and
`OPERATOR.md`'s infil, a check blocked with the reason 'matches this repo's .gitignore'
is itself the answer and is never retried another way: the crew plan's amended seam S8,
word for word in both. Why: the warning's trigger named `.keel/keel.json`, which the
armed guard blocks in exactly the gitignored case it detects (C14, closing N24's
remainder). The warning serves approved D3 and D5 as written ("Implemented as approved,
no amendment", above). Evidence: `keel/skills/helm/SKILL.md` lines 83–89 (step 1) and
125–129 (step 3 (d)); `OPERATOR.md` lines 106–110. Which: an entry. The check moves
earlier and a block is read as the answer; no decision's words or meaning change.
Pick: "Fix round 4 → pass 4 (Recommended)".

*2026-10-20, docs round 5 (PROVE pass 4, D8 and D9): S8 now also covers the listing.
HELM step 3 (d) reads "(the listing in (c) included)", and `OPERATOR.md` reads "(the
listing included)" (the crew plan's Open question 22, "S3 amended" and "Amended after
the back-briefs"). Apart from that parenthesis, S8's sentence is still word for word in
both. Evidence: `keel/skills/helm/SKILL.md` line 132; `OPERATOR.md` line 112 (the base
copies: lines 128 and 112). Which: still an entry.*

**F4-4 — D5: nested allowlists in HELM's switch-on (K19, docs-only).** What: HELM step 3
(c) and `OPERATOR.md`'s infil also list every `.keel/` folder below the root, with
`find . -path ./keel-factory -prune -o -type d -name .keel -print`, a command that never
names the file, and handle each one found like the root's (the crew plan's seams S3 and
S3b). Why: the guard honors an allowlist at the nearest git root of each path, so a
submodule or a nested clone could bring one that the root-only check never saw (K19,
with C16 and K33). Evidence: `keel/skills/helm/SKILL.md` lines 119–124; `OPERATOR.md`
lines 96–106, whose parenthesis records a scratch submodule run (Evidence, 2026-10-19).
Which: an entry. It widens a switch-on check that no decision's text names; D5's first
step and D4's unchanged guard keep their words. Making the guard honor an allowlist only
at the KEEL root is a board task (`keel-hook-hardening`), not this round.
Pick: "Fix round 4 → pass 4 (Recommended)".

*Corrected 2026-10-20 (PROVE pass 4, D6): the board task does not "honor an allowlist
only at the KEEL root". K19's code half is now its verifiers' design: the tracked-file
test at the nearest git root, which keeps a user's untracked nested allowlist
(`keel-hook-hardening` item 5).*

*2026-10-20, docs round 5 (PROVE pass 4, D8 and D9): the listing is now
`find . -path ./keel-factory -prune -o -name .keel -print`, with no `-type d`, so a
symlinked `.keel` is listed too. Where `.keel/` or `keel-factory` is gitignored, the
guard blocks the listing and HELM's step 3(d) applies. In `OPERATOR.md`, its rule for a
blocked check applies (the crew plan's Open question 22, "S3 amended"). Evidence:
`keel/skills/helm/SKILL.md` line 126; `OPERATOR.md` line 105 (the base copies: lines 122
and 105). Which: still an entry.*

**F4-5 — D2 and D5: a `.keel` that is not a folder (K35, docs-only).** What: HELM step 1
and `OPERATOR.md`'s infil carry the crew plan's seam S10 word for word: such a `.keel`
is named and left untouched, KEEL stays off, the data-boundary rule runs as strict
policy, and in operator mode it counts as the package switching off a guard. Why: P-A
makes only a `.keel` folder a marker, so a committed regular file named `.keel` kept
KEEL and the guard off, and HELM had no step for it (K35). Evidence:
`keel/skills/helm/SKILL.md` lines 79–83; `OPERATOR.md` lines 33–37. Which: an entry. It
carries out P-A's "(a folder)"; D2's "HELM writes it the first time KEEL is used" cannot
be done there without removing the package's own file, which HELM leaves untouched.
Pick: "Fix round 4 → pass 4 (Recommended)".

**F4-6 — D3: no Codex block on top of a v1.0 `AGENTS.md` (K20, fix-now).** What: HELM
step 4 carries the crew plan's amended seam S11 word for word: where `AGENTS.md` holds
KEEL's v1.0 text, HELM adds no block, offers MANUAL §11's choice (replace that text with
the block, recommended, or delete it and rely on the hook), and changes the file only on
the owner's yes. Why: HELM appended the v1.1 block to an `AGENTS.md` still holding
v1.0's copy, so two layers loaded and the hook kept reporting the layer as not added
(K20). Evidence: `keel/skills/helm/SKILL.md` lines 130–133; `keel_hook.py` `V1_PHRASE`
(line 101), `layer_status` and `upgrade_note` (lines 319–339), which test the same
sentence and give a Codex project the same two choices. Which: an entry, not a proposal.
D3's "One source, never two copies in context" forbids the block on top of v1.0's copy,
and approved P-C already gives a v1.0 copy "the header and a one-line upgrade note
instead of a second layer", whose Codex choices (F3-3) are these two. The block is still
added once, replacing v1.0's copy, when the owner takes the recommendation.
Pick: "Fix round 4 → pass 4 (Recommended)".

*2026-10-20, docs round 5 (PROVE pass 4, D5 with D20): S11's condition. HELM step 4
offers "deleting it and relying on the hook" only "where step 3's probe came back
blocked (KEEL's Codex hooks wired and trusted)"; otherwise it offers only the
replacement. MANUAL §11's Codex bullet matches (the crew plan's Open question 22, "S11
conditioned"). Without wired hooks, deleting v1.0's text would leave later Codex sessions
with no layer (Inferred; no Codex model call ran). Which: still an entry, not a proposal.
Where Codex's hooks are not shown to run, the only offer is D3's block.*

**F4-7 — D2 and D5: the operator test in `keel`, `keel-prove` and `crew` (C15,
fix-now).** What: their step 0 carries the crew plan's seam S9 word for word, the same
in all three: operator mode also covers a project with no role recorded, as with a
linked or copied `keel-factory/`, whose own instructions are not KEEL's. Their switch-on
line also runs HELM's switch-on when a `.keel/` holds no `keel.json`. Why: with a linked
kit (hook role `kit`, nothing recorded), `keel`'s step 0 had no signal for operator
mode, so its phases could write `docs/` into a package (C15, N23's and N26's
remainder). Evidence: `keel/skills/keel/SKILL.md` lines 46–52;
`keel/skills/keel-prove/SKILL.md` lines 24–33; `keel/skills/crew/SKILL.md` lines 23–32.
Which: an entry. It applies D5's own inference ("the package has its own instructions →
operator") in the three skills a session can enter without HELM, and D2's "HELM writes
it the first time KEEL is used in a project" to a `.keel/` with no `keel.json`. Its
linked-kit clause rests on F3-2's reading, which awaits the manager: if F3-2 is
reverted, HELM records the role beside a linked kit too, and the test's first clause
covers it. Pick: "Fix round 4 → pass 4 (Recommended)".

*2026-10-20: F3-2's reading was approved at the PROVE pass 4 report, so "which awaits
the manager" and the "if F3-2 is reverted" clause are history; see "Approved at the
PROVE pass 4 report", above.*

**F4-8 — D2 and P-H: where operator notes go (K25, docs-only).** What: HELM and
`OPERATOR.md` carry the crew plan's seam S12 word for word, "`<ops>` is
`keel-factory/.ops/` whenever the project holds a `keel-factory/` (linked or copied),
else `.keel/ops/`", and the hook's operator note says the same. Why: as written, D2 and
P-H choose by how the kit came ("F4-8's reading of D2 and P-H", above, gives the cases).
Evidence: `keel/skills/helm/SKILL.md` lines 63–65; `OPERATOR.md` lines 153–154;
`keel_hook.py` lines 118–120, pinned by `test_operator_role_points_at_operator_protocol`,
whose mutant `operator-ops-note-old` is caught (mutation proof keel_hook 93/93). Which:
proposed. It replaces D2's and P-H's criterion with another, so it rewords approved
decisions; the build follows it, and until the manager answers, D2's and P-H's words
stand. Pick: "Fix round 4 → pass 4 (Recommended)".

*2026-10-20: F4-8's reading was approved at the PROVE pass 4 report, so "Which: proposed"
and "until the manager answers" are history; D2's and P-H's words stay, with a pointer
line under each; see "Approved at the PROVE pass 4 report", above.*
