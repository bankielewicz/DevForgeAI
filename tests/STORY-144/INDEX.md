# STORY-144 Test Suite - File Index

**Generated**: 2025-12-29
**Location**: `/mnt/c/Projects/DevForgeAI2/tests/STORY-144/`
**Status**: TDD RED Phase - All Tests Failing (Expected)

---

## Quick Start

### Run All Tests
```bash
bash /mnt/c/Projects/DevForgeAI2/tests/STORY-144/run-all-tests.sh
```

### Run Individual AC Tests
```bash
# AC#1: user-input-integration-guide.md
bash /mnt/c/Projects/DevForgeAI2/tests/STORY-144/test-ac1-user-input-integration-guide.sh

# AC#2: brainstorm-data-mapping.md
bash /mnt/c/Projects/DevForgeAI2/tests/STORY-144/test-ac2-brainstorm-data-mapping.sh

# AC#3: No unreferenced files
bash /mnt/c/Projects/DevForgeAI2/tests/STORY-144/test-ac3-no-unreferenced-files.sh

# AC#4: Commit message documentation
bash /mnt/c/Projects/DevForgeAI2/tests/STORY-144/test-ac4-commit-message-documentation.sh
```

---

## File Descriptions

### Test Files

#### 1. `test-ac1-user-input-integration-guide.sh`
- **Size**: 4.5 KB
- **Tests**: 8 test cases
- **Purpose**: Verify user-input-integration-guide.md is deleted or integrated into user-input-guidance.md
- **Key Assertion**: File must not exist as orphaned file after resolution
- **Status**: 7 failing, 1 passing
- **Run**: `bash test-ac1-user-input-integration-guide.sh`

#### 2. `test-ac2-brainstorm-data-mapping.sh`
- **Size**: 4.8 KB
- **Tests**: 9 test cases
- **Purpose**: Verify brainstorm-data-mapping.md is deleted or integrated into brainstorm-handoff-workflow.md
- **Key Assertion**: File must not exist as orphaned file after resolution
- **Status**: 4 failing, 5 passing
- **Run**: `bash test-ac2-brainstorm-data-mapping.sh`

#### 3. `test-ac3-no-unreferenced-files.sh`
- **Size**: 6.1 KB
- **Tests**: 10 test cases
- **Purpose**: Verify all files in references directory are referenced in SKILL.md or workflow files
- **Key Assertion**: All reference files must be found by grep in SKILL.md or other files
- **Status**: 5 failing, 5 passing
- **Run**: `bash test-ac3-no-unreferenced-files.sh`

#### 4. `test-ac4-commit-message-documentation.sh`
- **Size**: 5.5 KB
- **Tests**: 12 test cases
- **Purpose**: Verify commit message documents the resolution (action and justification)
- **Key Assertion**: Commit must mention STORY-144, files, actions, and reasoning
- **Status**: 9 failing, 3 passing
- **Run**: `bash test-ac4-commit-message-documentation.sh`

---

### Orchestration and Documentation

#### `run-all-tests.sh`
- **Size**: 3.2 KB
- **Purpose**: Master test runner that executes all 4 test suites
- **Output**: Summary of all 39 tests with pass/fail counts
- **Exit Code**: Number of total failures across all suites
- **Run**: `bash run-all-tests.sh`

#### `README.md`
- **Size**: 8.0 KB
- **Content**: 
  - Test suite overview
  - Individual test descriptions
  - How to run tests
  - Expected output examples
  - Test architecture and pyramid
  - Acceptance criteria mapping
  - Implementation checklist
  - File locations and references
  - Troubleshooting guide

#### `TEST-SUMMARY.md`
- **Size**: 10 KB
- **Content**:
  - Test generation completion status
  - Test statistics by AC
  - Detailed test coverage analysis
  - Test design principles (TDD, AAA, independence)
  - File structure and locations
  - How tests will pass (implementation steps)
  - Test quality metrics
  - Test dependencies

#### `EXECUTION-REPORT.md`
- **Size**: 12 KB
- **Content**:
  - Executive summary
  - Deliverables list
  - Test coverage details by AC
  - Execution results summary
  - Why tests fail (expected reasons)
  - Test design features
  - Step-by-step implementation guide
  - Test architecture explanation
  - Quality assurance metrics
  - Recommendations for implementation
  - File locations reference

#### `INDEX.md`
- **Size**: This file
- **Purpose**: Quick reference guide for all test files

---

## Test Statistics

