# TEST-SPECIFICATION: STORY-214 - Mandatory Deviation Consent Protocol

**Story ID:** STORY-214
**Implementation Type:** Documentation (.md)
**Test Output Type:** Test Specification Document + Structural Validation Tests

---

## Overview

This document specifies the validation criteria for STORY-214, which adds a "Workflow Deviation Protocol" section to the devforgeai-development SKILL.md file.

**Key Distinction:** This is a DOCUMENTATION-ONLY story. Tests validate **structure** (section headers, required patterns) rather than **runtime behavior**.

---

## Acceptance Criteria Mapping

| AC# | Description | Test Method | Test ID(s) |
|-----|-------------|-------------|------------|
| AC#1 | Protocol section header exists | grep pattern | TEST-001 |
| AC#2 | AskUserQuestion with three options | grep patterns | TEST-002, TEST-003, TEST-004, TEST-005 |
| AC#3 | Subagent omission deviation documented | grep patterns | TEST-006, TEST-007, TEST-008, TEST-009 |
| AC#4 | Documentation requirements for deviations | grep patterns | TEST-010, TEST-011, TEST-012 |
| AC#5 | RCA recommendation (optional) | grep patterns | TEST-013, TEST-014 |

---

## Technical Specification Mapping

| Req ID | Description | Test Method | Test ID |
|--------|-------------|-------------|---------|
| DOC-001 | Section header "## Workflow Deviation Protocol" | grep exact match | TEST-001 |
| DOC-002 | Three deviation types documented | grep patterns | TEST-006, TEST-007, TEST-008 |
| DOC-003 | AskUserQuestion pattern in section | grep context | TEST-002 |
| DOC-004 | "Follow workflow" option processing | grep | TEST-003 |
| DOC-005 | "Skip with documentation" option | grep | TEST-004 |
| DOC-006 | "User override" option | grep | TEST-005 |
| BR-001 | Protocol mandates AskUserQuestion | grep MUST/mandatory | TEST-017 |
| BR-002 | Timestamp requirement documented | grep timestamp | TEST-010 |
| NFR-001 | Uses HALT terminology | grep HALT | TEST-015 |
| NFR-002 | Section under 100 lines | line count | TEST-016 |

---

## Test Execution

### Executable Test Script

**Location:** `/mnt/c/Projects/DevForgeAI2/tests/STORY-214/test-ac-verification.sh`

**Execution:**
```bash
cd /mnt/c/Projects/DevForgeAI2
chmod +x tests/STORY-214/test-ac-verification.sh
./tests/STORY-214/test-ac-verification.sh
```

### Expected Results

**TDD Red Phase (Before Implementation):**
- All 17 tests should FAIL
- Exit code: 1
- Message: "TDD Red Phase: Tests failing as expected"

**TDD Green Phase (After Implementation):**
- All 17 tests should PASS
- Exit code: 0
- Message: "All tests passed!"

---

## Validation Patterns

### Structural Patterns (What to Test)

| Pattern Type | grep Expression | Purpose |
|--------------|-----------------|---------|
| Section header | `^## Workflow Deviation Protocol` | Validates AC#1 |
| AskUserQuestion | `AskUserQuestion` within section | Validates AC#2 |
| Option: Follow | `Follow workflow` (case-insensitive) | Validates AC#2 |
| Option: Skip | `Skip with documentation` (case-insensitive) | Validates AC#2 |
| Option: Override | `User override` (case-insensitive) | Validates AC#2 |
| Deviation: Phase | `phase skip` (case-insensitive) | Validates AC#3 |
| Deviation: Subagent | `subagent omission` (case-insensitive) | Validates AC#3 |
| Deviation: Sequence | `out-of-sequence` (case-insensitive) | Validates AC#3 |
| MANDATORY | `MANDATORY` or `mandatory` | Validates AC#3 |
| Timestamp | `timestamp` (case-insensitive) | Validates AC#4 |
| Implementation Notes | `Implementation Notes` | Validates AC#4 |
| Story file | `story file` or `story.md` | Validates AC#4 |
| RCA | `rca` or `root cause` | Validates AC#5 |
| Optional | `optional` or `not blocking` | Validates AC#5 |
| HALT | `HALT` | Validates NFR-001 |

### Anti-Patterns (What NOT to Test)

Per test-automator guidelines, avoid testing:
- Specific wording of explanatory text
- Narrative content that may change during refactoring
- Implementation details within the documentation

---

## Test Coverage Summary

| Category | Tests | Coverage |
|----------|-------|----------|
| AC#1 (Section header) | 1 | 100% |
| AC#2 (AskUserQuestion + options) | 4 | 100% |
| AC#3 (Deviation types) | 4 | 100% |
| AC#4 (Documentation requirements) | 3 | 100% |
| AC#5 (RCA recommendation) | 2 | 100% |
| NFR-001 (HALT terminology) | 1 | 100% |
| NFR-002 (Line count) | 1 | 100% |
| BR-001 (Mandatory AskUserQuestion) | 1 | 100% |
| **Total** | **17** | **100%** |

---

## Definition of Done Checklist (Test-Related)

- [x] Test specification document created
- [x] Executable test script created
- [x] All acceptance criteria have corresponding tests
- [x] All technical specification requirements mapped to tests
- [x] Tests follow structural validation pattern (no narrative testing)
- [x] Tests expected to FAIL initially (TDD Red phase)
- [ ] Tests pass after implementation (TDD Green phase)

---

## References

- **Story File:** `devforgeai/specs/Stories/STORY-214-mandatory-deviation-consent-protocol.story.md`
- **Target File:** `.claude/skills/devforgeai-development/SKILL.md`
- **Source RCA:** RCA-019
- **Architecture Constraints:** `devforgeai/specs/context/architecture-constraints.md` (HALT pattern, lines 107-132)

---

**Generated:** 2026-01-13
**Test Author:** claude/test-automator
**Phase:** TDD Red (Test-First)
