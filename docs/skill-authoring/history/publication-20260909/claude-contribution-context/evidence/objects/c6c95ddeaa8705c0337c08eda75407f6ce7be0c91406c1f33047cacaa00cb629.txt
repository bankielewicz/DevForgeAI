---
schema_version: "devforge.artifact/v1"
artifact_id: "XPKG-{{number}}"
artifact_type: "expert-package"
project_id: "{{project_id}}"
revision: 1
status: draft
created_at_utc: "{{ISO-8601-UTC-time}}"
producer:
  skill: "devforge-project-expert-creator"
  skill_revision: "{{exact-skill-revision-or-digest}}"
execution_ref: "{{SESSION-ID}}@{{revision}}"
upstream: []
evidence: []
supersedes: null
decision_ref: null
missing_inputs: []
---

# Expert package and provenance record

## Candidate identity

- Expert specification: {{XSPEC-ID@revision}}
- Native skill name: {{name}}
- Source skill directory: {{declared project-relative directory}}
- Package revision / manifest digest: {{identity}}
- Structural binding reference: {{external receipt or NOT_RUN}}
- Behavioral status: NOT_EVALUATED

## Package files

| Relative path | SHA-256 | Purpose | Governing knowledge/reference |
| --- | --- | --- | --- |
| SKILL.md | {{digest}} | {{activation and workflow}} | {{source refs}} |
| {{focused reference path}} | {{digest}} | {{version-specific guidance}} | {{source refs}} |

## Intended runtime targets

| Terminal | Declared compatible skill format | Required resources | Installation destination selected by operator |
| --- | --- | --- | --- |
| {{target}} | {{format}} | {{resources}} | {{destination}} |

This immutable candidate record does not carry subsequent evaluation results.
Installation receipts, observed discovery, installed hashes, and adoption belong
to EVREPORT and the external registry. Editing only a source directory is not
evidence that the terminal loaded it.

## Candidate limits

- Intended task scope: {{scope from XSPEC}}
- Missing resources or unsupported targets: {{items}}
- Prior package superseded: {{reference or none}}
- Handoff reference: {{HANDOFF-ID@revision}}

## Provider authoring and evaluation inputs

- Assigned provider source: {{canonical path}}
- Intended runtime export/install mode: {{mode; observed installed identity belongs in later evaluation}}
- Runtime file manifest: {{paths and hashes; authoring-only files excluded}}
- Authored eval cases/fixtures: {{separate paths and hashes}}
- Version-specific knowledge and refresh conditions: {{sources, applicability, and change triggers}}
