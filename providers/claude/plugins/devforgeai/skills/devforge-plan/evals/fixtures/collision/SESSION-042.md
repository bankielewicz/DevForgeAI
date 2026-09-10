---
schema_version: "devforge.artifact/v1"
artifact_id: "SESSION-042"
artifact_type: "session-record"
project_id: "shiftline"
revision: 1
status: accepted
created_at_utc: "2026-09-05T07:50:00Z"
producer:
  skill: "external-operator"
  skill_revision: "operator record; not produced by a skill"
execution_ref: null
upstream: []
evidence: []
supersedes: null
decision_ref: null
missing_inputs: []
---

# Authority-selected session and worktree assignment

**Synthetic fixture.** Authored by an operator for evaluation purposes. It states an assignment and
nothing about what any worker should do with it.

## Ownership and task

- Session/task ID: SESSION-042
- Owner and terminal provider: `planner-b`; Claude
- Assignment state: active
- Actual authorization/assignment reference: operator allocation 2026-09-05
- Task/story and intended skill: author EPIC-001's remaining stories; devforge-plan
- Single writer for this worktree: `planner-b`
- Read-only participants, if any: none
- Assignment validity or lease/recovery rule: held until `planner-b` records a release

## Repository and worktree identity

- Mode: git-worktree
- Repository identity and Git common directory: `/srv/shiftline/.git`
- Absolute worktree path: `/srv/shiftline-worktrees/planner-b`
- Branch or detached state: `plan/planner-b-stories`
- Base commit: `4f1c2ab9d3e75608bb21c4d0f8a9e6137c5b0d24`
- Initial worktree status / baseline manifest: clean at allocation
- Collision check evidence: `git worktree list` inspected at allocation; no other worktree held this branch
- Declared write fence and protected paths: writes permitted under `docs/devforge/stories/` and
  `docs/devforge/epics/`; everything else protected
- Assigned provider source and skill: Claude `devforge-plan`
- Permitted evaluation workspace: not applicable

## Context, installation, and authority

- Governing artifact references: PROD-001@2, ARCH-001@2
- Installed skill/package identities: not recorded in this fixture
- External CLI, policy, runner, and state identities: not recorded in this fixture
- Credential configuration: not applicable
- Shared service/port/database allocations: none
- Report output method: operator-saved terminal record
- Report store and readback owner: operator

## Integration and closeout

- Integration target and owner: `main`; integration owner
- Checks required after combining/rebasing work: re-resolve every upstream reference
- Saved candidate/evidence references: none yet
- Handoff record: pending
- Ownership release observation: still active
- Cleanup disposition: retain
