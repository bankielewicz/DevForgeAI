---
schema_version: "devforge.artifact/v1"
artifact_id: "PROD-001"
artifact_type: "product-brief"
project_id: "riverbend-running-club"
revision: 2
status: accepted
created_at_utc: "2026-09-01T11:20:00Z"
producer:
  skill: "devforge-define-product"
  skill_revision: "unknown (fixture; no installed SKILL.md was hashed)"
execution_ref: null
upstream:
  - artifact_id: "IDEAS-001"
    revision: 2
    store: project
    path: "docs/devforge/ideas/IDEAS-001.md"
    sha256: "1111111111111111111111111111111111111111111111111111111111111111"
    sections:
      - "IDEA-001"
      - "IDEA-002"
      - "DEC-001"
evidence: []
supersedes:
  artifact_id: "PROD-001"
  revision: 1
  store: project
  path: "docs/devforge/product/PROD-001.r1.md"
  sha256: "2222222222222222222222222222222222222222222222222222222222222222"
decision_ref: "Ada, session of 2026-09-01"
missing_inputs:
  - "No baseline for how many members currently know a session is cancelled before travelling."
---

# Product brief and delivery scope

Synthetic fixture. Every requirement, measure and decision below was invented for evaluation.

## Problem, people, and value

Selected ideas: IDEA-001 and IDEA-002 from IDEAS-001@2, adopted by Ada as DEC-001. Riverbend's members cannot reliably find out whether a session is on and who is coming; the answer scrolls out of a group chat. Target users are the club's ~90 members and its four run leaders. Evidence is the secretary's own account; nothing has been measured.

## Outcomes and success measures

| Outcome ID | Desired outcome | Measurement | Baseline / unknown | Target / decision needed | Source |
| --- | --- | --- | --- | --- | --- |
| OUT-001 | A member can tell whether a session is on without asking anyone. | Count of "is it still on?" messages in the club group chat per week. | Unknown; nobody has counted. Ada estimates "a few every week" and that estimate is not a measurement. | Decision needed after one week of counting. | IDEAS-001@2 IDEA-001 |
| OUT-002 | A run leader knows the expected number before leaving home. | Leader reports, per session, whether the number they expected matched who arrived. | Unknown. | Decision needed. | IDEAS-001@2 IDEA-002 |

## Functional requirements

| Requirement ID | Behavior | User / trigger | Observable result | Source idea or constraint | Priority |
| --- | --- | --- | --- | --- | --- |
| REQ-001 | Show this week's sessions with time, meeting point, route name, pace groups and an on/off state. | Any visitor opening the page. | The current week's sessions are listed with all five fields and a state of on, cancelled or moved. | IDEAS-001@2 IDEA-001 | MVP |
| REQ-002 | A member marks themselves in or out for a session. | A member on the session page. | The member's state changes and is visible to leaders within one page refresh. | IDEAS-001@2 IDEA-002 | MVP |
| REQ-003 | A leader sets a session's state to cancelled or moved with a short reason. | A run leader. | The session's state and reason change on the page for every visitor. | IDEAS-001@2 IDEA-001 | MVP |
| REQ-004 | A leader sees the list of members marked in for a session. | A run leader. | The count and the names are shown for the selected session. | IDEAS-001@2 IDEA-002 | MVP |

## Nonfunctional requirements

| Requirement ID | Concern | Measurable criterion | Conditions | Evidence / source | Decision state |
| --- | --- | --- | --- | --- | --- |
| NFR-001 | Operations | The page renders usably on a 2019-era Android phone over a 3G connection. | The reference device is the oldest phone among the four leaders. | User constraint, Ada 2026-08-28 | adopted |
| NFR-002 | Security | Only a member of the club can mark someone in or out, and only a leader can change a session state. | All write paths. | Proposed by the assistant; Ada has not ruled on the mechanism. | proposed |

## MVP or iteration boundary

- Included requirement IDs: REQ-001, REQ-002, REQ-003, REQ-004, NFR-001
- Explicit non-goals: replacing the club's group chat for conversation; a route library (IDEA-003); push notifications of any kind (IDEA-004); anything that requires installing an app.
- Deferred work and rationale: IDEA-003 and IDEA-004 are deferred until DEC-001's outcomes have a baseline; both would widen the release past what one volunteer can build.
- Constraints already adopted: NFR-001, per Ada's stated constraint of 2026-08-28.
- Unresolved choices and owners: NFR-002's mechanism (Ada). OUT-001 and OUT-002 targets (Ada, after one week of counting).

## Discovery evidence

| Evidence ID | Claim | Source URL or immutable file | Version / retrieval date | Observation or inference | Limit |
| --- | --- | --- | --- | --- | --- |
| EVID-001 | Members repeatedly ask whether a session is still on. | IDEAS-001@2, IDEA-001, reporting the secretary's own account. | 2026-08-28 | Observation of one person's report, not of the chat itself. | One informant. No count exists. |

## Acceptance and continuation

Adopted by Ada on 2026-09-01 for REQ-001 through REQ-004 and NFR-001. NFR-002 remains a proposal. Continuation: devforge-design for the session page flows; devforge-architect for the stack, which has not been chosen.
