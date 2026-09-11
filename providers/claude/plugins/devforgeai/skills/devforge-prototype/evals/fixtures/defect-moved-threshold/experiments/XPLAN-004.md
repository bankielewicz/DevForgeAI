---
schema_version: "devforge.artifact/v1"
artifact_id: "XPLAN-010"
artifact_type: "experiment-plan"
project_id: "ferrymap"
revision: 1
status: draft
created_at_utc: "2026-09-09T08:00:00Z"
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

# Prototype experiment plan

Synthetic fixture. Paired with XREPORT-004.md, which moves this plan's threshold.

## Decision this experiment informs

- Source requirement/decision references: ARCH-014@2 section s4 (draft)
- Hypothesis: the fan-out approach keeps p95 end-to-end update latency at or under 250 ms with 400 concurrent viewers
- Why inspection alone is insufficient: the path does not exist in this codebase
- Permitted prototype path: experiments/XPLAN-010/
- Allowed tools and services: local container and repository harness only
- Time/resource bound: 3 hours
- Stop conditions: the time bound; anything outside the permitted path

## Cases and observation method

| Case ID | Setup / input | Observation method | Success threshold | Failure condition | Source |
| --- | --- | --- | --- | --- | --- |
| XPCASE-001 | 400 viewers, one route | p95 over a 5-minute run | p95 at or under 250 ms | p95 above 250 ms | ARCH-014.s4 |

## Expected deliverables

Prototype files, reproduction steps, raw latency output, and a prototype-report.

## Pre-execution record

- Plan identity frozen before execution: revision 1 hashed at 2026-09-09T08:03:00Z, self-recorded
- Unresolved choices: none
- Measurement limitations: one machine, loopback transport
- Production status: experiment only; disposition is decided from observations
