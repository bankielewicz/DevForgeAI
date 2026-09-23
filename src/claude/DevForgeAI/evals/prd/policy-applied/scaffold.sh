#!/usr/bin/env bash
# Seeds the fixture documents for this case.
set -euo pipefail
mkdir -p docs/specs/brainstorm docs/specs/policy
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
    disposition: promoted
    reason: "Removes most booking calls"
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
    disposition: promoted
    reason: "Directly targets late payments"
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

Online booking and online fee payment were promoted. Loyalty points were parked. Wearable sync was rejected.

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
cat > docs/specs/policy/POL-001.md <<'FIXTURE_EOF'
---
id: POL-001
type: policy
title: "Organization A engineering policy (vendored)"
status: approved
version: 3
created: 2026-06-01
updated: 2026-09-01
owner: "Organization A architecture board"
authors: ["Organization A architecture board"]
reviewed_by: ["Organization A architecture board"]
approved_by: "Organization A CTO"
approved_on: 2026-09-01
upstream: []
supersedes: []
superseded_by: null
blocked_by: []
# --- policy-specific ---
scope: organization
source: {repository: "github.com/org-a/engineering-policy", ref: "v3.0.0"}
---

# POL-001 — Organization A engineering policy (vendored)

## 1. Scope and ownership

Applies to every product at Organization A. Owned by the architecture board; changes need CTO approval.

## 2. Settings

```yaml items
settings:
  - id: SET-01
    status: active
    key: architecture.mandated_platforms
    class: organizational_policy
    value:
      capability: "identity and authentication"
      platform: "Org A Identity Platform (OIDC)"
      source: "ADR-104 (Organization A architecture repository)"
    overridable_by: []
    rationale: "One identity platform across all products; no product runs its own sign-in"
  - id: SET-02
    status: active
    key: quality.required_categories
    class: organizational_policy
    value:
      - compliance
      - accessibility
    applies_when:
      operating_context:
        - internal
        - pilot
        - production
    overridable_by: []
    rationale: "SOC 2 scope and the organization's accessibility commitment cover internal tools too"
```

## Change Log

| Version | Date | Author | Change | Settings affected |
|---|---|---|---|---|
| 3 | 2026-09-01 | Architecture board | Accessibility required for internal tools | SET-02 |
FIXTURE_EOF
