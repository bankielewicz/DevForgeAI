# STORY-127: Plan File Resume Convention - Test Suite Summary

**Status**: GENERATED (Red Phase - TDD)
**Test Framework**: Bash (native to DevForgeAI)
**Test Location**: `/mnt/c/Projects/DevForgeAI2/devforgeai/tests/STORY-127/`
**Created**: 2025-12-23

---

## Overview

This test suite validates STORY-127: Plan File Resume Convention, which solves the problem of duplicate plan files (from STORY-114) by implementing an intelligent plan file detection and resume mechanism.

**Problem Solved**: During STORY-114, two random-named plan files were created (`clever-snuggling-otter.md` and `enchanted-booping-pizza.md`) because the system didn't detect existing plan files before creating new ones.

**Solution**: Implement plan file convention with story ID-based naming and automatic detection of existing plans.

---

## Test Files Generated

| Test File | Acceptance Criteria | Status | Test Cases |
|-----------|-------------------|--------|-----------|
| `test-ac1-claude-md-section.sh` | AC#1 | FAILING | 5 |
| `test-ac2-phase0-search.sh` | AC#2 | FAILING | 6 |
| `test-ac3-story-id-priority.sh` | AC#3 | FAILING | 6 |
| `test-ac4-new-plan-naming.sh` | AC#4 | FAILING | 7 |
| `test-ac5-backward-compat.sh` | AC#5 | FAILING | 7 |
| **TOTAL** | **5 AC** | **RED** | **31 tests** |

---

## Acceptance Criteria Mapping

### AC#1: CLAUDE.md Includes Plan File Convention Section

**Test File**: `test-ac1-claude-md-section.sh`
**Purpose**: Verify CLAUDE.md documents the plan file convention with all required details

**Test Cases**:
1. **1.1**: Plan File Convention section exists
   - Search: `grep "## Plan File Convention" CLAUDE.md`
   - Expected: Section header found

2. **1.2**: Documents checking for existing plan files
   - Search: Section content for keywords "check", "existing", "plan"
   - Expected: Language about detecting existing plans

3. **1.3**: Documents search algorithm (glob + grep)
   - Search: Section for "glob", "grep", "algorithm", ".claude/plans"
   - Expected: Both glob (file listing) and grep (pattern matching) mentioned

4. **1.4**: Documents naming convention with story ID
   - Search: Keywords "naming", "story ID", or STORY- examples
   - Expected: Naming convention with story IDs documented

5. **1.5**: Documents resume vs create decision logic
   - Search: Keywords "resume" and "create" or "new"
   - Expected: Both decision paths documented

**Running the test**:
```bash
bash devforgeai/tests/STORY-127/test-ac1-claude-md-section.sh
```

**Expected output (RED phase)**:
```
RESULT: FAILED - AC#1 not implemented
Tests Failed: 5
```

---

### AC#2: /dev Phase 0 Checks for Existing Plans

**Test File**: `test-ac2-phase0-search.sh`
**Purpose**: Verify devforgeai-development SKILL.md Phase 0 implements plan file search

**Test Cases**:
1. **2.1**: Phase 0 includes plan file search logic
   - Location: devforgeai-development SKILL.md Phase 0 section
   - Expected: Plan file search documented before new creation

2. **2.2**: Search uses Glob to list plan files
   - Search: `Glob(pattern=".claude/plans/*.md")` pattern
   - Expected: Glob tool invoked for file listing

3. **2.3**: Search uses Grep to find story ID
   - Search: `Grep(pattern="STORY-...")` or similar
   - Expected: Grep tool invoked for pattern matching

4. **2.4**: Resume prompt documented in Phase 0
   - Search: Resume prompt text "Existing plan file found..."
   - Expected: Prompt text documented

5. **2.5**: Resume logic uses AskUserQuestion
   - Search: `AskUserQuestion()` invocation
   - Expected: User interaction documented

6. **2.6**: Search executes BEFORE creating new plan
   - Logic check: Phase 0 order verification
   - Expected: Search comes before new plan creation

**Running the test**:
```bash
bash devforgeai/tests/STORY-127/test-ac2-phase0-search.sh
```

**Expected output (RED phase)**:
```
RESULT: FAILED - AC#2 not implemented
Tests Failed: 6
```

---

### AC#3: Plan Files with Story ID Are Prioritized

**Test File**: `test-ac3-story-id-priority.sh`
**Purpose**: Verify story ID files are suggested before random-named files

**Test Cases**:
1. **3.1**: Prioritization strategy documented
   - Keywords: "prioritize", "suggest first", "prefer"
   - Expected: Prioritization approach documented

