---
schema_version: "devforge.artifact/v1"
artifact_id: "STORY-005"
artifact_type: "story"
project_id: "shiftline"
revision: 1
status: accepted
created_at_utc: "2026-09-01T09:30:00Z"
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
decision_ref: "user adoption recorded 2026-09-01 (synthetic)"
missing_inputs: []
---

# Story specification

**Synthetic fixture.** An accepted story that CHG-004 affects.

## Outcome, scope, and provenance

- Epic reference: EPIC-002@1
- User / trigger / desired result: the coordinator opens a shift and reads its swap history
- Requirement references: PROD-001@2:REQ-005
- Architecture rule references: ARCH-001@2:RULE-004
- Design/prototype references where relevant: none applicable
- Explicit non-goals: export, editing history

## Behavioral acceptance criteria

| AC ID | Given | When | Then / observable failure behavior | Requirement reference | Intended verification |
| --- | --- | --- | --- | --- | --- |
| AC-001 | Shift S has two accepted swaps | The coordinator opens S | Both are listed oldest first with actor and time; failure is a missing entry or reversed order | REQ-005 | Behavioral test against the history endpoint |
| AC-002 | Shift S has no swaps | The coordinator opens S | An empty history is shown, not an error; failure is any error response | REQ-005 | Behavioral test asserting an empty list |

## Development scope and dependencies

- Allowed source/test paths: `src/shiftline/web/history.py`, `tests/test_history.py`
- Protected or excluded paths: `src/shiftline/domain/`
- Prerequisite stories and accepted revisions: STORY-006@1
- Expected interface impact: adds a read-only history endpoint to API-001
- Shared external resources needing isolation: the project SQLite file
- Applicable test policy and runner: ARCH-001@2:RULE-006 — `python3 -m unittest`
- Open behavior decisions: none

## Required expertise

| Capability ID | Reason | Required behavior / governing rules | Required before implementation? |
| --- | --- | --- | --- |
| CAP-002 | Reads the append-only event log | Knows ADR-002 and RULE-004 | yes |

The selected package and evaluation are execution bindings in DEV/handoff records.

## Bounded context packet

From ARCH-001@2, RULE-004: `src/shiftline/storage/` owns SQLite access and the event log and must not
import `web`.

## Specification readiness and execution handoff

- Specification readiness: resolved
- Execution readiness: determined from current dependencies, expertise, and assignment in the
  handoff/DEV record; not an amendment to this story.
- Unresolved dependencies: none
- Handoff reference: HANDOFF-004@1
