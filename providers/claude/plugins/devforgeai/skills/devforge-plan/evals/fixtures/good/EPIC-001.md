---
schema_version: "devforge.artifact/v1"
artifact_id: "EPIC-001"
artifact_type: "epic"
project_id: "shiftline"
revision: 1
status: draft
created_at_utc: "2026-09-02T10:05:00Z"
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
      - REQ-001
      - REQ-002
      - REQ-003
      - REQ-004
      - REQ-005
      - NFR-001
  - artifact_id: ARCH-001
    revision: 2
    store: project
    path: docs/devforge/architecture/ARCH-001.md
    sha256: "107ce6fab5b5b944fd0f7b66c8c342f007c7ad2132b6f83aa1e4b3ede50da427"
    sections:
      - ADR-002
      - RULE-003
      - RULE-004
      - RULE-006
      - API-001
      - CAP-001
      - CAP-002
evidence: []
supersedes: null
decision_ref: null
missing_inputs:
  - "REQ-004 denial behaviour: undefined in PROD-001@2 and unconstrained by ARCH-001@2; owner is the coordinator"
---

# Epic

**Synthetic fixture.** A conforming epic, written against the `shared/` fixtures.

## Outcome and source coverage

- User-visible outcome: a volunteer arranges a shift swap end to end without the coordinator, and the
  coordinator can see what changed
- Delivery slice: PROD-001@2
- Requirement references: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, NFR-001
- Governing architecture reference: ARCH-001@2, rules RULE-003, RULE-004, RULE-006, ADR-002, API-001
- Non-goals: shift creation, volunteer onboarding, payroll export, mobile push notifications,
  multi-site coordination

## Story membership and dependency order

| Allocated story ID | Useful outcome | Requirement coverage | Depends on | Definition state |
| --- | --- | --- | --- | --- |
| STORY-001 | A volunteer offers an assigned shift and it appears to eligible volunteers | REQ-001 | none | authored |
| STORY-002 | An eligible volunteer claims an open offer and both rosters update | REQ-002 | STORY-001 | planned |
| STORY-003 | A claim is refused when it would breach minimum staffing | REQ-003 | STORY-002 | planned |
| STORY-004 | Ineligible claims are handled per the coordinator's decision | REQ-004 | STORY-002 | blocked |
| STORY-005 | The coordinator reads a shift's swap history | REQ-005, NFR-001 | STORY-002 | planned |

Story IDs are allocated before their definitions are authored. Membership is a relationship, not a
causal dependency from this epic back to its derived stories.

## Coverage and delivery readiness

| Requirement | Covered by stories | Deferred / unresolved part | Rationale and decision reference |
| --- | --- | --- | --- |
| REQ-001 | STORY-001 | none | — |
| REQ-002 | STORY-002 | none | — |
| REQ-003 | STORY-003 | none | — |
| REQ-004 | STORY-004 | denial behaviour undefined | PROD-001@2 records the open question; coordinator owns it |
| REQ-005 | STORY-005 | none | — |
| NFR-001 | STORY-005 | none | ADR-002 append-only log |

- Optional sprint grouping: none — the user did not ask for one
- Cross-story integration checks: a swap accepted in STORY-002 appears in the history read by STORY-005
- Shared files or resources needing serialized integration: the SQLite schema touched by STORY-002 and
  STORY-005
- Completion evidence: none
- Handoff reference: HANDOFF-001@1
