# Templates

The artifact set. Copy into a new project's `docs/`, then fill in.

**Fixed artifacts, composable process:** the shape of this directory does not vary
between projects. Which skills you run to fill it does.

## The manifest

| Artifact | Phase | SPRINT | STANDARD | PLATFORM |
|---|---|---|---|---|
| `RECON.md` | pre-BRIEF (existing systems only) | if inherited | if existing | if existing |
| `BRIEF.md` | 1 | short form | yes | yes |
| `CONTRACT.md` | 2 | no | yes | yes |
| `ACCEPTANCE.md` | 2 | few lines | yes | yes |
| `schemas/` | 2 | types only | yes | yes |
| `TRACEABILITY.md` | 2, updated at 5 | no | **yes** | **yes** |
| `COST_MODEL.md` | 2, measured at 5 | if metered | yes | yes + CI |
| `DESIGN.md` | 3 | least-confident only | yes | yes |
| `STATE.md` | 4 | yes | yes | yes |
| `CONTEXT.md` | ongoing | no | yes | yes |
| `DECISIONS.md` | ongoing | yes | yes | yes |
| `AI_WORKFLOW.md` | ongoing | no | yes | yes |
| `CHANGELOG.md` | ongoing | no | yes | yes |
| `AUDIT.md` | on resume | no | no | yes |
| `DEMO.md` | 5 | no | no | yes |
| `ops/DEPLOYMENT.md` | ops | no | no | yes |
| `ops/RUNBOOK.md` | ops | no | no | yes |

`STATE.md` is the **state file**: it carries phase approvals, and it is the first
thing a resuming session reads. Slice-level work itself is tracked on the task board
(`.scratch/task_board/`, via the skills in `keel-factory/keel/skills-board/`), not in
`docs/` — see `keel/framework/TASK-BOARD-CROSSREF.md`. `SLICES.md` is kept in this
directory only as a superseded pointer, for anyone who still has the old name
memorized.

## Two rules about these files

**Placeholders are dangerous, not neutral.** A permissive schema, a gate citing a
command that does not exist, or a traceability row left blank all look like a contract
while guaranteeing nothing. Fill them in or delete them; never ship them as-is.

**These outrank prose.** Where `schemas/` and `CONTRACT.md` disagree, the schema wins.
Where `ACCEPTANCE.md` and anyone's opinion disagree, the gate wins.
