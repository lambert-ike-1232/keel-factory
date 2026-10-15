# KEEL cross-referenced against the task board skills

**Source:** *Skills*, Miguel Hernandez, MIT licensed. 16 skills for Claude Code and
Codex, covering three families: a file-based task board, Diataxis documentation
maintenance, and a daily workflow (commit, handoff/resume-handoff, spike,
post-creation-audit). Installed in full at `keel/skills-board/` (both `claude/` and
`codex/` variants — the bundle ships identical skill bodies per runtime, differing
only in frontmatter and sidecar metadata, so both were kept rather than flattened to
one).

Cited, not absorbed, except where stated below as a deliberate replacement.

---

## 1. Why this one gets a cross-reference, not just a copy

Every other addition to this factory (ECC, McKnight) sits on a different clock from
KEEL and slots in without conflict. This one doesn't. Two of its pieces do the same
job, at the same clock, as something KEEL already has:

- The task board and `docs/SLICES.md` both exist to track slice-level work in
  progress.
- `task-interview` and BRIEF's own Interviewing section both exist to grill an
  unscoped idea into recorded decisions.

Running both unreconciled would mean two systems of record for the same thing,
which is exactly the kind of untraceable drift Rule 3 exists to prevent. So this
had to be decided, not merely adopted. Both decisions below were made explicitly,
not inferred.

## 2. Decision: the task board replaces `docs/SLICES.md`

**Rationale.** The board is the more mature mechanism on every axis that matters:
a real status/gate state model (`draft`/`scoped`/`gate`/`blocked-by`/`superseded`)
instead of a flat checklist, actual standard-library-only validator and
index-generator scripts (`validate_board.py`, `generate_index.py`) instead of
prose convention, and native support for orchestrating several non-interfering
tasks together (`orchestrate-implementation`) — something SLICES.md never
attempted.

**What changes:**
- SLICE phase now produces board tasks under `.scratch/task_board/` (via
  `task-board-init`, `to-task`) instead of a `docs/SLICES.md` checklist.
- Running the work: one task under `focused-implementation`; several
  non-interfering tasks together under `orchestrate-implementation`.
- Reconciling drift: `task-board-triage`, instead of a human eyeballing a stale
  checklist.
- `keel/templates/SLICES.md` is retired, not deleted — see its own header. The
  board skills' own guardrail says it best: *do not delete a superseded document,
  mark it superseded and let the record stand.*

**What this fixes in `LOOPS.md`.** The Operational Loop draft named **State** as a
required component and said nothing built it. The task board is a concrete,
working implementation of exactly that: state that persists across sessions,
lives in the repo, and survives losing a session — which is the literal design
goal stated in the board's own README.

**What this does NOT fix.** A board task's `status: scoped` / `gate: none` is
still the *same agent* labeling its own work ready. That is not the independent
done-checker LOOPS.md requires. `keel-prove`'s fresh-context three-axis review
remains the thing that actually says "done" — the board gives you resumable,
inspectable state to run that review *against*; it does not replace the review.

## 3. Decision: `task-interview` replaces BRIEF's Interviewing section

**Rationale.** Convergent design, independently arrived at: BRIEF's Interviewing
section already says *"finding facts is your job; making decisions is the user's."*
`task-interview`'s description states the same split more operationally —
*"exploring the codebase for anything the code can answer and asking the user only
what the code cannot"* — and ships the actual mechanics (what counts as a resolved
vs. open question, how an answer gets recorded) that BRIEF's one paragraph left
implicit.

**What changes:** `keel/skills/keel/SKILL.md`'s Interviewing section now delegates
to `task-interview` rather than restating its own version. BRIEF still produces
`docs/BRIEF.md` with `[GUESS: ...]` tags resolved — only the grilling mechanism
underneath changed, not what BRIEF is for or what it produces.

**Amended 2026-10-14 — how questions reach the user.** That delegation quietly dropped a
rule. BRIEF's numbered round attached a recommended answer to every question;
`task-interview` never required one, so the rule survived only in the fallback path. It
is restored as a KEEL layer rather than an edit to the vendored skill (the reasoning is
in §5). The standing rule in `CLAUDE.md` and the `keel` skill's Interviewing section
require every question put to the user to carry two or three options and a recommended
pick, and the frontier — every question whose prerequisites are settled — is asked
together. `task-interview`'s warning against batching every question at once is about
dependency order, which the frontier already respects, so the two now agree.

## 4. Adopted without a decision needed — no conflict, additive

| Skill | Role |
|---|---|
| `handoff` / `resume-handoff` | Fills a real, previously-named-but-unbuilt gap: Rule 4's context escape-hatch ladder (*"continue → clear → handoff → sub-agent → compact"*) names "handoff" as a step and never defined one until now. `resume-handoff`'s re-verification-before-acting is the same discipline this factory's own `CLAUDE.md` "On session start" section asks for, more fully worked out. |
| `to-follow-on` | Splits work off an in-flight task — the board-native version of a descope, feeding `DECISIONS.md`/`TRACEABILITY.md` the same way a declared descope already does. |
| `post-creation-audit` | A lighter sibling to `keel-prove`, not a replacement — a hygiene pass (tests, docs, cleanup) rather than an adversarial three-axis review. Reach for `keel-prove` when the question is "is this actually done"; reach for this when the question is "did I leave the place tidy." |
| `commit` | Clean, revertible, conventionally-typed commits. Nothing in KEEL did this before. Invocation-only (`/commit`), deliberately never fires on its own. |
| `spike` | Formalizes what `keel/skills/keel/SKILL.md`'s "Other entry points" already gestured at in one paragraph ("a design question you cannot settle on paper — prototype it, throwaway, no tests or abstractions"). Same idea, fully built out with scratch-space discipline and a stated promote-or-discard decision. |
| `diataxis-manage-docs` + 3 phase skills | Orthogonal — documentation maintenance over time, categorized by the Diataxis framework (tutorial/how-to/reference/explanation). Doesn't compete with any KEEL phase; adopted as a parallel discipline for projects that reach the point of needing one. |

## 5. Decision: CREW wraps `orchestrate-implementation` instead of extending it

**Rationale.** Team coordination needed somewhere to live, and the obvious home was
`orchestrate-implementation`, which already keeps interfering streams apart. But the
bundle's own README says it is generated from a separate authoring repository, and that
"edits made directly to a bundle here would be overwritten by the next publish." Its
claude/ and codex/ copies are also byte-identical, so every edit would have to be made
twice.

**What changes:** team coordination lives in a KEEL-owned layer — `CREW.md` and
`keel/skills/crew/` — that starts from this skill's set and streams and adds owners,
briefs, and landing. Ownership goes in the plan task's `## Lanes` table, not a new
frontmatter field: the shared schema is the bundle's to change, and the validator
rejects unknown keys today. The vendored skills stay untouched, so a re-sync from
upstream stays clean.

## 6. Provenance

Copied in full on 2026-10-14, cross-referenced the same day. Decisions on §2, §3, and
§5 were made explicitly by the framework's owner, not inferred by whoever was doing the
copying — recorded here so the reasoning survives independent of who reads this next.
