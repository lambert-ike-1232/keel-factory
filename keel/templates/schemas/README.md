# Schemas

**The actual source of truth for this project's contracts.** They outrank any prose in
`CONTRACT.md` the moment they disagree. Validate against them in CI, not in code review.

| File | Holds |
|---|---|
| `input.schema.json` | The shape of a request or job input |
| `output.schema.json` | The shape of a result, including terminal states |
| `config.schema.json` | Project-level configuration |
| `errors.schema.json` | The error envelope |
| `audit_log.schema.json` | An audit log entry, if the project needs one |

Changing any of these is a **versioning event**, not a quiet edit.

---

## Do not ship the placeholders

Replacing the domain fields with real, constrained definitions is a **prerequisite to
writing implementation code**, not a cleanup task for later.

A schema that accepts anything — unconstrained domain fields, or
`additionalProperties: true` — is the most dangerous state this template can be left
in, **because it looks like a contract while validating nothing.** You cannot reliably
validate input, reject malformed requests, secure the boundary, version the contract,
or write meaningful tests against it, and every downstream guarantee in
`ACCEPTANCE.md` quietly becomes untrue.

Rules:

- Keep `additionalProperties: false`. Add fields deliberately.
- Every field gets a type, and constraints wherever the domain has them: `enum`,
  min/max, `format`, `maxLength`.
- **Size limits are a security control**, not a nicety.
- Each schema gets at least one valid and one deliberately invalid example, exercised
  by a contract test, so a contract regression fails CI rather than reaching a client.
