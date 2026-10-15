# Contract: [Project name]

Phase 2 of KEEL. **Stop point at STANDARD and above.**

Every line here is a *decision*, not a category of options. "A database" is not a
decision; "PostgreSQL 16 on Fly.io, single region" is.

---

## Production Build Contract

| | |
|---|---|
| **Runtime** | [exact language and version] |
| **Framework** | [exact, with version] |
| **Deploy target** | [platform, region, tier] |
| **Persistence** | [store, version, where it runs] |
| **Secrets policy** | [where they live, how they reach the process, what is never written to disk] |
| **Primary interface** | [CLI / HTTP / library / UI] |

### Authentication & authorization
[The actual model. Who can call what, how identity is established, how it is enforced,
and what a rejected request looks like.]

### Data model & state transitions
[Entities, their fields, and the legal transitions between states. A state that cannot
be reached and a state that cannot be left are both bugs.]

### Observability contract
[What is logged, at what level, in what structure. What is measured. What is audited.
What is redacted, and how that redaction is *tested*.]

### Limits & quotas
[Real numeric limits from the actual platform: request size, timeout, memory, payload,
rate limit, storage. Not remembered — looked up.]

### Toolchain

*(Rule 6a.)* What must be installed for this project's acceptance gate to run at all.
Verified during this phase, not assumed. Details and status in `ACCEPTANCE.md`.

| Requirement | Version | Needed by |
|---|---|---|
| | | |

### Bound numbers

*(Rule 6d.)* Every numeric claim anywhere in this contract, and the check that asserts it.
A figure with no assertion behind it is decoration, and decoration cannot be breached
because nothing is watching.

| Figure | Value | Asserted by |
|---|---|---|
| | | `[test name]` |

### Cost budget
| | |
|---|---|
| **Unit of work** | [e.g. "one 10-page document, 2 target locales"] |
| **Unit cost ceiling** | [a number] |
| **Expected volume** | [a number, labelled Evidence or Inferred] |
| **Monthly ceiling at volume** | [a number] |

See `COST_MODEL.md` for the measured figures. This section is the *budget*; that file
is the *measurement*.

### Sensitive data classes
[What classes exist, where each may be stored, and what must never be logged.]

---

## Goals

[What this is for. Three to six lines.]

## Non-goals

[What this deliberately does not do. Each line here prevents an argument later.]

---

## Feature List

**Every line here becomes a row in `TRACEABILITY.md`.** Phrase each as a capability,
not a component, and keep them at a consistent grain.

### [Feature area 1]
- [ ] [Capability]
- [ ] [Capability]

### [Feature area 2]
- [ ] [Capability]

---

## Architecture

[The shape of the system. Which modules exist, what each hides, and how a request or
job actually travels. Name the seams.]

## Quality standards

[Numeric and testable. "Fast" is not a standard; "p95 under 800ms on the reference
fixture" is.]

## Error handling

[What a failure looks like to a caller. The error envelope, the categories, and which
failures are retryable.]

## Versioning

[What constitutes a breaking change to the contracts in `schemas/`, and what happens
when one is made.]
