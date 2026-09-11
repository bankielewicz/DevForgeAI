---
schema_version: "devforge.artifact/v1"
artifact_id: "XREPORT-006"
artifact_type: "prototype-report"
project_id: "ferrymap"
revision: 1
status: draft
created_at_utc: "2026-09-08T14:41:10Z"
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

# Prototype observations and disposition

Synthetic fixture. Invented project and invented numbers.

## Experiment identity

- artifact_id: XREPORT-006
- Plan reference: XPLAN-006@1
- Prototype directory / snapshot: experiments/XPLAN-006/ at branch experiment/fanout-latency
- File manifest and hash: experiments/XPLAN-006/manifest.json, listed in evidence
- Runtime and relevant configuration: PostgreSQL 16.3 in a local container, 8 vCPU / 16 GB host, single process, warm cache, loopback networking only
- Execution assignment: SESSION-208@1

## Actual observations

| Case ID | Observed output / measurement | Evidence reference | Outcome | Limit or failure cause |
| --- | --- | --- | --- | --- |
| XPCASE-001 | p95 412 ms over a 5-minute run at 400 viewers | evidence/measurements.txt lines 1-14 | threshold missed | Single machine, simulated viewers, loopback only |
| XPCASE-002 | 400 of 400 viewers resumed within 6.2 s of the restart | evidence/measurements.txt lines 15-22 | threshold met | One restart observed, not a sustained-failure test |
| XPCASE-003 | COULD_NOT_RUN | none | COULD_NOT_RUN | The load generator exhausted local file descriptors above 520 viewers; the ramp never reached 800 and no curve was recorded |

## Interpretation

Observed: at 400 viewers the p95 update latency was 412 ms, against the 250 ms threshold
recorded in XPLAN-006@1. The threshold was missed by 162 ms. Observed: reconnection after a
datastore restart was well inside its 10 s threshold. Observed: the headroom case produced
no measurement at all, so nothing is established above 400 viewers.

Recommended: ARCH-014.s4 is not supportable as written by this approach on this hardware.
The two recommendations worth putting to the owner of ARCH-014 are a larger latency budget
paired with the accepted age indicator in ARCH-011.s3, or client polling at a stated
interval. Both are proposals; neither is adopted here.

## Disposition

- Proposed disposition: keep as reference
- User decision reference: null
- Required production hardening: authentication on the connection, backpressure and
  connection limits, reconnection storms, error handling, tests, observability, and a
  measurement on representative hardware rather than a loopback host
- Changed product/design/architecture assumptions: ARCH-014@2 section s4 - the 250 ms
  figure is not met by this approach and is named here for its owner, not amended
- Reproduction steps: experiments/XPLAN-006/RUN.md, verified once end to end on 2026-09-08
- Next experiment or owning skill: the owner of ARCH-014 decides between a revised budget
  and polling; a further experiment is only warranted if a budget is chosen and its value
  is itself uncertain
- Handoff reference: HANDOFF-091@1
- Unavailable measurements: XPCASE-003 recorded COULD_NOT_RUN with its cause; no claim is
  made about behaviour above 400 viewers
