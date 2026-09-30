---
id: CTX-002
type: context
title: "shiftlog: architecture overview"
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
  - {id: ARCH-001, item: CMP-01, relation: constrains, version: 1, hash: null}
  - {id: ARCH-001, item: CMP-02, relation: constrains, version: 1, hash: null}
  - {id: ARCH-001, item: CMP-03, relation: constrains, version: 1, hash: null}
supersedes: []
superseded_by: null
blocked_by: []
# --- context-specific ---
document: architecture
freshness_days: 90
---

# CTX-002 — Architecture overview

## 1. Components

| Component | Item | Kinds | Responsibility | Documents |
|---|---|---|---|---|
| shiftlog CLI | ARCH-001#CMP-01 | user-interface | Commands and all output | front-end.md, ui-mockups.md |
| Shift service | ARCH-001#CMP-02 | service | Shift rules and weekly totals | middle-tier.md |
| Local database | ARCH-001#CMP-03 | relational-store | Stores shifts in a SQLite file | rdbms.md |

Open architectural questions are the DEC items of ARCH-001; it has none open.

## 2. Error handling

- **Convention:** the service raises a subclass of `ShiftError` for every rule violation; the CLI maps
  each subclass to one message and exit code (front-end.md, section 4). No other exception crosses from
  the service to the CLI.

## 3. Logging

- **Convention:** nothing is logged to standard output. With `--verbose`, debug logs go to standard error.

## 4. Configuration

- **Convention:** the only setting is the database path, read from `SHIFTLOG_DB`, defaulting to the
  user's data folder.

## 5. Security basics

- **Convention:** the database file is created readable and writable by its owner only.

## Change Log

| Version | Date | Author | Change | Items affected |
|---|---|---|---|---|
| 1 | 2026-09-29 | claude-code (session 00000000-0000-0000-0000-000000000000) | Initial draft from ARCH-001 v1 | all |
| 1 | 2026-09-29 | Example Owner | Approved | — |
