---
schema_version: "devforge.artifact/v1"
artifact_id: "EPIC-002"
artifact_type: "epic"
project_id: "shiftline"
revision: 1
status: accepted
created_at_utc: "2026-09-01T09:00:00Z"
producer:
  skill: "devforge-plan"
  skill_revision: "unknown (synthetic fixture; no installed skill produced these bytes)"
execution_ref: null
upstream:
  - artifact_id: PROD-001
    revision: 2
    store: project
    path: docs/devforge/product/PROD-001.md
    sha256: "6a24a663b0472fdbb1eab071c02abc744d8c3d817a08627c07bb1056c2775d14"
    sections:
      - REQ-005
      - NFR-001
evidence: []
supersedes: null
decision_ref: "user adoption recorded 2026-09-01 (synthetic)"
missing_inputs: []
---

# Epic

**Synthetic fixture.** An existing, accepted epic with two member stories. It stages the case where
someone asks what to implement next, and the case where an accepted amendment revises only the affected
stories rather than regenerating the backlog.

## Outcome and source coverage

- User-visible outcome: the coordinator can see and trust the swap history for any shift
- Delivery slice: PROD-001@2
- Requirement references: REQ-005, NFR-001
- Governing architecture reference: ARCH-001@2, rules RULE-004, ADR-002
- Non-goals: exporting the history, editing a past swap, retention policy

## Story membership and dependency order

| Allocated story ID | Useful outcome | Requirement coverage | Depends on | Definition state |
| --- | --- | --- | --- | --- |
| STORY-005 | The coordinator reads a shift's ordered swap history | REQ-005 | STORY-006 | authored |
| STORY-006 | Every accepted swap writes an append-only audit row | NFR-001 | none | authored, accepted |

## Coverage and delivery readiness

| Requirement | Covered by stories | Deferred / unresolved part | Rationale and decision reference |
| --- | --- | --- | --- |
| REQ-005 | STORY-005 | none | — |
| NFR-001 | STORY-006 | none | ADR-002 |

- Optional sprint grouping: none
- Cross-story integration checks: a swap written by STORY-006 is readable by STORY-005
- Shared files or resources needing serialized integration: the event table
- Completion evidence: STORY-006 accepted 2026-09-04 (synthetic); STORY-005 not started
- Handoff reference: HANDOFF-004@1
