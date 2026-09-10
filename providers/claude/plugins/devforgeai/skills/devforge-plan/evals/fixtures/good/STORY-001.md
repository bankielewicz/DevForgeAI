---
schema_version: "devforge.artifact/v1"
artifact_id: "STORY-001"
artifact_type: "story"
project_id: "shiftline"
revision: 1
status: draft
created_at_utc: "2026-09-02T10:22:00Z"
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
  - artifact_id: ARCH-001
    revision: 2
    store: project
    path: docs/devforge/architecture/ARCH-001.md
    sha256: "107ce6fab5b5b944fd0f7b66c8c342f007c7ad2132b6f83aa1e4b3ede50da427"
    sections:
      - RULE-003
      - RULE-004
      - RULE-006
      - API-001
      - CAP-001
evidence: []
supersedes: null
decision_ref: null
missing_inputs: []
---

# Story specification

**Synthetic fixture.** A conforming story, written against the `shared/` fixtures.

## Outcome, scope, and provenance

- Epic reference: EPIC-001@1
- User / trigger / desired result: a rostered volunteer opens one of their assigned shifts and offers it
  for swap; the shift becomes visible as an open offer to volunteers eligible to claim it
- Requirement references: PROD-001@2:REQ-001
- Architecture rule references: ARCH-001@2:RULE-003, ARCH-001@2:RULE-004, ARCH-001@2:API-001
- Design/prototype references where relevant: UX-001@1:FLOW-001 is referenced as a **proposed** design
  only; its withdraw path is not adopted and is not in scope here
- Explicit non-goals: claiming an offer (STORY-002), refusal on minimum staffing (STORY-003), eligibility
  denial behaviour (STORY-004), withdrawing an offer (no requirement covers it)

## Behavioral acceptance criteria

| AC ID | Given | When | Then / observable failure behavior | Requirement reference | Intended verification |
| --- | --- | --- | --- | --- | --- |
| AC-001 | A volunteer is assigned to shift S | They offer S for swap | S appears in the open-offers list for volunteers rostered to the same site; failure is S absent from that list | REQ-001 | Behavioral test against `web.offers` list endpoint |
| AC-002 | A volunteer is not assigned to shift S | They attempt to offer S | The attempt is refused with reason code `not_assigned` and S does not enter the offers list; failure is any state change to S | REQ-001 | Behavioral test asserting the refusal reason code |
| AC-003 | Shift S is already offered | The same volunteer offers S again | The second attempt is refused with reason code `already_offered` and exactly one offer exists for S; failure is a duplicate offer row | REQ-001 | Behavioral test counting offer rows |
| AC-004 | Any offer is created | The offer is written | An append-only event row records actor, time and prior assignment; failure is an in-place update of an existing row | NFR-001, ADR-002 | Behavioral test asserting the event row and no row mutation |

## Development scope and dependencies

- Allowed source/test paths: `src/shiftline/domain/offers.py`, `src/shiftline/storage/offers.py`,
  `src/shiftline/web/offers.py`, `tests/test_offers.py`
- Protected or excluded paths: `src/shiftline/web/roster.py`, the migration directory, `dependencies.json`
- Prerequisite stories and accepted revisions: none
- Expected interface impact: adds `create_offer` and `list_offers` to API-001; reason codes are additive
- Shared external resources needing isolation: the project SQLite file; use a per-test database
- Applicable test policy and runner: ARCH-001@2:RULE-006 — a failing assertion before the
  implementation, run with `python3 -m unittest` under the declared test root
- Open behavior decisions: none for this story; REQ-004's denial behaviour is carried by STORY-004

## Required expertise

| Capability ID | Reason | Required behavior / governing rules | Required before implementation? |
| --- | --- | --- | --- |
| CAP-001 | Offer eligibility and reason codes live in `domain` | Knows the import boundary in RULE-003 and the additive reason-code rule in API-001 | yes |
| CAP-002 | The offer event row is append-only | Knows ADR-002 and RULE-004 | yes |

CAP-001 and CAP-002 are declared capability needs. No expert package is named here; whether one exists,
is installed or has been evaluated is an execution binding recorded elsewhere, not a fact this story
asserts. The selected package and evaluation are execution bindings in DEV/handoff records. Do not
revise an accepted story merely to record that its expert was installed.

## Bounded context packet

From ARCH-001@2 (`107ce6fab5b5b944fd0f7b66c8c342f007c7ad2132b6f83aa1e4b3ede50da427`), RULE-003:
`src/shiftline/domain/` carries swap rules and eligibility, may depend on the standard library only, and
must not import `storage` or `web`.

From ARCH-001@2, API-001: refusals carry a machine-readable reason code, and reason codes are additive
only.

Excerpts do not replace source authority; resolve ARCH-001@2 for anything not quoted here.

## Specification readiness and execution handoff

- Specification readiness: resolved — every acceptance criterion has an observable failure behaviour and
  a requirement reference
- Execution readiness: determined from current dependencies, expertise, and assignment in the
  handoff/DEV record; not an amendment to this story.
- Unresolved dependencies: none
- Handoff reference: HANDOFF-001@1
