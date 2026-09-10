---
schema_version: "devforge.artifact/v1"
artifact_id: "STORY-033"
artifact_type: "story"
project_id: "tidepool"
revision: 1
status: accepted
created_at_utc: "2026-08-19T15:05:00Z"
producer:
  skill: "devforge-plan"
  skill_revision: "unknown (synthetic fixture)"
execution_ref: "SESSION-055@1"
upstream:
  - artifact_id: "ARCH-002"
    revision: 3
    store: "project"
    path: "docs/devforge/architecture/ARCH-002.md"
    sha256: "548cd935bac43bc868c5da880988a0f43051c18d0fd1c94612259df4e8e8f94e"
    sections: ["AR-02"]
evidence: []
supersedes: null
decision_ref: "USER-ADOPTION-2026-08-19"
missing_inputs: []
---

# STORY-033: Paginate the site list

Synthetic fixture. Ready and unchanged.

## Acceptance criteria

- AC-1: The site list returns at most 50 rows per page with a stable cursor.
- AC-2: The cursor survives a site being added or removed between pages.
- AC-3: No change to the survey capture or reconciliation paths.

Nothing upstream of this story has changed since it was accepted.
