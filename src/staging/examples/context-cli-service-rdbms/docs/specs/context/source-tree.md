---
id: CTX-004
type: context
title: "shiftlog: source tree"
status: draft
version: 1
created: 2026-09-29
updated: 2026-09-29
owner: "Example Owner"
authors: ["Example Owner", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-opus-5-5"
  session: "00000000-0000-0000-0000-000000000000"
reviewed_by: []
approved_by: ""
approved_on: null
upstream:
  - {id: ARCH-001, relation: constrains, version: 1, hash: null}
supersedes: []
superseded_by: null
blocked_by: []
# --- context-specific ---
document: source-tree
freshness_days: 90
---

# CTX-004 — Source tree

## Contents

- [1. Roots](#1-roots)
- [2. Layout conventions](#2-layout-conventions)
- [3. Generated files](#3-generated-files)

## 1. Roots

```yaml items
roots:
  - id: SRC-01
    status: active
    path: "src/shiftlog/cli/"
    holds: code
    component: "ARCH-001#CMP-01"
    basis: convention
    notes: ""
  - id: SRC-02
    status: active
    path: "src/shiftlog/service/"
    holds: code
    component: "ARCH-001#CMP-02"
    basis: convention
    notes: ""
  - id: SRC-03
    status: active
    path: "src/shiftlog/db/"
    holds: code
    component: "ARCH-001#CMP-03"
    basis: convention
    notes: ""
  - id: SRC-04
    status: active
    path: "migrations/"
    holds: code
    component: "ARCH-001#CMP-03"
    basis: convention
    notes: "Alembic revisions (tech-stack.md, TEC-04)"
  - id: SRC-05
    status: active
    path: "tests/cli/"
    holds: tests
    component: "ARCH-001#CMP-01"
    basis: convention
    notes: ""
  - id: SRC-06
    status: active
    path: "tests/service/"
    holds: tests
    component: "ARCH-001#CMP-02"
    basis: observed
    observed_in: "tests/service/"
    observed_on: 2026-09-29
    notes: ""
  - id: SRC-07
    status: active
    path: "tests/db/"
    holds: tests
    component: "ARCH-001#CMP-03"
    basis: convention
    notes: ""
  - id: SRC-08
    status: active
    path: "docs/"
    holds: docs
    component: null
    basis: convention
    notes: ""
  - id: SRC-09
    status: active
    path: "build/"
    holds: generated
    component: null
    basis: observed
    observed_in: ".gitignore"
    observed_on: 2026-09-29
    notes: ""
  - id: SRC-10
    status: active
    path: "config/"
    holds: config
    component: null
    basis: proposed
    notes: "[NEEDS CLARIFICATION: confirm config/ for the default configuration file]"
```

## 2. Layout conventions

- **Convention:** one package per component under `src/shiftlog/`; a test folder per component under
  `tests/`, named like the package.

## 3. Generated files

- **Convention:** `build/` is written by the build and never edited or committed.

## Change Log

| Version | Date | Author | Change | Items affected |
|---|---|---|---|---|
| 1 | 2026-09-29 | claude-code (session 00000000-0000-0000-0000-000000000000) | Initial draft from ARCH-001 v1; SRC-10 awaits confirmation | all |
