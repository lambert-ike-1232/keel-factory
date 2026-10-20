---
type: llm
focus: last_message
---

The user gave a one-line idea: a small web app where a book club votes on the next book.
Judge only the reply. Formatting does not matter: options may be lettered, bulleted or
written inline.

PASS if all of these hold:
- The reply ends the turn on one round of numbered questions for the user, not on a
  finished or half-finished build.
- Each question offers two or three concrete options, and each question marks one
  option as recommended (or "my pick"), with a short reason.
- The questions cover what the idea leaves open, such as who uses it and how they sign
  in, where it runs, or how voting works, rather than generic filler.
- The reply does not present application code as written or delivered.

FAIL if the reply builds or delivers the app, asks open-ended questions with no options,
gives options without a recommended pick, or asks nothing at all.
