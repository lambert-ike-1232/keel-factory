---
# Did the plugin's front door run? A tool_used Skill grader is an indicator only in a
# two-arm run (excluded from the score automatically); it counts under --ablation none.
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:keel:)?helm"'
---
