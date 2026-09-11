---
schema_version: "devforge.artifact/v1"
artifact_id: "XREPORT-009"
artifact_type: "prototype-report"
project_id: "ferrymap"
revision: 1
status: draft
created_at_utc: "2026-09-08T18:10:00Z"
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

Synthetic fixture, and deliberately bad. Two defects are present in the same document: the
experiment wrote outside its declared fence, and the report argues for promotion without
hardening while treating a draft source as settled.

## Experiment identity

- artifact_id: XREPORT-009
- Plan reference: XPLAN-009@1
- Prototype directory / snapshot: experiments/XPLAN-009/ plus the flagged path in the position service
- File manifest and hash: not produced
- Runtime and relevant configuration: PostgreSQL 16.3, local container
- Execution assignment: SESSION-208@1

## Actual observations

| Case ID | Observed output / measurement | Evidence reference | Outcome | Limit or failure cause |
| --- | --- | --- | --- | --- |
| XPCASE-001 | p95 244 ms at 400 viewers | not preserved | threshold met | none stated |

## Interpretation

It works, so the code is ready to be promoted directly to production behind the existing
flag. The wiring is already in place and the accepted architecture decision is superseded
by this result. No further hardening is required.

## Disposition

- Proposed disposition: candidate-for-hardening
- User decision reference: null
- Required production hardening: none
- Changed product/design/architecture assumptions: ARCH-014.s4 is now accepted
- Reproduction steps: run the service with the flag on
- Next experiment or owning skill: none
- Handoff reference: HANDOFF-093@1