2. **3.2**: Deprioritizing random names documented
   - Keywords: "random name", "deprioritize", "avoid"
   - Expected: Random-named files clearly deprioritized

3. **3.3**: Search sorts by story ID match
   - Logic: Name matches before content matches
   - Fixture: Creates test plan files with mixed naming
   - Expected: STORY-127-plan-file-resume.md suggested first

4. **3.4**: Word boundary matching prevents false positives
   - Keywords: "word boundary", "\\b", "false positive"
   - Purpose: Prevent STORY-11 matching STORY-114
   - Expected: Word boundary matching documented

5. **3.5**: Multiple matches handling documented
   - Keywords: "multiple match", "multiple file", "several plan"
   - Expected: Strategy for handling multiple matches

6. **3.6**: Practical simulation of prioritization logic
   - Fixture: Creates 3 test files (name match, content match, no match)
   - Expected: Correct categorization and priority order

**Running the test**:
```bash
bash devforgeai/tests/STORY-127/test-ac3-story-id-priority.sh
```

**Expected output (RED phase)**:
```
RESULT: FAILED - AC#3 not implemented
Tests Failed: 6
```

---

### AC#4: New Plans Use Story ID in Filename

**Test File**: `test-ac4-new-plan-naming.sh`
**Purpose**: Verify new plan filenames follow STORY-XXX-description.md pattern

**Test Cases**:
1. **4.1**: CLAUDE.md documents story ID naming convention
   - Pattern: `STORY-XXX-description.md`
   - Example: `STORY-127-plan-file-resume.md`
   - Expected: Examples provided

2. **4.2**: Documentation contrasts good vs bad naming
   - Good examples: STORY-127-...
   - Bad examples: groovy-swimming-lake.md
   - Expected: Explicit contrast provided

3. **4.3**: Avoids random adjective-noun combinations
   - Examples to avoid: clever-snuggling-otter, enchanted-booping-pizza
   - Expected: Clear guidance against random naming

4. **4.4**: Phase 0 creates new plan with story ID
   - Location: SKILL.md Phase 0 new plan creation
   - Pattern: `.claude/plans/STORY-{ID}-...md`
   - Expected: Story ID required in new filename

5. **4.5**: Naming pattern documented
   - Pattern: `STORY-{ID}-{description}.md`
   - Expected: Pattern template provided

6. **4.6**: Practical validation of STORY-XXX pattern
   - Regex: `^STORY-[0-9]+-.*\.md$`
   - Valid: STORY-127-plan-file-resume.md, STORY-001-test.md
   - Invalid: groovy-swimming-lake.md, plan.md
   - Expected: 5 invalid names correctly rejected

7. **4.7**: Exception for exploratory work documented
   - Optional: Exception for non-story exploration
   - Expected: Mention of exception (optional)

**Running the test**:
```bash
bash devforgeai/tests/STORY-127/test-ac4-new-plan-naming.sh
```

**Expected output (RED phase)**:
```
RESULT: FAILED - AC#4 not implemented
Tests Failed: 6
```

---

### AC#5: Backward Compatibility

**Test File**: `test-ac5-backward-compat.sh`
**Purpose**: Verify existing random-named files with story ID are detected and work

**Test Cases**:
1. **5.1**: Backward compatibility explicitly documented
   - Keywords: "backward", "compatibility", "existing random", "legacy"
   - Expected: Backward compatibility explicitly mentioned

2. **5.2**: Random-named files with story ID are detected
   - Fixture: Creates `clever-snuggling-otter.md` with STORY-114
   - Expected: File detected via grep search

3. **5.3**: No errors with mixed naming conventions
   - Fixture: Mix of old random names and new STORY-XXX names
   - Expected: No I/O errors, grep succeeds

4. **5.4**: Search algorithm handles both naming styles
   - Algorithm: Glob + Grep works for ANY filename
   - Expected: No filename format exclusions

5. **5.5**: STORY-114 scenario addressed
   - Problem: Multiple random-named plans created
   - Expected: Problem scenario documented

6. **5.6**: Practical detection with mixed fixture
   - Fixture: STORY-114 files with random names + new STORY-127 file
   - Expected: Detection finds multiple matches

7. **5.7**: Resume prompt works with random-named files
   - Prompt: Uses `{filename}` placeholder
   - Expected: Works for any filename format

**Running the test**:
```bash
bash devforgeai/tests/STORY-127/test-ac5-backward-compat.sh
```

**Expected output (RED phase)**:
```
RESULT: FAILED - AC#5 not implemented
Tests Failed: 7
```

---

## Running All Tests

