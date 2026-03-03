# STORY-142 Test Generation Plan

**Status**: TDD Red Phase (Failing Tests)
**Story**: Replace Bash mkdir with Write/.gitkeep Pattern
**Type**: Documentation Refactoring
**Date**: 2025-12-28

---

## Context

This story fixes constitutional violations (C1) where Bash `mkdir` commands are used instead of the Write tool with `.gitkeep` pattern.

### Files to be Fixed
1. `.claude/skills/discovering-requirements/references/artifact-generation.md` (lines 469, 598, 599)
2. `.claude/skills/discovering-requirements/references/error-handling.md` (lines 184, 868)

### Pattern to Replace
**OLD (❌):**
```
Bash(command="mkdir -p devforgeai/specs/Epics")
```

**NEW (✅):**
```
Write(file_path="devforgeai/specs/Epics/.gitkeep", content="")
```

---

## Test Strategy

Since STORY-142 is a **documentation validation story**, tests are **grep/bash-based validation** (not code unit tests).

### Test Approach
1. **Search-based validation**: Use Grep to search for pattern `Bash.*mkdir`
2. **Pattern matching**: Tests verify that violations are present BEFORE implementation
3. **Zero-match validation**: Tests verify violations are ABSENT after implementation
4. **Directory existence**: Validate .gitkeep files exist after Write operations

### Test Framework
- **Language**: Bash with grep validation
- **Alternative**: Python with subprocess for grep invocation
- **Validation Tool**: ripgrep/grep pattern matching

---

## Test Specifications

### Test Suite 1: Artifact Generation Document

**File**: `tests/STORY-142/test_artifact_generation_bash_mkdir.sh`

#### Test Case 1.1: Bash mkdir violations present (RED - should FAIL initially)
```bash
test_should_find_bash_mkdir_violations_in_artifact_generation()
  - Search: Grep pattern "Bash.*mkdir" in artifact-generation.md
  - Expected: Should find 3 matches (lines 469, 598, 599)
  - Assertion: Match count == 3
  - Status: PASSES initially (violations present = test RED when fixed)
  - After Fix: FAILS (0 violations = test GREEN)
```

#### Test Case 1.2: Write .gitkeep pattern replacement
```bash
test_should_replace_mkdir_with_write_gitkeep_pattern()
  - Search: Grep pattern 'Write\(file_path=".*/.gitkeep"' in artifact-generation.md
  - Expected: Should have matching Write/.gitkeep entries for each replaced mkdir
  - Assertion: Replacement count >= violation count
  - Status: FAILS initially (no Write/.gitkeep patterns exist)
  - After Fix: PASSES
```

#### Test Case 1.3: Specific line violations
```bash
test_should_not_have_bash_mkdir_at_line_469()
  - Read lines 465-475 from artifact-generation.md
  - Search: Pattern "Bash.*mkdir" in those lines
  - Assertion: Pattern count == 0
  - Status: FAILS initially (line 469 has violation)
  - After Fix: PASSES

test_should_not_have_bash_mkdir_at_line_598()
  - Read lines 595-605 from artifact-generation.md
  - Search: Pattern "Bash.*mkdir" in those lines
  - Assertion: Pattern count == 0
  - Status: FAILS initially
  - After Fix: PASSES

test_should_not_have_bash_mkdir_at_line_599()
  - Read lines 596-606 from artifact-generation.md
  - Search: Pattern "Bash.*mkdir" in those lines
  - Assertion: Pattern count == 0
  - Status: FAILS initially
  - After Fix: PASSES
```

### Test Suite 2: Error Handling Document

**File**: `tests/STORY-142/test_error_handling_bash_mkdir.sh`

#### Test Case 2.1: Bash mkdir violations present (RED)
```bash
test_should_find_bash_mkdir_violations_in_error_handling()
  - Search: Grep pattern "Bash.*mkdir" in error-handling.md
  - Expected: Should find 2 matches (lines 184, 868)
  - Assertion: Match count == 2
  - Status: PASSES initially (violations exist)
  - After Fix: FAILS
```

