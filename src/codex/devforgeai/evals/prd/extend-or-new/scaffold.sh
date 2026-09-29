#!/usr/bin/env bash
# Seeds Ledgerly's onboarding BRN-001 and approved PRD-001, plus the account-closure BRN-002 (VER-06).
set -euo pipefail
mkdir -p docs/specs/brainstorm
mkdir -p docs/specs/prd
cat > docs/specs/brainstorm/BRN-001.md <<'FIXTURE'
---
id: BRN-001
type: brainstorm
title: "Recovering stalled sign-ups in Ledgerly onboarding"
status: converged
version: 1
created: 2026-08-01
updated: 2026-08-03
owner: "Sam Ortiz"
authors: ["Sam Ortiz", "claude-code"]
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
participants: ["Sam Ortiz"]
sources: []
---

# BRN-001 — Recovering stalled sign-ups in Ledgerly onboarding

## 1. Context

Ledgerly is a bookkeeping app for freelancers. Forty percent of new users stall during onboarding.

## 2. Problems

```yaml items
problems:
  - id: PRB-01
    status: active
    statement: "New users abandon onboarding at the bank-connection step"
    who: "New Ledgerly user"
    evidence: "Funnel report, Q3 2026"
    severity: high
```

## 3. Target users

New Ledgerly users in their first week.

## 4. Ideas

```yaml items
ideas:
  - id: IDEA-01
    status: active
    idea: "Email users who stall at bank connection with a resume link"
    addresses:
      - PRB-01
    value: "high"
    effort: "medium"
    risk: "low"
    score: null
    disposition: promoted
    reason: "Direct and cheap"
```

## 5. Evaluation method

Rated with the growth team (diverge-converge).

## 6. Convergence

The resume email was promoted.

## 7. Assumptions and open questions

```yaml items
assumptions:
  - id: ASM-01
    status: active
    statement: "We believe that most stalled users still want to finish onboarding."
    validation: "Resume-link click rate"
    state: open
```

- None.

## 8. Candidate success signals

- More new users finish onboarding.

## Change Log

