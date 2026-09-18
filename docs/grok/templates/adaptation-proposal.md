# Template: Adaptation proposal

**Producer:** `skill-builder` mode `propose`  
**Consumers:** human selection → `skill-builder` `author_set`; later `skill-validator` (manual request)  
**Operational schemas:** `project-evidence-v1`, `adaptation-proposal-v1`  
**Does not:** install packages, write `.agents/devforgeai/project-binding.json`, test generated skills, or implement the product.

Fill from bounded discovery. Missing facts are unknown, not proof of absence.

## Envelope

| Field | Value |
| --- | --- |
| Run ID | [UTC `YYYYMMDDTHHMMSSffffffZ`] |
| Project root | [resolved path; no silent Windows/WSL substitution] |
| Producer | skill-builder propose |
| Downstream consumer | Human, then author_set for selected members |
| Failure behavior | BLOCKED proposal may still list independently actionable members |
| Non-claims | Not an installation; not skill quality evidence; not product architecture |

## Upstream inputs

| Role | Locator | SHA-256 | Notes |
| --- | --- | --- | --- |
| User request | | | |
| Root instructions | | | |
| Manifests / docs in scope | | | |
| Existing skills | | | or none |

Discovery ceilings, exclusions, and uninspected roots: [complete / DISCOVERY_LIMIT / list].

## Facts

| ID | Category | Statement | Basis | Sources |
| --- | --- | --- | --- | --- |
| F-001 | language / toolchain / architecture / domain / development_style / requirements / existing_skills / constraint | | observed / user_supplied / unknown | |

## Requirements for the skill set

| ID | Origin | Statement | Verification |
| --- | --- | --- | --- |
| R-001 | user / source / derived | | |

## Proposed members

| ID | Name | Role | Action | Responsibility | Exclusions | Triggers | Near-misses | Parent core | Lineage |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| M-001 | | core / project_variant / expertise | retain / create / revise | | | | | digest or n/a | retained/modified/removed rows or empty |

A `project_variant` requires a distinct name, parent digest, and one lineage row per parent requirement. An `expertise` member requires domain/architecture facts or explicit user-supplied domain requirements.

## Handoffs between members

| ID | Producer | Consumer | Artifact role | Format | Required | Failure behavior |
| --- | --- | --- | --- | --- | --- | --- |
| H-001 | | | | json / text / file_set | yes / no | block_consumer / report_optional_absence |

Dependency graph must be acyclic. A consumer depends on every required producer.

## Gaps

| Code | Member | Requirement IDs | Description | Minimum resolution |
| --- | --- | --- | --- | --- |
| | | | | |

## State

- Proposal state: `PROPOSED` / `BLOCKED` / `NO_CHANGE`
- Independently actionable members: [IDs]
- Next action: human `adaptation-selection-v1` with member IDs, destinations, and permitted effects. Do not author unselected members. Do not create the operational binding here.
