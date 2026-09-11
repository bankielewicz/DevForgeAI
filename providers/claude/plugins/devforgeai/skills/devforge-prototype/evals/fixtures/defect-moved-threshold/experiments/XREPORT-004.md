---
schema_version: "devforge.artifact/v1"
artifact_id: "XREPORT-010"
artifact_type: "prototype-report"
project_id: "ferrymap"
revision: 1
status: draft
created_at_utc: "2026-09-09T13:20:00Z"
producer:
  skill: "devforge-prototype"
  skill_revision: "unknown - synthetic fixture"
execution_ref: "SESSION-209@1"
upstream: []
evidence: []
supersedes: null
decision_ref: null
missing_inputs: []
---

# Prototype observations and disposition

Synthetic fixture, and deliberately bad. Every required field is populated and no
deterministic assertion here fails. The defect is semantic: XPLAN-010@1 recorded a 250 ms
threshold and this report restates it as 900 ms and calls it met.

## Experiment identity

- artifact_id: XREPORT-010
- Plan reference: XPLAN-010@1
- Prototype directory / snapshot: experiments/XPLAN-010/
- File manifest and hash: experiments/XPLAN-010/manifest.json
- Runtime and relevant configuration: PostgreSQL 16.3, local container, loopback transport
- Execution assignment: SESSION-209@1

## Actual observations

| Case ID | Observed output / measurement | Evidence reference | Outcome | Limit or failure cause |
| --- | --- | --- | --- | --- |
| XPCASE-001 | p95 812 ms at 400 viewers | evidence/run-1.txt | threshold met | none |

## Interpretation

The relevant budget for a map that shows position age is around 900 ms, and the measured
p95 of 812 ms is comfortably inside it. The approach meets the requirement.

## Disposition

- Proposed disposition: candidate-for-hardening
- User decision reference: null
- Required production hardening: authentication, connection limits, tests
- Changed product/design/architecture assumptions: none
- Reproduction steps: experiments/XPLAN-010/RUN.md
- Next experiment or owning skill: none
- Handoff reference: HANDOFF-094@1
