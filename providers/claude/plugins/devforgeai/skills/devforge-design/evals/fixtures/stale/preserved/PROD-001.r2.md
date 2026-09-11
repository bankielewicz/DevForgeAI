---
schema_version: "devforge.artifact/v1"
artifact_id: "PROD-001"
artifact_type: "product-brief"
project_id: "havenlist"
revision: 2
status: accepted
created_at_utc: "2026-08-14T09:20:00Z"
producer:
  skill: "operator"
  skill_revision: "unknown (synthetic fixture; no skill produced this)"
execution_ref: null
upstream: []
evidence: []
supersedes: null
decision_ref: "adopted by the Havenlist steering group, 2026-08-14"
missing_inputs: []
---

# Havenlist product brief

**Synthetic fixture.** Havenlist is an invented neighbourhood tool-lending library. Nothing here is a real product decision.

## Who it is for

Neighbours who want to borrow a hedge trimmer twice a year rather than own one, and the two volunteers who keep the shed running.

## Accepted requirements

| ID | Requirement | Notes |
| --- | --- | --- |
| REQ-004 | A new neighbour can create an account with an email address and a postcode, and is told immediately when the postcode is outside the served area. | The served-area list is fixed and known at signup time. |
| REQ-005 | A signup that fails validation preserves everything the person already typed. | Volunteers reported people abandoning at this point. |
| REQ-006 | Someone who has an account but no borrowing history sees an explanation of how to borrow, not an empty list. | |
| REQ-007 | Account creation is confirmed by email before the first borrow request is accepted. | The unconfirmed state must be visible to the person. |
| REQ-011 | A person can recover a signup interrupted by a closed browser without re-entering their email address. | |

## Out of scope for this revision

Payments, deposits, late fees, and any volunteer-facing administration screen.

## Open questions

Whether the postcode check happens as the person types or on submit is undecided and affects the error experience.
