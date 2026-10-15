# Brief: [Project or feature name]

**Tier:** SPRINT | STANDARD | PLATFORM — *(state it, do not drift into it)*
**Date:** [YYYY-MM-DD]

Phase 1 of KEEL. Fill in Part 1 by hand, in plain language, before any agent is
involved. "I don't know yet" is a legitimate answer and a better one than an
invention: it becomes a decision to make rather than an assumption to discover later.

---

## Part 1 — Intake

### 1. What are you building?
[One or two sentences, as if explaining to a colleague.]

### 2. Who is it for?
[Who uses it. What do they do today instead?]

### 3. Must-haves
[The core capabilities. What makes it useful, not everything you can imagine. Each
line here becomes a row in `TRACEABILITY.md`, so phrase them as capabilities.]

-
-
-

### 4. What is it explicitly NOT doing?
[Just as important. Anything ruled out here saves a scope argument later.]

-
-

### 5. What's the hard part?
[The thing you suspect will actually be difficult or cause rework.]

### 6. What does "done and working" look like?
[How would you demonstrate it? Numeric targets — speed, accuracy, volume, cost — go here.]

### 7. Inputs and outputs
- Takes in:
- Produces:

### 8. How do people interact with it?
[CLI, REST API, web UI, scheduled job, library, chat, something else.]

### 9. Sensitive data
[Personal data, credentials, internal documents, financial or health data, customer
content. Say what, or "none."]

### 10. Constraints
- Language/stack: [or "recommend one"]
- Where it runs:
- Storage:
- External services (LLM provider, APIs, internal systems):
- **Cost ceiling:** [especially for metered APIs. A number if you have one.]
- Timeline:

### 11. Scale
[10 requests a day or 10,000? One user or a team? Small inputs or large files? A rough
answer is enough; it changes the architecture.]

### 12. Anything else
[Prior art, an existing repo to learn from, decisions already made, things to avoid.]

---

## Part 2 — The rewrite *(agent fills in)*

**The brief I'm working from:**

> [The intake above, restated as the brief a senior engineer would have needed.
> Keep the user's words where possible. Tag every gap with `[GUESS: ...]`.]

### Guesses to resolve

| # | Guess | Resolution |
|---|---|---|
| 1 | `[GUESS: ...]` | |
| 2 | `[GUESS: ...]` | |

Every row gets resolved, or explicitly accepted as a standing assumption. None are
left open into Phase 2.

---

## Part 3 — The announcement

Three to six sentences announcing this to its users, as if it already shipped. Not a
summary of the plan: an announcement.

> [Write it here.]

**If you cannot write this, you are building the wrong thing.** Finding that out now
costs five minutes.

---

## Part 4 — Open decisions carried forward

[Anything the grilling surfaced that CONTRACT has to settle. Nothing important may
exist only in chat.]
