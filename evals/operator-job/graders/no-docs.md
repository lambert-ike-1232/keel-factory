---
# Operator footprint: nothing KEEL-shaped in the package's own tree, so no docs/ or
# .scratch/ among the files created. Scored in both arms.
type: regex
target: files
flags: m
match: not_contains
pattern: '(?:^|/)(?:docs|\.scratch)/'
---
