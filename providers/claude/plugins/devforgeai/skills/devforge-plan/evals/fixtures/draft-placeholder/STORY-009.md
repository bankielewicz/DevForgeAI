---
schema_version: "devforge.artifact/v1"
artifact_id: "STORY-009"
artifact_type: "story"
project_id: "shiftline"
revision: 1
status: draft
created_at_utc: "2026-09-03T08:15:00Z"
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
evidence: []
supersedes: null
decision_ref: null
missing_inputs: []
---

# Story specification

**Synthetic fixture.** This story is complete in shape and has a template placeholder surviving in a
required field. It is a draft and cannot be presented as ready. The defect is deliberate.

## Outcome, scope, and provenance

- Epic reference: EPIC-001@1
- User / trigger / desired result: the coordinator opens a shift and reads its ordered swap history
- Requirement references: PROD-001@2:REQ-005
- Architecture rule references: ARCH-001@2:RULE-004, ARCH-001@2:ADR-002
- Design/prototype references where relevant: none applicable
- Explicit non-goals: exporting the history, editing a past swap

## Behavioral acceptance criteria

| AC ID | Given | When | Then / observable failure behavior | Requirement reference | Intended verification |
| --- | --- | --- | --- | --- | --- |
| AC-001 | Shift S has two accepted swaps | The coordinator opens S | Both swaps are listed oldest first with actor and time; failure is a missing entry or reversed order | REQ-005 | Behavioral test against the history endpoint |
| AC-002 | Shift S has no swaps | The coordinator opens S | An empty history is shown, not an error; failure is any error response | REQ-005 | Behavioral test asserting an empty list |

## Development scope and dependencies

- Allowed source/test paths: `src/shiftline/web/history.py`, `src/shiftline/storage/events.py`,
  `tests/test_history.py`
- Protected or excluded paths: `src/shiftline/domain/`, the migration directory
- Prerequisite stories and accepted revisions: STORY-002@1
- Expected interface impact: adds a read-only history endpoint to API-001
- Shared external resources needing isolation: the project SQLite file
- Applicable test policy and runner: {{ARCH rule and supported adapter}}
- Open behavior decisions: none

## Required expertise

| Capability ID | Reason | Required behavior / governing rules | Required before implementation? |
| --- | --- | --- | --- |
| CAP-002 | Reads the append-only event log | Knows ADR-002 and RULE-004 | yes |

The selected package and evaluation are execution bindings in DEV/handoff records. Do not revise an
accepted story merely to record that its expert was installed.

## Bounded context packet

From ARCH-001@2, ADR-002: the swap event log is append-only and is never updated in place.

## Specification readiness and execution handoff

- Specification readiness: blocked — the test policy field still holds a template placeholder
- Execution readiness: determined from current dependencies, expertise, and assignment in the
  handoff/DEV record; not an amendment to this story.
- Unresolved dependencies: none
- Handoff reference: HANDOFF-002@1
