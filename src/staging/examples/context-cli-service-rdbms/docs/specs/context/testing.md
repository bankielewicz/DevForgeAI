---
id: CTX-005
type: context
title: "shiftlog: testing"
status: approved
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
approved_by: "Example Owner"
approved_on: 2026-09-29
upstream:
  - {id: ARCH-001, relation: constrains, version: 1, hash: null}
supersedes: []
superseded_by: null
blocked_by: []
# --- context-specific ---
document: testing
freshness_days: 90
---

# CTX-005 — Testing

## 1. The pass rule

- **DevForgeAI rule — pass rule:** 100% of the required tests pass. A failing test is accepted
  only as a named exception that records the test, the reason and the approver, and it is always
  reported apart from "tests passed". This is not a configurable threshold.

## 2. Investigating a failing test

- **DevForgeAI rule — investigating a failing test:** a failing test is never investigated by
  changing the working tree.
  1. Before the first change for a work item, run the required tests on the unchanged branch and record
     the results with the commit they ran on. Compare a later failure with that record first.
  2. To run or read the old code, use a separate, disposable worktree at that commit
     (`git worktree add --detach <path> <commit>`, removed afterwards), or `git show <commit>:<path>`.
     Never restore, check out, stash, reset, clean or download files into the working tree to
     investigate a failure.
  3. Commit the work in progress on the work item's branch before each full run of the required tests.
  4. A failure already present in the baseline is reported as present before the change. The pass rule
     still applies to it: it is fixed, or accepted as a named exception.

## 3. Testing policy in force

No policy document sets a testing value, so each is DevForgeAI's default.

| Setting | Value | Source |
|---|---|---|
| testing.method | tdd | (default) |
| testing.coverage_metric | line | (default) |
| testing.coverage_threshold | none: not enforced, reported as "no coverage threshold set" | (default) |
| testing.coverage_scope | every `holds: code` root in source-tree.md | (default) |
| testing.coverage_exclusions | the `generated`, `tests` and `fixtures` roots | (default) |
| testing.exception_approvers | the story's owner | (default) |

## 4. Test levels

| Kind | Levels | Tests root | Basis |
|---|---|---|---|
| user-interface | unit, through Typer's `CliRunner` | tests/cli/ | Convention |
| service | unit | tests/service/ | Observed (tests/service/, 2026-09-29) |
| relational-store | integration, against a temporary SQLite file | tests/db/ | Convention |

## 5. Naming

- **DevForgeAI rule — test naming:** each test's name or tag cites the acceptance
  criterion or verification item it covers, for example `test_STORY_NNN_AC_NN_<what>` or
  `@STORY-NNN @AC-NN`.
- **Convention:** `test_STORY_NNN_AC_NN_<what>` for every test that verifies an acceptance criterion.

## 6. Fixtures and test data

- **Convention:** each database test creates its own temporary SQLite file through the `db` fixture in
  `tests/conftest.py`; no test shares a database.

## 7. Running the tests

| Component | Command | Basis |
|---|---|---|
| ARCH-001#CMP-01 | `pytest tests/cli` | Convention |
| ARCH-001#CMP-02 | `pytest tests/service` | Convention |
| ARCH-001#CMP-03 | `pytest tests/db` | Convention |

## Change Log

| Version | Date | Author | Change | Items affected |
|---|---|---|---|---|
| 1 | 2026-09-29 | claude-code (session 00000000-0000-0000-0000-000000000000) | Initial draft from ARCH-001 v1 | all |
| 1 | 2026-09-29 | Example Owner | Approved | — |
