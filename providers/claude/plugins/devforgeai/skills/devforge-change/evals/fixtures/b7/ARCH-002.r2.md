---
schema_version: "devforge.artifact/v1"
artifact_id: "ARCH-002"
artifact_type: "architecture-contract"
project_id: "tidepool"
revision: 2
status: superseded
created_at_utc: "2026-06-30T10:00:00Z"
producer:
  skill: "devforge-architect"
  skill_revision: "unknown (synthetic fixture)"
execution_ref: "SESSION-038@1"
upstream: []
evidence: []
supersedes: null
decision_ref: "USER-ADOPTION-2026-06-30"
missing_inputs: []
---

# Tidepool architecture contract (preserved revision 2)

Synthetic fixture. Preserved bytes for the revision superseded by ARCH-002@3.

## AR-04 Conflict resolution

Survey submissions are reconciled **on the client**, which merges two captures using the
most recent capture timestamp and uploads the merged result.

Revision 3 reversed this. A candidate still written against this text is working from a
superseded rule.
