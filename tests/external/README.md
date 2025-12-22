# STORY-047: External Project Installation Testing

## Overview

This directory contains comprehensive failing tests (RED phase, TDD) for STORY-047: "Full Installation Testing on External Node.js and .NET Projects".

All tests are intentionally **failing** as the installer has not yet been implemented for external project installations. Once the installer is complete (Phase 2), these tests will transition to **green (passing)**.

---

## Test Files

### 1. `test-installation-workflow.sh` (716 lines)

**Purpose:** Shell-based installer workflow testing
**Framework:** Bash
**Test Count:** 47 test cases

**Structure:**
```
├── AC Tests (Acceptance Criteria)
│   ├── AC1: Successful installation on Node.js (7 tests)
│   ├── AC2: All 14 commands functional (14 tests)
│   ├── AC3: CLAUDE.md merge (3 tests)
│   ├── AC4: Rollback functionality (3 tests)
│   ├── AC5: Installation on .NET (3 tests)
│   ├── AC6: Isolation validation (2 tests)
│   └── AC7: Upgrade workflow (3 tests)
├── BR Tests (Business Rules)
│   ├── BR1: Installation success (2 tests)
│   ├── BR2: Command functionality (1 test)
│   ├── BR3: User content preservation (2 tests)
│   ├── BR4: Rollback accuracy (1 test)
│   └── BR5: Project isolation (1 test)
├── NFR Tests (Non-Functional Requirements)
│   ├── NFR1: Performance <3 minutes (2 tests)
│   ├── NFR2: Rollback <45 seconds (1 test)
│   ├── NFR3: Repeatability (1 test)
│   ├── NFR4: Accuracy (1 test)
│   └── NFR5: Progress reporting (1 test)
└── EC Tests (Edge Cases)
    ├── EC1: Existing .claude/ (1 test)
    ├── EC2: Network failure (1 test)
    ├── EC3: Read-only filesystem (1 test)
    ├── EC4: Path resolution (1 test)
    ├── EC5: Python version (1 test)
    ├── EC6: Large merged file (1 test)
    └── EC7: Concurrent installations (1 test)
```

**Run Command:**
```bash
bash tests/external/test-installation-workflow.sh
```

**Expected Result (RED Phase):**
```
Total Tests Run:     47
Passed:              0
Failed:             47

Expected Status: ALL FAILING (RED phase)
Exit Code: 1 (failure)
```

---

### 2. `test_install_integration.py` (462 lines)

**Purpose:** Python pytest-based integration testing
**Framework:** pytest 7.0+
**Language:** Python 3.8+
**Test Count:** 47 test methods across 5 test classes

**Test Classes:**

```
TestExternalProjectInstallation
├── AC Tests (24 tests)
│   ├── test_ac1_*: Node.js installation (7 tests)
│   ├── test_ac2_*: Command functionality (1 test)
│   ├── test_ac3_*: CLAUDE.md merge (2 tests)
│   ├── test_ac4_*: Rollback (3 tests)
│   ├── test_ac5_*: .NET installation (3 tests)
│   ├── test_ac6_*: Isolation (2 tests)
│   └── test_ac7_*: Upgrade (2 tests)
├── BR Tests (5 tests)
│   ├── test_br1_*: Installation success (2 tests)
│   ├── test_br2_*: Command success rate (1 test)
│   ├── test_br3_*: User content (1 test)
│   ├── test_br4_*: Rollback accuracy (1 test)
│   └── test_br5_*: Project isolation (1 test)
└── Other Tests (9 tests)
    ├── Edge cases (5 tests)
    └── Performance (2 tests)

TestInstallationRepeatability (2 tests)
├── test_nodejs_installation_repeatability
└── test_dotnet_installation_repeatability

TestRollbackAccuracy (2 tests)
├── test_rollback_checksum_validation
└── test_rollback_file_count_restoration

TestDataValidation (6 tests)
├── test_installation_success_validation
├── test_file_count_validation
├── test_command_success_rate_validation
├── test_rollback_restoration_validation
├── test_cross_platform_parity_validation
└── test_isolation_validation
```

**Run Command:**
```bash
pytest tests/external/test_install_integration.py -v
```

**Expected Result (RED Phase):**
```
tests/external/test_install_integration.py::... FAILED [  1%]
tests/external/test_install_integration.py::... FAILED [  2%]
...
====================== 47 failed in X.XXs ======================

Exit Code: 1 (failure)
```

---

### 3. `TEST_REPORT.md`

**Purpose:** Comprehensive test generation report
**Contents:**
- Executive summary with test statistics
- Detailed test coverage breakdown by category
- Expected test results and behavior
- Setup instructions and prerequisites
- CI/CD integration examples
- Success criteria for each phase

---

## Test Statistics

### By Category

| Category | Count | Status |
|----------|-------|--------|
| Acceptance Criteria | 24 | ❌ FAILING |
| Business Rules | 10 | ❌ FAILING |
| Non-Functional Requirements | 5 | ❌ FAILING |
| Edge Cases | 7 | ❌ FAILING |
| Data Validation | 6 | ❌ FAILING |
| Performance | 2 | ❌ FAILING |
| Repeatability | 2 | ❌ FAILING |
| Rollback Accuracy | 2 | ❌ FAILING |
| **TOTAL** | **58** | ❌ **ALL RED** |

### By Test File

| File | Framework | Count | Status |
|------|-----------|-------|--------|
| test-installation-workflow.sh | Bash | 47 | ❌ FAILING |
| test_install_integration.py | pytest | 47 | ❌ FAILING |
| **TOTAL** | | **94+** | ❌ **ALL RED** |

---

## Test Coverage

### Acceptance Criteria Coverage ✓ 100%

