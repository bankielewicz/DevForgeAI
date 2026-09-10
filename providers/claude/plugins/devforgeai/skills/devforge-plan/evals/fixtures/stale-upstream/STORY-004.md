---
schema_version: "devforge.artifact/v1"
artifact_id: "STORY-004"
artifact_type: "story"
project_id: "shiftline"
revision: 1
status: draft
created_at_utc: "2026-09-02T11:05:00Z"
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
      - REQ-003
  - artifact_id: ARCH-001
    revision: 2
    store: project
    path: docs/devforge/architecture/ARCH-001.md
    sha256: "107ce6fab5b5b944fd0f7b66c8c342f007c7ad2132b6f83aa1e4b3ede50da427"
    sections:
      - RULE-003
      - RULE-006
      - API-001
      - CAP-001
evidence: []
supersedes: null
decision_ref: null
missing_inputs: []
---

# Story specification

**Synthetic fixture.** This story cites `ARCH-001@2` by digest. The live file at the architecture path
in this directory is revision 3 and hashes differently. The revision-2 bytes are preserved at
`preserved/ARCH-001.r2.md`. Nothing in this fixture says what should be done about that.

## Outcome, scope, and provenance

- Epic reference: EPIC-001@1
- User / trigger / desired result: a claim that would leave a shift below its minimum staffing is refused
  with a reason the volunteer can read
- Requirement references: PROD-001@2:REQ-003
- Architecture rule references: ARCH-001@2:RULE-003, ARCH-001@2:API-001
- Design/prototype references where relevant: UX-001@1:FLOW-002 is a proposed design only
- Explicit non-goals: eligibility by site (REQ-004), notification wording

## Behavioral acceptance criteria

| AC ID | Given | When | Then / observable failure behavior | Requirement reference | Intended verification |
| --- | --- | --- | --- | --- | --- |
| AC-001 | Shift S is staffed at its minimum | A volunteer claims an open offer on S | The claim is refused with reason code `below_minimum` and no roster changes; failure is any roster change | REQ-003 | Behavioral test asserting the reason code and unchanged roster |
| AC-002 | Shift S is one above its minimum | A volunteer claims an open offer on S | The claim succeeds and S is left at its minimum; failure is a refusal | REQ-003 | Behavioral test asserting the accepted claim |
| AC-003 | A claim is refused | The refusal is returned | The volunteer sees the reason code and the current staffing level as of the claim time; failure is a bare error | REQ-003 | Behavioral test asserting the payload |

AC-003 is phrased in terms of "as of the claim time". ARCH-001 revision 3 narrows RULE-003 so that the
domain layer may not read the system clock directly.

## Development scope and dependencies

- Allowed source/test paths: `src/shiftline/domain/staffing.py`, `src/shiftline/web/offers.py`,
  `tests/test_staffing.py`
- Protected or excluded paths: `src/shiftline/storage/`, the migration directory
- Prerequisite stories and accepted revisions: STORY-002@1
- Expected interface impact: adds the `below_minimum` reason code to API-001
- Shared external resources needing isolation: the project SQLite file
- Applicable test policy and runner: ARCH-001@2:RULE-006 — a failing assertion before the
  implementation, run with `python3 -m unittest`
- Open behavior decisions: none

## Required expertise

| Capability ID | Reason | Required behavior / governing rules | Required before implementation? |
| --- | --- | --- | --- |
| CAP-001 | Minimum-staffing rule lives in `domain` | Knows RULE-003 and the additive reason-code rule | yes |

The selected package and evaluation are execution bindings in DEV/handoff records.

## Bounded context packet

From ARCH-001@2 (`107ce6fab5b5b944fd0f7b66c8c342f007c7ad2132b6f83aa1e4b3ede50da427`), RULE-003:
`src/shiftline/domain/` may depend on the standard library only and must not import `storage` or `web`.

## Specification readiness and execution handoff

- Specification readiness: resolved as authored against ARCH-001@2
- Execution readiness: determined from current dependencies, expertise, and assignment in the
  handoff/DEV record; not an amendment to this story.
- Unresolved dependencies: none recorded at authoring time
- Handoff reference: HANDOFF-001@1
