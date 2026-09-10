---
schema_version: "devforge.artifact/v1"
artifact_id: "ARCH-001"
artifact_type: "architecture-contract"
project_id: "shiftline"
revision: 2
status: accepted
created_at_utc: "2026-08-26T15:02:00Z"
producer:
  skill: "devforge-architect"
  skill_revision: "unknown (synthetic fixture; no skill produced these bytes)"
execution_ref: null
upstream:
  - artifact_id: PROD-001
    revision: 2
    store: project
    path: docs/devforge/product/PROD-001.md
    sections:
      - REQ-001
      - REQ-002
      - REQ-003
      - REQ-005
      - NFR-001
evidence: []
supersedes: null
decision_ref: "user adoption recorded 2026-08-26 (synthetic)"
missing_inputs: []
---

# Architecture and project contract — Shiftline

**Synthetic fixture.** These rules govern nothing real.

## Scope, current system, and requirement coverage

Greenfield. Covers PROD-001 revision 2 requirements REQ-001, REQ-002, REQ-003, REQ-005 and NFR-001.
REQ-004 is listed as an open behaviour and no rule constrains it yet.

## Architecture decisions

| ADR ID | Requirement references | Decision | Alternatives / rationale | Decision state | Adoption reference |
| --- | --- | --- | --- | --- | --- |
| ADR-001 | REQ-001, REQ-002 | Single Python service with a SQLite store | Rejected a hosted queue as unnecessary for one site | accepted | 2026-08-26 adoption |
| ADR-002 | NFR-001 | Append-only swap event log, never updated in place | Rejected mutable rows because history must survive | accepted | 2026-08-26 adoption |

## Approved stack and version-specific knowledge

| Rule ID | Capability | Package/provider | Exact version or accepted range | Real manifest/lockfile | Verified API reference | Decision reference |
| --- | --- | --- | --- | --- | --- | --- |
| RULE-001 | Persistence | sqlite3 (standard library) | Python 3.12 | dependencies.json | Python 3.12 sqlite3 docs, retrieved 2026-08-24 | ADR-001 |
| RULE-002 | Runtime | CPython | 3.12.x | dependencies.json | — | ADR-001 |

A newer release is a research trigger, not an approved upgrade. No substitution of the persistence
package is permitted without an amendment.

## Source tree and dependency boundaries

| Rule ID | Path / module | Responsibility | Allowed dependencies | Prohibited placement or direction |
| --- | --- | --- | --- | --- |
| RULE-003 | `src/shiftline/domain/` | Swap rules and eligibility | standard library only | must not import `storage` or `web` |
| RULE-004 | `src/shiftline/storage/` | SQLite access and the event log | `domain` | must not import `web` |
| RULE-005 | `src/shiftline/web/` | HTTP entry points | `domain`, `storage` | no business rules here |

## Data, API, and integration contracts

| Contract ID | Owner | Inputs/outputs | Errors and authorization | Compatibility rule | Requirement reference |
| --- | --- | --- | --- | --- | --- |
| API-001 | `web.offers` | Create offer; list offers; claim offer | Refusal carries a machine-readable reason code | Reason codes are additive only | REQ-001, REQ-002, REQ-003 |

## Verification and operations

| Rule ID | Applicable work | Required check | Exact command / adapter | Environment | Failure / unavailable handling |
| --- | --- | --- | --- | --- | --- |
| RULE-006 | Any production behaviour change | Test-first: a failing assertion before the implementation | `python3 -m unittest` under the project's declared test root | Linux, Python 3.12 | A skipped or empty suite is not a failing assertion |

- Security and tenant boundaries: one site per deployment; no cross-site read path exists
- Migration, recovery, and observability: append-only event log is the recovery record
- Prototype adoption policy: no prototype has been hardened for production
- Worktree/session and integration policy: one writer per worktree, per the execution contract
- External enforcement coverage: the DevForge CLI covers the project candidate's structural policy and
  the RED-to-GREEN workflow. No adapter checks planning artifacts.

## Expertise map

| Capability ID | Concrete task/goal | Required behavior | Relevant source references |
| --- | --- | --- | --- |
| CAP-001 | Implement swap eligibility and refusal rules in `domain` | Knows the minimum-staffing rule, the reason codes, and the import boundary | RULE-003, API-001, REQ-003 |
| CAP-002 | Implement the append-only event log in `storage` | Knows ADR-002, the sqlite3 version and the no-update-in-place rule | RULE-001, RULE-004, ADR-002 |

Current availability is derived from package and evaluation records; do not update this contract to
change a capability's readiness status.
