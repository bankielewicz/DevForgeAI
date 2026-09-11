---
schema_version: "devforge.artifact/v1"
artifact_id: "STORY-{{number}}"
artifact_type: "story"
project_id: "{{project_id}}"
revision: 1
status: draft
created_at_utc: "{{ISO-8601-UTC-time}}"
producer:
  skill: "devforge-plan"
  skill_revision: "{{exact-skill-revision-or-digest}}"
execution_ref: "{{SESSION-ID}}@{{revision}}"
upstream: []
evidence: []
supersedes: null
decision_ref: null
missing_inputs: []
---

# Story specification

## Outcome, scope, and provenance

- Epic reference: {{EPIC-ID@revision}}
- User / trigger / desired result: {{behavior}}
- Requirement references: {{PROD-ID@revision:REQ-ID}}
- Architecture rule references: {{ARCH-ID@revision:RULE-ID}}
- Design/prototype references where relevant: {{exact references or reason not applicable}}
- Explicit non-goals: {{boundaries}}

## Behavioral acceptance criteria

| AC ID | Given | When | Then / observable failure behavior | Requirement reference | Intended verification |
| --- | --- | --- | --- | --- | --- |
| AC-001 | {{state}} | {{action}} | {{result}} | {{REQ-ID}} | {{behavioral check}} |

## Development scope and dependencies

- Allowed source/test paths: {{declared fence}}
- Protected or excluded paths: {{paths}}
- Prerequisite stories and accepted revisions: {{dependencies}}
- Expected interface impact: {{contract references}}
- Shared external resources needing isolation: {{ports/databases/fixtures or none}}
- Applicable test policy and runner: {{ARCH rule and supported adapter}}
- Open behavior decisions: {{items; readiness stays blocked if consequential}}

## Required expertise

| Capability ID | Reason | Required behavior / governing rules | Required before implementation? |
| --- | --- | --- | --- |
| CAP-001 | {{need}} | {{expectations and source rules}} | yes |

The selected package and evaluation are execution bindings in DEV/handoff records. Do not revise an accepted story merely to record that its expert was installed.

## Bounded context packet

{{Only relevant excerpts, each with its source artifact, revision, digest, and stable section ID. Excerpts do not replace source authority.}}

## Specification readiness and execution handoff

- Specification readiness: {{requirements and acceptance behavior resolved or blocked}}
- Execution readiness: determined from current dependencies, expertise, and assignment in the handoff/DEV record; not an amendment to this story.
- Unresolved dependencies: {{items}}
- Handoff reference: {{HANDOFF-ID@revision}}
