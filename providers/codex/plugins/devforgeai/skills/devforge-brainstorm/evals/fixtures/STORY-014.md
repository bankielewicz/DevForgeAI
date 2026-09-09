---
schema_version: "devforge.artifact/v1"
artifact_id: "STORY-014"
artifact_type: "story"
project_id: "trailkeeper"
revision: 3
status: accepted
created_at_utc: "2026-09-01T09:15:00Z"
producer:
  skill: "devforge-plan"
  skill_revision: "unknown"
execution_ref: "SESSION-007@1"
upstream:
  - artifact_id: ARCH-002
    revision: 4
    store: project
    path: docs/devforge/architecture/ARCH-002.md
    sha256: "not-recorded-in-fixture"
    sections:
      - RULE-011
evidence: []
supersedes: null
decision_ref: "user adoption 2026-09-01, planning review"
missing_inputs: []
---

# Story: expire trail condition reports after 72 hours

## Statement

As a club member reading the conditions feed, I want reports older than 72
hours hidden by default, so that I do not plan a run around stale information.

## Acceptance criteria

- AC-1: A report with `posted_at` older than 72 hours does not appear in the
  default feed query.
- AC-2: A "show older reports" toggle returns them, ordered newest first.
- AC-3: The cutoff is evaluated in UTC against request time, not cached.

## Notes

Follows ARCH-002 RULE-011 (all timestamps stored and compared in UTC).
Test policy: unit coverage on the query builder plus one integration test.
