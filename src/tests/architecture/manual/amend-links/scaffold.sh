#!/usr/bin/env bash
# Seeds the fixtures for the manual SPEC-003 VER-12 (j) (amend-links); see docs/runbooks.
set -euo pipefail
mkdir -p docs/specs/arch docs/specs/prd
cat > docs/specs/prd/PRD-001.md <<'FIXTURE'
---
id: PRD-001
type: prd
title: "Volunteer shift sign-up for the Riverside Food Bank"
status: approved
version: 3
created: 2026-09-14
updated: 2026-09-27
owner: "Priya Nair"
authors: ["Priya Nair", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-opus-5-5"
  session: "fixture-session"
reviewed_by: ["Priya Nair"]
approved_by: "Priya Nair"
approved_on: 2026-09-27
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

Let the food bank's volunteers book warehouse shifts themselves instead of by phone, and give the
coordinator a live roster.

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
  - id: FR-003
    status: active
    statement: "The system shall show the coordinator each day's roster of booked volunteers."
    priority: must
    release: current
    notes: null
    upstream:
      - {id: BRN-001, item: IDEA-02, relation: derives, version: 1, hash: null}
```

## 7. Non-functional requirements

```yaml items
non_functional_requirements:
  - id: NFR-001
    status: active
    category: security
    statement: "An administrator can revoke a volunteer's signed-in sessions, and a revoked session stops working within 5 minutes."
    priority: must
    release: current
  - id: NFR-002
    status: active
    category: privacy
    statement: "Volunteer phone numbers are visible only to the coordinator."
    priority: must
    release: current
  - id: NFR-003
    status: active
    category: constraint
    statement: "The food bank has no on-site server, so the system runs on hosted services (applies to the whole product)."
    priority: must
    release: current
```

## 8. User experience

Mobile-first web pages; no app to install.

## 9. Constraints and dependencies

NFR-003 records the hosting constraint.

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
- [NEEDS ADR: where the coordinator's daily roster is served from; affects FR-003]

## 13. Epic map

<!-- GENERATED: epics whose upstream cites this PRD. Do not edit by hand. -->

## Change Log

| Version | Date | Author | Change | Items affected |
|---|---|---|---|---|
| 1 | 2026-09-14 | claude-code (session fixture-session) | Initial draft from BRN-001. Policy resolution: interview.max_calls=8 (default); architecture.mandated_platforms=none (default); quality.required_categories=floor only (default) | all |
| 1 | 2026-09-20 | Priya Nair | Approved | status |
| 2 | 2026-09-24 | Priya Nair | Priority change only: FR-003 should to must. No requirement text changed | FR-003 |
| 2 | 2026-09-24 | Priya Nair | Approved | status |
| 3 | 2026-09-27 | Priya Nair | Added a NEEDS ADR marker: where the roster is served from. No requirement changed | none |
| 3 | 2026-09-27 | Priya Nair | Approved | status |
FIXTURE
cat > docs/specs/arch/ARCH-001.md <<'FIXTURE'
---
id: ARCH-001
type: arch
title: "Riverside Food Bank volunteer shift sign-up architecture"
status: draft
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
approved_by: ""
approved_on: null
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

Defined against PRD-001 version 2 (approved): volunteers sign in, book warehouse shifts, and the coordinator sees the roster. No inspection scope was named, and no code was inspected.

## 2. Quality drivers

NFR-001 (session revocation) and NFR-002 (private phone numbers) drive the design; NFR-003 rules out an on-site server.

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
      - {id: PRD-001, item: NFR-002, relation: informed_by, version: 2, hash: null}
  - id: CMP-03
    status: active
    name: "Identity provider"
    responsibility: "Authenticates volunteers and issues sessions"
    owns_data:
      - "Volunteer credentials"
    interacts_with:
      - "CMP-01"
    deployment: "External; the provider is open (DEC-01)"
    upstream:
      - {id: PRD-001, item: NFR-001, relation: informed_by, version: 2, hash: null}
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
    question: "How are a volunteer's sessions revoked within 5 minutes (NFR-001)?"
    blocking: true
    state: open
    resolved_by: []
    notes: null
    upstream:
      - {id: PRD-001, item: FR-001, relation: informed_by, version: 2, hash: null}
      - {id: PRD-001, item: NFR-001, relation: informed_by, version: 2, hash: null}
```

## 5. Evidence inspected

```yaml items
evidence:
  - id: EVD-01
    status: active
    source: "PRD-001"
    kind: prd
    finding: "Version 2, status approved: sign-in (FR-001) with session revocation (NFR-001); the identity provider is a NEEDS ADR marker."
    classification: context
```

## 6. Deployment

The web app and the shift service run on the hosting provider (NFR-003).

## 7. Requirement changes proposed to the PRD owner

- None.

## 8. Open questions

- None.

## Change Log

| Version | Date | Author | Change | Items affected |
|---|---|---|---|---|
| 1 | 2026-09-21 | claude-code (session fixture-session) | Initial draft for PRD-001 v2. Policy resolution: interview.max_calls=8 (default); architecture.mandated_platforms=none (default); quality.required_categories=floor only (default) | all |
FIXTURE
