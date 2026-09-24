#!/usr/bin/env bash
# Seeds the fixture documents for this case.
set -euo pipefail
mkdir -p docs/specs/adr docs/specs/arch docs/specs/prd
cat > docs/specs/prd/PRD-001.md <<'FIXTURE_EOF'
---
id: PRD-001
type: prd
title: "Member self-service for Harbour Yoga Studio"
status: approved
version: 2
created: 2026-09-10
updated: 2026-09-14
owner: "Priya Nair"
authors: ["Priya Nair", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-opus-5-5"
  session: "fixture-session"
reviewed_by: ["Priya Nair"]
approved_by: "Priya Nair"
approved_on: 2026-09-14
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

Studio members sign in to a web app and book or cancel class places themselves, instead of phoning the front desk.

## 2. Problem and opportunity

Members can book class places only by phoning or visiting the front desk (BRN-001#PRB-01).

## 3. Users and personas

Members of the studio; front-desk staff who manage rosters and member accounts.

## 4. Goals and non-goals

**Goals**
- Members manage their own class bookings.

**Non-goals**
- Online payment of fees.

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
    statement: "The system shall let a signed-in member book and cancel a class place."
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
    category: security
    statement: "Front-desk staff can revoke a member's sessions, and a revoked session stops working within 5 minutes."
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

## 13. Epic map

<!-- GENERATED: epics whose upstream cites this PRD. Do not edit by hand. -->

## Change Log

| Version | Date | Author | Change | Items affected |
|---|---|---|---|---|
| 1 | 2026-09-12 | claude-code | Initial draft from BRN-001. Policy resolution: interview.max_calls=8 (default); architecture.mandated_platforms=none (default); quality.required_categories=floor only (default) | all |
| 2 | 2026-09-14 | claude-code | Added NFR-001 session revocation. Policy resolution: interview.max_calls=8 (default); architecture.mandated_platforms=none (default); quality.required_categories=floor only (default) | NFR-001 |
| 2 | 2026-09-14 | Priya Nair | Approved | status |
FIXTURE_EOF
cat > docs/specs/arch/ARCH-001.md <<'FIXTURE_EOF'
---
id: ARCH-001
type: arch
title: "Harbour Yoga Studio member self-service architecture"
status: draft
version: 2
created: 2026-09-11
updated: 2026-09-12
owner: "Priya Nair"
authors: ["Priya Nair", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-opus-5-5"
  session: "fixture-session"
reviewed_by: []
approved_by: ""
approved_on: null
upstream:
  - {id: PRD-001, relation: informed_by, version: 2, hash: null}
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

The member self-service web app for Harbour Yoga Studio, defined against PRD-001 version 2 (approved). SEED-MARKER-arch1

## 2. Quality drivers

PRD-001#NFR-001 (session revocation within 5 minutes).

## 3. Components

```mermaid
flowchart LR
    W[Web app] --> I[Identity]
    W --> B[Booking service]
```

```yaml items
components:
  - id: CMP-01
    status: active
    name: "Web app"
    responsibility: "Member-facing pages for sign-in and booking"
    interacts_with:
      - "CMP-02"
      - "CMP-03"
    deployment: "Studio web server"
    upstream:
      - {id: PRD-001, item: NFR-001, relation: informed_by, version: 2, hash: null}
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
      - {id: PRD-001, item: NFR-001, relation: informed_by, version: 2, hash: null}
  - id: CMP-03
    status: active
    name: "Booking service"
    responsibility: "Class places, bookings and cancellations"
    owns_data:
      - "Classes and bookings"
    interacts_with:
      - "CMP-01"
    deployment: "Studio web server"
    upstream:
      - {id: PRD-001, item: NFR-001, relation: informed_by, version: 2, hash: null}
```

## 4. Architectural questions

```yaml items
decisions:
  - id: DEC-01
    status: active
    question: "Which identity provider signs members in?"
    blocking: true
    state: resolved
    resolved_by: [ADR-002]
    notes: "Decided by Priya Nair"
    upstream:
      - {id: PRD-001, item: FR-001, relation: informed_by, version: 2, hash: null}
  - id: DEC-02
    status: active
    question: "How are member sessions revoked within 5 minutes?"
    blocking: true
    state: resolved
    resolved_by: [ADR-001]
    notes: "Decided by Priya Nair"
    upstream:
      - {id: PRD-001, item: FR-001, relation: informed_by, version: 2, hash: null}
      - {id: PRD-001, item: NFR-001, relation: informed_by, version: 2, hash: null}
```

## 5. Evidence inspected

```yaml items
evidence:
  - id: EVD-01
    status: active
    source: "PRD-001 (version 2, approved)"
    kind: prd
    finding: "Members sign in (FR-001) and book classes (FR-002); sessions must be revocable (NFR-001)"
    classification: context
  - id: EVD-02
    status: active
    source: "ADR-001 (version 1, accepted)"
    kind: adr
    finding: "Sessions are revoked through a server-side session store"
    classification: decided
  - id: EVD-03
    status: active
    source: "ADR-002 (version 1, accepted)"
    kind: adr
    finding: "Acme Cloud is the identity provider"
    classification: decided
```

## 6. Deployment

One studio web server, plus the identity provider.

## 7. Requirement changes proposed to the PRD owner

- None.

## 8. Open questions

- None.

## Change Log

| Version | Date | Author | Change | Items affected |
|---|---|---|---|---|
| 1 | 2026-09-11 | claude-code | Initial draft for PRD-001 v2. Policy resolution: interview.max_calls=8 (default); architecture.mandated_platforms=none (default); quality.required_categories=floor only (default) | all |
| 2 | 2026-09-12 | claude-code | DEC-02 resolved by ADR-001; DEC-01 resolved by ADR-002 (decided by Priya Nair). Policy resolution: interview.max_calls=8 (default); architecture.mandated_platforms=none (default); quality.required_categories=floor only (default) | DEC-01, DEC-02 |
FIXTURE_EOF
cat > docs/specs/adr/ADR-001.md <<'FIXTURE_EOF'
---
id: ADR-001
type: adr
title: "Revoke member sessions through a server-side session store"
status: accepted
version: 1
created: 2026-09-11
updated: 2026-09-11
owner: "Priya Nair"
authors: ["Priya Nair", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-opus-5-5"
  session: "fixture-session"
reviewed_by: []
approved_by: "Priya Nair"
approved_on: 2026-09-11
upstream:
  - {id: PRD-001, item: NFR-001, relation: informed_by, version: 2, hash: null}
  - {id: PRD-001, item: FR-001, relation: informed_by, version: 2, hash: null}
supersedes: []
superseded_by: null
blocked_by: []
# --- adr-specific ---
consulted: ["Front-desk lead"]
informed: []
---

# ADR-001 — Revoke member sessions through a server-side session store

## Context and problem statement

Front-desk staff must be able to revoke a member's sessions within 5 minutes (PRD-001#NFR-001). Answers ARCH-001#DEC-02.

## Decision drivers

- PRD-001#NFR-001

## Considered options

1. Server-side session store
2. Long-lived signed tokens

## Decision outcome

**Chosen option:** Server-side session store, because it fits the studio's small team.

### Consequences

- Good: one approach for the whole web app.
- Bad: the team must learn it.

### Confirmation

Reviewed in the first release review.

## Pros and cons of the options

### Server-side session store
- Good, because it meets the drivers above.
- Bad, because it adds work.

### Long-lived signed tokens
- Good, because it meets the drivers above.
- Bad, because it adds work.

## Status history

| Date | Status | Note |
|---|---|---|
| 2026-09-11 | accepted | Decided by Priya Nair |
FIXTURE_EOF
cat > docs/specs/adr/ADR-002.md <<'FIXTURE_EOF'
---
id: ADR-002
type: adr
title: "Use Acme Cloud for member identity and class photo storage"
status: superseded
version: 1
created: 2026-09-12
updated: 2026-09-12
owner: "Priya Nair"
authors: ["Priya Nair", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-opus-5-5"
  session: "fixture-session"
reviewed_by: []
approved_by: "Priya Nair"
approved_on: 2026-09-12
upstream:
  - {id: PRD-001, item: FR-001, relation: informed_by, version: 2, hash: null}
supersedes: []
superseded_by: ADR-003
blocked_by: []
# --- adr-specific ---
consulted: ["Front-desk lead"]
informed: []
---

# ADR-002 — Use Acme Cloud for member identity and class photo storage

## Context and problem statement

Members need an identity provider to sign in (PRD-001#FR-001), and the studio wants to store class photos. Answers ARCH-001#DEC-01.

## Decision drivers

- PRD-001#FR-001

## Considered options

1. Acme Cloud for both
2. Separate providers

## Decision outcome

**Chosen option:** Acme Cloud for both, because it fits the studio's small team.

### Consequences

- Good: one approach for the whole web app.
- Bad: the team must learn it.

### Confirmation

Reviewed in the first release review.

## Pros and cons of the options

### Acme Cloud for both
- Good, because it meets the drivers above.
- Bad, because it adds work.

### Separate providers
- Good, because it meets the drivers above.
- Bad, because it adds work.

## Status history

| Date | Status | Note |
|---|---|---|
| 2026-09-12 | accepted | Decided by Priya Nair |
| 2026-09-13 | superseded | Superseded by ADR-003 |
FIXTURE_EOF
cat > docs/specs/adr/ADR-003.md <<'FIXTURE_EOF'
---
id: ADR-003
type: adr
title: "Store class photos in Amazon S3"
status: accepted
version: 1
created: 2026-09-13
updated: 2026-09-13
owner: "Priya Nair"
authors: ["Priya Nair", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-opus-5-5"
  session: "fixture-session"
reviewed_by: []
approved_by: "Priya Nair"
approved_on: 2026-09-13
upstream:
  - {id: PRD-001, item: FR-002, relation: informed_by, version: 2, hash: null}
supersedes: [ADR-002]
superseded_by: null
blocked_by: []
# --- adr-specific ---
consulted: ["Front-desk lead"]
informed: []
---

# ADR-003 — Store class photos in Amazon S3

## Context and problem statement

Acme Cloud's photo storage was withdrawn, so ADR-002 is superseded as a whole. This ADR decides only where class photos are stored. It does not decide the identity provider, which is open again.

## Decision drivers

- PRD-001#FR-002

## Considered options

1. Amazon S3
2. The web server disk

## Decision outcome

**Chosen option:** Amazon S3, because it fits the studio's small team.

### Consequences

- Good: one approach for the whole web app.
- Bad: the team must learn it.

### Confirmation

Reviewed in the first release review.

## Pros and cons of the options

### Amazon S3
- Good, because it meets the drivers above.
- Bad, because it adds work.

### The web server disk
- Good, because it meets the drivers above.
- Bad, because it adds work.

## Status history

| Date | Status | Note |
|---|---|---|
| 2026-09-13 | accepted | Decided by Priya Nair |
FIXTURE_EOF
