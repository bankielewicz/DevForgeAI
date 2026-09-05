---
schema_version: "devforge.artifact/v1"
artifact_id: "ARCH-{{number}}"
artifact_type: "architecture-contract"
project_id: "{{project_id}}"
revision: 1
status: draft
created_at_utc: "{{ISO-8601-UTC-time}}"
producer:
  skill: "devforge-architect"
  skill_revision: "{{exact-skill-revision-or-digest}}"
execution_ref: "{{SESSION-ID}}@{{revision}}"
upstream: []
evidence: []
supersedes: null
decision_ref: null
missing_inputs: []
---

# Architecture and project contract

## Scope, current system, and requirement coverage

{{Delivery slice, existing repository observations, relevant product/design/prototype references, and unresolved gaps.}}

## Architecture decisions

| ADR ID | Requirement references | Decision | Alternatives / rationale | Decision state | Adoption reference |
| --- | --- | --- | --- | --- | --- |
| ADR-001 | {{REQ/NFR IDs}} | {{choice}} | {{evidence-backed rationale}} | proposed | null |

## Approved stack and version-specific knowledge

| Rule ID | Capability | Package/provider | Exact version or accepted range | Real manifest/lockfile | Verified API reference | Decision reference |
| --- | --- | --- | --- | --- | --- | --- |
| RULE-001 | {{persistence}} | {{selected package}} | {{version}} | {{path}} | {{URL/version/date}} | {{ADR and adoption}} |

Record prohibited substitutions and exceptions explicitly; a newer release is a research trigger, not an approved upgrade.

## Source tree and dependency boundaries

| Rule ID | Path / module | Responsibility | Allowed dependencies | Prohibited placement or direction |
| --- | --- | --- | --- | --- |
| RULE-002 | {{source path}} | {{responsibility}} | {{allowed}} | {{prohibited}} |

## Data, API, and integration contracts

| Contract ID | Owner | Inputs/outputs | Errors and authorization | Compatibility rule | Requirement reference |
| --- | --- | --- | --- | --- | --- |
| API-001 | {{module}} | {{contract}} | {{behavior}} | {{rule}} | {{requirement}} |

## Verification and operations

| Rule ID | Applicable work | Required check | Exact command / adapter | Environment | Failure / unavailable handling |
| --- | --- | --- | --- | --- | --- |
| RULE-003 | {{production behavior}} | {{TDD/test type}} | {{verified command or missing adapter}} | {{requirements}} | {{block/report rule}} |

- Security and tenant boundaries: {{applicable requirements and checks}}
- Migration, recovery, and observability: {{applicable requirements}}
- Prototype adoption policy: {{conditions}}
- Worktree/session and integration policy: {{execution contract and project-specific constraints}}
- External enforcement coverage: {{implemented adapter + evidence / unsupported}}

## Expertise map

| Capability ID | Concrete task/goal | Required behavior | Relevant source references |
| --- | --- | --- | --- |
| CAP-001 | {{task}} | {{capability expectations}} | {{rules/docs}} |

Current availability is derived from package and evaluation records; do not update this contract just to change a capability's readiness status.

## Contract adoption and handoff

{{Exact adopted revision, remaining proposals, external policy owner, and HANDOFF reference.}}
