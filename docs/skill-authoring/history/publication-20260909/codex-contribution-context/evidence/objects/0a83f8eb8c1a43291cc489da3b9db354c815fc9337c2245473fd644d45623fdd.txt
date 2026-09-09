---
schema_version: "devforge.artifact/v1"
artifact_id: "SESSION-{{number}}"
artifact_type: "session-record"
project_id: "{{project_id}}"
revision: 1
status: draft
created_at_utc: "{{ISO-8601-UTC-time}}"
producer:
  skill: "external-operator"
  skill_revision: "{{exact-producer-revision-or-digest}}"
execution_ref: null
upstream: []
evidence: []
supersedes: null
decision_ref: null
missing_inputs: []
---

# Authority-selected session and worktree assignment

This record is maintained outside the worker's writable candidate. Its own execution_ref is null because it establishes the execution context rather than consuming itself.

## Ownership and task

- Session/task ID: {{stable ID}}
- Owner and terminal provider: {{owner; Codex/Claude}}
- Assignment state: {{proposed / active / paused / released / revoked}}
- Actual authorization/assignment reference: {{source}}
- Task/story and intended skill: {{IDs}}
- Single writer for this worktree: {{owner}}
- Read-only participants, if any: {{identities/scope}}
- Assignment validity or lease/recovery rule: {{operator-selected rule}}

## Repository and worktree identity

- Mode: {{single-writer-bootstrap / git-worktree}}
- Repository identity and Git common directory: {{verified values}}
- Absolute worktree path: {{verified path}}
- Branch or detached state: {{observed value}}
- Base commit: {{actual SHA; unavailable in pre-Git bootstrap}}
- Initial worktree status / baseline manifest: {{raw observation}}
- Collision check evidence: {{worktree/branch/ownership inspection}}
- Declared write fence and protected paths: {{paths}}
- Assigned provider source and skill: {{canonical provider source; one bounded skill}}
- Permitted evaluation workspace: {{absolute root and ownership}}
- Allowed Git metadata/ref operations: {{operator scope}}

## Context, installation, and authority

- Governing artifact references: {{exact adopted revisions}}
- Installed skill/package identities: {{actual paths and digests}}
- External CLI, policy, runner, and state identities: {{authority-selected references}}
- Credential configuration: {{method/profile reference only; never secret values}}
- Shared service/port/database allocations: {{isolated assignments or none}}
- Report output method: {{permitted outbox / operator-saved terminal record}}
- Report store and readback owner: {{external location and owner}}

## Integration and closeout

- Integration target and owner: {{branch/base/owner}}
- Checks required after combining/rebasing work: {{requirements}}
- Saved candidate/evidence references: {{actual references or none}}
- Handoff record: {{HANDOFF reference}}
- Ownership release observation: {{operator record or still active}}
- Cleanup disposition: {{retain / separately authorized cleanup; preserve dirty work}}
