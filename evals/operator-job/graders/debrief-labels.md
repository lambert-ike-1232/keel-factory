---
# OPERATOR.md's exfil step: a debrief kept at .keel/ops/debrief.md, every claim labeled
# Evidence, Inferred or Missing evidence. Fails when the file is missing. KEEL path, so
# an indicator in two-arm runs.
type: regex
arm: with-only
target:
  source: file
  path: .keel/ops/debrief.md
pattern: '^(?=[\s\S]*\bEvidence\b)(?=[\s\S]*\bInferred\b)(?=[\s\S]*\bMissing\b)'
---
