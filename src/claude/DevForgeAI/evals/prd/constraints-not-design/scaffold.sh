#!/usr/bin/env bash
# Seeds a converged bakery pre-order BRN-001 (VER-10).
set -euo pipefail
mkdir -p docs/specs/brainstorm
cat > docs/specs/brainstorm/BRN-001.md <<'FIXTURE'
---
id: BRN-001
type: brainstorm
title: "Online pre-orders for Crumb & Co bakery"
status: converged
version: 1
created: 2026-09-05
updated: 2026-09-06
owner: "Lena Brooks"
authors: ["Lena Brooks", "claude-code"]
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
participants: ["Lena Brooks"]
sources: []
---

# BRN-001 — Online pre-orders for Crumb & Co bakery

## 1. Context

Crumb & Co is a two-shop bakery. Celebration cakes are its most profitable line.

## 2. Problems

```yaml items
problems:
  - id: PRB-01
    status: active
    statement: "Customers can only order celebration cakes in person, so weekday orders are lost"
    who: "Customer"
    evidence: "Counter notes, summer 2026"
    severity: high
  - id: PRB-02
    status: active
    statement: "Unpaid pre-orders are often never collected"
    who: "Bakery owner"
    evidence: "Uncollected-order tally, 2026"
    severity: medium
```

## 3. Target users

Customers ordering celebration cakes, and bakery staff preparing them.

## 4. Ideas

```yaml items
ideas:
  - id: IDEA-01
    status: active
    idea: "Customers order cakes online and pick a collection time"
    addresses:
      - PRB-01
    value: "high"
    effort: "medium"
    risk: "low"
    score: null
    disposition: promoted
    reason: "Captures weekday orders"
  - id: IDEA-02
    status: active
    idea: "Customers pay by card when they order"
    addresses:
      - PRB-02
    value: "high"
    effort: "medium"
    risk: "low"
    score: null
    disposition: promoted
    reason: "Paid orders get collected"
  - id: IDEA-03
    status: active
    idea: "Same-day delivery by courier"
    addresses:
      - PRB-01
    value: "medium"
    effort: "high"
    risk: "low"
    score: null
    disposition: parked
    reason: "Later, once volumes are known"
```

## 5. Evaluation method

Rated high, medium or low with the owner (diverge-converge).

## 6. Convergence

Online ordering and upfront card payment were promoted; courier delivery was parked.

## 7. Assumptions and open questions

```yaml items
assumptions:
  - id: ASM-01
    status: active
    statement: "We believe that customers will pay upfront for a cake."
    validation: "Share of online orders completed at the payment step"
    state: open
```

- None.

## 8. Candidate success signals

- More weekday cake orders.
- Fewer uncollected orders.

## Change Log

| Version | Date | Author | Change |
|---|---|---|---|
| 1 | 2026-09-06 | claude-code (session fixture-session) | Converged |
FIXTURE
