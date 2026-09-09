---
schema_version: "devforge.artifact/v1"
artifact_id: "XPLAN-{{number}}"
artifact_type: "experiment-plan"
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

# Prototype experiment plan

## Decision this experiment informs

- Source requirement/decision references: {{IDs and exact revisions}}
- Hypothesis: {{falsifiable statement}}
- Why inspection alone is insufficient: {{reason}}
- Permitted prototype path: {{workspace-relative fence}}
- Allowed tools and services: {{approved capabilities}}
- Time/resource bound: {{actual bound}}
- Stop conditions: {{resource, authority, or feasibility conditions}}

## Cases and observation method

| Case ID | Setup / input | Observation method | Success threshold | Failure condition | Source |
| --- | --- | --- | --- | --- | --- |
| XPCASE-001 | {{setup}} | {{measurement}} | {{threshold}} | {{failure}} | {{source}} |

## Expected deliverables

{{Prototype files, reproducible execution steps, raw observations, and a prototype-report.}}

## Pre-execution record

- Plan identity frozen before execution: {{artifact revision and external hash reference}}
- Unresolved choices: {{items}}
- Measurement limitations: {{limits}}
- Production status: experiment only; disposition is decided from observations.
