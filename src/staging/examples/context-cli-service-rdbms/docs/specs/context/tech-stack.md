---
id: CTX-003
type: context
title: "shiftlog: tech stack"
status: approved
version: 1
created: 2026-09-29
updated: 2026-09-29
owner: "Example Owner"
authors: ["Example Owner", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-opus-5-5"
  session: "00000000-0000-0000-0000-000000000000"
reviewed_by: []
approved_by: "Example Owner"
approved_on: 2026-09-29
upstream:
  - {id: ARCH-001, relation: constrains, version: 1, hash: null}
supersedes: []
superseded_by: null
blocked_by: []
# --- context-specific ---
document: tech-stack
freshness_days: 90
---

# CTX-003 — Tech stack

## Contents

- [1. Technologies](#1-technologies)
- [2. Upgrades](#2-upgrades)

## 1. Technologies

```yaml items
technologies:
  - id: TEC-01
    status: active
    name: "Python"
    version_range: ">=3.12,<3.13"
    used_by:
      - "ARCH-001#CMP-01"
      - "ARCH-001#CMP-02"
      - "ARCH-001#CMP-03"
    basis: decision
    upstream:
      - {id: ADR-001, relation: constrains, version: 1, hash: null}
    notes: ""
  - id: TEC-02
    status: active
    name: "Typer"
    version_range: "0.12.x"
    used_by:
      - "ARCH-001#CMP-01"
    basis: convention
    notes: "Confirmed by the owner on 2026-09-29"
  - id: TEC-03
    status: active
    name: "SQLite"
    version_range: "3.x"
    used_by:
      - "ARCH-001#CMP-03"
    basis: decision
    upstream:
      - {id: ADR-002, relation: constrains, version: 1, hash: null}
    notes: "The version bundled with Python's sqlite3 module"
  - id: TEC-04
    status: active
    name: "Alembic"
    version_range: "1.13.x"
    used_by:
      - "ARCH-001#CMP-03"
    basis: convention
    notes: ""
  - id: TEC-05
    status: active
    name: "pytest"
    version_range: "8.x"
    used_by:
      - "ARCH-001#CMP-01"
      - "ARCH-001#CMP-02"
      - "ARCH-001#CMP-03"
    basis: observed
    observed_in: "pyproject.toml"
    observed_on: 2026-09-29
    notes: ""
```

## 2. Upgrades

- **DevForgeAI rule — ambiguities log:** a version change to a technology listed
  here is recorded in the work item's ambiguities log, and the work continues, only when all of
  these hold: the item is an active decision or convention; the new version is within its
  `version_range` and isn't a new major version; the change is small and reversible; and it
  changes no required behaviour, scope, interface, permission or security, and no spec or
  acceptance-criterion obligation, policy value or approval. Otherwise it is asked about, and
  so is every new technology. Logging never authorizes contradicting a spec.
- **Convention:** dependency updates go in their own pull request, never mixed with a story's changes.

## Change Log

| Version | Date | Author | Change | Items affected |
|---|---|---|---|---|
| 1 | 2026-09-29 | claude-code (session 00000000-0000-0000-0000-000000000000) | Initial draft from ARCH-001 v1 | all |
| 1 | 2026-09-29 | Example Owner | Approved | — |
