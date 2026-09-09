---
schema_version: "devforge.artifact/v1"
artifact_id: "IDEAS-001"
artifact_type: "idea-ledger"
project_id: "trailkeeper"
revision: 2
status: draft
created_at_utc: "2026-08-30T12:05:00Z"
producer:
  skill: "devforge-brainstorm"
  skill_revision: "unknown"
execution_ref: null
upstream:
  - artifact_id: CHANGE-003
    revision: 1
    store: project
    path: docs/devforge/changes/CHANGE-003.md
    sha256: "219c4c18864eb61aa70ccd10fcde1daa74bcbbc5aad64b969470d012b49617bb"
    sections:
      - "Requested change"
      - "Scope"
evidence: []
supersedes:
  artifact_id: "IDEAS-001"
  revision: 1
  sha256: "not-recorded-in-fixture"
decision_ref: "user adoption 2026-08-30, club planning call"
missing_inputs: []
---

# Idea ledger

## Problem and current focus

I run a small trail-running club. Two separate annoyances keep coming up. As of
CHANGE-003 the conditions idea is deliberately narrowed to one trail.

## Ideas and alternatives

| Idea ID | Origin and source | Problem / affected people | Proposed outcome | State | Related idea IDs |
| --- | --- | --- | --- | --- | --- |
| IDEA-001 | user | Members show up to the Ridgeway loop when it is closed or flooded; nobody has current conditions. | A shared place members post and read Ridgeway conditions. | adopted, narrowed per CHANGE-003@1 | none |
| IDEA-002 | user | I spend Sunday evenings manually texting who is running which route next week. | Something that collects route signups without me chasing people. | proposed | none |

## Assumptions and open questions

| Item ID | Statement or question | Evidence or unknown | Consequence | Next observation |
| --- | --- | --- | --- | --- |
| OPEN-001 | Members would actually post conditions rather than only read them. | unknown | A read-only feed with no contributors is useless. | Ask 5 members whether they would post after a run. |
| OPEN-003 | One trail is enough to be useful. | CHANGE-003@1 rationale | If wrong, the feed answers the wrong question. | Ask 5 members which trail they checked last Saturday. |

## Decisions and parked alternatives

| Decision ID | Exact adopted statement or proposal | Decision state | User decision reference | Supersedes |
| --- | --- | --- | --- | --- |
| DEC-001 | Keep both ideas open until one shows a clearer problem. | superseded | null | null |
| DEC-002 | Cover only the Ridgeway loop for now, not every club trail. | adopted | user adoption 2026-08-30, club planning call | DEC-001 |

## Next useful step

- Selected idea IDs: IDEA-001
- Proposed discovery or experiment: Ask 5 club members about OPEN-003.
- Relevant capability need: none
- Non-goals for that step: No app build, no stack selection.
- Handoff reference: HANDOFF-002@1
