---
schema_version: "devforge.artifact/v1"
artifact_id: "IDEAS-{{number}}"
artifact_type: "idea-ledger"
project_id: "{{project_id}}"
revision: 1
status: draft
created_at_utc: "{{ISO-8601-UTC-time}}"
producer:
  skill: "devforge-brainstorm"
  skill_revision: "{{exact-skill-revision-or-digest}}"
execution_ref: "{{SESSION-ID}}@{{revision}}"
upstream: []
evidence: []
supersedes: null
decision_ref: null
missing_inputs: []
---

# Idea ledger

## Problem and current focus

{{User's words or attributed summary. Preserve uncertainty.}}

## Ideas and alternatives

| Idea ID | Origin and source | Problem / affected people | Proposed outcome | State | Related idea IDs |
| --- | --- | --- | --- | --- | --- |
| IDEA-001 | {{user / AI proposal / evidence reference}} | {{problem}} | {{outcome}} | proposed | {{split/merge/alternative links}} |

## Assumptions and open questions

| Item ID | Statement or question | Evidence or unknown | Consequence | Next observation |
| --- | --- | --- | --- | --- |
| OPEN-001 | {{uncertainty}} | {{reference or unknown}} | {{why it matters}} | {{smallest useful check}} |

## Decisions and parked alternatives

| Decision ID | Exact adopted statement or proposal | Decision state | User decision reference | Supersedes |
| --- | --- | --- | --- | --- |
| DEC-001 | {{statement}} | proposed | null | null |

## Next useful step

- Selected idea IDs: {{IDs or unresolved}}
- Proposed discovery or experiment: {{task}}
- Relevant capability need: {{need, existing skill, or none}}
- Non-goals for that step: {{boundaries}}
- Handoff reference: {{HANDOFF-ID@revision}}
