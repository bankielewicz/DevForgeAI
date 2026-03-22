# STORY-210: Generate Validation Tests for PATTERNS.md Knowledge Base

**Story Type:** Documentation
**Artifact:** devforgeai/RCA/PATTERNS.md (Markdown knowledge base file)
**Test Framework:** Bash script validation (file existence, content structure)
**Test Location:** devforgeai/tests/STORY-210/ (per source-tree.md)

## Plan Overview

This plan documents the strategy for generating bash validation tests for STORY-210 that validate the PATTERNS.md knowledge base file structure and content.

### Story Context

STORY-210 documents recurring RCA patterns in the framework. The primary pattern is PATTERN-001 (Premature Workflow Completion) which has been identified 3 times (RCA-009, RCA-013, RCA-018).

**Key Acceptance Criteria:**
- AC-1: File exists at devforgeai/RCA/PATTERNS.md
- AC-2: Pattern template structure (ID, identified date, recurrences, description, root cause, detection, prevention, metrics)
- AC-3: PATTERN-001 specifically documented with RCA references
- AC-4: Detection indicators for both user and Claude (self-detection)
- AC-5: Related RCAs cross-referenced in table format

## Test Suite Structure

### Test Files Organization

```
devforgeai/tests/STORY-210/
├── test-ac1-file-exists.sh           # AC-1: File exists at correct location
├── test-ac2-template-structure.sh    # AC-2: Pattern template structure
├── test-ac3-pattern-001-documented.sh # AC-3: PATTERN-001 content
├── test-ac4-detection-indicators.sh  # AC-4: User and Claude detection sections
├── test-ac5-rca-cross-references.sh  # AC-5: RCA cross-reference table
└── run-all-tests.sh                  # Test runner script
```

### Expected Test Results (Initial - Red Phase)

All tests should FAIL initially since the file doesn't exist yet:

```
✗ FAIL: PATTERNS.md file exists at devforgeai/RCA/PATTERNS.md
✗ FAIL: Pattern template includes Pattern ID section
✗ FAIL: PATTERN-001 documented with RCA-009 reference
✗ FAIL: Detection indicators "For User:" section present
✗ FAIL: RCA cross-reference table present
```

## Test Implementation Details

### Test AC-1: File Exists at Correct Location

**File:** test-ac1-file-exists.sh
**Validation Points:**
1. File exists at `devforgeai/RCA/PATTERNS.md`
2. File is readable
3. File is not empty (has content)

**Assertions:**
- `[ -f "$PATTERNS_FILE" ]` - File exists
- `[ -r "$PATTERNS_FILE" ]` - File is readable
- `[ -s "$PATTERNS_FILE" ]` - File is non-empty

