---
# A KEEL tier named right next to the word "tier" (markup, a colon or "is" may sit
# between), in the reply the user reads. KEEL vocabulary, so an indicator in two-arm runs.
type: regex
arm: with-only
target: last_message
flags: i
pattern: '\b(sprint|standard|platform)\b[\s*_—–-]*tier\b|\btier\b[\s*_:=—–-]*(?:(?:is|would be|of)\s+)?[\s*_]*(sprint|standard|platform)\b'
---
