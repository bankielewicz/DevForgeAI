# STORY-144 Test Suite
## Integrate or Remove Orphaned Files

**Story ID**: STORY-144
**Status**: Test-Driven Development (TDD) Red Phase
**Test Framework**: Bash/Shell
**Location**: `/mnt/c/Projects/DevForgeAI2/tests/STORY-144/`

---

## Overview

This test suite validates the cleanup and resolution of orphaned documentation files in the DevForgeAI ideation skill. The tests cover four acceptance criteria:

1. **AC#1**: user-input-integration-guide.md reviewed and resolved
2. **AC#2**: brainstorm-data-mapping.md reviewed and resolved
3. **AC#3**: No unreferenced files remain in references directory
4. **AC#4**: Commit message documents justification

---

## Current Test Status: FAILING (Expected)

**This is the RED phase of TDD.** Tests are written FIRST, before implementation. All tests are expected to FAIL initially because:

1. Orphaned files still exist
2. Content has not been integrated
3. Files are still referenced in SKILL.md
4. Commit message has not been created

**Implementation tasks will make these tests pass.**

---

## Test Files

### 1. `test-ac1-user-input-integration-guide.sh`
**Purpose**: Verify user-input-integration-guide.md is resolved (deleted or integrated)

**Tests**:
- File must not exist as orphaned reference (after resolution)
- Filename should not appear in SKILL.md references
- If integrated, content should exist in user-input-guidance.md
- Target file user-input-guidance.md must exist
- If integrated, content sections preserved (Load Mechanism, Error Handling)
- Orphaned file path exists (prerequisite check)
- No dangling references after deletion
- Section headers preserved if integrated

**Expected Result**: 8 tests, initially FAILING because file exists

---

### 2. `test-ac2-brainstorm-data-mapping.sh`
**Purpose**: Verify brainstorm-data-mapping.md is resolved (deleted or integrated)

**Tests**:
- File must not exist as orphaned reference (after resolution)
- Filename should not appear in SKILL.md references
- If integrated, content should exist in brainstorm-handoff-workflow.md
- Target file brainstorm-handoff-workflow.md must exist
- If integrated, content sections preserved
- Orphaned file path exists (prerequisite check)
- No dangling references after deletion
- Orphaned file is valid markdown format
- Integration complete (target file has sufficient content)

**Expected Result**: 9 tests, initially FAILING because file exists

---

### 3. `test-ac3-no-unreferenced-files.sh`
**Purpose**: Verify all files in references directory are referenced in SKILL.md or workflow files

**Tests**:
- References directory exists
- SKILL.md exists
- All .md files in references are referenced (MAIN TEST - currently FAILING)
- All reference files follow naming conventions
- No hidden files in references directory
- All reference files are valid markdown or config format
- user-input-integration-guide.md is resolved
- brainstorm-data-mapping.md is resolved
- No obvious circular references
- Comprehensive reference scan with detailed output

**Expected Result**: 10 tests, AC#3 test FAILING if unreferenced files exist

---

### 4. `test-ac4-commit-message-documentation.sh`
**Purpose**: Verify commit message documents the resolution action and justification

**Expected Format**:
```
chore(ideation): resolve orphaned reference files

- user-input-integration-guide.md: [INTEGRATED/DELETED] - [reason]
- brainstorm-data-mapping.md: [INTEGRATED/DELETED] - [reason]
```

**Tests**:
- Git repository exists
- Commits exist in repository
- Commit mentions STORY-144
- Commit mentions resolution action (orphaned/resolve/remove/integrate)
- Commit lists affected files
- Commit documents action taken (INTEGRATED or DELETED)
- Commit includes justification
- Commit follows conventional commit format
- Commit affects ideation skill files
- Both files documented in commit
- Commit has sufficient detail (multi-line)
- Commit scope mentions ideation

**Expected Result**: 12 tests, all FAILING until commit is created

---

## How to Run Tests

### Run All Tests
```bash
bash /mnt/c/Projects/DevForgeAI2/tests/STORY-144/run-all-tests.sh
```

### Run Individual Test Suite
```bash
# AC#1 tests
bash /mnt/c/Projects/DevForgeAI2/tests/STORY-144/test-ac1-user-input-integration-guide.sh

# AC#2 tests
bash /mnt/c/Projects/DevForgeAI2/tests/STORY-144/test-ac2-brainstorm-data-mapping.sh

# AC#3 tests
bash /mnt/c/Projects/DevForgeAI2/tests/STORY-144/test-ac3-no-unreferenced-files.sh

# AC#4 tests
bash /mnt/c/Projects/DevForgeAI2/tests/STORY-144/test-ac4-commit-message-documentation.sh
```

### Expected Output (Red Phase)
```
✓ PASSED (Expected failure in Red phase)  - For prerequisite tests
✗ FAILED (Expected to fail in Red phase)  - For tests requiring implementation
```

---

## Test Architecture

### AAA Pattern (Arrange, Act, Assert)

Each test follows the Arrange-Act-Assert pattern:

1. **Arrange**: Set up test preconditions (paths, files, directories)
2. **Act**: Execute the behavior being tested (check file existence, search for references)
3. **Assert**: Verify the outcome (file deleted, references gone, content integrated)

### Test Isolation

- Each test is independent and can run in any order
- No shared state between tests
- Tests use absolute paths to avoid working directory issues
- Prerequisite tests verify infrastructure (file paths exist)

### Failure Detection

Tests use the `should_fail` parameter to distinguish:
- **Tests that should PASS in Red phase** (prerequisites, setup validation)
- **Tests that should FAIL in Red phase** (actual implementation requirements)

---

## Test Pyramid

The test suite maintains TDD principles:

```
       /\
      /  \       AC#4: Commit message (integration test)
     /    \
    /------\
   /        \    AC#3: Reference verification (unit test)
  /          \
 /------------\
/              \  AC#1, AC#2: File operations (unit tests)
```

**Distribution**:
- **Unit Tests** (AC#1, AC#2): File existence, path validation, reference checks
- **Integration Tests** (AC#3): Multi-file reference scanning
- **Documentation Tests** (AC#4): Commit message format validation

---

## Acceptance Criteria Mapping

| AC | Test File | Tests | Status |
|----|-----------|-------|--------|
| AC#1 | test-ac1-user-input-integration-guide.sh | 8 | RED (Failing) |
| AC#2 | test-ac2-brainstorm-data-mapping.sh | 9 | RED (Failing) |
| AC#3 | test-ac3-no-unreferenced-files.sh | 10 | RED (Failing) |
| AC#4 | test-ac4-commit-message-documentation.sh | 12 | RED (Failing) |
| **TOTAL** | **4 test files** | **39 tests** | **RED Phase** |

---

## Implementation Checklist

To make these tests pass, implement the following:

### Phase 1: File Analysis (Manual)
- [ ] Review user-input-integration-guide.md (max 30 minutes)
  - Valuable content? → Move to AC#1 implementation
  - Redundant? → Mark for deletion
- [ ] Review brainstorm-data-mapping.md (max 30 minutes)
  - Valuable content? → Move to AC#2 implementation
  - Redundant? → Mark for deletion

### Phase 2: Integration (If Content Valuable)
- [ ] If user-input-integration-guide.md valuable:
  - [ ] Copy content to user-input-guidance.md Section 5
  - [ ] Verify content preserved completely
  - [ ] Delete original file
  - [ ] Remove references from SKILL.md
- [ ] If brainstorm-data-mapping.md valuable:
  - [ ] Copy content to brainstorm-handoff-workflow.md
  - [ ] Verify content preserved completely
  - [ ] Delete original file
  - [ ] Remove references from SKILL.md

### Phase 3: Deletion (If Content Redundant)
- [ ] If user-input-integration-guide.md redundant:
  - [ ] Delete file: `.claude/skills/devforgeai-ideation/references/user-input-integration-guide.md`
  - [ ] Remove reference from SKILL.md
- [ ] If brainstorm-data-mapping.md redundant:
  - [ ] Delete file: `.claude/skills/devforgeai-ideation/references/brainstorm-data-mapping.md`
  - [ ] Remove reference from SKILL.md

### Phase 4: Commit with Documentation
- [ ] Create commit with message:
  ```
  chore(ideation): resolve orphaned reference files

  - user-input-integration-guide.md: [INTEGRATED/DELETED] - [reason]
  - brainstorm-data-mapping.md: [INTEGRATED/DELETED] - [reason]
  ```

---

## File Locations

**Orphaned Files to Resolve**:
- `/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-ideation/references/user-input-integration-guide.md`
- `/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-ideation/references/brainstorm-data-mapping.md`

**Integration Target Files**:
- `/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-ideation/references/user-input-guidance.md` (Section 5)
- `/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-ideation/references/brainstorm-handoff-workflow.md`

**SKILL.md to Update**:
- `/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-ideation/SKILL.md`

**Git Repository**:
- `/mnt/c/Projects/DevForgeAI2/` (contains .git/)

---

## Exit Codes

Test scripts return:
- **0**: All tests passed
- **N**: N tests failed (where N > 0)

Example:
```bash
$ bash test-ac1-user-input-integration-guide.sh
...
Tests Failed: 5
exit $TESTS_FAILED  # Exits with code 5
```

Master test runner sums all failures from all test files.

---

## Test Maintenance

### Updating Tests
If requirements change:
1. Update test expectations in the script
2. Add new test functions with `run_test` helper
3. Keep AAA pattern consistent
4. Update this README

### Adding New Tests
To add a new test:
```bash
run_test \
    "test-descriptive-name" \
    "test_command_or_condition" \
    "true_or_false"  # Should fail initially?
```

---

## TDD Workflow

This test suite implements Test-Driven Development:

### Phase 1: RED (Current)
- ✓ Tests written and failing
- ✓ Acceptance criteria documented in tests
- ✓ Test framework selected (Bash/Shell)
- ⏳ Waiting for implementation

### Phase 2: GREEN (Next)
- Implement file cleanup
- Make failing tests pass
- All tests should exit with code 0

### Phase 3: REFACTOR (Final)
- Optimize implementation if needed
- Improve code quality
- Verify all tests still pass

---

## Troubleshooting

### Test Hangs
- Check file paths are correct
- Verify grep patterns are matching
- Look for recursive directory scans that may be slow

### Permission Errors
- Ensure test files are executable: `chmod +x *.sh`
- Verify read/write access to test directories
- Check git repository permissions

### Git Errors
- Verify git repository exists: `git rev-parse --git-dir`
- Check git config is accessible
- Ensure you have git installed

---

## References

- Story File: `/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-144-integrate-remove-orphaned-files.story.md`
- Tech Stack: `/mnt/c/Projects/DevForgeAI2/devforgeai/specs/context/tech-stack.md`
- Source Tree: `/mnt/c/Projects/DevForgeAI2/devforgeai/specs/context/source-tree.md`

---

## Summary

**Test Suite Statistics**:
- Total Test Files: 4
- Total Tests: 39
- Test Framework: Bash/Shell Scripts
- Status: RED Phase (All Tests Failing - Expected)
- Coverage: 100% of acceptance criteria

**Next Steps**:
1. Review orphaned files (AC#1, AC#2)
2. Make decision: integrate or delete
3. Update SKILL.md references
4. Create commit with documentation
5. Run tests to verify implementation