```
Total Files:        8 (4 test + 1 runner + 3 docs)
Total Tests:        39 test cases
Total Size:         ~42 KB
Test Framework:     Bash/Shell Scripts
Status:             RED Phase (Tests Failing)

By Acceptance Criteria:
├── AC#1: 8 tests (user-input-integration-guide.md)
├── AC#2: 9 tests (brainstorm-data-mapping.md)
├── AC#3: 10 tests (no unreferenced files)
└── AC#4: 12 tests (commit message)

Current Results:
├── Tests Passing:   16 (41%)
├── Tests Failing:   23 (59%)
└── Avg Time/Test:   ~100ms
```

---

## File Dependency Map

```
run-all-tests.sh
├── Invokes → test-ac1-user-input-integration-guide.sh
├── Invokes → test-ac2-brainstorm-data-mapping.sh
├── Invokes → test-ac3-no-unreferenced-files.sh
└── Invokes → test-ac4-commit-message-documentation.sh

Test Files Depend On:
├── /mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-ideation/SKILL.md
├── /mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-ideation/references/
├── /mnt/c/Projects/DevForgeAI2/.git/
└── Standard Unix tools (bash, grep, find, git, wc, file)
```

---

## Implementation Guide

### Prerequisites
- Bash shell available
- Git repository initialized
- Project structure in place

### Typical Workflow

1. **Read This File** (you are here)
2. **Run Tests** to see what's failing
   ```bash
   bash run-all-tests.sh
   ```
3. **Review Failing Tests** to understand requirements
   - Read test file comments
   - Check README.md for details
4. **Implement Changes**
   - Decide on each orphaned file
   - Integrate or delete
   - Update SKILL.md
5. **Create Commit**
   - Follow message format from test expectations
   - Include all required details
6. **Re-run Tests** to verify all pass
   ```bash
   bash run-all-tests.sh
   ```

---

## Key Paths

### Orphaned Files (to be resolved)
```
.claude/skills/devforgeai-ideation/references/user-input-integration-guide.md
.claude/skills/devforgeai-ideation/references/brainstorm-data-mapping.md
```

### Integration Targets (if content valuable)
```
.claude/skills/devforgeai-ideation/references/user-input-guidance.md (Section 5)
.claude/skills/devforgeai-ideation/references/brainstorm-handoff-workflow.md
```

### File to Update (references)
```
.claude/skills/devforgeai-ideation/SKILL.md
```

### Test Directory
```
tests/STORY-144/
```

---

## Documentation Files

| File | Purpose | Audience |
|------|---------|----------|
| INDEX.md (this file) | Quick reference | Everyone |
| README.md | How to run tests | Developers |
| TEST-SUMMARY.md | Test design and coverage | QA/Architects |
| EXECUTION-REPORT.md | Detailed results and implementation | Project Managers |

---

## Test Execution Output Format

When you run tests, you'll see output like:

```
========================================
AC#1: user-input-integration-guide.md
========================================

[TEST 1] test-ac1-file-deleted-or-integrated
✗ FAILED (Expected to fail in Red phase)

[TEST 2] test-ac1-file-not-referenced-in-skill
✗ FAILED (Expected to fail in Red phase)

...

Summary: AC#1 Tests
Tests Run:    8
Tests Passed: 1
Tests Failed: 7
```

Color codes:
- 🟢 ✓ PASSED - Test is passing
- 🔴 ✗ FAILED - Test is failing
- 🟡 [TEST N] - Test identifier
- 🔵 [YELLOW] - Section header

---

## Troubleshooting

### Tests Won't Run
```bash
# Check file permissions
chmod +x /mnt/c/Projects/DevForgeAI2/tests/STORY-144/*.sh

# Check bash is available
which bash
```

### Git Errors
```bash
# Verify git repo exists
cd /mnt/c/Projects/DevForgeAI2
git status
```

### Reference Errors
```bash
# Check paths exist
ls -la .claude/skills/devforgeai-ideation/references/
ls .claude/skills/devforgeai-ideation/SKILL.md
```

---

## Summary

This test suite provides:
- ✓ Clear specifications for what needs to be implemented
- ✓ Automated validation that implementation is complete
- ✓ Comprehensive documentation for reference
- ✓ Fail-fast testing to catch issues early

**Status**: Ready for implementation
**Next Action**: Begin GREEN phase by making tests pass

For detailed information, see individual documentation files:
- Implementation steps → EXECUTION-REPORT.md
- Test details → TEST-SUMMARY.md
- How to run → README.md

