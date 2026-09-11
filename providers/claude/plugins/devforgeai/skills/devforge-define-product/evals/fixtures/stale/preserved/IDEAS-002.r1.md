---
schema_version: "devforge.artifact/v1"
artifact_id: "IDEAS-002"
artifact_type: "idea-ledger"
project_id: "northgate-tool-library"
revision: 1
status: draft
created_at_utc: "2026-08-19T16:40:00Z"
producer:
  skill: "devforge-brainstorm"
  skill_revision: "unknown (fixture; no installed SKILL.md was hashed)"
execution_ref: null
upstream: []
evidence: []
supersedes: null
decision_ref: "DEC-002"
missing_inputs: []
---

# Idea ledger: Northgate Tool Library

Synthetic fixture. This is the **preserved revision 1** - the exact bytes that PROD-002 cites. Invented for evaluation.

## Ideas

| Idea ID | Idea | Problem it addresses | Who is affected | Origin | State |
| --- | --- | --- | --- | --- | --- |
| IDEA-010 | A member can see which tools are on the shelf right now. | People come in for a tool that is already out. | Members; the two volunteers on the desk. | user | proposed |
| IDEA-011 | Borrowing and returning is recorded, so a tool has a current holder. | The paper book is illegible and nobody reconciles it. | Desk volunteers. | user | proposed |
| IDEA-012 | Members reserve a tool for a specific weekend. | Popular tools are gone by Saturday morning. | Members. | AI proposal | proposed |

## Decisions

| Decision ID | What was decided | Basis | State | Decision reference |
| --- | --- | --- | --- | --- |
| DEC-002 | The first release covers borrowing and returning only - IDEA-010 and IDEA-011. Reservations are out. | Sam, 2026-08-19: "Just borrowing and returning. If we can't get that right the rest doesn't matter." | adopted | Sam, session of 2026-08-19 |

## Open questions

| ID | Statement | Consequence if wrong | Smallest observation |
| --- | --- | --- | --- |
| Q-010 | Volunteers will record a return at the desk rather than afterwards. | The current-holder field is wrong most of the time and IDEA-010 shows stale data. | Watch two Saturday shifts and count returns recorded at the desk. |
