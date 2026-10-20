---
# HELM's first step records the role. KEEL-only name, so an indicator in two-arm runs.
type: regex
arm: with-only
target:
  source: file
  path: .keel/keel.json
pattern: '"role"\s*:\s*"operator"'
---
