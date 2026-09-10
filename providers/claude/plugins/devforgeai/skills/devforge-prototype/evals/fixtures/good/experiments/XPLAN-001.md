---
schema_version: "devforge.artifact/v1"
artifact_id: "XPLAN-006"
artifact_type: "experiment-plan"
project_id: "ferrymap"
revision: 1
status: draft
created_at_utc: "2026-09-08T09:12:44Z"
producer:
  skill: "devforge-prototype"
  skill_revision: "unknown - synthetic fixture, no installed SKILL.md was hashed"
execution_ref: "SESSION-208@1"
upstream: []
evidence: []
supersedes: null
decision_ref: null
missing_inputs: []
---

# Prototype experiment plan

Synthetic fixture. Invented project and invented numbers.

## Decision this experiment informs

- Source requirement/decision references: ARCH-014@2 section s4 (draft), under accepted ARCH-009.s1 and ARCH-011.s3
- Hypothesis: a single-process fan-out over one persistent connection per viewer, reading position changes from PostgreSQL 16 LISTEN/NOTIFY, keeps p95 end-to-end update latency at or under 250 ms with 400 concurrent viewers on one route
- Why inspection alone is insufficient: the fan-out path does not exist in this codebase, the 250 ms figure came from a design workshop rather than a measurement, and the accepted single-datastore rule rules out the cache the approach would otherwise lean on
- Permitted prototype path: experiments/XPLAN-006/
- Allowed tools and services: local PostgreSQL 16 container, repository test harness, local load generation. No cloud services, no production data, no new project dependencies
- Time/resource bound: 4 hours of work; no single measurement run longer than 10 minutes
- Stop conditions: the time bound is reached; the question needs production data or a credential; any change would be required outside experiments/XPLAN-006/

## Cases and observation method

| Case ID | Setup / input | Observation method | Success threshold | Failure condition | Source |
| --- | --- | --- | --- | --- | --- |
| XPCASE-001 | 400 simulated viewers, one route, 2 position updates per second | End-to-end timestamp delta at the client stub, 5-minute run, p95 reported | p95 at or under 250 ms | p95 above 250 ms | ARCH-014.s4 |
| XPCASE-002 | Same load, one PostgreSQL restart mid-run | Count of viewers that reconnect and resume within 10 s | All viewers resume within 10 s | Any viewer stalls past 10 s | ARCH-011.s3 |
| XPCASE-003 | Load ramp to 800 viewers | p95 latency at each 100-viewer step | Recorded curve, no threshold | Run cannot sustain the ramp | Headroom question raised in the workshop |

## Expected deliverables

Prototype files under experiments/XPLAN-006/, a reproduction script invocation, raw
per-run latency output, and a prototype-report.

## Pre-execution record

- Plan identity frozen before execution: revision 1 hashed at 2026-09-08T09:14:02Z; the digest is held in the session record SESSION-208@1. No DevForge command binds a plan's bytes outside the evaluated agent's reach, so this freeze is self-recorded and is stated as such
- Unresolved choices: whether LISTEN/NOTIFY payload size will force a second query per update
- Measurement limitations: one machine, simulated viewers rather than real devices, no
  mobile radio behaviour, warm database cache throughout
- Production status: experiment only; disposition is decided from observations
