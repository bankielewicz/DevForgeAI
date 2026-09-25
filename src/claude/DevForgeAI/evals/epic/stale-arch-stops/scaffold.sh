#!/usr/bin/env bash
# Seeds the fixture documents for this case.
set -euo pipefail
mkdir -p docs/specs/adr docs/specs/arch docs/specs/policy docs/specs/prd
cat > docs/specs/prd/PRD-001.md <<'FIXTURE_EOF'
---
id: PRD-001
type: prd
title: "Member self-service for Harbour Yoga Studio"
status: approved
version: 2
created: 2026-09-10
updated: 2026-09-15
owner: "Priya Nair"
authors: ["Priya Nair", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-opus-5-5"
  session: "fixture-session"
reviewed_by: ["Priya Nair"]
approved_by: "Priya Nair"
approved_on: 2026-09-15
upstream:
  - {id: BRN-001, item: PRB-01, relation: derives, version: 1, hash: null}
supersedes: []
superseded_by: null
blocked_by: []
# --- prd-specific ---
target_release: "Spring launch"
stage: mvp
operating_context: internal
stakeholders: ["Priya Nair", "Front-desk lead"]
---

# PRD-001 — Member self-service for Harbour Yoga Studio

## 1. Summary

Studio members use a web app to book, cancel and manage their class places themselves, instead of phoning the front desk.

## 2. Problem and opportunity

Members can book class places only by phoning or visiting the front desk (BRN-001#PRB-01).

## 3. Users and personas

Members of the studio; front-desk staff who manage rosters, refunds and member accounts.

## 4. Goals and non-goals

**Goals**
- Members manage their own class bookings.

**Non-goals**
- Replacing the studio's accounting system.

## 5. Success metrics

```yaml items
success_metrics:
  - id: SM-01
    status: active
    metric: "Share of class bookings made online"
    baseline: "0%"
    target: "60% by the end of the spring term"
    measured_by: "Booking records"
    upstream:
      - {id: BRN-001, item: IDEA-01, relation: derives, version: 1, hash: null}
```

## 6. Functional requirements

```yaml items
functional_requirements:
  - id: FR-001
    status: active
    statement: "The system shall let a member sign in to the studio web app with their own account."
    priority: must
    release: current
    notes: null
    upstream:
      - {id: BRN-001, item: IDEA-01, relation: derives, version: 1, hash: null}
  - id: FR-002
    status: active
    statement: "The system shall show members the class timetable and let them book and cancel a class place."
    priority: must
    release: current
    notes: null
    upstream:
      - {id: BRN-001, item: IDEA-01, relation: derives, version: 1, hash: null}
  - id: FR-003
    status: active
    statement: "The system shall let a member join a waiting list for a full class."
    priority: should
    release: current
    notes: null
    upstream:
      - {id: BRN-001, item: IDEA-01, relation: derives, version: 1, hash: null}
  - id: FR-004
    status: active
    statement: "The system shall let a member add a booked class to their phone's calendar."
    priority: could
    release: current
    notes: null
    upstream:
      - {id: BRN-001, item: IDEA-01, relation: derives, version: 1, hash: null}
  - id: FR-005
    status: active
    statement: "The system shall send members a text-message reminder before each booked class."
    priority: must
    release: later
    notes: null
    upstream:
      - {id: BRN-001, item: IDEA-01, relation: derives, version: 1, hash: null}
  - id: FR-006
    status: active
    statement: "The system shall stream classes live to members at home."
    priority: wont
    release: current
    notes: null
    upstream:
      - {id: BRN-001, item: IDEA-01, relation: derives, version: 1, hash: null}
  - id: FR-007
    status: active
    statement: "The system shall let members rate a class after attending it."
    priority: null
    release: current
    notes: null
    upstream:
      - {id: BRN-001, item: IDEA-01, relation: derives, version: 1, hash: null}
  - id: FR-008
    status: active
    statement: "The system shall email a member when a place becomes free on a class they are waiting for."
    priority: must
    release: current
    notes: null
    upstream:
      - {id: BRN-001, item: IDEA-01, relation: derives, version: 1, hash: null}
  - id: FR-009
    status: active
    statement: "The system shall export each day's class rosters to the studio's accounting system."
    priority: must
    release: current
    notes: null
    upstream:
      - {id: BRN-001, item: IDEA-01, relation: derives, version: 1, hash: null}
  - id: FR-010
    status: active
    statement: "The system shall let front-desk staff refund a cancelled class place, recording every refund in an audit log."
    priority: must
    release: current
    notes: null
    upstream:
      - {id: BRN-001, item: IDEA-01, relation: derives, version: 1, hash: null}
  - id: FR-011
    status: active
    statement: "The system shall let members update their contact details."
    priority: must
    release: current
    notes: null
    upstream:
      - {id: BRN-001, item: IDEA-01, relation: derives, version: 1, hash: null}
  - id: FR-012
    status: active
    statement: "The system shall let front-desk staff upload the term timetable as a PDF that members can download."
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
    category: performance
    statement: "Member-facing pages respond within 2 seconds for 95% of requests during the busiest booking hour."
    priority: must
    release: current
```

## 8. User experience

Mobile-friendly web pages.

## 9. Constraints and dependencies

None known.

## 10. Assumptions and risks

```yaml items
assumptions:
  - id: ASM-01
    status: active
    statement: "Most members will book online rather than by phone if they can"
    validation: "SM-01 after the first month"
    state: open
```

## 11. Release and rollout

Launch at the start of the spring term.

## 12. Open questions

- [NEEDS ADR: identity provider for member sign-in; affects FR-001]
- [NEEDS ADR: integration with the studio's accounting system; affects FR-009]
- [NEEDS ADR: payment provider for refunds; affects FR-010]

## 13. Epic map

<!-- GENERATED: epics whose upstream cites this PRD. Do not edit by hand. -->

## Change Log

| Version | Date | Author | Change | Items affected |
|---|---|---|---|---|
| 1 | 2026-09-10 | claude-code | Initial draft from BRN-001. Policy resolution: interview.max_calls=8 (default); architecture.mandated_platforms=none (default); quality.required_categories=floor only (default) | all |
| 1 | 2026-09-12 | Priya Nair | Approved | status |
| 2 | 2026-09-15 | claude-code | Added FR-011 and FR-012 and the rating request FR-007. Policy resolution: interview.max_calls=8 (default); architecture.mandated_platforms=none (default); quality.required_categories=floor only (default) | FR-007, FR-011, FR-012 |
| 2 | 2026-09-15 | Priya Nair | Approved | status |
FIXTURE_EOF
cat > docs/specs/arch/ARCH-001.md <<'FIXTURE_EOF'
---
id: ARCH-001
type: arch
title: "Harbour Yoga Studio member self-service architecture"
status: approved
version: 3
created: 2026-09-16
updated: 2026-09-18
owner: "Priya Nair"
authors: ["Priya Nair", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-opus-5-5"
  session: "fixture-session"
reviewed_by: []
approved_by: "Priya Nair"
approved_on: 2026-09-18
upstream:
  - {id: PRD-001, relation: informed_by, version: 1, hash: null}
supersedes: []
superseded_by: null
blocked_by: []
# --- arch-specific ---
system: "Harbour Yoga Studio member self-service"
outcome: create
inspection_scope: []
---

# ARCH-001 — Harbour Yoga Studio member self-service architecture

## 1. Context and scope

The member self-service web app for Harbour Yoga Studio, defined against PRD-001 version 1 (approved).

## 2. Quality drivers

PRD-001#NFR-001 (pages respond within 2 seconds at the busiest hour).

## 3. Components

```mermaid
flowchart LR
    W[Web app] --> I[Identity]
    W --> B[Booking service]
    B --> N[Notifications]
    W --> F[File store]
```

```yaml items
components:
  - id: CMP-01
    status: active
    name: "Web app"
    responsibility: "Member-facing and front-desk pages"
    interacts_with:
      - "CMP-02"
      - "CMP-03"
      - "CMP-05"
    deployment: "Studio cloud region"
    upstream:
      - {id: PRD-001, item: NFR-001, relation: informed_by, version: 1, hash: null}
  - id: CMP-02
    status: active
    name: "Identity"
    responsibility: "Signs members in and manages their sessions"
    owns_data:
      - "Member accounts and sessions"
    interacts_with:
      - "CMP-01"
    deployment: "Identity provider"
    upstream:
      - {id: PRD-001, item: NFR-001, relation: informed_by, version: 1, hash: null}
  - id: CMP-03
    status: active
    name: "Booking service"
    responsibility: "Timetable, bookings, waiting lists, refunds and the audit log"
    owns_data:
      - "Classes, bookings and waiting lists"
      - "Refund audit records"
    interacts_with:
      - "CMP-01"
      - "CMP-04"
    deployment: "Studio cloud region"
    upstream:
      - {id: PRD-001, item: NFR-001, relation: informed_by, version: 1, hash: null}
  - id: CMP-04
    status: active
    name: "Notifications"
    responsibility: "Emails and text messages to members"
    interacts_with:
      - "CMP-03"
    deployment: "External messaging services"
    upstream:
      - {id: PRD-001, item: NFR-001, relation: informed_by, version: 1, hash: null}
  - id: CMP-05
    status: active
    name: "File store"
    responsibility: "Stores uploaded timetables for download"
    interacts_with:
      - "CMP-01"
    deployment: "Harbour Group File Store"
    upstream:
      - {id: PRD-001, item: NFR-001, relation: informed_by, version: 1, hash: null}
      - {id: POL-001, item: SET-01, relation: constrains, version: 1, hash: null}
```

## 4. Architectural questions

```yaml items
decisions:
  - id: DEC-01
    status: active
    question: "Which identity provider signs members in?"
    blocking: true
    state: open
    resolved_by: []
    notes: "Options: Acme Identity or a self-hosted server; not decided"
    upstream:
      - {id: PRD-001, item: FR-001, relation: informed_by, version: 1, hash: null}
  - id: DEC-02
    status: active
    question: "Where do the booking pages and booking data run, so that pages respond within 2 seconds at the busiest hour?"
    blocking: true
    state: resolved
    resolved_by: [ADR-001]
    notes: "Decided by Priya Nair"
    upstream:
      - {id: PRD-001, item: FR-002, relation: informed_by, version: 1, hash: null}
      - {id: PRD-001, item: NFR-001, relation: informed_by, version: 1, hash: null}
  - id: DEC-03
    status: active
    question: "Which service sends member emails?"
    blocking: true
    state: resolved
    resolved_by: [ADR-002]
    notes: "Decided by Priya Nair"
    upstream:
      - {id: PRD-001, item: FR-008, relation: informed_by, version: 1, hash: null}
  - id: DEC-04
    status: active
    question: "Where are audit records stored, and for how long?"
    blocking: true
    state: resolved
    resolved_by: [ADR-003]
    notes: "Decided by Priya Nair"
    upstream:
      - {id: PRD-001, item: FR-010, relation: informed_by, version: 1, hash: null}
  - id: DEC-05
    status: active
    question: "Which component owns member contact details?"
    blocking: true
    state: resolved
    resolved_by: [ADR-004]
    notes: "Decided by Priya Nair"
    upstream:
      - {id: PRD-001, item: FR-011, relation: informed_by, version: 1, hash: null}
  - id: DEC-06
    status: active
    question: "Which SMS gateway sends class reminders?"
    blocking: true
    state: open
    resolved_by: []
    notes: "Not decided; the reminders are planned for a later release"
    upstream:
      - {id: PRD-001, item: FR-005, relation: informed_by, version: 1, hash: null}
  - id: DEC-07
    status: active
    question: "Which platform stores uploaded files?"
    blocking: true
    state: resolved
    resolved_by: [POL-001#SET-01]
    notes: "Mandated platform for file storage"
    upstream:
      - {id: PRD-001, item: FR-012, relation: informed_by, version: 1, hash: null}
```

## 5. Evidence inspected

```yaml items
evidence:
  - id: EVD-01
    status: active
    source: "PRD-001 (version 1, approved)"
    kind: prd
    finding: "Twelve functional requirements and one performance requirement; three NEEDS ADR markers"
    classification: context
  - id: EVD-02
    status: active
    source: "POL-001 (version 1, approved)"
    kind: policy
    finding: "SET-01 mandates the Harbour Group File Store for file storage"
    classification: policy
  - id: EVD-03
    status: active
    source: "ADR-001 (version 1, accepted)"
    kind: adr
    finding: "Booking pages and data run as one managed web app and database in the studio's cloud region"
    classification: decided
  - id: EVD-04
    status: active
    source: "ADR-002 (version 1, accepted)"
    kind: adr
    finding: "Acme Cloud sends member emails and stores audit records"
    classification: decided
  - id: EVD-05
    status: active
    source: "ADR-003 (version 1, accepted)"
    kind: adr
    finding: "Audit records are kept in the booking database for seven years"
    classification: decided
  - id: EVD-06
    status: active
    source: "ADR-004 (version 1, accepted)"
    kind: adr
    finding: "The booking service owns member contact details"
    classification: decided
```

## 6. Deployment

One managed web app and database in the studio's cloud region, the identity provider, external messaging services and the Harbour Group File Store.

## 7. Requirement changes proposed to the PRD owner

- None.

## 8. Open questions

- None.

## Change Log

| Version | Date | Author | Change | Items affected |
|---|---|---|---|---|
| 1 | 2026-09-16 | claude-code | Initial draft for PRD-001 v1; DEC-07 resolved by POL-001#SET-01 (mandated platform). Policy resolution: interview.max_calls=8 (default); architecture.mandated_platforms=Harbour Group File Store for file storage (POL-001#SET-01); quality.required_categories=floor only (default) | all |
| 2 | 2026-09-17 | claude-code | DEC-02 resolved by ADR-001; DEC-03 resolved by ADR-002; DEC-05 resolved by ADR-004 (decided by Priya Nair). Policy resolution: interview.max_calls=8 (default); architecture.mandated_platforms=Harbour Group File Store for file storage (POL-001#SET-01); quality.required_categories=floor only (default) | DEC-02, DEC-03, DEC-05 |
| 3 | 2026-09-18 | claude-code | DEC-04 resolved by ADR-003 (decided by Priya Nair). Policy resolution: interview.max_calls=8 (default); architecture.mandated_platforms=Harbour Group File Store for file storage (POL-001#SET-01); quality.required_categories=floor only (default) | DEC-04 |
| 3 | 2026-09-18 | Priya Nair | Approved | status |
FIXTURE_EOF
cat > docs/specs/adr/ADR-001.md <<'FIXTURE_EOF'
---
id: ADR-001
type: adr
title: "Run the booking pages and data as one managed web app and database"
status: accepted
version: 1
created: 2026-09-17
updated: 2026-09-17
owner: "Priya Nair"
authors: ["Priya Nair", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-opus-5-5"
  session: "fixture-session"
reviewed_by: []
approved_by: "Priya Nair"
approved_on: 2026-09-17
upstream:
  - {id: PRD-001, item: FR-002, relation: informed_by, version: 2, hash: null}
  - {id: PRD-001, item: NFR-001, relation: informed_by, version: 2, hash: null}
supersedes: []
superseded_by: null
blocked_by: []
# --- adr-specific ---
consulted: ["Front-desk lead"]
informed: []
---

# ADR-001 — Run the booking pages and data as one managed web app and database

## Context and problem statement

Member pages must respond within 2 seconds at the busiest hour (PRD-001#NFR-001). Answers ARCH-001#DEC-02.

## Decision drivers

- PRD-001#NFR-001
- The studio's small team

## Considered options

1. One managed web app and database in one cloud region
2. Separate services per feature

## Decision outcome

**Chosen option:** One managed web app and database in one cloud region, because it fits the studio's small team.

### Consequences

- Good: one approach for the whole web app.
- Bad: the team depends on one provider.

### Confirmation

Reviewed in the first release review.

## Pros and cons of the options

### One managed web app and database in one cloud region
- Good, because it meets the drivers above.
- Bad, because it adds a dependency.

### Separate services per feature
- Good, because it meets the drivers above.
- Bad, because it adds work.

## Status history

| Date | Status | Note |
|---|---|---|
| 2026-09-17 | accepted | Decided by Priya Nair |
FIXTURE_EOF
cat > docs/specs/adr/ADR-002.md <<'FIXTURE_EOF'
---
id: ADR-002
type: adr
title: "Use Acme Cloud for member emails and audit records"
status: superseded
version: 1
created: 2026-09-17
updated: 2026-09-17
owner: "Priya Nair"
authors: ["Priya Nair", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-opus-5-5"
  session: "fixture-session"
reviewed_by: []
approved_by: "Priya Nair"
approved_on: 2026-09-17
upstream:
  - {id: PRD-001, item: FR-008, relation: informed_by, version: 2, hash: null}
supersedes: []
superseded_by: ADR-003
blocked_by: []
# --- adr-specific ---
consulted: ["Front-desk lead"]
informed: []
---

# ADR-002 — Use Acme Cloud for member emails and audit records

## Context and problem statement

Members get emails (PRD-001#FR-008) and refunds are audited (PRD-001#FR-010). Answers ARCH-001#DEC-03.

## Decision drivers

- PRD-001#NFR-001
- The studio's small team

## Considered options

1. Acme Cloud
2. The studio mail server

## Decision outcome

**Chosen option:** Acme Cloud, because it fits the studio's small team.

### Consequences

- Good: one approach for the whole web app.
- Bad: the team depends on one provider.

### Confirmation

Reviewed in the first release review.

## Pros and cons of the options

### Acme Cloud
- Good, because it meets the drivers above.
- Bad, because it adds a dependency.

### The studio mail server
- Good, because it meets the drivers above.
- Bad, because it adds work.

## Status history

| Date | Status | Note |
|---|---|---|
| 2026-09-17 | accepted | Decided by Priya Nair |
| 2026-09-19 | superseded | Superseded by ADR-003 (audit records move to the booking database) |
FIXTURE_EOF
cat > docs/specs/adr/ADR-003.md <<'FIXTURE_EOF'
---
id: ADR-003
type: adr
title: "Keep audit records in the booking database for seven years"
status: accepted
version: 1
created: 2026-09-18
updated: 2026-09-18
owner: "Priya Nair"
authors: ["Priya Nair", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-opus-5-5"
  session: "fixture-session"
reviewed_by: []
approved_by: "Priya Nair"
approved_on: 2026-09-18
upstream:
  - {id: PRD-001, item: FR-010, relation: informed_by, version: 2, hash: null}
supersedes: [ADR-002]
superseded_by: null
blocked_by: []
# --- adr-specific ---
consulted: ["Front-desk lead"]
informed: []
---

# ADR-003 — Keep audit records in the booking database for seven years

## Context and problem statement

Refunds must be recorded in an audit log (PRD-001#FR-010). Answers ARCH-001#DEC-04.

## Decision drivers

- PRD-001#NFR-001
- The studio's small team

## Considered options

1. The booking database
2. Acme Cloud storage

## Decision outcome

**Chosen option:** The booking database, because it fits the studio's small team.

### Consequences

- Good: one approach for the whole web app.
- Bad: the team depends on one provider.

### Confirmation

Reviewed in the first release review.

## Pros and cons of the options

### The booking database
- Good, because it meets the drivers above.
- Bad, because it adds a dependency.

### Acme Cloud storage
- Good, because it meets the drivers above.
- Bad, because it adds work.

## Status history

| Date | Status | Note |
|---|---|---|
| 2026-09-18 | accepted | Decided by Priya Nair |
FIXTURE_EOF
cat > docs/specs/policy/POL-001.md <<'FIXTURE_EOF'
---
id: POL-001
type: policy
title: "Harbour Group engineering policy (vendored)"
status: approved
version: 1
created: 2026-08-01
updated: 2026-08-01
owner: "Harbour Group architecture board"
authors: ["Harbour Group architecture board"]
reviewed_by: ["Harbour Group architecture board"]
approved_by: "Harbour Group CTO"
approved_on: 2026-08-01
upstream: []
supersedes: []
superseded_by: null
blocked_by: []
# --- policy-specific ---
scope: organization
source: {repository: "github.com/harbour-group/engineering-policy", ref: "v1.0.0"}
---

# POL-001 — Harbour Group engineering policy (vendored)

## 1. Scope and ownership

Applies to every product at Harbour Group. Owned by the architecture board; changes need CTO approval.

## 2. Settings

```yaml items
settings:
  - id: SET-01
    status: active
    key: architecture.mandated_platforms
    class: organizational_policy
    value:
      capability: "file storage"
      platform: "Harbour Group File Store"
      source: "Harbour Group architecture standard AS-12"
    overridable_by: []
    rationale: "One file store across the group, with shared backup and retention"
```

## Change Log

| Version | Date | Author | Change | Settings affected |
|---|---|---|---|---|
| 1 | 2026-08-01 | Architecture board | Initial policy | SET-01 |
FIXTURE_EOF
