#!/usr/bin/env bash
# Seeds the fixture documents for this case.
set -euo pipefail
mkdir -p docs/specs/adr docs/specs/prd
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
cat > docs/specs/adr/ADR-001.md <<'FIXTURE_EOF'
---
id: ADR-001
type: adr
title: "Send structured application logs to the studio's hosted log service"
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
  - {id: PRD-001, item: FR-001, relation: informed_by, version: 2, hash: null}
supersedes: []
superseded_by: null
blocked_by: []
# --- adr-specific ---
consulted: ["Front-desk lead"]
informed: []
---

# ADR-001 — Send structured application logs to the studio's hosted log service

## Context and problem statement

The web app needs one place to record sign-in attempts, bookings and errors (PRD-001#FR-001) so front-desk staff can answer members' questions. This decides only where application logs go.

## Decision drivers

- PRD-001#FR-001

## Considered options

1. Hosted log service
2. Log files on the web server

## Decision outcome

**Chosen option:** Hosted log service, because it fits the studio's small team.

### Consequences

- Good: one approach for the whole web app.
- Bad: the team must learn it.

### Confirmation

Reviewed in the first release review.

## Pros and cons of the options

### Hosted log service
- Good, because it meets the drivers above.
- Bad, because it adds work.

### Log files on the web server
- Good, because it meets the drivers above.
- Bad, because it adds work.

## Status history

| Date | Status | Note |
|---|---|---|
| 2026-09-11 | accepted | Decided by Priya Nair |
FIXTURE_EOF
