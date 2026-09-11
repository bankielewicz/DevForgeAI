---
schema_version: "devforge.artifact/v1"
artifact_id: "EPIC-{{number}}"
artifact_type: "epic"
project_id: "{{project_id}}"
revision: 1
status: draft
created_at_utc: "{{ISO-8601-UTC-time}}"
producer:
  skill: "devforge-plan"
  skill_revision: "{{exact-skill-revision-or-digest}}"
execution_ref: "{{SESSION-ID}}@{{revision}}"
upstream: []
evidence: []
supersedes: null
decision_ref: null
missing_inputs: []
---

# Epic

## Outcome and source coverage

- User-visible outcome: {{outcome}}
- Delivery slice: {{PROD-ID@revision}}
- Requirement references: {{REQ/NFR IDs}}
- Governing architecture reference: {{ARCH-ID@revision and relevant rule IDs}}
- Non-goals: {{explicit exclusions}}

## Story membership and dependency order

| Allocated story ID | Useful outcome | Requirement coverage | Depends on | Definition state |
| --- | --- | --- | --- | --- |
| {{STORY-ID}} | {{outcome}} | {{requirements}} | {{story IDs}} | planned |

Story IDs can be allocated before their definitions are authored. Later execution readiness and selected story revisions belong to handoff/registry records; membership is not a causal dependency from the epic back to its derived stories.

## Coverage and delivery readiness

| Requirement | Covered by stories | Deferred / unresolved part | Rationale and decision reference |
| --- | --- | --- | --- |
| {{requirement}} | {{story IDs}} | {{gap}} | {{reference}} |

- Optional sprint grouping: {{none or user-selected grouping}}
- Cross-story integration checks: {{checks on combined result}}
- Shared files or resources needing serialized integration: {{items}}
- Completion evidence: {{QA/release references, initially none}}
- Handoff reference: {{HANDOFF-ID@revision}}
