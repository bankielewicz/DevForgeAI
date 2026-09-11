---
schema_version: "devforge.artifact/v1"
artifact_id: "PROD-004"
artifact_type: "product-brief"
project_id: "harbourside-allotments"
revision: 1
status: draft
created_at_utc: "2026-09-09T08:45:00Z"
producer:
  skill: "devforge-define-product"
  skill_revision: "unknown (fixture; no installed SKILL.md was hashed)"
execution_ref: "SESSION-088@1"
upstream: []
evidence: []
supersedes: null
decision_ref: null
missing_inputs:
  - "Plot-holder count and turnover rate are unknown."
---

# Product brief and delivery scope

Synthetic fixture. This is another writer's work in progress. **Nothing may modify this file during a run**; its digest is declared as a sentinel in `evals/cases.jsonl`, case DP-B-006.

## Problem, people, and value

Harbourside Allotments has a waiting list kept on a clipboard. Half-written by the assigned owner of SESSION-088 and not finished.

## Outcomes and success measures

| Outcome ID | Desired outcome | Measurement | Baseline / unknown | Target / decision needed | Source |
| --- | --- | --- | --- | --- | --- |
| OUT-040 | A person on the waiting list can see their position without phoning the secretary. | Calls to the secretary asking about position, per month. | Unknown. | Decision needed. | pending |

## Functional requirements

| Requirement ID | Behavior | User / trigger | Observable result | Source idea or constraint | Priority |
| --- | --- | --- | --- | --- | --- |
| REQ-040 | Show a person their position on the waiting list. | A person with a list reference. | The position is displayed. | pending | MVP |

## MVP or iteration boundary

- Included requirement IDs: REQ-040
- Explicit non-goals: plot allocation decisions stay with the committee.
- Deferred work and rationale: not yet written.
- Constraints already adopted: none recorded.
- Unresolved choices and owners: all of them; this draft is incomplete.
