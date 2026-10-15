# Deployment: [Project name]

PLATFORM tier. The hosting contract, against the platform's **actual numeric limits**
rather than remembered ones.

---

## Target

| | |
|---|---|
| Platform | |
| Region(s) | |
| Tier / plan | |
| Runtime version | |
| Scaling model | [fixed / autoscale, with bounds] |

## Real limits

Looked up, not recalled. These constrain the design; if the design exceeds them, the
design is wrong.

| Limit | Value | Source |
|---|---|---|
| Request timeout | | |
| Max payload | | |
| Memory | | |
| Concurrent executions | | |
| Storage | | |
| Rate limit | | |
| Monthly cost at this tier | | |

## Secrets

| Secret | Where it lives | How it reaches the process | Never |
|---|---|---|---|
| | | | written to disk / baked into the image / logged |

## Deploy

```bash
[exact command]
```

## Rollback

```bash
[exact command]
```
**Time to roll back:** [measured, not estimated]

## Health

| Endpoint / signal | What it proves | Checked how often |
|---|---|---|
| | | |

## What is persisted, and what happens if it is lost

[Be specific. "The database" is not an answer.]