**Expected Result:** FAIL (file doesn't exist yet)

### Test AC-2: Pattern Template Structure

**File:** test-ac2-template-structure.sh
**Validation Points:**
1. File contains "# Recurring RCA Patterns" header
2. Pattern template includes all required sections:
   - Pattern ID (PATTERN-NNN)
   - First Identified
   - Recurrences
   - Frequency
   - Status
   - Behavior section
   - Root Cause section
   - Detection Indicators section
   - Prevention Strategy section
   - Metrics section
   - Related RCAs section
3. Pattern Index section exists
4. "Adding New Patterns" guide section exists

**Grep Patterns to Validate:**
```bash
grep -q "^# Recurring RCA Patterns" "$PATTERNS_FILE"
grep -q "^## PATTERN-001:" "$PATTERNS_FILE"
grep -q "^\\*\\*First Identified:\\*\\*" "$PATTERNS_FILE"
grep -q "^\\*\\*Recurrences:\\*\\*" "$PATTERNS_FILE"
grep -q "^### Behavior" "$PATTERNS_FILE"
grep -q "^### Root Cause" "$PATTERNS_FILE"
grep -q "^### Detection Indicators" "$PATTERNS_FILE"
grep -q "^\\*\\*For User:\\*\\*" "$PATTERNS_FILE"
grep -q "^\\*\\*For Claude" "$PATTERNS_FILE"
grep -q "^### Prevention Strategy" "$PATTERNS_FILE"
grep -q "^### Metrics" "$PATTERNS_FILE"
grep -q "^### Related RCAs" "$PATTERNS_FILE"
grep -q "^## Pattern Index" "$PATTERNS_FILE"
grep -q "^## Adding New Patterns" "$PATTERNS_FILE"
```

**Expected Result:** FAIL (structure not present)

### Test AC-3: PATTERN-001 Specifically Documented

**File:** test-ac3-pattern-001-documented.sh
**Validation Points:**
1. PATTERN-001 section exists
2. Pattern name is "Premature Workflow Completion"
3. RCA-009 is referenced as first identification
4. RCA-013 is referenced in recurrences
5. RCA-018 is referenced in recurrences
6. Behavior mentions "completes early phases but skips late phases"
7. Root cause mentions "Missing enforcement for administrative phases"
8. CLI validation gates are mentioned in prevention
9. TodoWrite integration mentioned in solution
10. All story references are accurate (STORY-027, STORY-057, STORY-078)

**Grep Patterns:**
```bash
grep -q "^## PATTERN-001:" "$PATTERNS_FILE"
grep -q "Premature Workflow Completion" "$PATTERNS_FILE"
grep -q "RCA-009" "$PATTERNS_FILE"
grep -q "RCA-013" "$PATTERNS_FILE"
grep -q "RCA-018" "$PATTERNS_FILE"
grep -q "completes.*early phases.*skips late phases" "$PATTERNS_FILE"
grep -q "Missing enforcement for.*administrative phases" "$PATTERNS_FILE"
```

**Expected Result:** FAIL (content not present)

### Test AC-4: Detection Indicators for User and Claude

**File:** test-ac4-detection-indicators.sh
**Validation Points:**
1. "Detection Indicators" section exists
2. "For User:" subsection present
3. "For Claude (self-detection):" subsection present
4. User indicators include:
   - "Workflow displays \"COMPLETE\" but todo list shows pending phases"
   - "Story file not updated"
   - "No git commit"
5. Claude indicators include:
   - "About to display \"Workflow Complete\" banner"
   - "TodoWrite shows <10 phases completed"
   - "Run self-check before declaring complete"

**Grep Patterns:**
```bash
grep -q "^### Detection Indicators" "$PATTERNS_FILE"
grep -q "^\\*\\*For User:\\*\\*" "$PATTERNS_FILE"
grep -q "^\\*\\*For Claude" "$PATTERNS_FILE"
grep -q "Workflow displays.*COMPLETE.*todo list shows pending" "$PATTERNS_FILE"
grep -q "Story file not updated" "$PATTERNS_FILE"
grep -q "No git commit" "$PATTERNS_FILE"
grep -q "About to display.*Workflow Complete.*banner" "$PATTERNS_FILE"
```

**Expected Result:** FAIL (sections not present)

### Test AC-5: Related RCAs Cross-Referenced

**File:** test-ac5-rca-cross-references.sh
**Validation Points:**
1. "Related RCAs" section with table format exists
2. RCA-009 present with date 2025-11-14 and STORY-027
3. RCA-011 present with date 2025-11-19 and STORY-044
4. RCA-013 present with date 2025-11-22 and STORY-057
5. RCA-018 present with date 2025-12-05 and STORY-078
6. Relationship descriptions present:
   - RCA-009: "First identification"
   - RCA-011: "Phase 1 Step 4 specific"
   - RCA-013: "Late-phase pattern (4.5-7)"
   - RCA-018: "Comprehensive analysis"

**Grep Patterns:**
```bash
grep -q "^### Related RCAs" "$PATTERNS_FILE"
grep -q "RCA-009.*2025-11-14.*STORY-027" "$PATTERNS_FILE"
grep -q "RCA-011.*2025-11-19.*STORY-044" "$PATTERNS_FILE"
grep -q "RCA-013.*2025-11-22.*STORY-057" "$PATTERNS_FILE"
grep -q "RCA-018.*2025-12-05.*STORY-078" "$PATTERNS_FILE"
grep -q "First identification" "$PATTERNS_FILE"
grep -q "Phase 1.*specific" "$PATTERNS_FILE"
grep -q "Late-phase.*4.5-7" "$PATTERNS_FILE"
grep -q "Comprehensive analysis" "$PATTERNS_FILE"
```

**Expected Result:** FAIL (table not present)

## Test Output Format

Each test will follow bash testing pattern from STORY-041:

```bash
#!/bin/bash
set -e

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TEST_NAME="AC#X: [Test Description]"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Helper functions
assert_file_exists() { ... }
assert_contains() { ... }
assert_pattern_matches() { ... }

# Test execution
assert_file_exists "$PATTERNS_FILE" "PATTERNS.md exists"
assert_contains "$PATTERNS_FILE" "PATTERN-001" "Pattern ID present"

# Summary
echo ""
echo "====== Test Results ======"
echo "Tests run:   $TESTS_RUN"
echo "Passed:      $TESTS_PASSED"
echo "Failed:      $TESTS_FAILED"

if [ "$TESTS_FAILED" -eq 0 ]; then
    exit 0
else
    exit 1
fi
```

## Helper Functions Template

```bash
# Check file exists
assert_file_exists() {
    local file="$1"
    local description="$2"
    ((TESTS_RUN++))

    if [ -f "$file" ] && [ -s "$file" ]; then
        echo -e "${GREEN}✓ PASS${NC}: $description"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: $description"
        ((TESTS_FAILED++))
        return 1
    fi
}

# Check grep pattern exists
assert_contains() {
    local file="$1"
    local pattern="$2"
    local description="$3"
    ((TESTS_RUN++))

    if grep -q "$pattern" "$file" 2>/dev/null; then
        echo -e "${GREEN}✓ PASS${NC}: $description"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  Pattern not found: $pattern"
        ((TESTS_FAILED++))
        return 1
    fi
}
```

## Test Runner (run-all-tests.sh)

Orchestrates all AC tests and provides summary:

```bash
#!/bin/bash

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TESTS_DIR="devforgeai/tests/STORY-210"

echo "Running STORY-210 Validation Tests..."
echo ""

TOTAL_PASSED=0
TOTAL_FAILED=0

for test_file in "$TESTS_DIR"/test-ac*.sh; do
    echo "Running $(basename "$test_file")..."
    bash "$test_file"
    STATUS=$?

    if [ $STATUS -eq 0 ]; then
        ((TOTAL_PASSED++))
    else
        ((TOTAL_FAILED++))
    fi
done

echo ""
echo "====== Test Suite Summary ======"
echo "Test files: 5"
echo "Passed: $TOTAL_PASSED"
echo "Failed: $TOTAL_FAILED"

exit $TOTAL_FAILED
```

## Implementation Checklist

- [ ] Create test directory: devforgeai/tests/STORY-210/
- [ ] Generate test-ac1-file-exists.sh
- [ ] Generate test-ac2-template-structure.sh
- [ ] Generate test-ac3-pattern-001-documented.sh
- [ ] Generate test-ac4-detection-indicators.sh
- [ ] Generate test-ac5-rca-cross-references.sh
- [ ] Generate run-all-tests.sh orchestrator
- [ ] Verify all tests FAIL (Red Phase) - file doesn't exist yet
- [ ] Document test patterns in this plan file
- [ ] Ensure shell scripts use LF line endings (WSL compatibility)

## Line Ending Normalization

All generated `.sh` files MUST use LF line endings for WSL compatibility. After generation, verify with:

```bash
file devforgeai/tests/STORY-210/*.sh
# Should show "with LF line terminators" not CRLF
```

If CRLF detected, normalize via Edit tool:

```python
Edit(
    file_path="devforgeai/tests/STORY-210/test-ac1-file-exists.sh",
    old_string="\r\n",
    new_string="\n",
    replace_all=true
)
```

## Progress Tracking

### Phase 1: Test Generation (CURRENT)
- [ ] All 5 AC tests generated
- [ ] All tests FAIL initially (TDD Red)
- [ ] Run-all-tests.sh orchestrator created

### Phase 2: Pattern Implementation
- [ ] PATTERNS.md file created by implementation
- [ ] All tests GREEN after implementation
- [ ] Story marked "Dev Complete"

### Phase 3: QA Validation
- [ ] QA runs tests to validate implementation
- [ ] Coverage validation passes
- [ ] Story approved for release

## References

- **Story File:** /mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-210-rca-018-patterns-knowledge-base.story.md
- **Test Pattern Reference:** /mnt/c/Projects/DevForgeAI2/devforgeai/tests/STORY-041/test-ac1-directory-structure.sh
- **Source Tree Constraint:** devforgeai/specs/context/source-tree.md lines 436
- **Tech Stack:** devforgeai/specs/context/tech-stack.md (Bash for validation)

## Notes

- Tests are **non-executable** - They validate structure, not runtime behavior
- Tests are **destructive proof** - FAIL initially to prove tests are real (TDD Red)
- Pattern: File existence → Template structure → Specific content → Section separation → Cross-references
- All tests should execute in <5 seconds total
- Pattern follows STORY-041 bash test conventions for consistency
