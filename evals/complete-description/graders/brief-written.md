---
# docs/BRIEF.md exists and carries the stack the user named. Fails when the file is
# missing. KEEL path, so an indicator in two-arm runs.
type: regex
arm: with-only
target:
  source: file
  path: docs/BRIEF.md
flags: i
pattern: '^(?=[\s\S]*\bnext(?:\.js)?\b)(?=[\s\S]*\bpostgre)'
---
