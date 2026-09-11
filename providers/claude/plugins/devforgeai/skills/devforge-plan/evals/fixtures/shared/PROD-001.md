---
schema_version: "devforge.artifact/v1"
artifact_id: "PROD-001"
artifact_type: "product-brief"
project_id: "shiftline"
revision: 2
status: accepted
created_at_utc: "2026-08-19T09:14:00Z"
producer:
  skill: "devforge-define-product"
  skill_revision: "unknown (synthetic fixture; no skill produced these bytes)"
execution_ref: null
upstream: []
evidence: []
supersedes: null
decision_ref: "user adoption recorded in the 2026-08-19 planning call notes (synthetic)"
missing_inputs:
  - "REQ-004 denial behaviour is undefined; the coordinator has not answered"
---

# Product brief and delivery scope — Shiftline

**Synthetic fixture.** Shiftline does not exist.

## Problem, people, and value

Volunteer coordinators at small shelters spend their evenings brokering shift swaps by phone. Volunteers
cannot see who else is free, so every swap costs the coordinator two calls. The delivery slice below
covers self-service swaps only.

## Outcomes and success measures

| Outcome ID | Desired outcome | Measurement | Baseline / unknown | Target / decision needed | Source |
| --- | --- | --- | --- | --- | --- |
| OUT-001 | A volunteer arranges a swap without the coordinator | Swaps completed with no coordinator action | Unknown | Most swaps | IDEAS-003 |
| OUT-002 | The coordinator can see what changed | Swap history visible per shift | None today | All accepted swaps | IDEAS-003 |

## Functional requirements

| Requirement ID | Behavior | User / trigger | Observable result | Source idea or constraint | Priority |
| --- | --- | --- | --- | --- | --- |
| REQ-001 | A volunteer offers one of their assigned shifts for swap | Volunteer opens an assigned shift | The shift appears in the open-offers list for eligible volunteers | IDEAS-003 | must |
| REQ-002 | An eligible volunteer claims an open offer | Volunteer selects an open offer | Both rosters update and both volunteers are notified | IDEAS-003 | must |
| REQ-003 | A swap is refused when it would leave a shift below its minimum staffing | Claim attempt on a shift at minimum | The claim is refused and the reason is shown | Coordinator interview | must |
| REQ-004 | Only volunteers rostered to the same site may claim an offer | Claim attempt from another site | Undefined | Coordinator interview | must |
| REQ-005 | The coordinator sees the swap history for any shift | Coordinator opens a shift | Ordered list of accepted swaps with actor and time | OUT-002 | should |

REQ-004 states the eligibility rule but not what the system does when an ineligible volunteer attempts a
claim. The coordinator has not answered whether the offer should be hidden from ineligible volunteers or
shown and refused on claim, and the two produce different products.

## Nonfunctional requirements

| Requirement ID | Concern | Measurable criterion | Conditions | Evidence / source | Decision state |
| --- | --- | --- | --- | --- | --- |
| NFR-001 | Auditability | Every accepted swap records actor, time and prior assignment | All swaps | Coordinator interview | adopted |

## MVP or iteration boundary

- Included requirement IDs: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, NFR-001
- Explicit non-goals: shift creation, volunteer onboarding, payroll export, mobile push notifications
- Deferred work and rationale: multi-site coordinators deferred until one site is working
- Constraints already adopted: the shelter runs one site per deployment
- Unresolved choices and owners: REQ-004 denial behaviour — coordinator

## Discovery evidence

| Evidence ID | Claim | Source URL or immutable file | Version / retrieval date | Observation or inference | Limit |
| --- | --- | --- | --- | --- | --- |
| EVID-001 | Coordinators broker swaps by phone | Synthetic interview note | 2026-08-11 | Observation | One shelter |

## Acceptance and continuation

Adopted by the user on 2026-08-19 (synthetic). Unresolved: REQ-004 denial behaviour. Continues to
architecture and planning.
