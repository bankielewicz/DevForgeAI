---
schema_version: "devforge.artifact/v1"
artifact_id: "IDEAS-006"
artifact_type: "idea-ledger"
project_id: "harbourside"
revision: 1
status: draft
created_at_utc: "2026-08-28T09:14:00Z"
producer:
  skill: "devforge-brainstorm"
  skill_revision: "unknown"
execution_ref: null
upstream: []
evidence: []
supersedes: null
decision_ref: null
missing_inputs: []
---

# Harbourside volunteer scheduling

## Problem and current focus

Volunteer shifts at the sailing club are arranged in a group chat. People miss
messages, two volunteers turn up for the same slot, and nobody can see the week
at a glance.

## Ideas and alternatives

| ID | Origin | Problem | Idea | State | Related |
| --- | --- | --- | --- | --- | --- |
| IDEA-001 | user | Shifts are arranged in chat and get missed | A visible weekly rota anyone can read | proposed | none |
| IDEA-002 | AI proposal | Double-booking is only noticed on the day | A claim step that shows who already took a slot | proposed | IDEA-001 |

## Assumptions and open questions

| ID | Assumption or question | Consequence | Smallest observation that settles it |
| --- | --- | --- | --- |
| OPEN-001 | Volunteers would read a rota they had to open | If not, a rota changes nothing | Ask five volunteers where they last checked their shift |

## Decisions and parked alternatives

| ID | Decision | State | Basis | Supersedes |
| --- | --- | --- | --- | --- |
| DEC-001 | Keep both ideas open for now | proposed | null | null |

## Next useful step

Watch one week of the group chat and count how many messages exist only to
re-state a shift that was already agreed.
