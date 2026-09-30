---
id: CTX-012
type: context
title: "shiftlog: middle tier"
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
document: middle-tier
freshness_days: 90
---

# CTX-012 — Middle tier

## 1. Components covered

- ARCH-001#CMP-02 Shift service

## 2. Domain structure

- **Convention:** a `Shift` dataclass and one `ShiftService` class hold all shift rules.

## 3. Boundaries within a component

- **Convention:** the CLI calls only `ShiftService`; `ShiftService` reaches the database only through
  the repository in `src/shiftlog/db/`.

## 4. Orchestration

- **Convention:** none is needed: every command is one call to the service in one process.

## 5. Validation

- **Convention:** the service validates every time it receives and raises `ValidationError` (a
  `ShiftError`) before touching the database.

## 6. Transactions

- **Convention:** one transaction per service call, opened by the repository.

## Change Log

| Version | Date | Author | Change | Items affected |
|---|---|---|---|---|
| 1 | 2026-09-29 | claude-code (session 00000000-0000-0000-0000-000000000000) | Initial draft from ARCH-001 v1 | all |
| 1 | 2026-09-29 | Example Owner | Approved | — |
