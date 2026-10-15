# RECON — the orientation gate

**Status: active discipline, not a numbered phase.** KEEL's five phases
(BRIEF→CONTRACT→DESIGN→SLICE→PROVE) are unchanged. RECON runs *before* BRIEF when the
work targets an existing system, and feeds BRIEF a grounded starting point. It is placed
the way the task board and LOOPS were placed — added around the five phases, never
renumbering them.

**The question it answers:** *What is already here, and what conventions does it keep?* —
asked before proposing any change, so that change extends the system instead of fighting
it.

This is the factory's answer to "take on any project and learn the best practices of the
infrastructure in place." You cannot improve a system competently until you have read its
house style off its own code, and you cannot do that honestly without separating what you
observed from what you assumed.

---

## When RECON runs

| Situation | RECON? |
|---|---|
| Greenfield — nothing exists yet | **No.** Go straight to BRIEF. |
| Existing system you know well, small change | **No**, or a half-page. The shape is already known. |
| Existing system, unfamiliar, or inherited | **Yes.** Full recon before BRIEF. |
| A claim that something is "basically done" | RECON *or* `audit` — see the gradient in `../../ARCHITECTURE.md` §5. Audit if there is a doneness claim to verify; recon if you are orienting to improve. Often recon first, audit later. |
| The system (or part of it) is an opaque binary / runtime / capture | **Yes**, and recon reaches for PERCEPTION (REA, `../capabilities/reverse-engineering/`) for the opaque parts. |

HELM (`../skills/helm/SKILL.md`) is what decides this at the front door. RECON is where it
routes an existing-but-unfamiliar system.

## How RECON runs

Fill in `templates/RECON.md`. The order matters — each section grounds the next.

1. **State authorization first.** Recon reads a system. If any part is a binary, a live
   service, or anything you do not own, the data-boundary rule (`../../CLAUDE.md` →
   "Data boundary") applies before you touch it. Name what you are authorized to examine.
2. **Establish what the system is** — by running its build/test/run commands where
   possible, not by trusting a README that may be stale. Label every claim Evidence /
   Inferred / Missing evidence.
3. **Read the house style off the actual code and history.** This is the heart of it.
   Naming, layout, error handling, test shape, commit conventions, what the codebase
   repeatedly chooses and repeatedly avoids. Cite real files. The output is a description
   of *this system's* best practices, not a lecture on best practices in general.
4. **Map the parts and seams.** For opaque regions, use PERCEPTION and keep its
   observed/inferred/unknown labels intact. Mark what you could not see as Missing
   evidence rather than guessing.
5. **Read health and risk honestly.** Where it is fragile, undocumented, surprising;
   which green tests you do not trust; which unknowns a change would depend on.
6. **Bridge to a backlog.** Turn the assessment into a prioritized list of candidate
   improvements, each respecting the conventions from step 3, each destined to become a
   board task if the user agrees. This is the "means toward improving it" — and it is a
   proposal, not a license to start. Present it as ranked options with your recommended
   first pick, so the user picks from it; never hand them an open "what would you like
   to improve?" (`DOCTRINE.md` §2).

## What RECON produces, and where it goes

- `docs/RECON.md` — the map, committed to the repo like any other KEEL artifact.
- Into BRIEF: the chosen direction plus the house-style constraints and unknowns BRIEF's
  grilling must carry. BRIEF does not re-derive what recon established.
- Into the task board: once the user picks improvements to pursue, each becomes a task
  (`to-task`) carrying its house-style constraints, so execution respects them.

## The discipline that keeps RECON honest

- **Describe before you prescribe.** Sections 1–4 of the template are pure description.
  No improvement is proposed until §5, after the system has been understood on its own
  terms. An agent that starts proposing changes in §1 has not done recon; it has done
  opinion.
- **The house style outranks your preferences.** If the system consistently does
  something you would not, that is a convention to respect, not a bug to fix — unless the
  evidence that it causes harm is explicit. Recon finds the system's standards; it does
  not import yours. (This is the same posture `keel-prove`'s Standards axis already takes:
  a documented repo standard always overrides the baseline.)
- **Opaque is not unknowable, but unseen is not seen.** Where source is absent, PERCEPTION
  can often still answer the question — but a perceived fact is labeled as what it is, and
  static analysis never claims to have observed runtime behavior.
- **Recon ends in a proposal, not a plan.** It hands BRIEF a grounded direction. It does
  not authorize building. The user chooses what, from the backlog, is worth a brief.

## Relationship to the other "understand existing state" tools

Full gradient in `../../ARCHITECTURE.md` §5. In short: RECON is the broadest and
earliest — first contact with a whole system. `diataxis-audit` is narrower (docs only),
`task-board-triage` narrower still (board vs. repo), and KEEL `audit` is a different
thing entirely (adversarial verification of a doneness claim). REA is the sense that any
of them reach for when the target is opaque. Reach for the broadest that fits, and do not
run a narrow health check when the real need is whole-system orientation.
