#!/usr/bin/env bash
# Seeds an existing brainstorm on the same topic as the prompt.
# The graders check that the SEED-MARKER line and version 1 survive the run.
set -euo pipefail
mkdir -p docs/specs/brainstorms
cat > docs/specs/brainstorms/BRN-001-reduce-onboarding-drop-off.md <<'EOF'
---
id: BRN-001
type: brainstorm
title: "Reduce onboarding drop-off in the mobile banking app"
status: draft
version: 1
created: 2026-09-01
updated: 2026-09-01
owner: "Dana Reyes"
authors: ["Dana Reyes", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-opus-5-5"
  session: "seed-session"
reviewed_by: []
approved_by: ""
approved_on: null
upstream: []
supersedes: []
superseded_by: null
blocked_by: []
# --- brainstorm-specific ---
participants: ["Dana Reyes"]
sources: []
---

# BRN-001 — Reduce onboarding drop-off in the mobile banking app

## 1. Context

New users abandon sign-up at identity verification. SEED-MARKER-7f3a

## 2. Problems

```yaml items
problems:
  - id: PRB-01
    status: active
    statement: "New users give up during identity verification"
    who: "First-time customers on mobile"
    evidence: "Support tickets"
    severity: high
```

## 3. Target users

First-time customers signing up on iOS and Android.

## 4. Ideas

```yaml items
ideas:
  - id: IDEA-01
    status: active
    idea: "Let users resume verification later"
    addresses:
      - PRB-01
    value: null
    effort: null
    risk: null
    score: null
    disposition: open
    reason: null
```

## 5. Evaluation method

Not yet evaluated.

## 6. Convergence

Not yet converged.

## 7. Assumptions and open questions

```yaml items
assumptions:
  - id: ASM-01
    status: active
    statement: "We believe users would return to finish verification"
    validation: "Check resume rates in a prototype test"
    state: open
```

- [NEEDS CLARIFICATION: which verification step loses the most users?]

## 8. Candidate success signals

- Sign-up completion rate recovers

## Change Log

| Version | Date | Author | Change |
|---|---|---|---|
| 1 | 2026-09-01 | Dana Reyes | Initial draft |
EOF
