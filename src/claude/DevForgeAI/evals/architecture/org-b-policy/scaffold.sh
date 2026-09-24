#!/usr/bin/env bash
# Seeds the fixture documents for this case.
set -euo pipefail
mkdir -p docs/specs/policy docs/specs/prd
cat > docs/specs/prd/PRD-001.md <<'FIXTURE_EOF'
---
id: PRD-001
type: prd
title: "Member self-service for Harbour Yoga Studio"
status: approved
version: 2
created: 2026-09-10
updated: 2026-09-14
owner: "Priya Nair"
authors: ["Priya Nair", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-opus-5-5"
  session: "fixture-session"
reviewed_by: ["Priya Nair"]
approved_by: "Priya Nair"
approved_on: 2026-09-14
upstream:
  - {id: BRN-001, item: PRB-01, relation: derives, version: 1, hash: null}
supersedes: []
superseded_by: null
blocked_by: []
# --- prd-specific ---
target_release: "Spring launch"
stage: mvp
operating_context: internal
stakeholders: ["Priya Nair", "Front-desk lead"]
---

# PRD-001 — Member self-service for Harbour Yoga Studio

## 1. Summary

Studio members sign in to a web app and book or cancel class places themselves, instead of phoning the front desk.

## 2. Problem and opportunity

Members can book class places only by phoning or visiting the front desk (BRN-001#PRB-01).

## 3. Users and personas

Members of the studio; front-desk staff who manage rosters and member accounts.

## 4. Goals and non-goals

**Goals**
- Members manage their own class bookings.

**Non-goals**
- Online payment of fees.

## 5. Success metrics

```yaml items
success_metrics:
  - id: SM-01
    status: active
    metric: "Share of class bookings made online"
    baseline: "0%"
    target: "60% by the end of the spring term"
    measured_by: "Booking records"
    upstream:
      - {id: BRN-001, item: IDEA-01, relation: derives, version: 1, hash: null}
```

## 6. Functional requirements

```yaml items
functional_requirements:
  - id: FR-001
    status: active
    statement: "The system shall let a member sign in to the studio web app with their own account."
    priority: must
    release: current
    notes: null
    upstream:
      - {id: BRN-001, item: IDEA-01, relation: derives, version: 1, hash: null}
  - id: FR-002
    status: active
    statement: "The system shall let a signed-in member book and cancel a class place."
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
    category: security
    statement: "Front-desk staff can revoke a member's sessions, and a revoked session stops working within 5 minutes."
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
```

## 11. Release and rollout

Launch at the start of the spring term.

## 12. Open questions

- [NEEDS ADR: identity provider for member sign-in; affects FR-001]

## 13. Epic map

<!-- GENERATED: epics whose upstream cites this PRD. Do not edit by hand. -->

## Change Log

| Version | Date | Author | Change | Items affected |
|---|---|---|---|---|
| 1 | 2026-09-12 | claude-code | Initial draft from BRN-001. Policy resolution: interview.max_calls=8 (default); architecture.mandated_platforms=none (default); quality.required_categories=floor only (default) | all |
| 2 | 2026-09-14 | claude-code | Added NFR-001 session revocation. Policy resolution: interview.max_calls=8 (default); architecture.mandated_platforms=none (default); quality.required_categories=floor only (default) | NFR-001 |
| 2 | 2026-09-14 | Priya Nair | Approved | status |
FIXTURE_EOF
cat > docs/specs/policy/POL-001.md <<'FIXTURE_EOF'
---
id: POL-001
type: policy
title: "Organization B engineering policy (vendored)"
status: approved
version: 1
created: 2026-08-15
updated: 2026-08-15
owner: "Organization B engineering lead"
authors: ["Organization B engineering lead"]
reviewed_by: ["Organization B engineering lead"]
approved_by: "Organization B engineering lead"
approved_on: 2026-08-15
upstream: []
supersedes: []
superseded_by: null
blocked_by: []
# --- policy-specific ---
scope: organization
source: {repository: "github.com/org-b/policies", ref: "2026-08-15"}
---

# POL-001 — Organization B engineering policy (vendored)

## 1. Scope and ownership

Applies to all Organization B products. No platform is mandated for identity; each product decides.

## 2. Settings

```yaml items
settings:
  - id: SET-01
    status: active
    key: interview.max_calls
    class: interaction_default
    value: 5
    overridable_by:
      - project
      - local
    rationale: "Shorter interviews; teams prefer to fill gaps in review"
```

## Change Log

| Version | Date | Author | Change | Settings affected |
|---|---|---|---|---|
| 1 | 2026-08-15 | Engineering lead | Initial policy | all |
FIXTURE_EOF
