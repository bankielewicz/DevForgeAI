#!/usr/bin/env bash
# Seeds BRN-001, fully cited by PRD-001, and BRN-002, cited by no PRD (VER-03).
set -euo pipefail
mkdir -p docs/specs/brainstorm
mkdir -p docs/specs/prd
cat > docs/specs/brainstorm/BRN-001.md <<'FIXTURE'
---
id: BRN-001
type: brainstorm
title: "Volunteer shift sign-up for the Riverside Food Bank"
status: converged
version: 1
created: 2026-09-10
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
upstream: []
supersedes: []
superseded_by: null
blocked_by: []
# --- brainstorm-specific ---
participants: ["Priya Nair"]
sources: ["Coordinator call log, August 2026"]
---

# BRN-001 — Volunteer shift sign-up for the Riverside Food Bank

## 1. Context

The Riverside Food Bank runs three warehouse shifts a day with about 120 active volunteers. The coordinator fills shifts by phone, and about one shift in six starts short-staffed.

## 2. Problems

```yaml items
problems:
  - id: PRB-01
    status: active
    statement: "Volunteers can only sign up for shifts by phoning the coordinator, so shifts go unfilled"
    who: "Volunteer"
    evidence: "Coordinator call log, August 2026"
    severity: high
  - id: PRB-02
    status: active
    statement: "Volunteers forget shifts they signed up for, and the warehouse runs short-staffed"
    who: "Shift coordinator"
    evidence: "No-show tally, summer 2026"
    severity: medium
```

## 3. Target users

Volunteers who pick their own shifts, and the shift coordinator who manages the rota.

## 4. Ideas

```yaml items
ideas:
  - id: IDEA-01
    status: active
    idea: "Volunteers see open shifts and sign up for them online"
    addresses:
      - PRB-01
    value: "high"
    effort: "medium"
    risk: "low"
    score: null
    disposition: promoted
    reason: "Removes most sign-up calls"
  - id: IDEA-02
    status: active
    idea: "Badges and a leaderboard for the volunteers who work the most shifts"
    addresses:
      - PRB-02
    value: "low"
    effort: "medium"
    risk: "low"
    score: null
    disposition: parked
    reason: "Worth trying once sign-up works"
  - id: IDEA-03
    status: active
    idea: "An automatic text reminder the day before each shift"
    addresses:
      - PRB-02
    value: "medium"
    effort: "low"
    risk: "low"
    score: null
    disposition: promoted
    reason: "Cheap and aimed straight at no-shows"
  - id: IDEA-04
    status: active
    idea: "A native mobile app for volunteers"
    addresses:
      - PRB-01
    value: "low"
    effort: "high"
    risk: "medium"
    score: null
    disposition: rejected
    reason: "A mobile-friendly website covers the need"
```

## 5. Evaluation method

Value, effort and risk rated high, medium or low with the coordinator (diverge-converge).

## 6. Convergence

Online sign-up and day-before reminders were promoted. Badges were parked until sign-up works. A native app was rejected.

## 7. Assumptions and open questions

```yaml items
assumptions:
  - id: ASM-01
    status: active
    statement: "We believe that most volunteers will sign up online once they can see open shifts."
    validation: "Share of shifts filled online in the first month"
    state: open
```

- None.

## 8. Candidate success signals

- Fewer shifts that start short-staffed.
- Fewer volunteer no-shows.

## Change Log

