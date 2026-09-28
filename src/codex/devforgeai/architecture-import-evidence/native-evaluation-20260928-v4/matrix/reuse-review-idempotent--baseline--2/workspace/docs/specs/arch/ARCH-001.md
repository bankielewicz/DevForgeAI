---
id: ARCH-001
type: arch
title: "Riverside Food Bank volunteer shift sign-up architecture"
status: approved
version: 1
created: 2026-09-21
updated: 2026-09-28
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
  - {id: PRD-001, relation: informed_by, version: 2, hash: null}
supersedes: []
superseded_by: null
blocked_by: []
# --- arch-specific ---
system: "Riverside Food Bank volunteer shift sign-up"
outcome: reuse
inspection_scope: []
---

# ARCH-001 — Riverside Food Bank volunteer shift sign-up architecture

## 1. Context and scope

Originally defined against PRD-001 version 1; reviewed for reuse against approved PRD-001 version 2. The PRD change log records only FR-003's priority changing from should to must, with no requirement text changed. The existing scope still covers volunteer sign-in, warehouse shift booking, and the coordinator's roster. The user confirmed reuse on 2026-09-28; no architectural change or new architecture version is needed. No inspection scope was named, and no code was inspected.

Reuse preserves the existing blocking question DEC-02 about session revocation within 5 minutes. ADR-001 resolves the identity provider choice (DEC-01), but does not resolve DEC-02.

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
    deployment: "External: Auth0 (ADR-001)"
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
    state: resolved
    resolved_by: [ADR-001]
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
    finding: "Version 2, status approved: the change log records only FR-003's priority changing from should to must, with no requirement text changed. Sign-in (FR-001), session revocation (NFR-001), privacy (NFR-002), and hosting (NFR-003) remain in scope. The identity provider NEEDS ADR marker is addressed by ADR-001; DEC-02 remains open."
    classification: context
  - id: EVD-02
    status: active
    source: "ADR-001"
    kind: adr
    finding: "Version 1, status accepted: Auth0 handles volunteer sign-in, resolving DEC-01. The ADR does not specify how sessions are revoked within 5 minutes and does not resolve DEC-02."
    classification: decided
```

## 6. Deployment

The web app and the shift service run on the hosting provider (NFR-003); Auth0 is external.

## 7. Requirement changes proposed to the PRD owner

- None.

## 8. Open questions

- DEC-02 (blocking, open): How are a volunteer's sessions revoked within 5 minutes (NFR-001)? Reuse confirmation does not close this decision; resolving architectural evidence is still required.

## Change Log

| Version | Date | Author | Change | Items affected |
|---|---|---|---|---|
| 1 | 2026-09-21 | claude-code (session fixture-session) | Initial draft for PRD-001 v1. Policy resolution: interview.max_calls=8 (default); architecture.mandated_platforms=none (default); quality.required_categories=floor only (default) | all |
| 1 | 2026-09-22 | Priya Nair | Approved | status |
| 1 | 2026-09-25 | claude-code (session prior-review-session) | Reviewed against PRD-001 v2: reuse confirmed, no architectural change. Policy resolution: interview.max_calls=8 (default); architecture.mandated_platforms=none (default); quality.required_categories=floor only (default) | none |
| 1 | 2026-09-28 | Codex | User confirmed reuse for PRD-001 v2: FR-003 priority only, no architectural change. Aligned context, evidence, and item references with v2; retained the existing approval and architecture version. DEC-02 remains open and blocking; ADR-001 resolves DEC-01 only | context, upstream references, EVD-01, EVD-02, open questions |
