---
schema_version: "devforge.artifact/v1"
artifact_id: "XSPEC-002"
artifact_type: "expert-spec"
project_id: "synthetic-notes"
revision: 1
status: draft
created_at_utc: "2026-09-05T13:20:00Z"
producer:
  skill: "devforge-project-expert-creator"
  skill_revision: "unknown; synthetic fixture"
execution_ref: null
upstream: []
evidence: []
supersedes: null
decision_ref: null
missing_inputs: []
---

# Project expert specification: notes export

Synthetic fixture. A partially filled specification for an evaluation case.

## Concrete capability

- Capability ID and task: CAP-004, export notes to a plain-text digest
- Why current skills are insufficient: notes-storage owns the JSON store and does
  not own an export format.
- Reuse versus new skill decision: {{rationale}}
- Intended native skill name: notes-export
- Supported target terminals: Claude, to be evaluated separately

## Governing knowledge

| Knowledge ID | Approved rule | Exact upstream reference | Verification date |
| --- | --- | --- | --- |
| KNOW-001 | Standard library only. | ARCH-001 RULE-002 | 2026-09-02 |
| KNOW-002 | {{fact}} | {{ARCH reference}} | {{date}} |

## Candidate-independent acceptance expectations

| Case ID | Task | Expected observable behaviour | Failure that matters |
| --- | --- | --- | --- |
| XCASE-001 | Export a store with three notes. | A digest listing all three in stored order. | Silent reordering. |

## Permissions and refresh

- Refresh triggers: {{relevant versions, rules, source layout, observed failures}}