| Version | Date | Author | Change |
|---|---|---|---|
| 1 | 2026-09-12 | claude-code (session fixture-session) | Converged |
FIXTURE
cat > docs/specs/brainstorm/BRN-002.md <<'FIXTURE'
---
id: BRN-002
type: brainstorm
title: "Booking donation drop-offs at the Riverside Food Bank"
status: converged
version: 1
created: 2026-09-15
updated: 2026-09-16
owner: "Priya Nair"
authors: ["Priya Nair", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-opus-5-5"
  session: "fixture-session"
reviewed_by: []
approved_by: ""
approved_on: null
upstream: []
supersedes: []
superseded_by: null
blocked_by: []
# --- brainstorm-specific ---
participants: ["Priya Nair"]
sources: []
---

# BRN-002 — Booking donation drop-offs at the Riverside Food Bank

## 1. Context

Large donations arrive without notice two or three times a week.

## 2. Problems

```yaml items
problems:
  - id: PRB-01
    status: active
    statement: "Donors arrive unannounced with large loads, and the dock has no one free to unload"
    who: "Warehouse lead"
    evidence: "Dock log, September 2026"
    severity: high
```

## 3. Target users

Donors with large loads, and the warehouse lead who staffs the dock.

## 4. Ideas

```yaml items
ideas:
  - id: IDEA-01
    status: active
    idea: "Donors book a drop-off slot online for loads over ten boxes"
    addresses:
      - PRB-01
    value: "high"
    effort: "medium"
    risk: "low"
    score: null
    disposition: promoted
    reason: "Lets the dock plan staff"
  - id: IDEA-02
    status: active
    idea: "A donor loyalty card"
    addresses:
      - PRB-01
    value: "low"
    effort: "medium"
    risk: "low"
    score: null
    disposition: rejected
    reason: "Doesn't address the dock problem"
```

## 5. Evaluation method

Rated high, medium or low with the warehouse lead (diverge-converge).

## 6. Convergence

Online drop-off booking was promoted; the loyalty card was rejected.

## 7. Assumptions and open questions

```yaml items
assumptions:
  - id: ASM-01
    status: active
    statement: "We believe that large donors will book ahead if asked."
    validation: "Share of large loads booked in the first month"
    state: open
```

- None.

## 8. Candidate success signals

- Fewer unannounced large drop-offs.

## Change Log

| Version | Date | Author | Change |
|---|---|---|---|
| 1 | 2026-09-16 | claude-code (session fixture-session) | Converged |
FIXTURE
cat > docs/specs/prd/PRD-001.md <<'FIXTURE'
---
id: PRD-001
type: prd
title: "Volunteer shift sign-up"
status: draft
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
approved_by: ""
approved_on: null
upstream:
  - {id: BRN-001, item: PRB-01, relation: derives, version: 1, hash: null}
  - {id: BRN-001, item: PRB-02, relation: derives, version: 1, hash: null}
supersedes: []
superseded_by: null
blocked_by: []
# --- prd-specific ---
target_release: "Spring pilot"
stage: mvp
operating_context: pilot
stakeholders: ["Priya Nair"]
---

# PRD-001 — Volunteer shift sign-up

## 1. Summary

Volunteers see open shifts and sign up online, and get a text the day before.

## 2. Problem and opportunity

Sign-up is phone-only (BRN-001#PRB-01), and forgotten shifts leave the warehouse short (BRN-001#PRB-02).

## 3. Users and personas

Volunteers and the shift coordinator.

## 4. Goals and non-goals

**Goals**
- Every shift is filled without phone calls.

**Non-goals** (explicitly out of scope)
- A native mobile app.

## 5. Success metrics

```yaml items
success_metrics:
  - id: SM-01
    status: active
    metric: "Share of shifts filled online"
    baseline: "0%"
    target: "70% by the end of the pilot"
    measured_by: "Rota export"
    upstream:
      - {id: BRN-001, item: IDEA-01, relation: derives, version: 1, hash: null}
```

## 6. Functional requirements

```yaml items
functional_requirements:
  - id: FR-001
    status: active
    statement: "The system shall let a volunteer see open shifts and sign up for one online."
    priority: must
    release: current
    notes: null
    upstream:
      - {id: BRN-001, item: IDEA-01, relation: derives, version: 1, hash: null}
  - id: FR-002
    status: active
    statement: "The system shall text each volunteer a reminder the day before their shift."
    priority: should
    release: current
    notes: null
    upstream:
      - {id: BRN-001, item: IDEA-03, relation: derives, version: 1, hash: null}
```

## 7. Non-functional requirements

```yaml items
non_functional_requirements:
  - id: NFR-001
    status: active
    category: security
    statement: "Only signed-in volunteers can see the rota."
    priority: must
    release: current
```

## 8. User experience

Mobile-friendly web pages.

## 9. Constraints and dependencies

None beyond section 7.

## 10. Assumptions and risks

```yaml items
assumptions:
  - id: ASM-01
    status: active
    statement: "Most volunteers will sign up online once they can see open shifts."
    validation: "SM-01 after the first month"
    state: open
    upstream:
      - {id: BRN-001, item: ASM-01, relation: derives, version: 1, hash: null}
```

## 11. Release and rollout

One site first, then all sites.

## 12. Open questions

- [NEEDS CLARIFICATION: reliability requirements for pilot]

## 13. Epic map

<!-- GENERATED: epics whose upstream cites this PRD. Do not edit by hand. -->

## Change Log

| Version | Date | Author | Change | Items affected |
|---|---|---|---|---|
| 1 | 2026-09-18 | claude-code (session fixture-session) | Initial draft | all |
FIXTURE
