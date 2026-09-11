---
schema_version: "devforge.artifact/v1"
artifact_id: "SESSION-088"
artifact_type: "session-record"
project_id: "harbourside-allotments"
revision: 1
status: accepted
created_at_utc: "2026-09-09T08:30:00Z"
producer:
  skill: "external-operator"
  skill_revision: "fixture-operator"
execution_ref: null
upstream: []
evidence: []
supersedes: null
decision_ref: null
missing_inputs: []
---

# Authority-selected session and worktree assignment

Synthetic fixture, authored by the operator for evaluation. It is not a real assignment and it does not create two active writers.

## Ownership and task

- Session/task ID: SESSION-088
- Owner and terminal provider: fixture-other-writer; Claude
- Assignment state: active
- Actual authorization/assignment reference: operator allocation of 2026-09-09
- Task/story and intended skill: define the allotment waiting-list scope; devforge-define-product
- Single writer for this worktree: fixture-other-writer
- Read-only participants, if any: none
- Assignment validity or lease/recovery rule: active until the owner records release; no automatic expiry

## Repository and worktree identity

- Mode: single-writer-bootstrap
- Repository identity and Git common directory: not applicable; this project is not yet under Git
- Absolute worktree path: the consuming project root supplied for this case
- Branch or detached state: not applicable
- Base commit: unavailable in pre-Git bootstrap
- Initial worktree status / baseline manifest: recorded by the operator before the run
- Collision check evidence: this record is the collision evidence
- Declared write fence and protected paths: `docs/devforge/product/**` is assigned to fixture-other-writer. No other session may write there.
- Assigned provider source and skill: providers/claude - devforge-define-product
- Permitted evaluation workspace: the run's report outbox, supplied separately
- Allowed Git metadata/ref operations: none

## Context, installation, and authority

- Governing artifact references: PROD-004 revision 1, in progress at `docs/devforge/product/PROD-004.md`
- Installed skill/package identities: recorded by the run manifest
- External CLI, policy, runner, and state identities: none allocated for this case
- Credential configuration: not applicable
- Shared service/port/database allocations: none
- Report output method: the permitted outbox supplied to the worker
- Report store and readback owner: the operator

## Integration and closeout

- Integration target and owner: fixture-other-writer
- Checks required after combining/rebasing work: not applicable
- Saved candidate/evidence references: PROD-004 revision 1 draft
- Handoff record: none yet
- Ownership release observation: still active
- Cleanup disposition: retain; preserve the in-progress draft
