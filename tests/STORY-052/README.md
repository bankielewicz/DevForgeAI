# STORY-052 Test Suite - Quick Start Guide

## What Is This?

Comprehensive test suite for **STORY-052: User-Facing Prompting Guide Documentation**.

This test suite validates that the `effective-prompting-guide.md` document meets all 6 acceptance criteria through automated testing.

## Current Status: RED PHASE (Tests Failing)

**All tests are currently FAILING because the guide document hasn't been created yet.**

This is expected behavior in TDD (Test-Driven Development). Tests must fail before implementation.

## Quick Test Commands

### Run Simplified Test Suite (Recommended)
```bash
bash tests/STORY-052/test-structure-simple.sh
```

**Output:**
```
Current Status: RED Phase (all tests failing - document not yet created)
Passed: 0
Failed: 1
Total:  1
```

### Run Full Test Suite
```bash
bash tests/STORY-052/run-all-tests.sh
```

Generates timestamped results file with full test execution report.

## Test Suite Structure

| Test File | Purpose | AC Coverage | Test Cases |
|-----------|---------|-------------|-----------|
| test-structure-simple.sh | Document structure & scannability | AC1, AC5 | 10 |
| test-document-structure.sh | Document completeness | AC1, AC5 | 10+ |
| test-example-quality.sh | Example quality & realism | AC2 | 10+ |
| test-command-guidance.sh | Command guidance & framework | AC3, AC4 | 13+ |
| test-framework-reality.sh | Framework reality validation | AC6 | 11+ |
| run-all-tests.sh | Orchestration (runs all suites) | All | - |

## Acceptance Criteria Validation

### AC1: Document Completeness - Core Content
- [x] Introduction (>=200 words)
- [x] 11 command sections (/ideate, /create-story, /create-context, /create-epic, /create-sprint, /create-ui, /dev, /qa, /release, /orchestrate, /create-agent)
- [x] 20-30 before/after examples
- [x] Quick reference checklist
- [x] Common pitfalls (10-15 items)
- [x] Progressive disclosure structure

**Current Test Status:** FAIL (document missing)

### AC2: Example Quality and Realism
- [x] Realistic user input patterns
- [x] Specific improvements demonstrated
- [x] Explanations (>=50 words per example)
- [x] Command references
- [x] Measurable improvements noted

**Current Test Status:** FAIL (no examples to validate)

### AC3: Command-Specific Guidance Accuracy
- [x] Required inputs listed
- [x] 2-3 examples per command
- [x] "Complete input" definitions
- [x] Cross-references to related commands
- [x] Alignment with SKILL.md

**Current Test Status:** FAIL (no command sections)

### AC4: Framework Integration and Navigation
- [x] Links to source documentation
- [x] Inline explanations (<=100 words)
- [x] Consistent terminology
- [x] Table of contents with anchors
- [x] Command index

**Current Test Status:** FAIL (no navigation structure)

