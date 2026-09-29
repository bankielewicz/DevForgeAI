---
id: ARCH-001
type: arch
title: "Volunteer shift sign-up for the Riverside Food Bank architecture"
status: draft
version: 1
created: 2026-09-28
updated: 2026-09-28
owner: "Priya Nair"
authors:
  - "Priya Nair"
  - "codex"
generated_by:
  tool: "codex"
  model: "unknown"
  session: "unknown"
reviewed_by: []
approved_by: ""
approved_on: null
upstream:
  - {id: PRD-001, relation: informed_by, version: 1, hash: null}
supersedes: []
superseded_by: null
blocked_by: []
# --- arch-specific ---
system: "Volunteer shift sign-up for the Riverside Food Bank"
outcome: null
inspection_scope: []
---

# ARCH-001 — Volunteer shift sign-up for the Riverside Food Bank architecture

## 1. Context and scope

This proposal describes PRD-001 version 1, status approved: browser-based volunteer sign-in,
warehouse shift booking, and a daily coordinator roster for approximately 120 volunteers and one
coordinator. Administrative session revocation and restricted access to volunteer phone numbers
are included. Payroll and donations are outside the product scope.

The PRD's operating context is internal; the release name Pilot does not override that context.
No inspection scope was named, so no code or configuration was inspected. No existing ARCH,
ADR, policy document or local preference file was found at the contract paths. Existing
implementation and reuse suitability are unknown.

A new ARCH is proposed because none covers this system. The request selected PRD-001 and directed
work without questions; it did not explicitly confirm the create outcome or any architectural
choice. Consequently outcome remains null, every decision remains open, and no ADR is written.
The components below are proposed logical responsibilities, not approved services or deployments.

## 2. Quality drivers

PRD-001#NFR-001 requires administrative revocation of a volunteer's signed-in sessions to take
effect within five minutes. Selecting an identity provider does not settle session invalidation
or enforcement at protected operations; ARCH-001#DEC-02 addresses those separately.

PRD-001#NFR-002 permits only the coordinator to see volunteer phone numbers. Data ownership,
role authority and access enforcement must agree across booking and roster work; see
ARCH-001#DEC-03 and ARCH-001#DEC-04. The administrative revocation role does not by itself grant
access to phone numbers.

PRD-001#NFR-003 requires hosted services for the whole product because there is no on-site server.
It constrains every proposed component, but selects neither a hosting platform nor deployment
units; ARCH-001#DEC-07 remains open.

The internal-context framework floor is constraint, security and privacy. All three categories
are covered by the NFRs above; no required category is missing. There are no additional applied
policy settings. The mobile browser experience and small volunteer population inform the
proposal without establishing unrequested performance or availability targets.

## 3. Components

All ownership and boundaries below are provisional under ARCH-001#DEC-03 and ARCH-001#DEC-05.
Arrows show required collaboration, not a selected protocol. Booking-to-roster consistency is
open under ARCH-001#DEC-06; shared authorization is open under ARCH-001#DEC-04.

```mermaid
flowchart LR
    CMP01["CMP-01 Browser experience"] --> CMP02["CMP-02 Identity and sessions"]
    CMP01 --> CMP03["CMP-03 Shifts and roster"]
    CMP01 --> CMP04["CMP-04 Volunteer profiles and access"]
    CMP03 --> CMP02
    CMP03 --> CMP04
    CMP04 --> CMP02
```

