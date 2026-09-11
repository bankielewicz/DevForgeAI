---
schema_version: "devforge.artifact/v1"
artifact_id: "HANDOFF-FIXTURE-021"
artifact_type: "handoff"
project_id: "synthetic-notes"
revision: 1
status: accepted
created_at_utc: "2026-09-04T08:30:00Z"
producer:
  skill: "operator standing in for an evaluator"
  skill_revision: "unknown; synthetic fixture"
execution_ref: null
upstream: []
evidence: []
supersedes: null
decision_ref: null
missing_inputs:
  - "Tier A discovery observation for the candidate: not obtained."
---

# Evaluator handoff and bounded repair specification

Synthetic fixture. Operator-authored for an evaluation case; no evaluation was
actually performed and no digest below identifies real evaluated bytes.

## Frozen target

- Candidate: notes-storage, source `project/experts/notes-storage`
- Accepted specification: XSPEC-001@1
- Package record: XPKG-001@1
- The candidate manifest supplied with this handoff lists one file, `SKILL.md`.

## Findings

| ID | Severity | Requirement | Expected behaviour | Observed |
| --- | --- | --- | --- | --- |
| F-001 | MAJOR | XSPEC-001 REQ-004 | A read error is surfaced to the caller without overwriting the input file. | The candidate's guidance does not mention the input file at all when describing read failure. |
| F-002 | MINOR | XSPEC-001 REQ-002 | Missing store file and empty note list are distinguished. | Present and correct; recorded as observed, no change requested. |
| F-003 | ADVISORY | none | The description could name the CLI formatting skill as an exclusion. | Suggestion only; not an accepted requirement. |
| F-004 | MAJOR | XSPEC-001 REQ-006 | Discovery and activation observed in a fresh terminal. | COULD_NOT_RUN: no installed copy was available in the evaluation environment. |

## Authorised changes

- CHG-001, required repair, for F-001: state the read-failure behaviour against
  REQ-004 in the candidate's guidance.
- No other change is authorised by this handoff.

F-003 is an unapproved proposal. F-004 is an evaluation prerequisite; it is not a
defect in the candidate and no edit resolves it.
