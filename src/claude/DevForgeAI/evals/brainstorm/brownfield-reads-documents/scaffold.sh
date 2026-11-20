#!/usr/bin/env bash
# Seeds BRN-001 and PRD-001 of the staged example brainstorm-brownfield, byte for byte, and a PRD-002 without frontmatter (VER-30).
set -euo pipefail
mkdir -p docs/specs/brainstorm
mkdir -p docs/specs/prd
cat > docs/specs/brainstorm/BRN-001.md <<'BRN'
---
id: BRN-001
type: brainstorm
title: "Reducing appointment no-shows at the dental clinic"
status: converged
version: 1
created: 2026-03-02
updated: 2026-03-02
owner: "Dana"
authors: ["Dana", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-opus-5-5"
  session: "fixture-brn-7c1e"
reviewed_by: []
approved_by: ""
approved_on: null
upstream: []
supersedes: []
superseded_by: null
blocked_by: []
# --- brainstorm-specific ---
participants: ["Dana"]
sources: ["Front-desk no-show log, January and February 2026"]
---

# BRN-001 — Reducing appointment no-shows at the dental clinic

## 1. Context

About one in eight booked appointments ends in a no-show. Booking is by phone only, during opening
hours.

## 2. Problems

```yaml items
problems:
  - id: PRB-01
    status: active
    statement: "Patients forget appointments booked weeks ahead."
    who: "Returning patient"
    evidence: "Front-desk no-show log, January and February 2026"
    severity: high
  - id: PRB-02
    status: active
    statement: "Patients can only book or move a visit by phone during opening hours."
    who: "Returning patient"
    evidence: "[NEEDS CLARIFICATION: how many calls go unanswered]"
    severity: medium
```

## 3. Target users

Returning patients who book check-ups months in advance.

## 4. Ideas

```yaml items
ideas:
  - id: IDEA-01
    status: active
    idea: "Text a reminder two days before the visit."
    addresses:
      - PRB-01
    value: "high"
    effort: "low"
    risk: "low"
    score: 4
    disposition: promoted
    reason: "Cheapest way to test whether forgetting is the cause."
  - id: IDEA-02
    status: active
    idea: "Let returning patients book a visit online."
    addresses:
      - PRB-02
    value: "high"
    effort: "medium"
    risk: "low"
    score: 3
    disposition: promoted
    reason: "Removes the opening-hours limit for most patients."
  - id: IDEA-03
    status: active
    idea: "Call every patient the day before."
    addresses:
      - PRB-01
    value: "medium"
    effort: "high"
    risk: "low"
    score: 0
    disposition: rejected
    reason: "The front desk has no time for it."
  - id: IDEA-04
    status: active
    idea: "Let patients move their own appointment online."
    addresses:
      - PRB-02
    value: "high"
    effort: "medium"
    risk: "medium"
    score: 2
    disposition: parked
    reason: "Wait until online booking is in use."
  - id: IDEA-05
    status: active
    idea: "Open a waitlist for freed slots."
    addresses:
      - PRB-01
    value: "medium"
    effort: "medium"
    risk: "low"
    score: 1
    disposition: parked
    reason: "Useful only once cancellations are recorded online."
  - id: IDEA-06
    status: active
    idea: "Charge a deposit at booking."
    addresses:
      - PRB-01
    value: "medium"
    effort: "medium"
    risk: "high"
    score: -1
    disposition: rejected
    reason: "Dana does not want to charge patients before a visit."
```

## 5. Evaluation method

Diverge-converge: problems were framed first, ideas were generated without judgment, and each
idea was then rated high, medium or low for value, effort and risk. The score is
2 × value − effort − risk, counting high = 3, medium = 2 and low = 1 (range −4 to 4); a higher
score is a stronger candidate for promotion.

## 6. Convergence

Dana promoted IDEA-01 and IDEA-02, parked IDEA-04 and IDEA-05 and rejected IDEA-03 and IDEA-06, and
said the brainstorm is done.

## 7. Assumptions and open questions

```yaml items
assumptions:
  - id: ASM-01
    status: active
    statement: "We believe that patients read texts from the clinic within a day."
    validation: "Send reminder texts for one month and count how many are opened."
    state: open
  - id: ASM-02
    status: active
    statement: "We believe that most no-shows are forgetfulness, not cancellations."
    validation: "Call the last 20 no-show patients."
    state: open
```

- [NEEDS CLARIFICATION: Which booking system does the clinic use?]

## 8. Candidate success signals

- No-show rate falls below one in twenty.

## Change Log

| Version | Date | Author | Change |
|---|---|---|---|
| 1 | 2026-03-02 | claude-code (session fixture-brn-7c1e) | Initial draft |
BRN
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
cat > docs/specs/prd/PRD-002.md <<'PRD2'
# PRD-002

Notes for a later release. fixture-prd2-91be
PRD2