```yaml items
components:
  - id: CMP-01
    status: active
    name: "Browser experience"
    responsibility: "Presents volunteer sign-in and booking, coordinator rosters and administrative revocation controls; does not own authoritative records or grant access by UI visibility."
    owns_data: []
    interacts_with:
      - "CMP-02"
      - "CMP-03"
      - "CMP-04"
    deployment: "Open: see DEC-07"
    upstream:
      - {id: PRD-001, item: NFR-001, relation: informed_by, version: 1, hash: null}
      - {id: PRD-001, item: NFR-002, relation: informed_by, version: 1, hash: null}
      - {id: PRD-001, item: NFR-003, relation: informed_by, version: 1, hash: null}
  - id: CMP-02
    status: active
    name: "Identity and sessions"
    responsibility: "Proposed authority for authentication, session validity and revocation; does not own bookings or volunteer phone numbers. Provider and revocation mechanism remain open."
    owns_data:
      - "Proposed: authentication identities and session revocation state"
    interacts_with:
      - "CMP-01"
      - "CMP-03"
      - "CMP-04"
    deployment: "Open: see DEC-07"
    upstream:
      - {id: PRD-001, item: NFR-001, relation: informed_by, version: 1, hash: null}
      - {id: PRD-001, item: NFR-003, relation: informed_by, version: 1, hash: null}
  - id: CMP-03
    status: active
    name: "Shifts and roster"
    responsibility: "Proposed authority for open shifts and bookings, providing the coordinator roster from booking state; does not authenticate users or own phone numbers."
    owns_data:
      - "Proposed: warehouse shifts and their bookable state"
      - "Proposed: bookings linked to volunteer identities"
    interacts_with:
      - "CMP-01"
      - "CMP-02"
      - "CMP-04"
    deployment: "Open: see DEC-07"
    upstream:
      - {id: PRD-001, item: NFR-001, relation: informed_by, version: 1, hash: null}
      - {id: PRD-001, item: NFR-002, relation: informed_by, version: 1, hash: null}
      - {id: PRD-001, item: NFR-003, relation: informed_by, version: 1, hash: null}
  - id: CMP-04
    status: active
    name: "Volunteer profiles and access"
    responsibility: "Proposed authority for volunteer contact records and application role assignments, supporting coordinator-only phone disclosure; does not own booking state or authentication credentials."
    owns_data:
      - "Proposed: volunteer profiles and phone numbers"
      - "Proposed: coordinator and administrator role assignments"
    interacts_with:
      - "CMP-01"
      - "CMP-02"
      - "CMP-03"
    deployment: "Open: see DEC-07"
    upstream:
      - {id: PRD-001, item: NFR-001, relation: informed_by, version: 1, hash: null}
      - {id: PRD-001, item: NFR-002, relation: informed_by, version: 1, hash: null}
      - {id: PRD-001, item: NFR-003, relation: informed_by, version: 1, hash: null}
```

## 4. Architectural questions

```yaml items
decisions:
  - id: DEC-01
    status: active
    question: "Which identity provider handles volunteer sign-in?"
    blocking: true
    state: open
    resolved_by: []
    notes: "Captures the PRD NEEDS ADR marker. Provider identity and trust also affect signed-in booking and the available revocation integration. No platform is mandated and no user choice was obtained."
    upstream:
      - {id: PRD-001, item: FR-001, relation: informed_by, version: 1, hash: null}
      - {id: PRD-001, item: FR-002, relation: informed_by, version: 1, hash: null}
      - {id: PRD-001, item: NFR-001, relation: informed_by, version: 1, hash: null}
  - id: DEC-02
    status: active
    question: "How will all protected operations reject a volunteer's revoked sessions within five minutes?"
    blocking: true
    state: open
    resolved_by: []
    notes: "Sign-in creates sessions and booking consumes them. Shared validity checks versus bounded token and cache lifetimes have different request costs and revocation guarantees; provider selection alone resolves neither. The same contract must cover session renewal."
    upstream:
      - {id: PRD-001, item: FR-001, relation: informed_by, version: 1, hash: null}
      - {id: PRD-001, item: FR-002, relation: informed_by, version: 1, hash: null}
      - {id: PRD-001, item: NFR-001, relation: informed_by, version: 1, hash: null}
  - id: DEC-03
    status: active
    question: "Which components are authoritative for shift, booking and volunteer contact records?"
    blocking: true
    state: open
    resolved_by: []
    notes: "The proposed division separates shift and booking ownership from contact ownership and joins them by volunteer identity. A single application data owner simplifies consistency; separate owners isolate contact access but require cross-component identity and read contracts. Ownership is not yet decided."
    upstream:
      - {id: PRD-001, item: FR-002, relation: informed_by, version: 1, hash: null}
      - {id: PRD-001, item: FR-003, relation: informed_by, version: 1, hash: null}
      - {id: PRD-001, item: NFR-002, relation: informed_by, version: 1, hash: null}
  - id: DEC-04
    status: active
    question: "What shared authorization model governs volunteer, coordinator and administrator access?"
    blocking: true
    state: open
    resolved_by: []
    notes: "The role authority and enforcement contract must govern signed-in booking, coordinator roster and phone access, and administrative revocation. Application-owned roles permit direct access changes but require application enforcement; identity-provider roles reduce duplication but introduce claim-refresh dependencies. UI hiding alone cannot enforce phone privacy."
    upstream:
      - {id: PRD-001, item: FR-002, relation: informed_by, version: 1, hash: null}
      - {id: PRD-001, item: FR-003, relation: informed_by, version: 1, hash: null}
      - {id: PRD-001, item: NFR-001, relation: informed_by, version: 1, hash: null}
      - {id: PRD-001, item: NFR-002, relation: informed_by, version: 1, hash: null}
  - id: DEC-05
    status: active
    question: "What component boundaries will separate the browser, identity, scheduling and profile responsibilities?"
    blocking: true
    state: open
    resolved_by: []
    notes: "The component diagram is provisional. One application with internal modules reduces cross-service coordination; separate services provide independent boundaries but add distributed interfaces and access enforcement. Each feature and quality capability depends on this shared division."
    upstream:
      - {id: PRD-001, item: FR-001, relation: informed_by, version: 1, hash: null}
      - {id: PRD-001, item: FR-002, relation: informed_by, version: 1, hash: null}
      - {id: PRD-001, item: FR-003, relation: informed_by, version: 1, hash: null}
      - {id: PRD-001, item: NFR-001, relation: informed_by, version: 1, hash: null}
      - {id: PRD-001, item: NFR-002, relation: informed_by, version: 1, hash: null}
      - {id: PRD-001, item: NFR-003, relation: informed_by, version: 1, hash: null}
  - id: DEC-06
    status: active
    question: "What consistency contract connects booking an open shift to the coordinator's roster?"
    blocking: true
    state: open
    resolved_by: []
    notes: "A roster read from authoritative committed bookings simplifies agreement between booking and roster; an asynchronously maintained projection separates reads but requires lag and recovery rules. Concurrent booking must respect authoritative open-shift state. No numeric roster freshness target is invented here."
    upstream:
      - {id: PRD-001, item: FR-002, relation: informed_by, version: 1, hash: null}
      - {id: PRD-001, item: FR-003, relation: informed_by, version: 1, hash: null}
  - id: DEC-07
    status: active
    question: "What hosted deployment topology will run the whole product?"
    blocking: true
    state: open
    resolved_by: []
    notes: "The PRD requires hosted services but leaves the platform, deployment units and environments unspecified. A hosted application with managed persistence concentrates operations; independently hosted functions or services add deployment and security coordination. The topology must preserve revocation and phone-access guarantees across all units."
    upstream:
      - {id: PRD-001, item: FR-001, relation: informed_by, version: 1, hash: null}
      - {id: PRD-001, item: FR-002, relation: informed_by, version: 1, hash: null}
      - {id: PRD-001, item: FR-003, relation: informed_by, version: 1, hash: null}
      - {id: PRD-001, item: NFR-001, relation: informed_by, version: 1, hash: null}
      - {id: PRD-001, item: NFR-002, relation: informed_by, version: 1, hash: null}
      - {id: PRD-001, item: NFR-003, relation: informed_by, version: 1, hash: null}
```

