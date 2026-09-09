---
schema_version: "devforge.artifact/v1"
artifact_id: "PROD-{{number}}"
artifact_type: "product-brief"
project_id: "{{project_id}}"
revision: 1
status: draft
created_at_utc: "{{ISO-8601-UTC-time}}"
producer:
  skill: "devforge-define-product"
  skill_revision: "{{exact-skill-revision-or-digest}}"
execution_ref: "{{SESSION-ID}}@{{revision}}"
upstream: []
evidence: []
supersedes: null
decision_ref: null
missing_inputs: []
---

# Product brief and delivery scope

## Problem, people, and value

{{Selected idea IDs, target users, problem, and evidence.}}

## Outcomes and success measures

| Outcome ID | Desired outcome | Measurement | Baseline / unknown | Target / decision needed | Source |
| --- | --- | --- | --- | --- | --- |
| OUT-001 | {{user value}} | {{observable measure}} | {{baseline}} | {{target}} | {{idea/evidence reference}} |

## Functional requirements

| Requirement ID | Behavior | User / trigger | Observable result | Source idea or constraint | Priority |
| --- | --- | --- | --- | --- | --- |
| REQ-001 | {{behavior}} | {{trigger}} | {{result}} | {{exact source section}} | {{release priority}} |

## Nonfunctional requirements

| Requirement ID | Concern | Measurable criterion | Conditions | Evidence / source | Decision state |
| --- | --- | --- | --- | --- | --- |
| NFR-001 | {{security / performance / accessibility / operations}} | {{criterion}} | {{scope}} | {{reference}} | proposed |

## MVP or iteration boundary

- Included requirement IDs: {{IDs}}
- Explicit non-goals: {{excluded outcomes}}
- Deferred work and rationale: {{items}}
- Constraints already adopted: {{decision references}}
- Unresolved choices and owners: {{items}}

## Discovery evidence

| Evidence ID | Claim | Source URL or immutable file | Version / retrieval date | Observation or inference | Limit |
| --- | --- | --- | --- | --- | --- |
| EVID-001 | {{claim}} | {{source}} | {{version/date}} | {{classification}} | {{limit}} |

## Acceptance and continuation

{{User adoption reference, unresolved decisions, and handoff to applicable design/architecture/planning work.}}
