---
# A passing unittest run appears in the transcript ("Ran N tests in Xs", blank line,
# "OK"). The trace is JSON, so newlines show as backslash-n; one or more backslashes
# are allowed in case the output is escaped twice. Scored in both arms.
type: regex
target: trace
pattern: 'Ran \d+ tests? in [0-9.]+s(?:\\+[rn]|\s)+OK'
---
