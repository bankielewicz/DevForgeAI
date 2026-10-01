#!/usr/bin/env bash
# Seeds the fixtures for SPEC-002 VER-34 (revisited-brainstorm-extends).
set -euo pipefail
mkdir -p docs/specs/brainstorm docs/specs/prd
cat > docs/specs/brainstorm/BRN-001.md <<'FIXTURE'
---
id: BRN-001
type: brainstorm
title: "Volunteer shift sign-up for the Riverside Food Bank"
status: converged
version: 2
created: 2026-09-10
updated: 2026-09-24
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
  - id: PRB-03
    status: active
    statement: "Volunteers without forklift or food-safety training sign up for shifts that need it"
    who: "Shift coordinator"
    evidence: "Coordinator notes, September 2026"
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
  - id: IDEA-05
    status: active
    idea: "Each shift lists the training it needs, and only volunteers with that training can sign up for it"
    addresses:
      - PRB-03
    value: "high"
    effort: "medium"
    risk: "low"
    score: null
    disposition: promoted
    reason: "Stops untrained sign-ups for forklift and food-safety shifts"
```

## 5. Evaluation method

Value, effort and risk rated high, medium or low with the coordinator (diverge-converge).

## 6. Convergence

Online sign-up and day-before reminders were promoted. Badges were parked until sign-up works. A native app was rejected. Revisited on 2026-09-24: shift training requirements were promoted.

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
| 2 | 2026-09-24 | claude-code (session fixture-session) | Revisited: PRB-03 and IDEA-05 added, IDEA-05 promoted |
FIXTURE
cat > docs/specs/prd/PRD-001.md <<'FIXTURE'
---
id: PRD-001
type: prd
title: "Volunteer shift sign-up for the Riverside Food Bank"
status: draft
version: 1
created: 2026-09-14
updated: 2026-09-20
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
target_release: "Pilot"
stage: mvp
operating_context: internal
stakeholders: ["Priya Nair"]
---

# PRD-001 — Volunteer shift sign-up for the Riverside Food Bank

## 1. Summary

Volunteers see open warehouse shifts and sign up online, and get a text reminder the day before, so
fewer shifts start short-staffed.

## 2. Problem and opportunity

Volunteers can only sign up by phoning the coordinator, so shifts go unfilled (BRN-001#PRB-01), and
volunteers forget shifts they signed up for, so the warehouse runs short-staffed (BRN-001#PRB-02).

## 3. Users and personas

About 120 active volunteers who pick their own shifts, and the shift coordinator who manages the rota.

## 4. Goals and non-goals

**Goals**
- Most shifts are filled online, without phone calls.
- Fewer volunteer no-shows.

**Non-goals** (explicitly out of scope)
- A native mobile app (rejected in the brainstorm).
- Badges and a leaderboard (parked in the brainstorm).

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
  - id: SM-02
    status: active
    metric: "Volunteer no-shows per month"
    baseline: "14"
    target: "7 by the end of the pilot"
    measured_by: "Coordinator's no-show tally"
    upstream:
      - {id: BRN-001, item: IDEA-03, relation: derives, version: 1, hash: null}
```

## 6. Functional requirements

```yaml items
functional_requirements:
  - id: FR-001
    status: active
    statement: "The system shall show volunteers the open warehouse shifts and let them sign up online."
    priority: must
    release: current
    notes: null
    upstream:
      - {id: BRN-001, item: IDEA-01, relation: derives, version: 1, hash: null}
  - id: FR-002
    status: active
    statement: "The system shall send each signed-up volunteer a text reminder the day before their shift."
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
    category: constraint
    statement: "The system runs on hosted services, because the food bank has no on-site server (applies to the whole product)."
    priority: must
    release: current
  - id: NFR-002
    status: active
    category: security
    statement: "A volunteer signs in before they can sign up for a shift."
    priority: must
    release: current
  - id: NFR-003
    status: active
    category: privacy
    statement: "Volunteer phone numbers are visible only to the coordinator."
    priority: must
    release: current
```

## 8. User experience

Mobile-friendly web pages; no app to install.

## 9. Constraints and dependencies

NFR-001 records the hosting constraint.

## 10. Assumptions and risks

```yaml items
assumptions:
  - id: ASM-01
    status: active
    statement: "We believe that most volunteers will sign up online once they can see open shifts."
    validation: "Share of shifts filled online in the first month"
    state: open
    upstream:
      - {id: BRN-001, item: ASM-01, relation: derives, version: 1, hash: null}
```

## 11. Release and rollout

Pilot with the Tuesday and Thursday shifts, then every shift.

## 12. Open questions

- None.

## 13. Epic map

<!-- GENERATED: epics whose upstream cites this PRD. Do not edit by hand. -->

## Change Log

| Version | Date | Author | Change | Items affected |
|---|---|---|---|---|
| 1 | 2026-09-14 | claude-code (session fixture-session) | Initial draft from BRN-001. Policy resolution: interview.max_calls=8 (default); architecture.mandated_platforms=none (default); quality.required_categories=floor only (default) | all |
FIXTURE
