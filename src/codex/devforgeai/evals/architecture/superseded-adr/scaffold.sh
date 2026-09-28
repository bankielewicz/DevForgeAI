#!/usr/bin/env bash
# Seeds the fixtures for SPEC-003 VER-05 (superseded-adr).
set -euo pipefail
mkdir -p docs/specs/adr docs/specs/arch docs/specs/prd
cat > docs/specs/prd/PRD-001.md <<'FIXTURE'
---
id: PRD-001
type: prd
title: "Volunteer shift sign-up for the Riverside Food Bank"
status: approved
version: 1
created: 2026-09-14
updated: 2026-09-20
owner: "Priya Nair"
authors: ["Priya Nair", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-opus-5-5"
  session: "fixture-session"
reviewed_by: ["Priya Nair"]
approved_by: "Priya Nair"
approved_on: 2026-09-20
upstream:
  - {id: BRN-001, item: PRB-01, relation: derives, version: 1, hash: null}
supersedes: []
superseded_by: null
blocked_by: []
# --- prd-specific ---
target_release: "Pilot"
stage: mvp
operating_context: internal
stakeholders: ["Priya Nair"]
---

# PRD-001 — Volunteer shift sign-up for the Riverside Food Bank

## 1. Summary

Let the food bank's volunteers book warehouse shifts themselves instead of by phone.

## 2. Problem and opportunity

The coordinator fills three warehouse shifts a day by phone, and about one shift in six starts
short-staffed (BRN-001#PRB-01).

## 3. Users and personas

About 120 active volunteers, who book from their phones, and one volunteer coordinator.

## 4. Goals and non-goals

**Goals**
- Volunteers book their own shifts.

**Non-goals** (explicitly out of scope)
- Payroll and donations; volunteers aren't paid.

## 5. Success metrics

```yaml items
success_metrics:
  - id: SM-01
    status: active
    metric: "Share of shifts that start fully staffed"
    baseline: "83%"
    target: "95% by the end of the pilot"
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

None beyond section 7.

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

Pilot with the Tuesday and Thursday shifts, then every shift.

## 12. Open questions

- [NEEDS ADR: identity provider for volunteer sign-in; affects FR-001]

## 13. Epic map

<!-- GENERATED: epics whose upstream cites this PRD. Do not edit by hand. -->

## Change Log

| Version | Date | Author | Change | Items affected |
|---|---|---|---|---|
| 1 | 2026-09-14 | claude-code (session fixture-session) | Initial draft from BRN-001. Policy resolution: interview.max_calls=8 (default); architecture.mandated_platforms=none (default); quality.required_categories=floor only (default) | all |
| 1 | 2026-09-20 | Priya Nair | Approved | status |
FIXTURE
cat > docs/specs/arch/ARCH-001.md <<'FIXTURE'
---
id: ARCH-001
type: arch
title: "Riverside Food Bank volunteer shift sign-up architecture"
status: approved
version: 1
created: 2026-09-21
updated: 2026-09-22
owner: "Priya Nair"
authors: ["Priya Nair", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-opus-5-5"
  session: "fixture-session"
reviewed_by: ["Priya Nair"]
approved_by: "Priya Nair"
approved_on: 2026-09-22
upstream:
  - {id: PRD-001, relation: informed_by, version: 1, hash: null}
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

Defined against PRD-001 version 1 (approved): volunteers sign in and book warehouse shifts. Payroll and donations are outside the system. No inspection scope was named, and no code was inspected.

## 2. Quality drivers

NFR-001 (phone numbers visible only to the coordinator) drives data ownership.

## 3. Components

```mermaid
flowchart LR
    W[CMP-01 Volunteer web app] --> S[CMP-02 Shift service]
    W --> I[CMP-03 Identity provider]
```

```yaml items
components:
  - id: CMP-01
    status: active
    name: "Volunteer web app"
    responsibility: "Sign-in and booking screens; holds no data of its own"
    owns_data: []
    interacts_with:
      - "CMP-02"
      - "CMP-03"
    deployment: "Static site on the hosting provider"
  - id: CMP-02
    status: active
    name: "Shift service"
    responsibility: "Shifts, bookings and volunteer contact details"
    owns_data:
      - "Shifts and bookings"
      - "Volunteer phone numbers"
    interacts_with:
      - "CMP-01"
    deployment: "One hosted service with its database"
    upstream:
      - {id: PRD-001, item: NFR-001, relation: informed_by, version: 1, hash: null}
  - id: CMP-03
    status: active
    name: "Identity provider"
    responsibility: "Authenticates volunteers and issues sessions"
    owns_data:
      - "Volunteer credentials"
    interacts_with:
      - "CMP-01"
    deployment: "Keycloak on the food bank's on-premises server (ADR-002)"
```

## 4. Architectural questions

```yaml items
decisions:
  - id: DEC-01
    status: active
    question: "Which identity provider handles volunteer sign-in?"
    blocking: true
    state: resolved
    resolved_by: [ADR-002]
    notes: null
    upstream:
      - {id: PRD-001, item: FR-001, relation: informed_by, version: 1, hash: null}
  - id: DEC-02
    status: active
    question: "Where are shift, booking and contact data stored, and which component owns them?"
    blocking: true
    state: resolved
    resolved_by: [ADR-001]
    notes: null
    upstream:
      - {id: PRD-001, item: FR-002, relation: informed_by, version: 1, hash: null}
      - {id: PRD-001, item: NFR-001, relation: informed_by, version: 1, hash: null}
```

## 5. Evidence inspected

```yaml items
evidence:
  - id: EVD-01
    status: active
    source: "PRD-001"
    kind: prd
    finding: "Version 1, status approved: sign-in (FR-001), booking (FR-002) and private phone numbers (NFR-001)."
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
    finding: "Version 1, status accepted: Keycloak on the on-premises server handles volunteer sign-in."
    classification: decided
```

## 6. Deployment

The web app and the shift service run on the hosting provider; Keycloak runs on the on-premises server (ADR-002).

## 7. Requirement changes proposed to the PRD owner

- None.

## 8. Open questions

- None.

## Change Log

| Version | Date | Author | Change | Items affected |
|---|---|---|---|---|
| 1 | 2026-09-21 | claude-code (session fixture-session) | Initial draft for PRD-001 v1. Policy resolution: interview.max_calls=8 (default); architecture.mandated_platforms=none (default); quality.required_categories=floor only (default) | all |
| 1 | 2026-09-22 | Priya Nair | Approved | status |
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
  - {id: PRD-001, item: FR-002, relation: informed_by, version: 1, hash: null}
  - {id: PRD-001, item: NFR-001, relation: informed_by, version: 1, hash: null}
supersedes: []
superseded_by: null
blocked_by: []
# --- adr-specific ---
consulted: []
informed: []
---

# ADR-001 — Keep shift, booking and contact data in one managed PostgreSQL database owned by the shift service

## Context and problem statement

Bookings (PRD-001#FR-002) and private phone numbers (PRD-001#NFR-001) need one owner.

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

Reviewed when the pilot ends.

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
title: "Run Keycloak on the food bank's on-premises server for volunteer sign-in"
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
  - {id: PRD-001, item: FR-001, relation: informed_by, version: 1, hash: null}
supersedes: []
superseded_by: ADR-003
blocked_by: []
# --- adr-specific ---
consulted: []
informed: []
---

# ADR-002 — Run Keycloak on the food bank's on-premises server for volunteer sign-in

## Context and problem statement

Volunteers must sign in (PRD-001#FR-001), and the food bank owned a server in its back office.

## Decision drivers

- Low running cost for a volunteer-run charity.

## Considered options

1. Run Keycloak on the food bank's on-premises server for volunteer sign-in
2. Do nothing for now

## Decision outcome

**Chosen option:** Keycloak on the on-premises server, because the server was already paid for.

### Consequences

- Good: one clear answer for every epic.
- Bad: it has to be revisited if the food bank's setup changes.

### Confirmation

Reviewed when the pilot ends.

## Pros and cons of the options

### Run Keycloak on the food bank's on-premises server for volunteer sign-in
- Good, because it settles the question now.

### Do nothing for now
- Bad, because epics would each decide on their own.

## Status history

| Date | Status | Note |
|---|---|---|
| 2026-09-21 | accepted | Decided by Priya Nair |
| 2026-09-26 | superseded | Superseded by ADR-003 |
FIXTURE
cat > docs/specs/adr/ADR-003.md <<'FIXTURE'
---
id: ADR-003
type: adr
title: "Retire the on-premises server and run every service on the hosting provider"
status: accepted
version: 1
created: 2026-09-26
updated: 2026-09-26
owner: "Priya Nair"
authors: ["Priya Nair", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-opus-5-5"
  session: "fixture-session"
reviewed_by: []
approved_by: "Priya Nair"
approved_on: 2026-09-26
upstream:
  - {id: PRD-001, item: FR-001, relation: informed_by, version: 1, hash: null}
  - {id: PRD-001, item: FR-002, relation: informed_by, version: 1, hash: null}
supersedes: [ADR-002]
superseded_by: null
blocked_by: []
# --- adr-specific ---
consulted: []
informed: []
---

# ADR-003 — Retire the on-premises server and run every service on the hosting provider

## Context and problem statement

The back-office server is being removed at the end of October, so nothing can keep running on it, including the Keycloak instance that ADR-002 chose. This decision is about hosting only: which identity provider replaces Keycloak is a separate decision that has not been made.

## Decision drivers

- Low running cost for a volunteer-run charity.

## Considered options

1. Retire the on-premises server and run every service on the hosting provider
2. Do nothing for now

## Decision outcome

**Chosen option:** run every service on the hosting provider, because the server is being removed.

### Consequences

- Good: one clear answer for every epic.
- Bad: it has to be revisited if the food bank's setup changes.

### Confirmation

Reviewed when the pilot ends.

## Pros and cons of the options

### Retire the on-premises server and run every service on the hosting provider
- Good, because it settles the question now.

### Do nothing for now
- Bad, because epics would each decide on their own.

## Status history

| Date | Status | Note |
|---|---|---|
| 2026-09-26 | accepted | Decided by Priya Nair |
FIXTURE
