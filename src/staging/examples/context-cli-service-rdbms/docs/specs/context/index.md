---
id: CTX-001
type: context
title: "shiftlog: project context index"
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
document: index
---

# CTX-001 — Project context index

## Documents

| File | ID | Version | Kinds | Purpose |
|---|---|---|---|---|
| [architecture.md](architecture.md) | CTX-002 | 1 | all | Components and the conventions that cut across layers |
| [tech-stack.md](tech-stack.md) | CTX-003 | 1 | all | Technologies, their allowed versions, and where each was chosen |
| [source-tree.md](source-tree.md) | CTX-004 | 1 | all | Where code, tests, configuration and documentation live |
| [testing.md](testing.md) | CTX-005 | 1 | all | How testing is done, and the testing policy in force |
| [front-end.md](front-end.md) | CTX-011 | 1 | user-interface | Command structure, flags, output and exit codes of the CLI |
| [middle-tier.md](middle-tier.md) | CTX-012 | 1 | service | How the shift service is organized and validates input |
| [rdbms.md](rdbms.md) | CTX-015 | 1 | relational-store | SQLite naming, migrations and transactions |
| [ui-mockups.md](ui-mockups.md) | CTX-017 | 1 | user-interface | The CLI style guide, and the approved designs |

## Loading

- **DevForgeAI rule — context loading:** read this index first. Then open only the documents
  for the kinds of the components the work touches, plus the core documents it needs, and a detail file
  only when its "read when" line in its parent applies. Never open every document by default.

## Change Log

| Version | Date | Author | Change | Items affected |
|---|---|---|---|---|
| 1 | 2026-09-29 | claude-code (session 00000000-0000-0000-0000-000000000000) | Initial draft from ARCH-001 v1 | all |
| 1 | 2026-09-29 | Example Owner | Approved | — |
