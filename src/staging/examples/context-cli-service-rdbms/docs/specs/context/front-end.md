---
id: CTX-011
type: context
title: "shiftlog: front end"
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
document: front-end
freshness_days: 90
---

# CTX-011 — Front end

## 1. Components covered

- ARCH-001#CMP-01 shiftlog CLI

## 2. Framework and structure

- **Convention:** one Typer command per module in `src/shiftlog/cli/` (tech-stack.md, TEC-02).

## 3. State

- **Convention:** the CLI holds no state between runs; everything it shows comes from the service.

## 4. Interaction and output

- **Convention:** commands are verbs: `start`, `stop`, `list`, `week`.
- **Convention:** every command that prints data accepts `--json`, which prints one JSON document and
  nothing else.
- **Convention:** exit codes are 0 on success, 1 for a user error (a `ShiftError`), and 2 for anything
  else.

## 5. Accessibility

- **Convention:** no meaning is carried by colour alone, and colour is off when `NO_COLOR` is set.

## 6. Design system

- **Convention:** terminal output follows `docs/cli-style.md` (ui-mockups.md, section 2).

## Change Log

| Version | Date | Author | Change | Items affected |
|---|---|---|---|---|
| 1 | 2026-09-29 | claude-code (session 00000000-0000-0000-0000-000000000000) | Initial draft from ARCH-001 v1 | all |
| 1 | 2026-09-29 | Example Owner | Approved | — |
