---
# The reply carries a numbered list with at least items 1 and 2 (Markdown bold,
# headings or "Q" prefixes allowed). Scored in both arms.
type: regex
target: last_message
flags: mi
pattern: '^[ \t>*#_]*q?1[.)][\s\S]*^[ \t>*#_]*q?2[.)]'
---
