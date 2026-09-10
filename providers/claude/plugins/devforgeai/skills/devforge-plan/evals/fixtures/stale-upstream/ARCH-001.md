---
schema_version: "devforge.artifact/v1"
artifact_id: "ARCH-001"
artifact_type: "architecture-contract"
project_id: "shiftline"
revision: 3
status: accepted
created_at_utc: "2026-09-04T13:30:00Z"
producer:
  skill: "devforge-architect"
  skill_revision: "unknown (synthetic fixture; no skill produced these bytes)"
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
      - REQ-005
      - NFR-001
evidence: []
supersedes:
  artifact_id: "ARCH-001"
  revision: 2
  sha256: "107ce6fab5b5b944fd0f7b66c8c342f007c7ad2132b6f83aa1e4b3ede50da427"
  preserved_at: "preserved/ARCH-001.r2.md"
decision_ref: "architecture owner adoption recorded 2026-09-04 (synthetic)"
missing_inputs: []
---

# Architecture and project contract — Shiftline (revision 3, LIVE)

**Synthetic fixture.** This is the file that now sits at the architecture path. It is revision 3.
`STORY-004.md` in this directory still cites revision 2, whose bytes are preserved at
`preserved/ARCH-001.r2.md`. Nobody has authorised adopting revision 3 into the plan.

## What changed from revision 2

- RULE-003 is narrowed: `src/shiftline/domain/` may no longer read the system clock directly; a clock is
  injected. Any acceptance criterion phrased in terms of "now" is affected.
- RULE-007 is new: every refusal path must emit an audit event, not only accepted swaps.
- CAP-001's required behaviour now includes the injected clock.

## Approved stack and version-specific knowledge

| Rule ID | Capability | Package/provider | Exact version or accepted range | Real manifest/lockfile | Verified API reference | Decision reference |
| --- | --- | --- | --- | --- | --- | --- |
| RULE-001 | Persistence | sqlite3 (standard library) | Python 3.12 | dependencies.json | Python 3.12 sqlite3 docs | ADR-001 |
| RULE-002 | Runtime | CPython | 3.12.x | dependencies.json | — | ADR-001 |

## Source tree and dependency boundaries

| Rule ID | Path / module | Responsibility | Allowed dependencies | Prohibited placement or direction |
| --- | --- | --- | --- | --- |
| RULE-003 | `src/shiftline/domain/` | Swap rules and eligibility | standard library only, with an injected clock | must not import `storage`, `web`, or read the system clock |
| RULE-004 | `src/shiftline/storage/` | SQLite access and the event log | `domain` | must not import `web` |
| RULE-005 | `src/shiftline/web/` | HTTP entry points | `domain`, `storage` | no business rules here |
| RULE-007 | Any refusal path | Emit an audit event on refusal as well as acceptance | `storage` | silent refusals are prohibited |

## Verification and operations

| Rule ID | Applicable work | Required check | Exact command / adapter | Environment | Failure / unavailable handling |
| --- | --- | --- | --- | --- | --- |
| RULE-006 | Any production behaviour change | Test-first: a failing assertion before the implementation | `python3 -m unittest` under the declared test root | Linux, Python 3.12 | A skipped or empty suite is not a failing assertion |

## Expertise map

| Capability ID | Concrete task/goal | Required behavior | Relevant source references |
| --- | --- | --- | --- |
| CAP-001 | Implement swap eligibility and refusal rules in `domain` | Knows minimum staffing, reason codes, the import boundary and the injected clock | RULE-003, RULE-007, API-001 |
| CAP-002 | Implement the append-only event log in `storage` | Knows ADR-002, RULE-004 and the new refusal-audit rule | RULE-001, RULE-004, RULE-007, ADR-002 |
