---
schema_version: "devforge.artifact/v1"
artifact_id: "ARCH-001"
artifact_type: "architecture-contract"
project_id: "synthetic-notes"
revision: 2
status: accepted
created_at_utc: "2026-09-02T16:40:00Z"
producer:
  skill: "operator"
  skill_revision: "unknown; synthetic fixture"
execution_ref: null
upstream: []
evidence: []
supersedes: "ARCH-001@1"
decision_ref: "owner decision 2026-09-02"
missing_inputs: []
---

# Architecture contract, revision 2

Synthetic fixture. Illustrative accepted rules for an evaluation case.

## RULE-001 Storage format

Notes are stored as a JSON list of `{id, text}` objects. `id` is a non-empty
unique string.

## RULE-002 Dependencies

Standard library only: `json` and `pathlib`. No third-party dependency, database
or network.

## RULE-003 Unknown fields

Fields present in a stored record that the current version does not recognise are
preserved unchanged across an edit. This rule is new at revision 2 and widens
RULE-003's scope from "not addressed" to a positive requirement.
