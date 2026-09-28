---
id: ARCH-001
type: arch
title: "Riverside Food Bank volunteer shift sign-up architecture"
status: draft
version: 2
created: 2026-09-21
updated: 2026-09-28
owner: "Priya Nair"
authors: ["Priya Nair", "claude-code", "codex"]
generated_by:
  tool: "codex"
  model: "GPT-6"
  session: null
reviewed_by: []
approved_by: null
approved_on: null
upstream:
  - {id: PRD-001, relation: informed_by, version: 1, hash: null}
supersedes: []
superseded_by: null
blocked_by: []
# --- arch-specific ---
system: "Riverside Food Bank volunteer shift sign-up"
outcome: amend
inspection_scope: []
---

# ARCH-001 — Riverside Food Bank volunteer shift sign-up architecture

## 1. Context and scope

Defined against PRD-001 version 1 (approved): volunteers sign in and book warehouse shifts. Payroll and donations are outside the system. No inspection scope was named, and no code was inspected.

This amendment reflects accepted ADR-003, which supersedes ADR-002 and retires the on-premises server at the end of October. ADR-003 settles hosting only; it explicitly leaves the replacement identity provider undecided. The user confirmed the amend outcome. Version 2 is a draft with a blocking identity decision; the version 1 approval remains recorded in the change log.

## 2. Quality drivers

NFR-001 (phone numbers visible only to the coordinator) drives data ownership.

## 3. Components

```mermaid
flowchart LR
    W[CMP-01 Volunteer web app] --> S[CMP-02 Shift service]
    W --> I[CMP-03 Identity provider - selection pending]
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
    deployment: "One service on the hosting provider (ADR-003), with its managed PostgreSQL database (ADR-001)"
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
    deployment: "Hosting provider required by ADR-003; replacement identity provider pending DEC-01"
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
    notes: "Reopened: ADR-002 is superseded by ADR-003. ADR-003 resolves hosting only and explicitly leaves the replacement identity provider undecided. A new identity-provider ADR is required."
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
  - id: DEC-03
    status: active
    question: "Where do services run after the on-premises server is retired?"
    blocking: true
    state: resolved
    resolved_by: [ADR-003]
    notes: "Every service runs on the hosting provider; this does not select the replacement identity provider."
    upstream:
      - {id: PRD-001, item: FR-001, relation: informed_by, version: 1, hash: null}
      - {id: PRD-001, item: FR-002, relation: informed_by, version: 1, hash: null}
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
    finding: "Version 1, status superseded by ADR-003: the former choice of Keycloak on the on-premises server no longer resolves DEC-01."
    classification: context
  - id: EVD-04
    status: active
    source: "ADR-003"
    kind: adr
    finding: "Version 1, status accepted: retires the on-premises server at the end of October and requires every service to run on the hosting provider. Explicitly leaves the replacement identity provider undecided. Resolves DEC-03, not DEC-01."
    classification: decided
```

## 6. Deployment

Every service must run on the hosting provider under ADR-003; no component may depend on the on-premises server after its retirement at the end of October. The web app remains a static site, and the shift service retains ownership of shifts, bookings and contact details in managed PostgreSQL under ADR-001. The replacement identity provider and its deployment details await DEC-01; ADR-003 does not authorize a particular provider or a relocation of Keycloak.

## 7. Requirement changes proposed to the PRD owner

- None.

## 8. Open questions

- [NEEDS ADR: replacement identity provider for volunteer sign-in, consistent with ADR-003 hosting; affects PRD-001#FR-001 and blocks DEC-01]. The existing PRD-001 sign-in question remains open; no requirement change is proposed.

## Change Log

| Version | Date | Author | Change | Items affected |
|---|---|---|---|---|
| 1 | 2026-09-21 | claude-code (session fixture-session) | Initial draft for PRD-001 v1. Policy resolution: interview.max_calls=8 (default); architecture.mandated_platforms=none (default); quality.required_categories=floor only (default) | all |
| 1 | 2026-09-22 | Priya Nair | Approved | status |
| 2 | 2026-09-28 | codex | User-confirmed amend outcome. Applied accepted ADR-003 hosting decision; retained ADR-001 data ownership; reclassified superseded ADR-002 as historical context and reopened identity-provider selection. Returned to draft pending the blocking identity decision and review. No code inspected. | outcome, status, CMP-02, CMP-03, DEC-01, DEC-03, EVD-03, EVD-04, deployment, open questions |
