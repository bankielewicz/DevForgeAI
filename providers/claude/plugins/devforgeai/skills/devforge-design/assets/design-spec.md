---
schema_version: "devforge.artifact/v1"
artifact_id: "UX-{{number}}"
artifact_type: "design-spec"
project_id: "{{project_id}}"
revision: 1
status: draft
created_at_utc: "{{ISO-8601-UTC-time}}"
producer:
  skill: "devforge-design"
  skill_revision: "{{exact-skill-revision-or-digest}}"
execution_ref: "{{SESSION-ID}}@{{revision}}"
upstream: []
evidence: []
supersedes: null
decision_ref: null
missing_inputs: []
---

# Experience and mockup specification

## Scope and requirement coverage

| Requirement reference | User goal | Flow ID | Design state |
| --- | --- | --- | --- |
| {{PROD-ID@revision:REQ-ID}} | {{goal}} | FLOW-001 | proposed |

## Journeys and interaction states

| Flow ID | Step / screen | Entry condition | User action | Result / next state | Requirement reference |
| --- | --- | --- | --- | --- | --- |
| FLOW-001 | {{screen}} | {{condition}} | {{action}} | {{result}} | {{requirement}} |

| State ID | Normal / loading / empty / error | Content and controls | Recovery | Keyboard/accessibility behavior |
| --- | --- | --- | --- | --- |
| UXS-001 | {{state}} | {{content}} | {{recovery}} | {{behavior}} |

## Mockup assets and preview

| Asset path | SHA-256 | Covered flow/state IDs | Preview instruction | Inspection result |
| --- | --- | --- | --- | --- |
| {{relative path}} | {{digest}} | {{IDs}} | {{exact local preview command or file}} | NOT_RUN |

## Feedback and iterations

| Feedback ID | Source | Requested change | Affected requirement/flow | Disposition | Resulting revision |
| --- | --- | --- | --- | --- | --- |
| FB-001 | {{user observation}} | {{change}} | {{IDs}} | {{adopted/proposed/declined}} | {{revision}} |

## Decisions and technical questions

{{Accepted interaction decisions, unresolved questions for a prototype, and limits of what the mockup demonstrates.}}

## Handoff

{{HANDOFF-ID@revision; accepted asset identities and remaining uncertainties.}}
