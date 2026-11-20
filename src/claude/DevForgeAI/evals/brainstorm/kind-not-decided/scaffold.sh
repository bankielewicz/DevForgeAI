#!/usr/bin/env bash
# Seeds the PRD of the staged example brainstorm-brownfield, byte for byte (VER-26).
set -euo pipefail
mkdir -p docs/specs/prd
cat > docs/specs/prd/PRD-001.md <<'PRD'
---
id: PRD-001
type: prd
title: "Online booking for returning patients"
status: approved
version: 3
created: 2026-03-09
updated: 2026-09-14
owner: "Dana"
authors: ["Dana", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-opus-5-5"
  session: "fixture-prd-4d2a"
reviewed_by: ["Dana"]
approved_by: "Dana"
approved_on: 2026-09-14
upstream:
  - {id: BRN-001, item: PRB-01, relation: derives, version: 1, hash: null}
  - {id: BRN-001, item: PRB-02, relation: derives, version: 1, hash: null}
supersedes: []
superseded_by: null
blocked_by: []
# --- prd-specific ---
target_release: "MVP"
stage: mvp
operating_context: production
stakeholders: ["Dana", "Front-desk lead"]
---

# PRD-001 — Online booking for returning patients

## 1. Summary

Returning patients book and cancel their own visits online and get a text reminder two days before.
The booking site has been live since March 2026.

## 2. Problem and opportunity

Patients forget visits booked weeks ahead (BRN-001#PRB-01) and can only book by phone during opening
hours (BRN-001#PRB-02).

## 3. Users and personas

Returning patients booking for themselves; front-desk staff who keep the practice calendar.

## 4. Goals and non-goals

**Goals**
- Returning patients can book a visit at any hour.
- Fewer visits are missed.

**Non-goals** (explicitly out of scope)
- Booking for new patients: the first visit needs a phone call.
- A deposit at booking (rejected in BRN-001).

## 5. Success metrics

```yaml items
success_metrics:
  - id: SM-01
    status: active
    metric: "Share of visits booked online"
    baseline: "0%"
    target: "at least 40% within six months"
    measured_by: "Booking site analytics"
    upstream:
      - {id: BRN-001, item: IDEA-02, relation: derives, version: 1, hash: null}
```

## 6. Functional requirements

```yaml items
functional_requirements:
  - id: FR-001
    status: active
    statement: "The system shall let a returning patient book a free slot online."
    priority: must
    release: current
    notes: null
    upstream:
      - {id: BRN-001, item: IDEA-02, relation: derives, version: 1, hash: null}
  - id: FR-002
    status: active
    statement: "The system shall let a returning patient cancel a booked visit online."
    priority: must
    release: current
    notes: null
    upstream:
      - {id: BRN-001, item: IDEA-02, relation: derives, version: 1, hash: null}
  - id: FR-003
    status: active
    statement: "The system shall send a text reminder two days before each booked visit."
    priority: must
    release: current
    notes: null
    upstream:
      - {id: BRN-001, item: IDEA-01, relation: derives, version: 1, hash: null}
  - id: FR-004
    status: active
    statement: "The system shall sign a returning patient in with a code sent to their phone."
    priority: must
    release: current
    notes: null
    upstream:
      - {id: BRN-001, item: IDEA-02, relation: derives, version: 1, hash: null}
  - id: FR-005
    status: active
    statement: "The system shall show a returning patient their upcoming visits."
    priority: should
    release: current
    notes: null
    upstream:
      - {id: BRN-001, item: IDEA-02, relation: derives, version: 1, hash: null}
  - id: FR-006
    status: active
    statement: "The system shall list each day's online bookings for front-desk staff."
    priority: should
    release: current
    notes: "Added in version 3."
    upstream:
      - {id: BRN-001, item: IDEA-02, relation: derives, version: 1, hash: null}
```

## 7. Non-functional requirements

```yaml items
non_functional_requirements:
  - id: NFR-001
    status: active
    category: privacy
    statement: "Visit details are shown only to the patient they belong to and to clinic staff."
    priority: must
    release: current
```

## 8. User experience

Mobile-friendly web pages. [NEEDS CLARIFICATION: wireframes not yet available]

## 9. Constraints and dependencies

The practice calendar stays the record of all visits.

## 10. Assumptions and risks

```yaml items
assumptions:
  - id: ASM-01
    status: active
    statement: "Patients read texts from the clinic within a day"
    validation: "Reminder pilot: count opened texts for one month"
    state: open
    upstream:
      - {id: BRN-001, item: ASM-01, relation: derives, version: 1, hash: null}
```

## 11. Release and rollout

Live since March 2026 for returning patients.

## 12. Open questions

- [NEEDS CLARIFICATION: whether online bookings can be written into the practice calendar]

## 13. Epic map

No epic cites this PRD yet.

## Change Log

| Version | Date | Author | Change | Items affected |
|---|---|---|---|---|
| 1 | 2026-03-09 | claude-code (session fixture-prd-4d2a) | Initial draft from BRN-001 | all |
| 2 | 2026-03-20 | claude-code (session fixture-prd-4d2a) | Added FR-005 | FR-005 |
| 3 | 2026-09-14 | claude-code (session fixture-prd-4d2a) | Added FR-006 | FR-006 |
| 3 | 2026-09-14 | Dana | Approved | status |
PRD
