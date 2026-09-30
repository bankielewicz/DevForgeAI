---
id: CTX-015
type: context
title: "shiftlog: relational database"
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
  - {id: ADR-002, relation: constrains, version: 1, hash: null}
supersedes: []
superseded_by: null
blocked_by: []
# --- context-specific ---
document: rdbms
freshness_days: 90
---

# CTX-015 — Relational database

## 1. Components covered

- ARCH-001#CMP-03 Local database

## 2. Engine and version

- **Decision** (ADR-002): SQLite 3, in a local file (tech-stack.md, TEC-03).

## 3. Naming

- **Convention:** tables are plural `snake_case` nouns; primary keys are `id`; foreign keys are
  `<table singular>_id`.

## 4. Migrations

- **Convention:** every schema change is an Alembic revision in `migrations/`.
- [Migration rules](rdbms/migrations.md): read when a story adds or changes a table or column.

## 5. Indexing

- **Convention:** an index is added only with the query that needs it, in the same revision.

## 6. Transactions

- **Convention:** SQLite's default serialized mode; no transaction stays open across user input.

## Change Log

| Version | Date | Author | Change | Items affected |
|---|---|---|---|---|
| 1 | 2026-09-29 | claude-code (session 00000000-0000-0000-0000-000000000000) | Initial draft from ARCH-001 v1 | all |
| 1 | 2026-09-29 | Example Owner | Approved | — |