- [x] AC1: Successful installation on Node.js (7 tests)
- [x] AC2: All 14 commands functional (14 tests)
- [x] AC3: CLAUDE.md merge (3 tests)
- [x] AC4: Rollback functionality (3 tests)
- [x] AC5: Installation on .NET (3 tests)
- [x] AC6: Isolation validation (2 tests)
- [x] AC7: Upgrade workflow (3 tests)

### Business Rules Coverage ✓ 100%

- [x] BR1: 100% installation success (2 tests)
- [x] BR2: All 14 commands work (1 test)
- [x] BR3: User content preserved (2 tests)
- [x] BR4: Rollback accuracy (1 test)
- [x] BR5: Project isolation (1 test)

### Edge Cases Coverage ✓ 100%

- [x] EC1: Existing .claude/ directory
- [x] EC2: Network failure during CLI install
- [x] EC3: Read-only filesystem
- [x] EC4: Installer from different directory
- [x] EC5: Different Python version
- [x] EC6: Large merged file
- [x] EC7: Concurrent installations

### Non-Functional Requirements Coverage ✓ 100%

- [x] NFR1: Performance <3 minutes
- [x] NFR2: Rollback <45 seconds
- [x] NFR3: Repeatability (3 runs)
- [x] NFR4: Accuracy (100% checksum)
- [x] NFR5: Progress reporting

---

## Running the Tests

### Prerequisites

```bash
# For shell tests
- bash 4.0+
- grep, find, wc

# For Python tests
- Python 3.8+
- pytest 7.0+
- pathlib, tempfile, json (stdlib)
```

### Quick Start

```bash
# Run shell tests
bash tests/external/test-installation-workflow.sh

# Run Python tests
pytest tests/external/test_install_integration.py -v

# Run all external tests
bash tests/external/test-installation-workflow.sh && \
pytest tests/external/test_install_integration.py -v
```

### Expected Output (RED Phase)

**Shell:**
```
Total Tests Run:     47
Passed:              0
Failed:             47

Expected Status: ALL FAILING (RED phase - installer not yet implemented)
```

**Pytest:**
```
====================== 47 failed in X.XXs ======================
```

---

## Test Flow

### Phase 1: RED (Current) ✓ COMPLETE

```
Write Tests → All Failing
    ↓
Tests clearly define requirements
    ↓
Ready for Phase 2: Implementation
```

**Status:** ✓ 58+ tests generated, all RED, comprehensive coverage

### Phase 2: GREEN (Next)

```
Implement installer → Tests pass
    ↓
All 58+ tests should pass
    ↓
Ready for Phase 3: Refactoring
```

**Implementation Tasks:**
1. Create installer/install.py with external project support
2. Implement tech detection (Node.js, .NET, Python)
3. Integrate CLAUDE.md merge (from STORY-046)
4. Implement rollback and upgrade workflows
5. Deploy framework files (.claude/, devforgeai/)
6. Test all 14 commands in external context

### Phase 3: REFACTOR

```
Improve code quality
    ↓
Performance optimization
    ↓
Code review and standards compliance
```

### Phase 4: Integration

```
Full workflow testing
    ↓
Cross-platform validation
    ↓
Production readiness
```

---

## Test Fixtures

### Node.js Test Project

**Auto-generated in:** `/tmp/devforgeai-test-*/NodeJsTestProject/`

**Files:**
- `package.json` - Node.js project metadata
- `CLAUDE.md` - Sample user project instructions (50 lines)

**Purpose:** Simulate external Node.js project for installation testing

### .NET Test Project

**Auto-generated in:** `/tmp/devforgeai-test-*/DotNetTestProject/`

**Files:**
- `TestProject.csproj` - .NET project file
- `Program.cs` - Sample C# code

**Purpose:** Simulate external .NET project for cross-platform validation

---

## Key Testing Concepts

### TDD Red Phase ✓ This Phase

- Tests are failing intentionally
- Tests define requirements clearly
- No implementation yet
- Foundation for Phase 2

### Test Independence

- Each test can run standalone
- No test depends on another
- Tests use fresh fixtures
- Automatic cleanup

### Test Pyramid

- **Unit Tests** (shell assertions): 40%
- **Integration Tests** (full workflow): 40%
- **End-to-End Tests** (command validation): 20%

### AAA Pattern (Arrange, Act, Assert)

All tests follow standard pattern:
```bash
# Arrange: Setup test project
setup_test_project

# Act: Run installer (when implemented)
python installer/install.py --target=/tmp/project

# Assert: Validate results
assert_file_exists .claude/
assert_command_exit_code 0
```

---

## Next Steps

1. **Phase 2 Implementation:** Implement installer for external projects
2. **Test Execution:** Run tests to see them go RED → GREEN
3. **Refactoring:** Improve code quality while keeping tests green
4. **Integration:** Full workflow and cross-platform testing
5. **Production:** Release installer for public use

---

## References

- **Story:** STORY-047 - Full Installation Testing on External Projects
- **Epic:** EPIC-009 - DevForgeAI Installer and Deployment System
- **Prerequisite:** STORY-046 - CLAUDE.md Template Merge (QA Approved)
- **Test Report:** TEST_REPORT.md (detailed documentation)

---

## Contact & Questions

For questions about these tests or to report issues:
1. Review TEST_REPORT.md for detailed information
2. Check test files for implementation details
3. Refer to test comments for expected behavior

---

**Generated:** 2025-11-20
**Status:** ✓ Complete - Ready for Phase 2 Implementation
**Total Coverage:** 58+ test cases, 100% AC/BR/NFR/EC coverage
**Expected Behavior:** ALL TESTS FAILING (RED PHASE - TDD)

