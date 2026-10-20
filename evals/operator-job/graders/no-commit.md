---
# The package's rule: leave changes uncommitted. No git commit in any shell call.
# Scored in both arms.
type: tool_used
tool: Bash
input_match: '\bgit(?:\s+-[cC]\s+\S+)*\s+commit\b'
min: 0
max: 0
---
