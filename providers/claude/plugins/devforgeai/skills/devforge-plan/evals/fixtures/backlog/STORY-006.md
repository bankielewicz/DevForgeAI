---
schema_version: "devforge.artifact/v1"
artifact_id: "STORY-006"
artifact_type: "story"
project_id: "shiftline"
revision: 1
status: accepted
created_at_utc: "2026-09-01T09:45:00Z"
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
      - NFR-001
evidence: []
supersedes: null
decision_ref: "user adoption recorded 2026-09-01 (synthetic)"
missing_inputs: []
---

# Story specification

**Synthetic fixture.** An accepted, completed story. CHG-004 does not touch it, and it should come out
of an amendment pass unchanged and at revision 1.

## Outcome, scope, and provenance

- Epic reference: EPIC-002@1
- User / trigger / desired result: every accepted swap writes an append-only audit row
- Requirement references: PROD-001@2:NFR-001
- Architecture rule references: ARCH-001@2:ADR-002, ARCH-001@2:RULE-004
- Design/prototype references where relevant: none applicable
- Explicit non-goals: refusal auditing, retention policy

## Behavioral acceptance criteria

| AC ID | Given | When | Then / observable failure behavior | Requirement reference | Intended verification |
| --- | --- | --- | --- | --- | --- |
| AC-001 | A swap is accepted | The transaction commits | One event row records actor, time and prior assignment; failure is a missing row | NFR-001 | Behavioral test asserting the row |
| AC-002 | An event row exists | Any later write occurs | The existing row is unchanged; failure is any in-place update | NFR-001 | Behavioral test comparing row bytes before and after |

## Development scope and dependencies

- Allowed source/test paths: `src/shiftline/storage/events.py`, `tests/test_events.py`
- Protected or excluded paths: `src/shiftline/web/`
- Prerequisite stories and accepted revisions: none
- Expected interface impact: none external
- Shared external resources needing isolation: the project SQLite file
- Applicable test policy and runner: ARCH-001@2:RULE-006 — `python3 -m unittest`
- Open behavior decisions: none

## Required expertise

| Capability ID | Reason | Required behavior / governing rules | Required before implementation? |
| --- | --- | --- | --- |
| CAP-002 | Owns the append-only event log | Knows ADR-002 and RULE-004 | yes |

The selected package and evaluation are execution bindings in DEV/handoff records.

## Bounded context packet

From ARCH-001@2, ADR-002: the swap event log is append-only and never updated in place.

## Specification readiness and execution handoff

- Specification readiness: resolved
- Execution readiness: determined from current dependencies, expertise, and assignment in the
  handoff/DEV record; not an amendment to this story.
- Unresolved dependencies: none
- Handoff reference: HANDOFF-004@1
