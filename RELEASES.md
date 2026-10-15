# Releases

One section per release, newest first. A release is cut with `harness/make_release.py`,
which refuses to run without a section here for the version in `VERSION`. How releases
travel between machines is in section 11 of `MANUAL.md`.

Each section says what the release contains and, separately, how much of it is proven:
Evidence (a check was run and passed), Inferred (reasoned, not run), or Missing evidence.

---

## v1.0.0 — 2026-10-15

The first versioned release. It's meant to be carried to another machine and used on
real projects from there.

### What it contains

- **KEEL:** the five phases, three tiers, and six rules, plus RECON, the doctrine, the
  grounding rule (`CAPABILITIES.md`), LOOPS, and CREW (several agents on one project).
- **HELM,** the router every session starts with, and **operator mode**
  (`OPERATOR.md`): the drop-in protocol for someone else's package.
- **The skills:** `helm`, `keel`, `keel-prove`, `crew`, Miguel Hernandez's 16 board and
  workflow skills, and the two senses (`deep-research`, `reverse-engineering`).
- **The harness:**
  - the data-boundary guard, in Python, and self-disarming when wired machine-wide;
  - three ECC hooks, which need Node;
  - `link_kit.py`, which links the master into projects instead of copying it;
  - `install_guard.py`, which sets the guard up on a machine;
  - `make_release.py`, which cuts releases.
- **Documents:** `MANUAL.md`, written to be enough on its own, plus `START-PROMPTS.md`,
  `QUICKSTART.md`, `ARCHITECTURE.md`, and the framework documents under
  `keel/framework/`.

### Proven — Evidence

The self-tests below are run again from a fresh clone of this release by
`make_release.py`.

| What | How |
| --- | --- |
| Data-boundary guard | 27-test self-test. Fifteen deliberately broken copies each failed it. It blocked secrets and allowed real work against a real project. |
| `link_kit.py` | 9-test self-test, including the guard working through links in a git repo. A round trip with the real master left it unchanged. |
| `install_guard.py` | 6-test self-test, against temporary settings files. |
| CREW's lane checker | 21-test self-test, including a real git diff. |
| Task-board validator | Proven to pass a clean board and fail a broken one. |
| Operator mode | Rehearsed on a throwaway package, then a read-only test drive on a real project. The project's own 1151 tests ran with its real database untouched, and no tracked file changed. |

### Written, not yet proven in use — Inferred

- CREW as a practice: no real multi-agent run yet. It stays Draft v0.1 until one.
- The suggest-don't-ask-blind posture: it is wording; no real interview has followed it
  yet.
- The guard arming itself inside a live session started in a package: rehearsed piece by
  piece, never yet observed live.

### Known gaps — Missing evidence

- The three ECC hooks (`block-no-verify.js`, `config-protection.js`, `cost-tracker.js`)
  have never run, because there was no Node.js on the machine that built this release.
- The guard doesn't follow symlinks, and it judges a searched directory as one path, not
  file by file. Both gaps are written up in `harness/DATA-BOUNDARY.md`.
- Reverse engineering needs REA installed separately; it isn't part of this release.
