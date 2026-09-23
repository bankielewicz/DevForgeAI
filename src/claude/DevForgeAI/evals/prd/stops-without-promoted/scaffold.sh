#!/usr/bin/env bash
# Seeds the fixture documents for this case.
set -euo pipefail
mkdir -p docs/specs/brainstorm
cat > docs/specs/brainstorm/BRN-001.md <<'FIXTURE_EOF'
---
id: BRN-001
type: brainstorm
title: "Member self-service for a boutique fitness studio"
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
reviewed_by: ["Priya Nair"]
approved_by: ""
approved_on: null
upstream: []
supersedes: []
superseded_by: null
blocked_by: []
# --- brainstorm-specific ---
participants: ["Priya Nair", "Front-desk lead"]
sources: ["Front-desk call log, August 2026", "Accounts receivable report, Q2 2026"]
---

# BRN-001 — Member self-service for a boutique fitness studio

## 1. Context

The studio runs about forty classes a week. Members book by phone or at the desk, and pay monthly fees by
bank transfer. Staff spend hours a day on bookings and chasing payments.

## 2. Problems

```yaml items
problems:
  - id: PRB-01
    status: active
    statement: "Members can book class places only by phoning or visiting the front desk"
    who: "Members"
    evidence: "Front-desk call log, August 2026"
    severity: high
  - id: PRB-02
    status: active
    statement: "Monthly fees are paid by bank transfer and a quarter of them arrive late"
    who: "Studio owner"
    evidence: "Accounts receivable report, Q2 2026"
    severity: medium
```

## 3. Target users

Studio members booking classes and paying fees, and front-desk staff who manage class rosters.

## 4. Ideas

```yaml items
ideas:
  - id: IDEA-01
    status: active
    idea: "Members book and cancel class places online"
    addresses:
      - PRB-01
    value: "high"
    effort: "medium"
    risk: "low"
    score: null
    disposition: parked
    reason: "Wait for the new front-desk system"
  - id: IDEA-02
    status: active
    idea: "Loyalty points for attendance streaks"
    addresses:
      - PRB-01
    value: "low"
    effort: "medium"
    risk: "low"
    score: null
    disposition: parked
    reason: "Nice to have once booking works"
  - id: IDEA-03
    status: active
    idea: "Members pay their monthly fee online by card"
    addresses:
      - PRB-02
    value: "high"
    effort: "medium"
    risk: "medium"
    score: null
    disposition: rejected
    reason: "The bank offers direct debit instead"
  - id: IDEA-04
    status: active
    idea: "Sync workouts from fitness wearables"
    addresses:
      - PRB-01
    value: "low"
    effort: "high"
    risk: "high"
    score: null
    disposition: rejected
    reason: "Does not address booking or payment"
```

## 5. Evaluation method

Value, effort and risk rated high, medium or low by the participants (diverge-converge).

## 6. Convergence

No idea was promoted. Booking and loyalty points were parked; online payment and wearable sync were rejected.

## 7. Assumptions and open questions

```yaml items
assumptions:
  - id: ASM-01
    status: active
    statement: "Most members will book online rather than by phone if they can"
    validation: "Share of bookings made online in the first month"
    state: open
```

## 8. Candidate success signals

- Fewer booking calls to the front desk.
- Fewer late fee payments.

## Change Log

| Version | Date | Author | Change |
|---|---|---|---|
| 1 | 2026-09-12 | claude-code | Converged with Priya Nair |
FIXTURE_EOF
