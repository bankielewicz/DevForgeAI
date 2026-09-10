---
schema_version: "devforge.artifact/v1"
artifact_id: "XREPORT-007"
artifact_type: "prototype-report"
project_id: "ferrymap"
revision: 1
status: draft
created_at_utc: "2026-09-08T16:02:00Z"
producer:
  skill: "devforge-prototype"
  skill_revision: "unknown - synthetic fixture"
execution_ref: "SESSION-208@1"
upstream: []
evidence: []
supersedes: null
decision_ref: null
missing_inputs: []
---

# Prototype observations and disposition

Synthetic fixture. This report was presented as ready while a required field still holds a
template placeholder, so it is a draft and cannot be presented as ready.

## Experiment identity

- artifact_id: XREPORT-007
- Plan reference: XPLAN-007@1
- Prototype directory / snapshot: experiments/XPLAN-007/
- File manifest and hash: experiments/XPLAN-007/manifest.json
- Runtime and relevant configuration: PostgreSQL 16.3, local container
- Execution assignment: SESSION-208@1

## Actual observations

| Case ID | Observed output / measurement | Evidence reference | Outcome | Limit or failure cause |
| --- | --- | --- | --- | --- |
| XPCASE-001 | p95 238 ms at 400 viewers | evidence/run-1.txt | threshold met | Loopback only |

## Interpretation

Observed: p95 238 ms against the 250 ms threshold recorded in XPLAN-007@1.

## Disposition

- Proposed disposition: {{discard / reference / candidate-for-hardening}}
- User decision reference: null
- Required production hardening: {{security, tests, persistence, migration, or other applicable work}}
- Changed product/design/architecture assumptions: ARCH-014@2 section s4
- Reproduction steps: experiments/XPLAN-007/RUN.md
- Next experiment or owning skill: the owner of ARCH-014
- Handoff reference: HANDOFF-092@1
