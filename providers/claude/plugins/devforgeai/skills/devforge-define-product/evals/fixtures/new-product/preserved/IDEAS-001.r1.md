---
schema_version: "devforge.artifact/v1"
artifact_id: "IDEAS-001"
artifact_type: "idea-ledger"
project_id: "riverbend-running-club"
revision: 1
status: draft
created_at_utc: "2026-08-21T18:05:00Z"
producer:
  skill: "devforge-brainstorm"
  skill_revision: "unknown (fixture; no installed SKILL.md was hashed)"
execution_ref: null
upstream: []
evidence: []
supersedes: null
decision_ref: null
missing_inputs:
  - "No measurement of how often a run is cancelled or moved; the club keeps no record of it."
---

# Idea ledger: Riverbend Running Club

Synthetic fixture. This is the **preserved revision 1** - the exact bytes that `IDEAS-001` revision 2 cites in its `supersedes` entry. Invented for evaluation.

## Context

Riverbend is a volunteer-run club of about 90 members with four weekly sessions. Everything currently lives in one WhatsApp group and a spreadsheet two people can edit. Ada (the club secretary) started this ledger.

## Ideas

| Idea ID | Idea | Problem it addresses | Who is affected | Origin | State | Related IDs |
| --- | --- | --- | --- | --- | --- | --- |
| IDEA-001 | One page showing this week's sessions: time, meeting point, route, pace groups, and whether it is still on. | Members ask "is it still on?" in the group chat and the answer scrolls away. | Members; the two run leaders who answer the same question repeatedly. | user | proposed | - |
| IDEA-002 | Members mark themselves in or out for a session so leaders know numbers before they arrive. | Leaders bring the wrong number of hi-vis vests and cannot plan pace groups. | Run leaders; new members who do not know whether to turn up. | user | proposed | - |
| IDEA-003 | A route library with distance, terrain and a note on whether it floods. | Route knowledge is in three people's heads; a new leader cannot pick a safe route. | Run leaders, especially new ones. | user | proposed | - |

## Decisions

No decision has been recorded. Ada has not adopted anything yet.

## Assumptions and open questions

| ID | Statement | Consequence if wrong | Smallest observation that would settle it |
| --- | --- | --- | --- |
| Q-001 | Members will mark themselves in if it takes one tap. | The leader-facing half of IDEA-002 has no data behind it. | Ask the next two sessions to reply in the group chat with a single emoji; count replies against attendance. |
| Q-002 | The club will keep using WhatsApp for conversation regardless. | A tool that tries to replace the group chat is a much larger scope. | Ask Ada and the four leaders whether they would move conversation off it. |

## Constraints stated by the user

- Ada, 2026-08-21: "It has to work on an old Android phone with a bad signal - that's what the leaders actually carry." Recorded as a firm constraint, user origin.

## Next step

Draw out whether the real problem is the weekly information or the attendance count. Non-goal: choosing anything to build with.