### Option 1: Run individual tests
```bash
bash devforgeai/tests/STORY-127/test-ac1-claude-md-section.sh
bash devforgeai/tests/STORY-127/test-ac2-phase0-search.sh
bash devforgeai/tests/STORY-127/test-ac3-story-id-priority.sh
bash devforgeai/tests/STORY-127/test-ac4-new-plan-naming.sh
bash devforgeai/tests/STORY-127/test-ac5-backward-compat.sh
```

### Option 2: Run all tests at once
```bash
#!/bin/bash
for test in devforgeai/tests/STORY-127/test-*.sh; do
  echo "Running: $(basename $test)"
  bash "$test"
  echo ""
done
```

### Option 3: Run with summary
```bash
cd /mnt/c/Projects/DevForgeAI2
bash devforgeai/tests/STORY-127/test-ac1-claude-md-section.sh 2>&1 | grep -E "PASS|FAIL|RESULT"
bash devforgeai/tests/STORY-127/test-ac2-phase0-search.sh 2>&1 | grep -E "PASS|FAIL|RESULT"
bash devforgeai/tests/STORY-127/test-ac3-story-id-priority.sh 2>&1 | grep -E "PASS|FAIL|RESULT"
bash devforgeai/tests/STORY-127/test-ac4-new-plan-naming.sh 2>&1 | grep -E "PASS|FAIL|RESULT"
bash devforgeai/tests/STORY-127/test-ac5-backward-compat.sh 2>&1 | grep -E "PASS|FAIL|RESULT"
```

---

## Current Test Status (RED Phase)

| Test | AC | Cases | Status |
|------|-------|-------|--------|
| test-ac1 | 1 | 5 | FAILING ✗ |
| test-ac2 | 2 | 6 | FAILING ✗ |
| test-ac3 | 3 | 6 | FAILING ✗ |
| test-ac4 | 4 | 7 | FAILING ✗ |
| test-ac5 | 5 | 7 | FAILING ✗ |
| **TOTAL** | **5** | **31** | **ALL FAILING** |

---

## Test Design Patterns

### Pattern 1: Documentation Verification
Tests 1.1-1.5, 2.1-2.6, etc. verify that documentation sections exist and contain required keywords.

**Implementation**:
```bash
grep -q "keyword" file.md
if [ $? -eq 0 ]; then
  echo "PASS"
else
  echo "FAIL"
fi
```

### Pattern 2: Fixture-Based Testing
Tests 3.3, 3.6, 5.2, 5.6 create temporary test fixtures to validate logic.

**Implementation**:
```bash
setup_fixture() {
  mkdir -p "$TEST_FIXTURE"
  # Create test files
}

cleanup_fixture() {
  rm -rf "$TEST_FIXTURE"
}
```

### Pattern 3: Practical Algorithm Testing
Tests validate that search algorithm works correctly with real file operations.

**Implementation**:
```bash
# Test file detection with glob + grep
for file in "$TEST_FIXTURE"/*.md; do
  if grep -q "STORY-127" "$file"; then
    matches+=("$file")
  fi
done
```

### Pattern 4: Pattern Matching Validation
Tests 4.6 validates naming against regex patterns.

**Implementation**:
```bash
pattern="^STORY-[0-9]+-.*\.md$"
if [[ $filename =~ $pattern ]]; then
  echo "PASS: Valid naming"
fi
```

---

## Test Framework Details

### Execution Environment
- **Framework**: Bash (native to DevForgeAI)
- **Requirements**: bash, grep, sed, find, mkdir, rm
- **Line Endings**: Unix (LF) - not Windows (CRLF)

### Color Output
- GREEN: ✓ PASS
- RED: ✗ FAIL
- YELLOW: Test description
- BLUE: (reserved for future use)

### Output Format
All tests follow consistent output format:
```
===============================================================================
TEST: Test name
===============================================================================

Test 1.1: Description...
✓ PASS: Details
Test 1.2: Description...
✗ FAIL: Expected vs actual

===============================================================================
TEST SUMMARY: Test name
===============================================================================
Tests Passed: X
Tests Failed: Y
Total Tests: X+Y

RESULT: FAILED - AC not implemented
```

---

## Implementation Roadmap

### GREEN Phase (Implementation)

To implement and pass all tests:

1. **Add Plan File Convention to CLAUDE.md**
   - New section: `## Plan File Convention`
   - Document: Glob + Grep search algorithm
   - Document: Story ID naming convention
   - Document: Resume vs create decision
   - Satisfy: AC#1 tests

2. **Add Plan File Search to devforgeai-development SKILL.md Phase 0**
   - Add plan file detection step
   - Use Glob to list `.claude/plans/*.md`
   - Use Grep to search for story ID
   - Add resume prompt with AskUserQuestion
   - Execute search BEFORE new plan creation
   - Satisfy: AC#2 tests

