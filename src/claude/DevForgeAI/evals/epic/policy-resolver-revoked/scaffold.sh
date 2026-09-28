#!/usr/bin/env bash
# Seeds the fixtures for SPEC-004 VER-15 (policy-resolver-revoked).
set -euo pipefail
mkdir -p docs/specs/adr docs/specs/arch docs/specs/policy docs/specs/prd
cat > docs/specs/prd/PRD-001.md <<'FIXTURE'
---
id: PRD-001
type: prd
title: "Volunteer shift sign-up for the Riverside Food Bank"
status: approved
version: 2
created: 2026-09-14
updated: 2026-09-18
owner: "Priya Nair"
authors: ["Priya Nair", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-opus-5-5"
  session: "fixture-session"
reviewed_by: ["Priya Nair"]
approved_by: "Priya Nair"
approved_on: 2026-09-18
upstream:
  - {id: BRN-001, item: PRB-01, relation: derives, version: 1, hash: null}
supersedes: []
superseded_by: null
blocked_by: []
# --- prd-specific ---
target_release: "Spring launch"
stage: mvp
operating_context: internal
stakeholders: ["Priya Nair"]
---

# PRD-001 — Volunteer shift sign-up for the Riverside Food Bank

## 1. Summary

Let the food bank's volunteers book warehouse shifts themselves instead of by phone, remind them before
each shift, and give the coordinator a live roster.

## 2. Problem and opportunity

The coordinator fills three warehouse shifts a day by phone, and about one shift in six starts
short-staffed (BRN-001#PRB-01).

## 3. Users and personas

About 120 active volunteers, who book from their phones, and one volunteer coordinator.

## 4. Goals and non-goals

**Goals**
- Volunteers book their own shifts, and fewer shifts start short-staffed.

**Non-goals** (explicitly out of scope)
- Payroll; volunteers aren't paid.

## 5. Success metrics

```yaml items
success_metrics:
  - id: SM-01
    status: active
    metric: "Share of shifts that start fully staffed"
    baseline: "83%"
    target: "95% by the end of the spring launch"
    measured_by: "Coordinator's shift log"
    upstream:
      - {id: BRN-001, item: IDEA-01, relation: derives, version: 1, hash: null}
```

## 6. Functional requirements

```yaml items
functional_requirements:
  - id: FR-001
    status: active
    statement: "The system shall let a volunteer sign in."
    priority: must
    release: current
    notes: null
    upstream:
      - {id: BRN-001, item: IDEA-01, relation: derives, version: 1, hash: null}
  - id: FR-002
    status: active
    statement: "The system shall let a signed-in volunteer book an open warehouse shift."
    priority: must
    release: current
    notes: null
    upstream:
      - {id: BRN-001, item: IDEA-01, relation: derives, version: 1, hash: null}
  - id: FR-003
    status: active
    statement: "The system shall show the coordinator each day's roster of booked volunteers."
    priority: should
    release: current
    notes: null
    upstream:
      - {id: BRN-001, item: IDEA-02, relation: derives, version: 1, hash: null}
  - id: FR-004
    status: active
    statement: "The system shall let a volunteer add a booked shift to their phone's calendar."
    priority: could
    release: current
    notes: null
    upstream:
      - {id: BRN-001, item: IDEA-01, relation: derives, version: 1, hash: null}
  - id: FR-005
    status: active
    statement: "The system shall let two volunteers swap booked shifts with each other."
    priority: must
    release: later
    notes: null
    upstream:
      - {id: BRN-001, item: IDEA-01, relation: derives, version: 1, hash: null}
  - id: FR-006
    status: active
    statement: "The system shall reimburse volunteers' travel costs."
    priority: wont
    release: current
    notes: null
    upstream:
      - {id: BRN-001, item: IDEA-03, relation: derives, version: 1, hash: null}
  - id: FR-007
    status: active
    statement: "The system shall let the coordinator message every volunteer booked on a shift."
    priority: null
    release: current
    notes: null
    upstream:
      - {id: BRN-001, item: IDEA-02, relation: derives, version: 1, hash: null}
  - id: FR-008
    status: active
    statement: "The system shall text a volunteer a reminder the day before a booked shift."
    priority: must
    release: current
    notes: null
    upstream:
      - {id: BRN-001, item: IDEA-01, relation: derives, version: 1, hash: null}
  - id: FR-009
    status: active
    statement: "The system shall import the current volunteer list from the coordinator's spreadsheet."
    priority: must
    release: current
    notes: null
    upstream:
      - {id: BRN-001, item: IDEA-02, relation: derives, version: 1, hash: null}
  - id: FR-010
    status: active
    statement: "The system shall let a volunteer pay the yearly membership fee online."
    priority: must
    release: current
    notes: null
    upstream:
      - {id: BRN-001, item: IDEA-03, relation: derives, version: 1, hash: null}
  - id: FR-011
    status: active
    statement: "The system shall send each month's volunteer hours to the regional food bank network."
    priority: must
    release: current
    notes: null
    upstream:
      - {id: BRN-001, item: IDEA-02, relation: derives, version: 1, hash: null}
  - id: FR-012
    status: active
    statement: "The system shall email a volunteer a confirmation when they book a shift."
    priority: must
    release: current
    notes: null
    upstream:
      - {id: BRN-001, item: IDEA-01, relation: derives, version: 1, hash: null}
```

## 7. Non-functional requirements

```yaml items
non_functional_requirements:
  - id: NFR-001
    status: active
    category: privacy
    statement: "Volunteer phone numbers are visible only to the coordinator."
    priority: must
    release: current
```

## 8. User experience

Mobile-first web pages; no app to install.

## 9. Constraints and dependencies

The food bank is a member of the regional food bank network, whose IT policy applies.

## 10. Assumptions and risks

```yaml items
assumptions:
  - id: ASM-01
    status: active
    statement: "Most volunteers have a smartphone with a web browser."
    validation: "Ask at the September volunteer meeting"
    state: open
    upstream:
      - {id: BRN-001, item: ASM-01, relation: derives, version: 1, hash: null}
```

## 11. Release and rollout

The spring launch covers every warehouse shift; shift swaps (FR-005) follow in a later release.

## 12. Open questions

- [NEEDS ADR: identity provider for volunteer sign-in; affects FR-001]
- [NEEDS ADR: how the volunteer list is imported from the coordinator's spreadsheet and kept in step with it; affects FR-009]
- [NEEDS ADR: payment provider for membership fees; affects FR-010]

## 13. Epic map

<!-- GENERATED: epics whose upstream cites this PRD. Do not edit by hand. -->

## Change Log

| Version | Date | Author | Change | Items affected |
|---|---|---|---|---|
| 1 | 2026-09-14 | claude-code (session fixture-session) | Initial draft from BRN-001. Policy resolution: interview.max_calls=8 (default); architecture.mandated_platforms=POL-001#SET-01; quality.required_categories=floor only (default) | all |
| 1 | 2026-09-16 | Priya Nair | Approved | status |
| 2 | 2026-09-18 | Priya Nair | Added FR-012 (booking confirmation email) and moved FR-005 to a later release | FR-005, FR-012 |
| 2 | 2026-09-18 | Priya Nair | Approved | status |
FIXTURE
cat > docs/specs/arch/ARCH-001.md <<'FIXTURE'
---
id: ARCH-001
type: arch
title: "Riverside Food Bank volunteer shift sign-up architecture"
status: approved
version: 1
created: 2026-09-22
updated: 2026-09-24
owner: "Priya Nair"
authors: ["Priya Nair", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-opus-5-5"
  session: "fixture-session"
reviewed_by: ["Priya Nair"]
approved_by: "Priya Nair"
approved_on: 2026-09-24
upstream:
  - {id: PRD-001, relation: informed_by, version: 2, hash: null}
supersedes: []
superseded_by: null
blocked_by: []
# --- arch-specific ---
system: "Riverside Food Bank volunteer shift sign-up"
outcome: create
inspection_scope: []
---

# ARCH-001 — Riverside Food Bank volunteer shift sign-up architecture

## 1. Context and scope

Defined against PRD-001 version 2 (approved): volunteers sign in, book warehouse shifts and get
reminders; the coordinator sees the roster; membership fees are paid online. Payroll is outside the
system. No inspection scope was named, and no code was inspected.

## 2. Quality drivers

NFR-001 (phone numbers visible only to the coordinator) drives data ownership. The regional network's
mandated mail relay (POL-001#SET-01) constrains email.

## 3. Components

```mermaid
flowchart LR
    W[CMP-01 Volunteer web app] --> S[CMP-02 Shift service]
    W --> I[CMP-03 Identity provider]
    S --> M[CMP-04 Mail relay]
```

```yaml items
components:
  - id: CMP-01
    status: active
    name: "Volunteer web app"
    responsibility: "Sign-in, booking, roster and payment screens; holds no data of its own"
    owns_data: []
    interacts_with:
      - "CMP-02"
      - "CMP-03"
    deployment: "Static site on the hosting provider"
  - id: CMP-02
    status: active
    name: "Shift service"
    responsibility: "Shifts, bookings, reminders and volunteer contact details"
    owns_data:
      - "Shifts and bookings"
      - "Volunteer phone numbers"
    interacts_with:
      - "CMP-01"
      - "CMP-04"
    deployment: "One hosted service with its database (ADR-001)"
    upstream:
      - {id: PRD-001, item: NFR-001, relation: informed_by, version: 2, hash: null}
  - id: CMP-03
    status: active
    name: "Identity provider"
    responsibility: "Authenticates volunteers and issues sessions"
    owns_data:
      - "Volunteer credentials"
    interacts_with:
      - "CMP-01"
    deployment: "External; the provider is open (DEC-01)"
  - id: CMP-04
    status: active
    name: "Mail relay"
    responsibility: "Delivers the emails the shift service sends; external, provided by the regional network"
    owns_data: []
    interacts_with:
      - "CMP-02"
    deployment: "External: Regional network mail relay (SMTP)"
    upstream:
      - {id: POL-001, item: SET-01, relation: constrains, version: 1, hash: null}
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
    notes: null
    upstream:
      - {id: PRD-001, item: FR-001, relation: informed_by, version: 2, hash: null}
  - id: DEC-02
    status: active
    question: "Where are shift, booking and contact data stored, and which component owns them?"
    blocking: true
    state: resolved
    resolved_by: [ADR-001]
    notes: null
    upstream:
      - {id: PRD-001, item: FR-002, relation: informed_by, version: 2, hash: null}
      - {id: PRD-001, item: NFR-001, relation: informed_by, version: 2, hash: null}
  - id: DEC-03
    status: active
    question: "How are shift reminders sent to volunteers' phones?"
    blocking: true
    state: resolved
    resolved_by: [ADR-002]
    notes: null
    upstream:
      - {id: PRD-001, item: FR-008, relation: informed_by, version: 2, hash: null}
  - id: DEC-04
    status: active
    question: "Where are the audit records of membership payments stored?"
    blocking: true
    state: resolved
    resolved_by: [ADR-003]
    notes: null
    upstream:
      - {id: PRD-001, item: FR-010, relation: informed_by, version: 2, hash: null}
  - id: DEC-05
    status: active
    question: "How are each month's volunteer hours sent to the regional food bank network?"
    blocking: true
    state: resolved
    resolved_by: [ADR-004]
    notes: null
    upstream:
      - {id: PRD-001, item: FR-011, relation: informed_by, version: 2, hash: null}
  - id: DEC-06
    status: active
    question: "How are shift-swap requests passed between volunteers?"
    blocking: true
    state: open
    resolved_by: []
    notes: null
    upstream:
      - {id: PRD-001, item: FR-005, relation: informed_by, version: 2, hash: null}
  - id: DEC-07
    status: active
    question: "Which email service sends booking confirmations?"
    blocking: true
    state: resolved
    resolved_by: [POL-001#SET-01]
    notes: null
    upstream:
      - {id: PRD-001, item: FR-012, relation: informed_by, version: 2, hash: null}
```

## 5. Evidence inspected

```yaml items
evidence:
  - id: EVD-01
    status: active
    source: "PRD-001"
    kind: prd
    finding: "Version 2, status approved: twelve functional requirements and NFR-001; three NEEDS ADR markers."
    classification: context
  - id: EVD-02
    status: active
    source: "ADR-001"
    kind: adr
    finding: "Version 1, status accepted: the shift service owns shift, booking and contact data in one managed PostgreSQL database."
    classification: decided
  - id: EVD-03
    status: active
    source: "ADR-002"
    kind: adr
    finding: "Version 1, status accepted: reminders go through the on-premises SMS modem."
    classification: decided
  - id: EVD-04
    status: active
    source: "ADR-003"
    kind: adr
    finding: "Version 1, status accepted: membership-payment audit records are kept in the hosting provider's log store."
    classification: decided
  - id: EVD-05
    status: active
    source: "ADR-004"
    kind: adr
    finding: "Version 1, status accepted: monthly hours are uploaded as a CSV file to the regional network's portal."
    classification: decided
  - id: EVD-06
    status: active
    source: "POL-001#SET-01"
    kind: policy
    finding: "Version 1, status approved, setting active: transactional email goes through the regional network mail relay."
    classification: policy
```

## 6. Deployment

The web app and the shift service run on the hosting provider; the identity provider is open (DEC-01),
and email goes through the regional network's relay.

## 7. Requirement changes proposed to the PRD owner

- None.

## 8. Open questions

- None.

## Change Log

| Version | Date | Author | Change | Items affected |
|---|---|---|---|---|
| 1 | 2026-09-22 | claude-code (session fixture-session) | Initial draft for PRD-001 v2. Policy resolution: interview.max_calls=8 (default); architecture.mandated_platforms=POL-001#SET-01; quality.required_categories=floor only (default) | all |
| 1 | 2026-09-24 | Priya Nair | Approved | status |
FIXTURE
cat > docs/specs/adr/ADR-001.md <<'FIXTURE'
---
id: ADR-001
type: adr
title: "Keep shift, booking and contact data in one managed PostgreSQL database owned by the shift service"
status: accepted
version: 1
created: 2026-09-21
updated: 2026-09-21
owner: "Priya Nair"
authors: ["Priya Nair", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-opus-5-5"
  session: "fixture-session"
reviewed_by: []
approved_by: "Priya Nair"
approved_on: 2026-09-21
upstream:
  - {id: PRD-001, item: FR-002, relation: informed_by, version: 2, hash: null}
  - {id: PRD-001, item: NFR-001, relation: informed_by, version: 2, hash: null}
supersedes: []
superseded_by: null
blocked_by: []
# --- adr-specific ---
consulted: []
informed: []
---

# ADR-001 — Keep shift, booking and contact data in one managed PostgreSQL database owned by the shift service

## Context and problem statement

Bookings (PRD-001#FR-002) and private phone numbers (PRD-001#NFR-001) need one owner (ARCH-001#DEC-02).

## Decision drivers

- Low running cost for a volunteer-run charity.

## Considered options

1. Keep shift, booking and contact data in one managed PostgreSQL database owned by the shift service
2. Do nothing for now

## Decision outcome

**Chosen option:** one managed PostgreSQL database, owned by the shift service, because it keeps phone numbers behind one API.

### Consequences

- Good: one clear answer for every epic.
- Bad: it has to be revisited if the food bank's setup changes.

### Confirmation

Reviewed when the spring launch ends.

## Pros and cons of the options

### Keep shift, booking and contact data in one managed PostgreSQL database owned by the shift service
- Good, because it settles the question now.

### Do nothing for now
- Bad, because epics would each decide on their own.

## Status history

| Date | Status | Note |
|---|---|---|
| 2026-09-21 | accepted | Decided by Priya Nair |
FIXTURE
cat > docs/specs/adr/ADR-002.md <<'FIXTURE'
---
id: ADR-002
type: adr
title: "Send shift reminders through the SMS modem on the food bank's on-premises server"
status: superseded
version: 1
created: 2026-09-21
updated: 2026-09-21
owner: "Priya Nair"
authors: ["Priya Nair", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-opus-5-5"
  session: "fixture-session"
reviewed_by: []
approved_by: "Priya Nair"
approved_on: 2026-09-21
upstream:
  - {id: PRD-001, item: FR-008, relation: informed_by, version: 2, hash: null}
supersedes: []
superseded_by: ADR-003
blocked_by: []
# --- adr-specific ---
consulted: []
informed: []
---

# ADR-002 — Send shift reminders through the SMS modem on the food bank's on-premises server

## Context and problem statement

Volunteers get a text reminder before each shift (PRD-001#FR-008, ARCH-001#DEC-03), and the food bank owned a server with an SMS modem in its back office.

## Decision drivers

- Low running cost for a volunteer-run charity.

## Considered options

1. Send shift reminders through the SMS modem on the food bank's on-premises server
2. Do nothing for now

## Decision outcome

**Chosen option:** the on-premises SMS modem, because it was already paid for.

### Consequences

- Good: one clear answer for every epic.
- Bad: it has to be revisited if the food bank's setup changes.

### Confirmation

Reviewed when the spring launch ends.

## Pros and cons of the options

### Send shift reminders through the SMS modem on the food bank's on-premises server
- Good, because it settles the question now.

### Do nothing for now
- Bad, because epics would each decide on their own.

## Status history

| Date | Status | Note |
|---|---|---|
| 2026-09-21 | accepted | Decided by Priya Nair |
| 2026-09-24 | superseded | Superseded by ADR-003 |
FIXTURE
cat > docs/specs/adr/ADR-003.md <<'FIXTURE'
---
id: ADR-003
type: adr
title: "Retire the on-premises server and keep membership-payment audit records in the hosting provider's log store"
status: accepted
version: 1
created: 2026-09-24
updated: 2026-09-24
owner: "Priya Nair"
authors: ["Priya Nair", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-opus-5-5"
  session: "fixture-session"
reviewed_by: []
approved_by: "Priya Nair"
approved_on: 2026-09-24
upstream:
  - {id: PRD-001, item: FR-010, relation: informed_by, version: 2, hash: null}
supersedes: [ADR-002]
superseded_by: null
blocked_by: []
# --- adr-specific ---
consulted: []
informed: []
---

# ADR-003 — Retire the on-premises server and keep membership-payment audit records in the hosting provider's log store

## Context and problem statement

Membership payments (PRD-001#FR-010) need an audit trail kept for seven years (ARCH-001#DEC-04). The back-office server is being removed at the end of October, so nothing can stay on it, including the SMS modem that ADR-002 chose. This decision settles where audit records are kept; how reminders are sent instead is a separate decision that has not been made.

## Decision drivers

- Low running cost for a volunteer-run charity.

## Considered options

1. Retire the on-premises server and keep membership-payment audit records in the hosting provider's log store
2. Do nothing for now

## Decision outcome

**Chosen option:** the hosting provider's log store with seven-year retention, and retire the on-premises server.

### Consequences

- Good: one clear answer for every epic.
- Bad: it has to be revisited if the food bank's setup changes.

### Confirmation

Reviewed when the spring launch ends.

## Pros and cons of the options

### Retire the on-premises server and keep membership-payment audit records in the hosting provider's log store
- Good, because it settles the question now.

### Do nothing for now
- Bad, because epics would each decide on their own.

## Status history

| Date | Status | Note |
|---|---|---|
| 2026-09-24 | accepted | Decided by Priya Nair |
FIXTURE
cat > docs/specs/policy/POL-001.md <<'FIXTURE'
---
id: POL-001
type: policy
title: "Regional Food Bank Network IT policy (vendored)"
status: approved
version: 1
created: 2026-08-01
updated: 2026-08-15
owner: "Regional Food Bank Network IT group"
authors: ["Regional Food Bank Network IT group"]
reviewed_by: ["Regional Food Bank Network IT group"]
approved_by: "Regional Food Bank Network director"
approved_on: 2026-08-15
upstream: []
supersedes: []
superseded_by: null
blocked_by: []
# --- policy-specific ---
scope: organization
source: {repository: "github.com/regional-food-bank-network/it-policy", ref: "v1.0.0"}
---

# POL-001 — Regional Food Bank Network IT policy (vendored)

## 1. Scope and ownership

Applies to the systems of every member food bank. Owned by the network's IT group; changes need the
director's approval.

## 2. Settings

```yaml items
settings:
  - id: SET-01
    status: deprecated
    key: architecture.mandated_platforms
    class: organizational_policy
    value:
      capability: "transactional email"
      platform: "Regional network mail relay (SMTP)"
      source: "Network IT standard 4 (email)"
    overridable_by: []
    rationale: "Member food banks send email only through the network relay, so every message passes its privacy checks"
```

## Change Log

| Version | Date | Author | Change | Settings affected |
|---|---|---|---|---|
| 1 | 2026-08-15 | Network IT group | Initial policy | SET-01 |
FIXTURE
