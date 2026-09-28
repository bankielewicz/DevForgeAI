---
id: ARCH-001
type: arch
title: "Riverside Food Bank volunteer shift sign-up architecture"
status: draft
version: 2
created: 2026-09-21
updated: 2026-09-28
owner: "Priya Nair"
authors: ["Priya Nair", "claude-code", "Codex"]
generated_by:
  tool: "claude-code"
  model: "claude-opus-5-5"
  session: "fixture-session"
reviewed_by: []
approved_by: null
approved_on: null
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

Reused for PRD-001 version 2 (approved): volunteers sign in, book warehouse shifts, and the coordinator sees the roster. The PRD change log records only FR-003's priority changing from should to must; no requirement text changed. The existing component responsibilities and deployment remain applicable. The user explicitly confirmed the reuse outcome on 2026-09-28. No inspection scope was named, and no code was inspected.

Reuse does not resolve DEC-02, the existing blocking question about session revocation within 5 minutes. ADR-001 resolves identity-provider selection (DEC-01) only. This revision remains draft pending resolution of DEC-02 and review; the version 1 approval is retained in the change log and is not carried forward as approval of version 2.

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
    finding: "Version 2, status approved: the change log records only FR-003 priority changing from should to must, with no requirement text changed. Sign-in (FR-001), session revocation (NFR-001), privacy (NFR-002), and hosting (NFR-003) are unchanged. The identity-provider NEEDS ADR marker is addressed by ADR-001; DEC-02 remains open."
    classification: context
  - id: EVD-02
    status: active
    source: "ADR-001"
    kind: adr
    finding: "Version 1, status accepted: Auth0 handles volunteer sign-in, resolving DEC-01. It does not specify how revoked sessions stop working within 5 minutes and does not resolve DEC-02."
    classification: decided
```

## 6. Deployment

The web app and the shift service run on the hosting provider (NFR-003); Auth0 is external.

## 7. Requirement changes proposed to the PRD owner

- None.

## 8. Open questions

- DEC-02 (blocking): How are a volunteer's sessions revoked within 5 minutes (PRD-001#NFR-001)? Reuse confirmation leaves this decision open; a resolving ADR is still needed.

## Change Log

| Version | Date | Author | Change | Items affected |
|---|---|---|---|---|
| 1 | 2026-09-21 | claude-code (session fixture-session) | Initial draft for PRD-001 v1. Policy resolution: interview.max_calls=8 (default); architecture.mandated_platforms=none (default); quality.required_categories=floor only (default) | all |
| 1 | 2026-09-22 | Priya Nair | Approved | status |
| 2 | 2026-09-28 | Codex | User confirmed reuse for approved PRD-001 v2; FR-003 priority changed from should to must with no requirement text change. Updated PRD references and evidence; retained components, deployment, and decision states. DEC-02 remains blocking and unresolved, so this revision is draft with prior approval cleared | outcome, upstream, evidence, status, DEC-02 |
