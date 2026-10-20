---
type: llm
focus: last_message
---

The user described a reading-list tracker in full: the users (a 12-person team with an
admin), the features, and the stack (Next.js with TypeScript, PostgreSQL through Prisma,
Tailwind). They did not say where it is deployed, how members sign in, how secrets are
kept, how long data is kept, or how errors and uptime are watched. Judge only the reply.
Formatting does not matter.

PASS if all of these hold:
- Before any code, the reply asks the user about at least three of: the deploy target or
  hosting, the sign-in method, how secrets are kept, data retention or backups, and
  observability (logs, error tracking, monitoring).
- Each question offers two or three concrete options with one marked as recommended.
- It does not re-open what the description settled (the users, the features, the stack)
  as open questions; confirming one in passing is fine.
- The reply does not present application code as written or delivered.

FAIL if the reply starts building, skips the production questions, asks them without
options or a recommended pick, or re-asks the settled choices.
