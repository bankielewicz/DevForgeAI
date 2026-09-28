#!/usr/bin/env bash
# Seeds a converged BRN-001 whose ideas are all parked or rejected (VER-05).
set -euo pipefail
mkdir -p docs/specs/brainstorm
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
    disposition: parked
    reason: "Revisit after the summer rota change"
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
    disposition: rejected
    reason: "Volunteers already get too many texts"
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
    reason: "A mobile-friendly website would cover the need"
```

## 5. Evaluation method

Value, effort and risk rated high, medium or low with the coordinator (diverge-converge).

## 6. Convergence

Nothing was promoted. The coordinator wants to revisit sign-up after the summer rota change.

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
