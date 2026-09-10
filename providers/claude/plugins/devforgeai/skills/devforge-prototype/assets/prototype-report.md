---
schema_version: "devforge.artifact/v1"
artifact_id: "XREPORT-{{number}}"
artifact_type: "prototype-report"
project_id: "{{project_id}}"
revision: 1
status: draft
created_at_utc: "{{ISO-8601-UTC-time}}"
producer:
  skill: "devforge-prototype"
  skill_revision: "{{exact-skill-revision-or-digest}}"
execution_ref: "{{SESSION-ID}}@{{revision}}"
upstream: []
evidence: []
supersedes: null
decision_ref: null
missing_inputs: []
---

# Prototype observations and disposition

## Experiment identity

- Plan reference: {{XPLAN-ID@revision}}
- Prototype directory / snapshot: {{path or immutable reference}}
- File manifest and hash: {{reference}}
- Runtime and relevant configuration: {{observed environment}}
- Execution assignment: {{session record reference}}

## Actual observations

| Case ID | Observed output / measurement | Evidence reference | Outcome | Limit or failure cause |
| --- | --- | --- | --- | --- |
| XPCASE-001 | {{actual observation}} | {{raw output reference}} | NOT_RUN | {{cause if applicable}} |

## Interpretation

{{Explain whether the planned threshold was met. Separate observed results from recommendations.}}

## Disposition

- Proposed disposition: {{discard / reference / candidate-for-hardening}}
- User decision reference: null
- Required production hardening: {{security, tests, persistence, migration, or other applicable work}}
- Changed product/design/architecture assumptions: {{exact references}}
- Reproduction steps: {{verified commands or unavailable steps}}
- Next experiment or owning skill: {{task and reason}}
- Handoff reference: {{HANDOFF-ID@revision}}
