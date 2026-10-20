---
description: >-
  Operator front door. The workspace is someone else's Python package whose README
  names the job and two rules: don't change the tests, leave changes uncommitted.
tags: [operator, front-door]
plugins: ["../.."]
expected_outcome: >-
  HELM records {"role": "operator"} in .keel/keel.json. The bug in calc.py is fixed,
  python3 -m unittest is run and passes, the tests are unchanged and nothing is
  committed. A debrief at .keel/ops/debrief.md labels its claims Evidence, Inferred or
  Missing evidence. No docs/ or .scratch/ appears in the package.
max_turns: 30
timeout_seconds: 600
allowed_tools: [Read, Write, Edit, Bash, Glob, Grep, Skill]
---

Use KEEL: this is someone else's package; do the job its README describes.
