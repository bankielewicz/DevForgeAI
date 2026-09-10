---
schema_version: "devforge.artifact/v1"
artifact_id: "IDEAS-001"
artifact_type: "idea-ledger"
project_id: "riverbend-running-club"
revision: 2
status: draft
created_at_utc: "2026-08-28T09:14:00Z"
producer:
  skill: "devforge-brainstorm"
  skill_revision: "unknown (fixture; no installed SKILL.md was hashed)"
execution_ref: null
upstream: []
evidence: []
supersedes:
  artifact_id: "IDEAS-001"
  revision: 1
  store: project
  path: "docs/devforge/ideas/archive/IDEAS-001.r1.md"
  sha256: "4dbe2259ecd3378c6993b2b088bfb9771db3d13bfd9a5532f8e2709637e971ac"
decision_ref: "DEC-001"
missing_inputs:
  - "No measurement of how often a run is cancelled or moved; the club keeps no record of it."
---

# Idea ledger: Riverbend Running Club

Synthetic fixture. The club, its members and every statement below were invented for evaluation.

## Context

Riverbend is a volunteer-run club of about 90 members with four weekly sessions. Everything currently lives in one WhatsApp group and a spreadsheet two people can edit. Ada (the club secretary) started this ledger.

## Ideas

| Idea ID | Idea | Problem it addresses | Who is affected | Origin | State | Related IDs |
| --- | --- | --- | --- | --- | --- | --- |
| IDEA-001 | One page showing this week's sessions: time, meeting point, route, pace groups, and whether it is still on. | Members ask "is it still on?" in the group chat and the answer scrolls away. | Members; the two run leaders who answer the same question repeatedly. | user | proposed | IDEA-004 |
| IDEA-002 | Members mark themselves in or out for a session so leaders know numbers before they arrive. | Leaders bring the wrong number of hi-vis vests and cannot plan pace groups. | Run leaders; new members who do not know whether to turn up. | user | proposed | - |
| IDEA-003 | A route library with distance, terrain and a note on whether it floods. | Route knowledge is in three people's heads; a new leader cannot pick a safe route. | Run leaders, especially new ones. | user | proposed | - |
| IDEA-004 | Cancellations push to whoever marked themselves in, rather than being announced to everyone. | A cancellation posted at 06:00 is missed by people already travelling. | Members who travel to the meeting point. | AI proposal | proposed | IDEA-001, IDEA-002 |

## Decisions

| Decision ID | What was decided | Basis | State | Decision reference |
| --- | --- | --- | --- | --- |
| DEC-001 | The first thing to build addresses this week's running information - IDEA-001 and IDEA-002 together. Route library and push cancellations are not first. | Ada, in the session of 2026-08-28: "Yes, I'm deciding that. If we fix 'is it on and who's coming' we've fixed the thing people actually complain about." | adopted | Ada, session of 2026-08-28 |

## Assumptions and open questions

| ID | Statement | Consequence if wrong | Smallest observation that would settle it |
| --- | --- | --- | --- |
| Q-001 | Members will mark themselves in if it takes one tap. | The leader-facing half of DEC-001 has no data behind it and IDEA-002 is worthless. | Ask the next two sessions to reply in the group chat with a single emoji; count replies against attendance. |
| Q-002 | The club will keep using WhatsApp for conversation regardless. | A tool that tries to replace the group chat is a much larger scope than DEC-001. | Ask Ada and the four leaders whether they would move conversation off it. |
| Q-003 | Assumed, not established: most members would open a web page rather than install anything. | An app-store distribution requirement changes the whole shape of the first release. | Ada does not know. Nobody has asked the members. |

## Constraints stated by the user

- Ada, 2026-08-28: "It has to work on an old Android phone with a bad signal - that's what the leaders actually carry." Recorded as a firm constraint, user origin.
- Ada, 2026-08-28: "I'd probably reach for whatever's cheapest to host, but I'm not attached to any of that." Recorded as a non-binding preference, user origin. No technology has been selected.

## Next step

The smallest discovery task that would move DEC-001 forward is Q-001: count emoji replies across two sessions. Non-goal for that task: do not build anything to collect the replies.
