---
description: >-
  Owner front door from a one-line idea. KEEL is not switched on yet; the prompt names it.
tags: [owner, front-door]
plugins: ["../.."]
expected_outcome: >-
  HELM runs and records {"role": "owner"} in .keel/keel.json. The reply states a tier,
  then ends on one numbered round of questions, each with two or three options and a
  recommended pick. No application code is written before BRIEF and CONTRACT are
  approved.
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Write, Edit, Bash, Glob, Grep, Skill]
---

Use KEEL. I want a small web app where my book club votes on the next book.
