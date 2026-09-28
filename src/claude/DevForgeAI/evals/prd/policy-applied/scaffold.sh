#!/usr/bin/env bash
# Seeds a converged BRN-001 and Organization A's POL-001 from src/staging/examples/policy-two-orgs/ (VER-15).
set -euo pipefail
mkdir -p docs/specs/brainstorm
mkdir -p docs/specs/policy
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
cat > docs/specs/policy/POL-001.md <<'FIXTURE'
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
FIXTURE