| Version | Date | Author | Change |
|---|---|---|---|
| 1 | 2026-08-03 | claude-code (session fixture-session) | Converged |
FIXTURE
cat > docs/specs/prd/PRD-001.md <<'FIXTURE'
---
id: PRD-001
type: prd
title: "Ledgerly onboarding recovery"
status: approved
version: 1
created: 2026-08-05
updated: 2026-08-20
owner: "Sam Ortiz"
authors: ["Sam Ortiz", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-opus-5-5"
  session: "fixture-session"
reviewed_by: []
approved_by: "Sam Ortiz"
approved_on: 2026-08-20
upstream:
  - {id: BRN-001, item: PRB-01, relation: derives, version: 1, hash: null}
supersedes: []
superseded_by: null
blocked_by: []
# --- prd-specific ---
target_release: "Onboarding recovery (Q4)"
stage: evolution
operating_context: production
stakeholders: ["Sam Ortiz"]
---

# PRD-001 — Ledgerly onboarding recovery

## 1. Summary

Bring back new Ledgerly users who stall at the bank-connection step of onboarding.

## 2. Problem and opportunity

Forty percent of new users stall at bank connection (BRN-001#PRB-01).

## 3. Users and personas

New Ledgerly users in their first week; the growth team owns this initiative.

## 4. Goals and non-goals

**Goals**
- More new users complete onboarding.

**Non-goals** (explicitly out of scope)
- Changes to existing users' accounts.

## 5. Success metrics

```yaml items
success_metrics:
  - id: SM-01
    status: active
    metric: "Onboarding completion rate"
    baseline: "60%"
    target: "70% by end of Q4"
    measured_by: "Growth funnel dashboard"
    upstream:
      - {id: BRN-001, item: IDEA-01, relation: derives, version: 1, hash: null}
```

## 6. Functional requirements

```yaml items
functional_requirements:
  - id: FR-001
    status: active
    statement: "The system shall email a resume link to a new user who stalls at bank connection for 24 hours."
    priority: must
    release: current
    notes: null
    upstream:
      - {id: BRN-001, item: IDEA-01, relation: derives, version: 1, hash: null}
```

## 7. Non-functional requirements

```yaml items
non_functional_requirements:
  - id: NFR-001
    status: active
    category: privacy
    statement: "Resume emails contain no financial data."
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
    statement: "Most stalled users still want to finish onboarding."
    validation: "Resume-link click rate"
    state: open
    upstream:
      - {id: BRN-001, item: ASM-01, relation: derives, version: 1, hash: null}
```

## 11. Release and rollout

One site first, then all sites.

## 12. Open questions

- None.

## 13. Epic map

<!-- GENERATED: epics whose upstream cites this PRD. Do not edit by hand. -->

## Change Log

| Version | Date | Author | Change | Items affected |
|---|---|---|---|---|
| 1 | 2026-08-05 | claude-code (session fixture-session) | Initial draft from BRN-001 | all |
| 1 | 2026-08-20 | Sam Ortiz | Approved | status |
FIXTURE
cat > docs/specs/brainstorm/BRN-002.md <<'FIXTURE'
---
id: BRN-002
type: brainstorm
title: "Self-service account closure in Ledgerly"
status: converged
version: 1
created: 2026-09-20
updated: 2026-09-22
owner: "Dana Whitfield"
authors: ["Dana Whitfield", "claude-code"]
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
participants: ["Dana Whitfield"]
sources: []
---

# BRN-002 — Self-service account closure in Ledgerly

## 1. Context

Ledgerly has no self-service way to close an account. The account-management team (not growth) owns account lifecycle, and the compliance team needs deletion by the January audit.

## 2. Problems

```yaml items
problems:
  - id: PRB-01
    status: active
    statement: "Users who want to leave must email support to close their account, which takes days"
    who: "Departing Ledgerly user"
    evidence: "Support tickets tagged closure, 2026"
    severity: high
  - id: PRB-02
    status: active
    statement: "Closed accounts keep financial data longer than the retention policy allows"
    who: "Compliance team"
    evidence: "Retention audit, July 2026"
    severity: high
```

## 3. Target users

Departing Ledgerly users, support staff, and the compliance team.

## 4. Ideas

```yaml items
ideas:
  - id: IDEA-01
    status: active
    idea: "A close-account button in settings, with a data export first"
    addresses:
      - PRB-01
    value: "high"
    effort: "medium"
    risk: "low"
    score: null
    disposition: promoted
    reason: "Removes the support queue"
  - id: IDEA-02
    status: active
    idea: "Automatic deletion of financial data 30 days after closure"
    addresses:
      - PRB-02
    value: "high"
    effort: "medium"
    risk: "low"
    score: null
    disposition: promoted
    reason: "Meets the retention policy"
  - id: IDEA-03
    status: active
    idea: "A win-back discount offered during closure"
    addresses:
      - PRB-01
    value: "low"
    effort: "medium"
    risk: "low"
    score: null
    disposition: rejected
    reason: "Feels manipulative"
```

## 5. Evaluation method

Rated with the account-management and compliance teams (diverge-converge).

## 6. Convergence

Self-service closure and automatic deletion were promoted; the win-back discount was rejected.

## 7. Assumptions and open questions

```yaml items
assumptions:
  - id: ASM-01
    status: active
    statement: "We believe that most closure requests need no support contact."
    validation: "Share of closures completed without a ticket"
    state: open
```

- None.

## 8. Candidate success signals

- Fewer closure support tickets.
- No closed account holds financial data past 30 days.

## Change Log

| Version | Date | Author | Change |
|---|---|---|---|
| 1 | 2026-09-22 | claude-code (session fixture-session) | Converged |
FIXTURE
