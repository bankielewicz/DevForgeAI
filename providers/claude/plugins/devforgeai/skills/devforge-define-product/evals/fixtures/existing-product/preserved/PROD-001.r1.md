---
schema_version: "devforge.artifact/v1"
artifact_id: "PROD-001"
artifact_type: "product-brief"
project_id: "riverbend-running-club"
revision: 1
status: superseded
created_at_utc: "2026-08-24T09:40:00Z"
producer:
  skill: "devforge-define-product"
  skill_revision: "unknown (fixture; no installed SKILL.md was hashed)"
execution_ref: null
upstream:
  - artifact_id: "IDEAS-001"
    revision: 1
    store: project
    path: "docs/devforge/ideas/archive/IDEAS-001.r1.md"
    sha256: "4dbe2259ecd3378c6993b2b088bfb9771db3d13bfd9a5532f8e2709637e971ac"
    sections:
      - "IDEA-001"
evidence: []
supersedes: null
decision_ref: null
missing_inputs:
  - "No baseline for how many members currently know a session is cancelled before travelling."
  - "Ada has adopted nothing yet; this revision is a draft scope for discussion."
---

# Product brief and delivery scope

Synthetic fixture. This is the **preserved revision 1** - the exact bytes that `PROD-001` revision 2 cites in its `supersedes` entry. Invented for evaluation.

## Problem, people, and value

Selected idea: IDEA-001 from IDEAS-001@1. Riverbend's members cannot reliably find out whether a session is on. Target users are the club's ~90 members and its four run leaders. Evidence is the secretary's own account; nothing has been measured.

## Outcomes and success measures

| Outcome ID | Desired outcome | Measurement | Baseline / unknown | Target / decision needed | Source |
| --- | --- | --- | --- | --- | --- |
| OUT-001 | A member can tell whether a session is on without asking anyone. | Count of "is it still on?" messages in the club group chat per week. | Unknown; nobody has counted. | Decision needed after one week of counting. | IDEAS-001@1 IDEA-001 |

## Functional requirements

| Requirement ID | Behavior | User / trigger | Observable result | Source idea or constraint | Priority |
| --- | --- | --- | --- | --- | --- |
| REQ-001 | Show this week's sessions with time, meeting point, route name, pace groups and an on/off state. | Any visitor opening the page. | The current week's sessions are listed with all five fields and a state of on, cancelled or moved. | IDEAS-001@1 IDEA-001 | MVP |
| REQ-003 | A leader sets a session's state to cancelled or moved with a short reason. | A run leader. | The session's state and reason change on the page for every visitor. | IDEAS-001@1 IDEA-001 | MVP |

## Nonfunctional requirements

| Requirement ID | Concern | Measurable criterion | Conditions | Evidence / source | Decision state |
| --- | --- | --- | --- | --- | --- |
| NFR-001 | Operations | The page renders usably on a 2019-era Android phone over a 3G connection. | The reference device is the oldest phone among the four leaders. | User constraint, Ada 2026-08-21 | adopted |

## MVP or iteration boundary

- Included requirement IDs: REQ-001, REQ-003, NFR-001
- Explicit non-goals: attendance marking; a route library; anything that requires installing an app.
- Deferred work and rationale: attendance marking deferred pending Q-001, which nobody has observed yet.
- Constraints already adopted: NFR-001, per Ada's stated constraint of 2026-08-21.
- Unresolved choices and owners: OUT-001's target (Ada); whether attendance belongs in the first release (Ada).

## Discovery evidence

| Evidence ID | Claim | Source URL or immutable file | Version / retrieval date | Observation or inference | Limit |
| --- | --- | --- | --- | --- | --- |
| EVID-001 | Members repeatedly ask whether a session is still on. | IDEAS-001@1, IDEA-001, reporting the secretary's own account. | 2026-08-21 | Observation of one person's report, not of the chat itself. | One informant. No count exists. |

## Acceptance and continuation

Nothing adopted. This revision was written for discussion and was superseded once Ada decided DEC-001.
