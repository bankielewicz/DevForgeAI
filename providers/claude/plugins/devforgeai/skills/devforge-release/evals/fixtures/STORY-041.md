---
schema_version: "devforge.artifact/v1"
artifact_id: "STORY-041"
artifact_type: "story"
project_id: "foldbench"
revision: 2
status: accepted
created_at_utc: "2026-08-19T13:02:51Z"
producer:
  skill: "devforge-plan"
  skill_revision: "SYNTHETIC-FIXTURE-plan-skill-digest-not-computed"
execution_ref: "SESSION-074@1"
upstream:
  - artifact_id: ARCH-003
    revision: 4
    store: project
    path: docs/devforge/architecture/ARCH-003.md
    sha256: "SYNTHETIC-FIXTURE-arch-003-digest-not-computed"
    sections:
      - RULE-011
      - RULE-014
evidence: []
supersedes: null
decision_ref: "adopted by the project owner, 2026-08-19"
missing_inputs: []
---

# STORY-041: a per-workspace retention window

**Synthetic evaluation fixture.**

Foldbench keeps every capture forever. Workspaces that run continuous imports fill up, and their owners have no way to say "anything older than ninety days can go."

## Acceptance criteria

- **AC-1** — The retention window is applied at query time, so an expired capture stops appearing in results.
- **AC-2** — Existing exports are unaffected: an export requested before the window change still contains what it contained.
- **AC-3** — The window is configurable per workspace, with a default of "keep everything" so existing workspaces do not change behaviour on upgrade.

## Out of scope

- Deleting expired rows from storage. That is a separate story; this one only stops surfacing them.
- Any change to the export format.

## Notes

RULE-014 applies: the config column is a schema change and needs a migration with a down path.
