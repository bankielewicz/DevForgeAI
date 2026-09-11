---
schema_version: "devforge.artifact/v1"
artifact_id: "PROD-005"
artifact_type: "product-brief"
project_id: "{{project_id}}"
revision: 1
status: draft
created_at_utc: "2026-09-09T21:10:00Z"
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

Synthetic fixture. This is a **half-filled draft**: several required fields still hold template placeholders, and `missing_inputs` is empty even though facts are plainly missing. A result in this state is a draft and cannot be presented as ready. Invented for evaluation.

## Problem, people, and value

Kestrel Book Group wants somewhere to record which member has which of the group's shared copies. Target users: {{who}}.

## Outcomes and success measures

| Outcome ID | Desired outcome | Measurement | Baseline / unknown | Target / decision needed | Source |
| --- | --- | --- | --- | --- | --- |
| OUT-050 | A member can find out who has a copy without asking the group. | Messages asking "who has the Ishiguro?" per month. | {{baseline}} | {{target}} | member request, 2026-09-09 |

## Functional requirements

| Requirement ID | Behavior | User / trigger | Observable result | Source idea or constraint | Priority |
| --- | --- | --- | --- | --- | --- |
| REQ-050 | Show each shared copy and its current holder. | Any member. | Each copy lists exactly one holder or "on the shelf". | member request, 2026-09-09 | MVP |
| REQ-051 | {{behavior}} | {{trigger}} | {{result}} | {{exact source section}} | {{release priority}} |

## Nonfunctional requirements

| Requirement ID | Concern | Measurable criterion | Conditions | Evidence / source | Decision state |
| --- | --- | --- | --- | --- | --- |
| NFR-050 | {{security / performance / accessibility / operations}} | {{criterion}} | {{scope}} | {{reference}} | proposed |

## MVP or iteration boundary

- Included requirement IDs: REQ-050
- Explicit non-goals: {{excluded outcomes}}
- Deferred work and rationale: {{items}}
- Constraints already adopted: none recorded
- Unresolved choices and owners: {{items}}

## Discovery evidence

| Evidence ID | Claim | Source URL or immutable file | Version / retrieval date | Observation or inference | Limit |
| --- | --- | --- | --- | --- | --- |
| EVID-050 | {{claim}} | {{source}} | {{version/date}} | {{classification}} | {{limit}} |

## Acceptance and continuation

{{User adoption reference, unresolved decisions, and handoff to applicable design/architecture/planning work.}}
