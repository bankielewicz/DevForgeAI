---
schema_version: "devforge.artifact/v1"
artifact_id: "PROD-001"
artifact_type: "product-brief"
project_id: "havenlist"
revision: 3
status: accepted
created_at_utc: "2026-09-08T10:00:00Z"
producer:
  skill: "operator"
  skill_revision: "unknown (synthetic fixture; no skill produced this)"
execution_ref: null
upstream: []
evidence: []
supersedes:
  artifact_id: "PROD-001"
  revision: 2
  sha256: "b863996bf1804f08980e5f051e9f568fa5e3187c1a70faa3f45f6e3e0f43e8f9"
  preserved_path: "preserved/PROD-001.r2.md"
decision_ref: "adopted by the Havenlist steering group, 2026-09-08"
missing_inputs: []
---

# Havenlist product brief

**Synthetic fixture.** This is revision 3. Revision 2's bytes are preserved at `preserved/PROD-001.r2.md`.

## Who it is for

Neighbours who want to borrow a hedge trimmer twice a year rather than own one, and the two volunteers who keep the shed running.

## Accepted requirements

| ID | Requirement | Notes |
| --- | --- | --- |
| REQ-004 | A new neighbour can create an account with an email address and a postcode. Postcodes outside the served area are accepted and the account is created in a waiting-list state. | **Changed in revision 3.** Immediate rejection is no longer the accepted behaviour. |
| REQ-005 | A signup that fails validation preserves everything the person already typed. | Unchanged. |
| REQ-006 | Someone who has an account but no borrowing history sees an explanation of how to borrow, not an empty list. | Unchanged. |
| REQ-007 | Account creation is confirmed by email before the first borrow request is accepted. | Unchanged. |
| REQ-011 | A person can recover a signup interrupted by a closed browser without re-entering their email address. | Unchanged. |
| REQ-014 | A waiting-list member is told what would change their status and is not shown borrowing controls. | **New in revision 3.** |

## Out of scope for this revision

Payments, deposits, late fees, and any volunteer-facing administration screen.
