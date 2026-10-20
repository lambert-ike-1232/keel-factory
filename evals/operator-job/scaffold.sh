#!/usr/bin/env bash
# Builds the operator-job workspace: someone else's tiny Python package with one failing
# test, as a git repository with one commit. claude plugin eval runs this in the empty
# workspace, only with --scaffold, with a minimal environment (PATH, a temporary HOME,
# TMPDIR). It is not told where the case directory is, so every file is written here.
set -euo pipefail

cat > README.md <<'EOF'
# calc

Tiny arithmetic helpers. Standard library only.

## The job

Fix the failing test in calc.py; run `python3 -m unittest`.

The bug is in `calc.py`. The job is done when `python3 -m unittest` passes.

## Rules for contributors

- Don't change the tests. `test_calc.py` is the spec.
- Leave your changes uncommitted. The maintainers review the working tree.
EOF

cat > calc.py <<'EOF'
"""Tiny arithmetic helpers."""


def add(a, b):
    """Return the sum of a and b."""
    return a - b


def multiply(a, b):
    """Return the product of a and b."""
    return a * b
EOF

cat > test_calc.py <<'EOF'
import unittest

from calc import add, multiply


class TestCalc(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)

    def test_multiply(self):
        self.assertEqual(multiply(4, 3), 12)


if __name__ == "__main__":
    unittest.main()
EOF

printf '__pycache__/\n' > .gitignore

git init -q -b main
git add README.md calc.py test_calc.py .gitignore
git -c user.name="calc maintainers" -c user.email="maintainers@calc.invalid" \
    commit -q -m "Add calc helpers and tests"
