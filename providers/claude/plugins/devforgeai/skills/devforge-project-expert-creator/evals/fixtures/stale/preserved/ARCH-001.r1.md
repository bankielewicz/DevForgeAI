---
schema_version: "devforge.artifact/v1"
artifact_id: "ARCH-001"
artifact_type: "architecture-contract"
project_id: "synthetic-notes"
revision: 1
status: accepted
created_at_utc: "2026-08-14T09:12:00Z"
producer:
  skill: "operator"
  skill_revision: "unknown; synthetic fixture"
execution_ref: null
upstream: []
evidence: []
supersedes: null
decision_ref: "owner decision 2026-08-14"
missing_inputs: []
---

# Architecture contract, revision 1

Synthetic fixture. Illustrative accepted rules for an evaluation case.

## RULE-001 Storage format

Notes are stored as a JSON list of `{id, text}` objects. `id` is a non-empty
unique string.

## RULE-002 Dependencies

Standard library only: `json` and `pathlib`. No third-party dependency, database
or network.

## RULE-003 Unknown fields

Not addressed at this revision.
