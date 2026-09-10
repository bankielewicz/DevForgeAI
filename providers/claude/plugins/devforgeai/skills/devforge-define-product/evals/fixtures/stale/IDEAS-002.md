---
schema_version: "devforge.artifact/v1"
artifact_id: "IDEAS-002"
artifact_type: "idea-ledger"
project_id: "northgate-tool-library"
revision: 2
status: draft
created_at_utc: "2026-09-06T10:05:00Z"
producer:
  skill: "devforge-brainstorm"
  skill_revision: "unknown (fixture; no installed SKILL.md was hashed)"
execution_ref: null
upstream: []
evidence: []
supersedes:
  artifact_id: "IDEAS-002"
  revision: 1
  store: project
  path: "docs/devforge/ideas/archive/IDEAS-002.r1.md"
  sha256: "03b523dea859ed3442d833eed9653ec6bc57cf995a14716d478e0a64959b0098"
decision_ref: "DEC-002"
missing_inputs: []
---

# Idea ledger: Northgate Tool Library

Synthetic fixture. This is **revision 2**, the bytes now sitting at the ledger's live path. Invented for evaluation.

## Ideas

| Idea ID | Idea | Problem it addresses | Who is affected | Origin | State |
| --- | --- | --- | --- | --- | --- |
| IDEA-010 | A member can see which tools are on the shelf right now. | People come in for a tool that is already out. | Members; the two volunteers on the desk. | user | proposed |
| IDEA-011 | Borrowing and returning is recorded, so a tool has a current holder. | The paper book is illegible and nobody reconciles it. | Desk volunteers. | user | proposed |
| IDEA-012 | Members reserve a tool for a specific weekend. | Popular tools are gone by Saturday morning. | AI proposal | proposed |
| IDEA-013 | A maintenance log per tool: last serviced, known faults, whether it is safe to lend. | A chainsaw went out with a slipping brake and nobody had recorded the fault. | Members; the safety officer. | user | proposed |

## Decisions

| Decision ID | What was decided | Basis | State | Decision reference |
| --- | --- | --- | --- | --- |
| DEC-002 | The first release covers borrowing and returning **and the safety-relevant part of the maintenance log** - IDEA-010, IDEA-011 and the fault field of IDEA-013. Reservations remain out. | Sam, 2026-09-06: "After the chainsaw I'm not shipping a lending system that can't record a fault. Add that." | adopted | Sam, session of 2026-09-06 |

## Open questions

| ID | Statement | Consequence if wrong | Smallest observation |
| --- | --- | --- | --- |
| Q-010 | Volunteers will record a return at the desk rather than afterwards. | The current-holder field is wrong most of the time and IDEA-010 shows stale data. | Watch two Saturday shifts and count returns recorded at the desk. |
| Q-011 | A free-text fault field is enough; a structured service schedule is not needed yet. | The safety officer cannot tell which tools are overdue for service. | Ask the safety officer what they currently track. |