3. **Implement Prioritization Logic**
   - Sort results: filename match (STORY-XXX) first
   - Sort results: content match second
   - Use word boundary grep (`\bSTORY-127\b`)
   - Prevent false positives (STORY-11 vs STORY-114)
   - Satisfy: AC#3 tests

4. **Enforce Story ID Naming Convention**
   - New plans: `STORY-{ID}-{description}.md`
   - Document examples: STORY-127-plan-file-resume.md
   - Contrast bad naming: groovy-swimming-lake.md
   - Exception for exploratory work (optional)
   - Satisfy: AC#4 tests

5. **Ensure Backward Compatibility**
   - Detect random-named files with story ID
   - No filename format restrictions
   - Works with STORY-114 existing files
   - Resume prompt works with any filename
   - Satisfy: AC#5 tests

### REFACTOR Phase (Quality)

After implementation:
- Code review for clarity and efficiency
- Extract common functions
- Optimize grep patterns (word boundaries)
- Add error handling
- Update documentation with examples

---

## Test Coverage Summary

| Area | Coverage | Test Cases |
|------|----------|-----------|
| CLAUDE.md Documentation | 100% | 5 (AC#1) |
| Phase 0 Search Logic | 100% | 6 (AC#2) |
| Prioritization Strategy | 100% | 6 (AC#3) |
| Naming Convention | 100% | 7 (AC#4) |
| Backward Compatibility | 100% | 7 (AC#5) |
| **Total** | **100%** | **31 tests** |

---

## Links to Implementation Files

### Files to Modify (from Story Technical Specification)

1. **CLAUDE.md** (Root level)
   - Add: `## Plan File Convention` section
   - Document: Detection, search, naming, decision logic
   - Lines to add: ~40 lines (estimated)

2. **.claude/skills/devforgeai-development/SKILL.md**
   - Add: Plan file search in Phase 01 (Pre-Flight Validation)
   - Add: Glob + Grep logic
   - Add: Resume prompt with AskUserQuestion
   - Lines to add: ~50 lines (estimated)

### Reference Documentation

- **Tech Stack**: `/mnt/c/Projects/DevForgeAI2/devforgeai/specs/context/tech-stack.md`
  - Framework: Claude Code Terminal
  - Test framework: Bash
  - Tools: Glob, Grep, AskUserQuestion

- **Coding Standards**: `/mnt/c/Projects/DevForgeAI2/devforgeai/specs/context/coding-standards.md`
  - Shell script testing (lines 249-270): Use explicit `bash` invocation
  - Line ending fix: `dos2unix` before execution

---

## Notes for Developer

### Important Implementation Details

1. **Word Boundary Matching**: Use `\b` in grep to prevent STORY-11 matching STORY-114
   ```bash
   grep -w "STORY-127" "$file"  # or grep "\bSTORY-127\b"
   ```

2. **Prioritization Order**:
   - Priority 1: Filename contains STORY-ID (highest - name match)
   - Priority 2: File content contains STORY-ID (medium - content match)
   - Priority 3: Unrelated files (lowest - deprioritized)

3. **Resume Prompt Suggestion Format**:
   ```
   Existing plan file found: {filename}
   Resume this plan? [Y/n]
   ```

4. **New Plan Filename Format**:
   - Pattern: `STORY-{ID}-{description}.md`
   - Example: `.claude/plans/STORY-127-plan-file-resume.md`
   - NOT: `.claude/plans/groovy-swimming-lake.md` (random naming)

5. **Phase 0 Execution Order**:
   - Step 1: Check for existing plans (glob + grep + AskUserQuestion)
   - Step 2: If no match, create new plan with story ID
   - NOT the other way around

### Known Test Patterns to Watch

1. **Line 1-50**: Test case setup and documentation
2. **Line 50-150**: Individual test functions (test_case_name)
3. **Line 150-end**: Main execution and summary

### Common Test Failures to Investigate

1. **Section not found**: Check for exact section header format: `## Plan File Convention`
2. **Algorithm not documented**: Look for Glob + Grep patterns
3. **Naming convention not clear**: Check for STORY-XXX examples
4. **Backward compatibility missing**: Ensure random-named file support

---

## Version History

| Date | Version | Changes |
|------|---------|---------|
| 2025-12-23 | 1.0 | Initial test suite generation (RED phase) |

---

**Generated**: 2025-12-23
**Test Framework**: Bash (native to DevForgeAI)
**Status**: All tests FAILING (RED Phase - TDD)
**Next Phase**: Implementation (GREEN Phase)