## 5. Evidence inspected

```yaml items
evidence:
  - id: EVD-01
    status: active
    source: "PRD-001"
    kind: prd
    finding: "Version 1, status approved: FR-001 through FR-003 require sign-in, signed-in booking and a coordinator roster; NFR-001 requires session revocation within five minutes, NFR-002 restricts phone visibility to the coordinator, and NFR-003 requires hosted services for the whole product. The identity provider has a NEEDS ADR marker. Operating context is internal."
    classification: context
```

## 6. Deployment

All server-side capabilities and persistent records must use hosted services under
PRD-001#NFR-003. Volunteers and the coordinator use mobile-capable browser pages without an
installed app. ARCH-001#DEC-07 leaves the hosting platform, units and environments open;
ARCH-001#DEC-05 leaves the mapping from logical components to application boundaries open.
No cloud vendor, database technology, runtime or existing deployment is established by evidence.

The proposed topology must allow every protected booking operation to enforce the revocation
contract in ARCH-001#DEC-02 and every contact-data path to enforce ARCH-001#DEC-04. These remain
decision constraints, not evidence that the proposed components already meet them.

## 7. Requirement changes proposed to the PRD owner

- None.

## 8. Open questions

- [NEEDS CLARIFICATION: No inspection scope was named and no code or configuration was inspected; existing implementation, deployment and reuse suitability are unknown.]
- [NEEDS CLARIFICATION: host model/session identity unavailable]
- [NEEDS CLARIFICATION: The create outcome has not been explicitly confirmed; outcome remains null under the request to proceed without questions.]

## Change Log

| Version | Date | Author | Change | Items affected |
|---|---|---|---|---|
| 1 | 2026-09-28 | codex (session unknown) | Initial draft for PRD-001 v1; all architectural questions open, no ADRs written, outcome unconfirmed. Policy resolution: interview.max_calls=8 (default); architecture.mandated_platforms=none (default); quality.required_categories=floor only (default) | all |