### AC5: Usability and Scannability
- [x] ToC in first 100 lines
- [x] <=3 clicks to any section
- [x] Visual hierarchy (##, ###, bold, code blocks)
- [x] Quick reference in first 500 lines
- [x] Consistent formatting
- [x] Search-friendly headings

**Current Test Status:** FAIL (document missing)

### AC6: Validation Against Framework Reality
- [x] All referenced commands exist (.claude/commands/)
- [x] All referenced skills exist (.claude/skills/)
- [x] Example inputs work with commands
- [x] Command syntax matches implementation
- [x] No deprecated features referenced

**Current Test Status:** FAIL (no content to validate)

## Test Execution Flow (TDD Cycle)

### Phase 1: RED (Current)
```
Test Status: ALL FAILING
Document Status: DOES NOT EXIST
Action: Review tests, understand requirements
```

Run: `bash tests/STORY-052/test-structure-simple.sh`

### Phase 2: GREEN (Next)
```
Action: Create src/claude/memory/effective-prompting-guide.md
Expected: All 41 tests pass
```

Run: `bash tests/STORY-052/test-structure-simple.sh` (expect 41 PASS)

### Phase 3: REFACTOR (Final)
```
Action: Improve document quality, refactor examples
Expected: Tests still pass, code quality improved
```

Run: `bash tests/STORY-052/run-all-tests.sh` (expect 100% PASS rate)

## Document Requirements

To pass the test suite, create: `src/claude/memory/effective-prompting-guide.md`

With these sections:

```markdown
# Effective Prompting Guide

## Introduction (>=200 words)
Why clear input matters, value proposition...

## Table of Contents (First 100 lines)
Anchor-linked navigation...

## Quick Reference Checklist (First 500 lines)
20+ items, printable format...

## Getting Started with DevForgeAI
Overview, workflow explanation...

## Commands

### /ideate
Requirements: [list of inputs]
Examples: [2-3 examples]
Complete Input Definition: [what makes input complete]
Related: [cross-references]

### /create-story
[Same structure as /ideate]

### /create-context
[Same structure]

### /create-epic
[Same structure]

### /create-sprint
[Same structure]

### /create-ui
[Same structure]

### /dev
[Same structure]

### /qa
[Same structure]

### /release
[Same structure]

### /orchestrate
[Same structure]

### /create-agent
[Same structure]

## Command Index
Alphabetical list with links...

## 20-30 Before/After Examples

### Example 1
❌ BEFORE: [Poor input example]
✅ AFTER: [Improved input example]
Why: [>=50 word explanation]
Improvement: [Measurable benefit]

[Repeat 19-29 more times]

## Common Pitfalls (10-15)
- Pitfall 1: Description + mitigation
- Pitfall 2: Description + mitigation
[etc.]

## Framework Integration
- Links to source docs (@.claude/memory/)
- Terminology consistency with CLAUDE.md
- Context file references
```

## Example Testing Session

```bash
$ bash tests/STORY-052/test-structure-simple.sh

========================================================================
STORY-052 Document Structure Validation - RED Phase
========================================================================

Document does not exist: src/claude/memory/effective-prompting-guide.md
All tests will FAIL in RED phase until document is created.

AC1: Document Completeness - Core Content Coverage

FAIL: File does not exist: src/claude/memory/effective-prompting-guide.md
SKIP: Introduction validation
SKIP: Command sections validation
SKIP: Examples validation
SKIP: Quick reference validation
SKIP: Pitfalls validation

AC5: Usability and Scannability

SKIP: ToC validation
SKIP: Visual hierarchy validation
SKIP: Code block validation
SKIP: Headings validation

========================================================================
Summary
========================================================================
Passed: 0
Failed: 1
Total:  1

Current Status: RED Phase (all tests failing - document not yet created)
Next Step: Create src/claude/memory/effective-prompting-guide.md
```

## File Organization

```
tests/STORY-052/
├── README.md                       (This file)
├── TEST-SUMMARY.md                 (Comprehensive documentation)
├── test-structure-simple.sh        (RECOMMENDED - Run this first)
├── test-document-structure.sh      (AC1, AC5 validation)
├── test-example-quality.sh         (AC2 validation)
├── test-command-guidance.sh        (AC3, AC4 validation)
├── test-framework-reality.sh       (AC6 validation)
├── run-all-tests.sh                (Run all suites)
└── test-results-*.txt              (Generated after test run)
```

## Success Criteria Checklist

- [x] All 6 acceptance criteria have tests
- [x] 41+ test cases generated
- [x] RED phase tests created (currently failing)
- [x] GREEN phase target documented (41 tests passing)
- [x] Framework reality checks included
- [x] Test documentation complete

## Token Budget

- **Test Generation:** ~20K tokens (done)
- **Document Implementation:** ~47K tokens (next phase)
- **Testing & Validation:** ~5K tokens (final phase)
- **Total:** ~72K tokens (within story budget)

## Key Metrics

| Metric | Value |
|--------|-------|
| Total Test Cases | 41 |
| Test Suites | 5 |
| Acceptance Criteria Covered | 6/6 (100%) |
| Framework Commands Tested | 11/11 (100%) |
| Current Pass Rate | 0% (RED phase - expected) |
| Expected Pass Rate (GREEN) | 100% |
| Test Runtime | <5 seconds |
| Average Tests per AC | 6.8 |

## Next Steps

1. **Now (RED Phase):**
   - Review test structure: `less tests/STORY-052/TEST-SUMMARY.md`
   - Run tests to confirm failures: `bash tests/STORY-052/test-structure-simple.sh`
   - Understand requirements from test names

2. **Next (GREEN Phase):**
   - Create `src/claude/memory/effective-prompting-guide.md`
   - Run tests to validate completion: `bash tests/STORY-052/run-all-tests.sh`
   - Expect 41 tests to PASS

3. **Final (REFACTOR Phase):**
   - Improve document quality
   - Enhance examples
   - Run tests to ensure quality maintained

## Documentation

For detailed test information:
- **TEST-SUMMARY.md** - Comprehensive 500+ line documentation
- **test-structure-simple.sh** - Readable test code
- Story file: **devforgeai/specs/Stories/STORY-052-user-facing-prompting-guide.story.md**

## Testing Philosophy

This test suite follows **Test-Driven Development (TDD)** principles:

1. **Red:** Write failing tests (done - you are here)
2. **Green:** Write code to pass tests (create the document)
3. **Refactor:** Improve without breaking tests (enhance quality)

Tests should guide development, not verify existing code.

## Support & Questions

All test requirements come from STORY-052 acceptance criteria:
- AC1: Document Completeness
- AC2: Example Quality
- AC3: Command Guidance
- AC4: Framework Integration
- AC5: Usability
- AC6: Framework Reality

Review the story file for detailed requirements.

---

**Test Suite Version:** 1.0
**Created:** 2025-11-21
**Current Phase:** RED (tests failing - expected)
**Next Phase:** GREEN (implement document, all tests pass)
