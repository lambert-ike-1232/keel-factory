# Runbook: [Project name]

PLATFORM tier. **Incident-shaped, not topic-shaped.** Each entry starts from a symptom
someone is actually looking at, at 3am, and ends in an exact command.

A runbook organised by subsystem is a reference document. A runbook organised by
symptom is a runbook.

---

## [Symptom, as it appears — e.g. "Jobs stuck in `running`"]

**Looks like:** [what the person sees — the alert, the dashboard, the user report]

**First check:**
```bash
[exact command]
```

**If [outcome A]:** [exact remedy command]

**If [outcome B]:** [exact remedy command]

**If neither:** escalate to [who], with [what to include]

**Root causes seen before:** [link `DECISIONS.md` entries]

---

## [Symptom]

**Looks like:**

**First check:**
```bash
```

**If:**

---

## Cost spike

**Looks like:** [where it shows up first]

**First check:**
```bash
[the command that breaks spend down by call site]
```

**Common causes:** cache disabled or cold · a call promoted a rung on the escape-hatch
ladder · context stuffing · retry storm · a fixture set that grew

**Remedy:** [exact commands]

---

## Escalation

| Condition | Who | How |
|---|---|---|
| | | |
