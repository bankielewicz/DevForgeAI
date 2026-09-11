---
schema_version: "devforge.artifact/v1"
artifact_id: "ARCH-005"
artifact_type: "architecture-contract"
project_id: "{{project_id}}"
revision: 1
status: draft
created_at_utc: "{{ISO-8601-UTC-time}}"
producer:
  skill: "devforge-architect"
  skill_revision: "unknown (synthetic fixture)"
execution_ref: null
upstream: []
evidence: []
supersedes: null
decision_ref: null
missing_inputs: []
---

# Architecture and project contract

Synthetic fixture: a partly filled draft, deliberately still holding template
placeholders in required fields. It exists so that "this is a draft and cannot be
presented as ready" has something concrete behind it.

## Scope, current system, and requirement coverage

A first slice of the reporting service. Existing repository observations are
recorded in the inventory note beside this file.

## Architecture decisions

| ADR ID | Requirement references | Decision | Alternatives / rationale | Decision state | Adoption reference |
| --- | --- | --- | --- | --- | --- |
| ADR-001 | REQ-010 | Read the CSV with csv-parse 5.5.6, already in the manifest | Hand-rolled parsing was rejected: quoting rules are the whole problem | proposed | null |
| ADR-002 | NFR-010 | {{choice}} | {{evidence-backed rationale}} | proposed | null |

## Approved stack and version-specific knowledge

| Rule ID | Capability | Package/provider | Exact version or accepted range | Real manifest/lockfile | Verified API reference | Decision reference |
| --- | --- | --- | --- | --- | --- | --- |
| RULE-001 | CSV import | csv-parse | 5.5.6 | package.json | {{URL/version/date}} | ADR-001 |

## Verification and operations

| Rule ID | Applicable work | Required check | Exact command / adapter | Environment | Failure / unavailable handling |
| --- | --- | --- | --- | --- | --- |
| RULE-003 | import behaviour | unit tests | npm test | Node 20.11.0 | block the dependent claim; no adapter is implemented |

## Contract adoption and handoff

{{Exact adopted revision, remaining proposals, external policy owner, and HANDOFF reference.}}
