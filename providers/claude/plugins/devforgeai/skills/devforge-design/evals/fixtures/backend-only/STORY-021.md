---
schema_version: "devforge.artifact/v1"
artifact_id: "STORY-021"
artifact_type: "story"
project_id: "havenlist"
revision: 1
status: accepted
created_at_utc: "2026-09-01T08:40:00Z"
producer:
  skill: "operator"
  skill_revision: "unknown (synthetic fixture; no skill produced this)"
execution_ref: null
upstream: []
evidence: []
supersedes: null
decision_ref: "adopted by the Havenlist steering group, 2026-09-01"
missing_inputs: []
---

# STORY-021: index the borrow-history lookup

**Synthetic fixture.**

The borrow-history query scans the full loans table. Add a composite index on `(member_id, returned_at)` so the lookup stays under the existing latency budget as the table grows.

## Acceptance criteria

- The index exists after migration and the migration is reversible.
- The existing borrow-history query plan uses it.
- No response body, page, wording, layout or interaction changes.

## Explicitly unchanged

Every screen. This story is invisible to members and volunteers. The history page renders exactly the same rows in exactly the same order.
