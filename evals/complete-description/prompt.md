---
description: >-
  Owner front door from a complete description that names the users, the stack and the
  features but leaves every production question open.
tags: [owner, front-door, production]
plugins: ["../.."]
expected_outcome: >-
  HELM runs and the work starts at BRIEF, at the STANDARD tier. Before any code, the
  reply raises at least three production questions (deploy target, sign-in method,
  secrets, data retention, observability), each with options and a recommended pick,
  without re-asking what the description settled. docs/BRIEF.md is written; no
  application source is.
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Write, Edit, Bash, Glob, Grep, Skill]
---

Use KEEL. Build a reading-list tracker for our 12-person team. Every member signs in,
adds books with a status (to read, reading, done) and a one-line note, and sees the whole
team's list sorted by most recently updated. An admin can remove any entry and invite or
remove members. Stack: Next.js with TypeScript, PostgreSQL through Prisma, and Tailwind
for styling. It should be production-ready, since the team will rely on it daily.
