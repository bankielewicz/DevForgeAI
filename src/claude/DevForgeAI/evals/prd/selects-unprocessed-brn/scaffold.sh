#!/usr/bin/env bash
# Seeds the fixture documents for this case.
set -euo pipefail
mkdir -p docs/specs/brainstorm docs/specs/prd
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
cat > docs/specs/brainstorm/BRN-002.md <<'FIXTURE_EOF'
---
id: BRN-002
type: brainstorm
title: "Account closure and personal data export for studio members"
status: converged
version: 1
created: 2026-09-15
updated: 2026-09-16
owner: "Leo Park"
authors: ["Leo Park", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-opus-5-5"
  session: "fixture-session-2"
reviewed_by: ["Leo Park"]
approved_by: ""
approved_on: null
upstream: []
supersedes: []
superseded_by: null
blocked_by: []
# --- brainstorm-specific ---
participants: ["Leo Park"]
sources: ["Data-protection audit, September 2026"]
---

# BRN-002 — Account closure and personal data export for studio members

## 1. Context

A data-protection audit found that members who leave cannot close their account or get a copy of their
data without emailing the owner. The data-protection lead owns the remediation, due before the annual audit
in March.

## 2. Problems

```yaml items
problems:
  - id: PRB-01
    status: active
    statement: "Former members cannot close their account or obtain their personal data without emailing the owner"
    who: "Former members"
    evidence: "Data-protection audit, September 2026"
    severity: high
```

## 3. Target users

Members leaving the studio, and the data-protection lead who answers their requests.

## 4. Ideas

```yaml items
ideas:
  - id: IDEA-01
    status: active
    idea: "Members close their own account, which erases their personal data after the legal retention period"
    addresses:
      - PRB-01
    value: "high"
    effort: "medium"
    risk: "medium"
    score: null
    disposition: promoted
    reason: "Required by the audit finding"
  - id: IDEA-02
    status: active
    idea: "Members download all their personal data as a file"
    addresses:
      - PRB-01
    value: "high"
    effort: "low"
    risk: "low"
    score: null
    disposition: promoted
    reason: "Required by the audit finding"
```

## 5. Evaluation method

Value, effort and risk rated by the data-protection lead.

## 6. Convergence

Both ideas were promoted to meet the audit deadline.

## 7. Assumptions and open questions

```yaml items
assumptions:
  - id: ASM-01
    status: active
    statement: "Self-service closure will replace nearly all emailed closure requests"
    validation: "Emailed closure requests in the quarter after launch"
    state: open
```

## 8. Candidate success signals

- No open audit finding on account closure at the March audit.

## Change Log

| Version | Date | Author | Change |
|---|---|---|---|
| 1 | 2026-09-16 | claude-code | Converged with Leo Park |
FIXTURE_EOF
cat > docs/specs/prd/PRD-001.md <<'FIXTURE_EOF'
---
id: PRD-001
type: prd
title: "Online class booking and fee payment"
status: draft
version: 1
created: 2026-09-13
updated: 2026-09-13
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
target_release: "Spring booking launch"
stage: mvp
operating_context: production
stakeholders: ["Priya Nair", "Front-desk lead"]
---

# PRD-001 — Online class booking and fee payment

## 1. Summary

Members book and cancel class places and pay their monthly fee online. SEED-MARKER-prd1

## 2. Problem and opportunity

Booking is phone-only (BRN-001#PRB-01) and fees arrive late (BRN-001#PRB-02).

## 3. Users and personas

Members; front-desk staff.

## 4. Goals and non-goals

**Goals**
- Members manage bookings and payments themselves.

**Non-goals**
- Loyalty points (parked in the brainstorm).

## 5. Success metrics

```yaml items
success_metrics:
  - id: SM-01
    status: active
    metric: "Share of class bookings made online"
    baseline: "0%"
    target: "60% by the end of the spring term"
    measured_by: "Booking system report"
    upstream:
      - {id: BRN-001, item: IDEA-01, relation: derives, version: 1, hash: null}
```

## 6. Functional requirements

```yaml items
functional_requirements:
  - id: FR-001
    status: active
    statement: "The system shall let a member book and cancel a class place online."
    priority: must
    release: current
    notes: null
    upstream:
      - {id: BRN-001, item: IDEA-01, relation: derives, version: 1, hash: null}
  - id: FR-002
    status: active
    statement: "The system shall let a member pay their monthly fee online by card."
    priority: must
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
    statement: "Members sign in before they can book, cancel or pay."
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
    upstream:
      - {id: BRN-001, item: ASM-01, relation: derives, version: 1, hash: null}
```

## 11. Release and rollout

Launch at the start of the spring term.

## 12. Open questions

- [NEEDS CLARIFICATION: reliability requirements for production]

## 13. Epic map

<!-- GENERATED: epics whose upstream cites this PRD. Do not edit by hand. -->

## Change Log

| Version | Date | Author | Change | Items affected |
|---|---|---|---|---|
| 1 | 2026-09-13 | claude-code | Initial draft from BRN-001. Policy resolution: interview.max_calls=8 (default); architecture.mandated_platforms=none (default); quality.required_categories=floor only (default) | all |
FIXTURE_EOF
