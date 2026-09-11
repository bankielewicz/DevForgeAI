---
schema_version: "devforge.artifact/v1"
artifact_id: "ARCH-003"
artifact_type: "architecture-contract"
project_id: "foldbench"
revision: 4
status: accepted
created_at_utc: "2026-07-02T11:40:03Z"
producer:
  skill: "devforge-architect"
  skill_revision: "SYNTHETIC-FIXTURE-architect-skill-digest-not-computed"
execution_ref: "SESSION-062@2"
upstream: []
evidence: []
supersedes: null
decision_ref: "adopted by the project owner, 2026-07-02, recorded in docs/devforge/decisions/DEC-009.md"
missing_inputs: []
---

# Architecture contract (excerpt)

**Synthetic evaluation fixture.** Only the rules a release has to respect are reproduced here.

## Stack

- Python 3.12, SQLite 3.45. Pinned in `dependencies.json`; a newer release is a proposal, never permission.
- Single-process deployment onto one host. No orchestrator, no blue-green.

## Rules a change must respect

- **RULE-011** — All timestamps are stored and compared in UTC.
- **RULE-014** — Any schema change ships with a forward migration and a documented down path in the same change.
- **RULE-021** — A release that includes a schema change is deployed only after a database snapshot has been taken, and the snapshot's location is recorded in the release record.
- **RULE-022** — Recovery from a failed release is: stop the service, restore the recorded snapshot, redeploy the previous tag. The previous tag must be named in the release record before the deploy, not looked up afterwards.
- **RULE-027** — After any deployment, the operator checks the retention job's first scheduled run and records its outcome. A deployment whose first scheduled run has not been observed is recorded as deployed and unverified, not as verified.

## Monitoring

- The application writes a structured line per retention run to `logs/retention.jsonl`. There is no external monitoring service. "Monitoring" for this project means a person reads that file after a release, per RULE-027.

## What this contract does not cover

- Hosted CI. None is configured, and nothing in this contract requires it.
- Rollout staging or canaries. Out of scope for a single-host deployment.
