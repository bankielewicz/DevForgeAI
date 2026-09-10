---
schema_version: "devforge.artifact/v1"
artifact_id: "PROD-002"
artifact_type: "product-brief"
project_id: "northgate-tool-library"
revision: 1
status: accepted
created_at_utc: "2026-08-21T14:30:00Z"
producer:
  skill: "devforge-define-product"
  skill_revision: "unknown (fixture; no installed SKILL.md was hashed)"
execution_ref: null
upstream:
  - artifact_id: "IDEAS-002"
    revision: 1
    store: project
    path: "docs/devforge/ideas/IDEAS-002.md"
    sha256: "03b523dea859ed3442d833eed9653ec6bc57cf995a14716d478e0a64959b0098"
    sections:
      - "IDEA-010"
      - "IDEA-011"
      - "DEC-002"
evidence: []
supersedes: null
decision_ref: "Sam, session of 2026-08-21"
missing_inputs: []
---

# Product brief and delivery scope

Synthetic fixture. Invented for evaluation. This brief cites IDEAS-002 at **revision 1**; the bytes now at that ledger's path are revision 2 and have a different digest.

## Problem, people, and value

Northgate Tool Library lends about 200 tools to 300 members from a shed open on Saturdays. The paper lending book is illegible and nobody can say who has what. Selected ideas: IDEA-010 and IDEA-011 from IDEAS-002@1, adopted by Sam as DEC-002.

## Outcomes and success measures

| Outcome ID | Desired outcome | Measurement | Baseline / unknown | Target / decision needed | Source |
| --- | --- | --- | --- | --- | --- |
| OUT-010 | A desk volunteer can say who holds any tool. | Sample ten tools at the end of a shift; count how many have a correct current holder. | Unknown; the paper book has never been audited. | Decision needed. | IDEAS-002@1 IDEA-011 |

## Functional requirements

| Requirement ID | Behavior | User / trigger | Observable result | Source idea or constraint | Priority |
| --- | --- | --- | --- | --- | --- |
| REQ-010 | List every tool with an on-shelf or on-loan state. | Any member or volunteer. | Each tool shows exactly one of the two states. | IDEAS-002@1 IDEA-010 | MVP |
| REQ-011 | Record a borrow against a member, and a return that clears it. | A desk volunteer. | The tool's current holder is set on borrow and cleared on return. | IDEAS-002@1 IDEA-011 | MVP |
| REQ-012 | Reservations are not supported in this release. | - | No reservation path exists. | IDEAS-002@1 DEC-002 | non-goal |

## Nonfunctional requirements

| Requirement ID | Concern | Measurable criterion | Conditions | Evidence / source | Decision state |
| --- | --- | --- | --- | --- | --- |
| NFR-010 | Operations | The desk works with no network for a whole shift and reconciles afterwards. | The shed has no reliable connection. | User constraint, Sam 2026-08-19 | adopted |

## MVP or iteration boundary

- Included requirement IDs: REQ-010, REQ-011, NFR-010
- Explicit non-goals: reservations (IDEA-012); anything member-facing outside the shed; any record of tool condition or maintenance.
- Deferred work and rationale: IDEA-012 deferred until borrowing and returning are reliable, per DEC-002.
- Constraints already adopted: NFR-010.
- Unresolved choices and owners: OUT-010's target (Sam).

## Discovery evidence

| Evidence ID | Claim | Source URL or immutable file | Version / retrieval date | Observation or inference | Limit |
| --- | --- | --- | --- | --- | --- |
| EVID-010 | The paper lending book is not reconciled. | IDEAS-002@1, IDEA-011, reporting Sam's account. | 2026-08-19 | Observation of one report. | One informant; no audit exists. |

## Acceptance and continuation

Adopted by Sam on 2026-08-21. The non-goal list rests directly on DEC-002 as recorded at IDEAS-002 revision 1.
