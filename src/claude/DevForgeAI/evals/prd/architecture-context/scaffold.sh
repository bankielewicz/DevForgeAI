#!/usr/bin/env bash
# Seeds the fixture documents for this case.
set -euo pipefail
mkdir -p docs/specs/adr docs/specs/brainstorm
cat > docs/specs/brainstorm/BRN-001.md <<'FIXTURE_EOF'
---
id: BRN-001
type: brainstorm
title: "Online appointment booking for a physiotherapy clinic"
status: converged
version: 1
created: 2026-09-20
updated: 2026-09-21
owner: "Clinic operations lead"
authors: ["Clinic operations lead", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-opus-5-5"
  session: "example-session"
reviewed_by: ["Clinic operations lead"]
approved_by: ""
approved_on: null
upstream: []
supersedes: []
superseded_by: null
blocked_by: []
# --- brainstorm-specific ---
participants: ["Clinic operations lead", "Front-desk lead"]
sources: ["Front-desk call log, August 2026"]
---

# BRN-001 — Online appointment booking for a physiotherapy clinic

## 1. Context

Front-desk staff spend most mornings on the phone booking and moving appointments, and missed
appointments are common. The clinic wants patients to book for themselves.

## 2. Problems

```yaml items
problems:
  - id: PRB-01
    status: active
    statement: "Patients can only book by phone during opening hours, so calls queue and some patients give up"
    who: "Patients"
    evidence: "Front-desk call log, August 2026"
    severity: high
  - id: PRB-02
    status: active
    statement: "Patients forget appointments, and the slot is lost"
    who: "Clinic"
    evidence: "[NEEDS CLARIFICATION: no-show rate not yet measured]"
    severity: medium
```

## 3. Target users

Patients booking their own appointments, and front-desk staff who manage the calendar.

## 4. Ideas

```yaml items
ideas:
  - id: IDEA-01
    status: active
    idea: "Patients book, move and cancel their own appointments online"
    addresses:
      - PRB-01
    value: "high"
    effort: "medium"
    risk: "medium"
    score: null
    disposition: promoted
    reason: "Removes most booking calls"
  - id: IDEA-02
    status: active
    idea: "Text-message reminders the day before an appointment"
    addresses:
      - PRB-02
    value: "medium"
    effort: "low"
    risk: "low"
    score: null
    disposition: promoted
    reason: "Cheap and directly targets no-shows"
  - id: IDEA-03
    status: active
    idea: "Waitlist that offers cancelled slots to waiting patients"
    addresses:
      - PRB-02
    value: "medium"
    effort: "medium"
    risk: "medium"
    score: null
    disposition: parked
    reason: "Worth doing after booking works"
  - id: IDEA-04
    status: active
    idea: "Native mobile app"
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

Value, effort and risk rated high, medium or low by the two participants (diverge-converge).

## 6. Convergence

Online self-booking and reminders were promoted. The waitlist was parked until booking works. The
native app was rejected.

## 7. Assumptions and open questions

```yaml items
assumptions:
  - id: ASM-01
    status: active
    statement: "Most patients will book online if it is available"
    validation: "Share of bookings made online in the first month"
    state: open
```

## 8. Candidate success signals

- Fewer booking calls to the front desk.
- Fewer missed appointments.

## Change Log

| Version | Date | Author | Change |
|---|---|---|---|
| 1 | 2026-09-21 | claude-code | Converged |
FIXTURE_EOF
cat > docs/specs/adr/ADR-002.md <<'FIXTURE_EOF'
---
id: ADR-002
type: adr
title: "ClinicCore is the calendar of record"
status: accepted
version: 1
created: 2026-08-01
updated: 2026-08-05
owner: "Clinic operations lead"
authors: ["Clinic operations lead"]
reviewed_by: ["Front-desk lead"]
approved_by: "Clinic operations lead"
approved_on: 2026-08-05
upstream: []
supersedes: []
superseded_by: null
blocked_by: []
# --- adr-specific ---
consulted: ["Front-desk lead"]
informed: []
---

# ADR-002 — ClinicCore is the calendar of record

## Context and problem statement

Appointments live in ClinicCore, the clinic's practice-management system. Any new booking channel could
keep its own calendar or use ClinicCore's.

## Decision outcome

**Chosen option:** ClinicCore stays the single calendar of record. No other system holds appointments.

## Status history

| Date | Status | Note |
|---|---|---|
| 2026-08-05 | accepted | |
FIXTURE_EOF
cat > docs/specs/adr/ADR-003.md <<'FIXTURE_EOF'
---
id: ADR-003
type: adr
title: "Synchronous booking writes vs scheduled import into ClinicCore"
status: proposed
version: 1
created: 2026-09-18
updated: 2026-09-18
owner: "Clinic operations lead"
authors: ["Clinic operations lead"]
reviewed_by: []
approved_by: ""
approved_on: null
upstream: []
supersedes: []
superseded_by: null
blocked_by: []
# --- adr-specific ---
consulted: []
informed: []
---

# ADR-003 — Synchronous booking writes vs scheduled import into ClinicCore

## Context and problem statement

Online bookings must reach ClinicCore (ADR-002). They could be written synchronously through its API when the
patient books, or imported by a scheduled job every few minutes.

## Considered options

1. Synchronous writes through the ClinicCore API.
2. Scheduled import every five minutes.

## Decision outcome

Not decided yet.

## Status history

| Date | Status | Note |
|---|---|---|
| 2026-09-18 | proposed | |
FIXTURE_EOF
