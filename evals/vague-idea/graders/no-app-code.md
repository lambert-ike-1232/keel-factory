---
# No application code before BRIEF and CONTRACT are approved: no source file or package
# manifest among the files created, outside docs/ (KEEL's specs) and .keel/.
# Scored in both arms.
type: regex
target: files
flags: m
match: not_contains
pattern: '^(?!(?:.*/)?(?:docs|\.keel)/)(?:.*/)?(?:[^/\n]+\.(?:m?jsx?|cjs|tsx?|py|rb|go|rs|java|kt|php|html?|css|scss|vue|svelte|sql|prisma)|package\.json|requirements\.txt|pyproject\.toml|Gemfile|go\.mod|Cargo\.toml|Dockerfile|docker-compose\.ya?ml)$'
---
