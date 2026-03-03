# ADR-025: QA Diff Regression Detection and Test Integrity System

**Date:** 2026-02-27
**Status:** Accepted
**Acceptance Date:** 2026-02-27
**Deciders:** Solo Developer, DevForgeAI Framework
**Tags:** qa, security, workflow, source-tree

## Context

Claude Code sessions can silently degrade codebases through three threat vectors:

1. **Code Removal** — Removing working production code during story implementation
2. **Test Tampering** — Weakening test assertions to "game" passing results
3. **Logic Degradation** — Simplifying conditionals, changing signatures, weakening validation

The current QA workflow (`devforgeai-qa`) validates what exists but has no mechanism to detect what was lost or degraded. This creates a trust gap where the developer cannot verify that Claude's implementation didn't break existing functionality.

**Forces:**
- Solo developer cannot manually review every line of every diff
- Claude sessions lack cross-session memory of what code existed before
- Test tampering is especially insidious — tests pass but are meaningless
- The `/dev` TDD workflow (Red → Green → Refactor) provides a natural snapshot point after Red phase

## Decision

We will add three new capabilities to the DevForgeAI framework:

### 1. Git Diff Regression Detection Phase (QA Skill)

Add a new phase to `devforgeai-qa` that analyzes `git diff main...HEAD` for production code regression patterns:
- Deleted function definitions, error handlers, validation logic, API endpoints
- Changed function signatures
- Severity classification: CRITICAL (public API), HIGH (internal), MEDIUM (logic simplification)
- Blocks QA approval on CRITICAL/HIGH findings

### 2. Red-Phase Test Integrity Checksums (Dev Skill)

After Red phase (Phase 02) completes in `implementing-stories`:
- Snapshot SHA-256 checksums of all test files, configs, and mocks
- Store in `devforgeai/qa/snapshots/{STORY_ID}/red-phase-checksums.json`
- During QA, compare current files against snapshot
- Any mismatch = CRITICAL: TEST TAMPERING (blocks QA, no override)

### 3. Test Folder Write Protection Rule

New rule file `.claude/rules/workflow/test-folder-protection.md`:
- tests/ folder restricted to test-automator and integration-tester subagents
- Other agents must use AskUserQuestion before modifying test files
- Enforceable at prompt level

### Source-Tree Update

Add new directory to source-tree.md:
```
devforgeai/qa/snapshots/          # Red-phase test integrity snapshots
    {STORY_ID}/
        red-phase-checksums.json  # SHA-256 checksums of test files
```

## Rationale

- **Phase-boundary checksums** solve the fundamental problem that git diff cannot distinguish who modified tests within a single commit
- **Heuristic pattern detection** catches specific tampering techniques (assertion weakening, test removal, threshold lowering)
- **Rule-based test protection** provides defense-in-depth at the prompt level
- **All tools already available** — git diff via Bash(git:*), SHA-256 via Python/Bash, pattern matching via Grep

## Consequences

### Positive

- **Trust restoration** — Developer can confidently delegate to Claude
- **Zero false negatives** for deleted public functions (exact pattern matching)
- **Defense-in-depth** — Three layers (diff analysis, checksum integrity, prompt rules)
- **No new external dependencies** — Uses existing tools (git, sha256sum, Grep)

### Negative

- **QA phase duration increases** — Additional ~10-30 seconds per story
- **Snapshot storage** — JSON files accumulate in devforgeai/qa/snapshots/
- **False positives possible** — Heuristic patterns may flag legitimate refactoring (~5% rate)
- **Source-tree.md update required** — This ADR

### Risks

- Heuristic patterns may need tuning over time as new tampering techniques emerge
- Very large diffs (100+ files) may exceed the 30-second target

## Alternatives Considered

1. **Subagent authorization logging** — Track which subagent wrote which file. Rejected: No built-in audit trail in Claude Code Terminal. Would require custom instrumentation that doesn't exist.

2. **Git commit per phase** — Commit after Red, Green, Refactor separately. Rejected: Changes current workflow significantly, adds git overhead, complicates rollback.

3. **Runtime behavioral testing** — Run production code before/after to detect behavior changes. Rejected: Aspirational — requires test harness infrastructure not in scope.

## Enforcement

### Context File Updates Required

| File | Change | Type |
|------|--------|------|
| `source-tree.md` | Add `devforgeai/qa/snapshots/` directory | Structure |

### Affected Skills

| Skill | Change |
|-------|--------|
| `devforgeai-qa` | Add diff regression detection phase |
| `implementing-stories` | Add Red-phase snapshot creation |

### New Artifacts

| Artifact | Location |
|----------|----------|
| Test protection rule | `.claude/rules/workflow/test-folder-protection.md` |
| Operational rules | `.claude/rules/workflow/operational-safety.md` |
| QA diff reference | `.claude/skills/devforgeai-qa/references/diff-regression-detection.md` |
| Snapshot reference | `.claude/skills/implementing-stories/references/test-integrity-snapshot.md` |