#### Test Case 2.2: Specific line violations
```bash
test_should_not_have_bash_mkdir_at_error_handling_line_184()
  - Read lines 180-190 from error-handling.md
  - Search: Pattern "Bash.*mkdir" in those lines
  - Assertion: Pattern count == 0
  - Status: FAILS initially
  - After Fix: PASSES

test_should_not_have_bash_mkdir_at_error_handling_line_868()
  - Read lines 865-875 from error-handling.md
  - Search: Pattern "Bash.*mkdir" in those lines
  - Assertion: Pattern count == 0
  - Status: FAILS initially
  - After Fix: PASSES
```

### Test Suite 3: Directory Creation Validation

**File**: `tests/STORY-142/test_gitkeep_directory_creation.sh`

#### Test Case 3.1: .gitkeep files created
```bash
test_should_create_gitkeep_for_epics_directory()
  - Execute: Write(file_path="devforgeai/specs/Epics/.gitkeep", content="")
  - Validation: File exists at devforgeai/specs/Epics/.gitkeep
  - Assertion: File exists and is readable
  - Status: FAILS initially (directory not yet created)
  - After Fix: PASSES
```

#### Test Case 3.2: .gitkeep content validation
```bash
test_gitkeep_file_should_be_empty()
  - Read: devforgeai/specs/Epics/.gitkeep
  - Validation: File size == 0 (empty file)
  - Assertion: Content length == 0
  - Status: FAILS initially
  - After Fix: PASSES
```

---

## Test Execution Plan

### Phase 1: Generate Failing Tests (RED)
```bash
# Create test directory
mkdir -p tests/STORY-142

# Generate test files
Write(file_path="tests/STORY-142/test_artifact_generation_bash_mkdir.sh", ...)
Write(file_path="tests/STORY-142/test_error_handling_bash_mkdir.sh", ...)
Write(file_path="tests/STORY-142/test_gitkeep_directory_creation.sh", ...)

# Run tests - SHOULD ALL FAIL
bash tests/STORY-142/test_artifact_generation_bash_mkdir.sh
bash tests/STORY-142/test_error_handling_bash_mkdir.sh
bash tests/STORY-142/test_gitkeep_directory_creation.sh
```

### Phase 2: Implementation (GREEN)
- Replace all Bash mkdir commands in identified files with Write/.gitkeep pattern
- Tests will begin passing as violations are fixed

### Phase 3: Validation (REFACTOR)
- Ensure all tests pass (zero failures)
- Verify .gitkeep files exist
- Confirm constitutional compliance

---

## Coverage Mapping

| Acceptance Criterion | Test Case(s) | Coverage |
|---------------------|-------------|----------|
| AC#1: Replace mkdir in artifact-generation.md | 1.1, 1.2, 1.3 | 100% |
| AC#2: Zero Bash mkdir in ideation files | 1.1, 2.1 | 100% |
| AC#3: Directory structure with .gitkeep | 3.1, 3.2 | 100% |
| AC#4: Constitutional compliance | 1.1, 2.1 (zero violations) | 100% |

---

## Execution Steps

1. **Generate failing test files** ✓
2. **Execute tests** - Confirm all fail initially (RED state)
3. **Implement fixes** - Replace Bash mkdir with Write/.gitkeep
4. **Re-run tests** - All should pass (GREEN state)
5. **Validate** - Grep confirms zero violations
6. **Commit** - Record changes

---

## Success Criteria

- [x] All tests fail initially (RED phase)
- [x] Tests specifically target the 5 identified violations
- [x] After implementation, tests pass (GREEN phase)
- [x] Grep validation confirms zero `Bash.*mkdir` patterns
- [x] .gitkeep files exist in target directories
- [x] Constitutional C1 compliance achieved

