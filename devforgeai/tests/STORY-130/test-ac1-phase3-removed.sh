#!/bin/bash
# STORY-130 AC#1: Phase 3 Verification Code Removed from /ideate Command
# Tests that Phase 3 artifact verification code has been removed from ideate.md
# Expected: All grep patterns return NO matches after implementation

# Note: No set -e because we want to run all tests even if some fail

IDEATE_FILE=".claude/commands/ideate.md"
PASS_COUNT=0
FAIL_COUNT=0
TOTAL_TESTS=9

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  STORY-130 AC#1: Phase 3 Verification Code Removed"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Helper function for pattern checking
check_pattern_removed() {
    local pattern="$1"
    local description="$2"

    if grep -q "$pattern" "$IDEATE_FILE" 2>/dev/null; then
        echo "✗ FAIL: Pattern still found - $description"
        echo "        Pattern: '$pattern'"
        ((FAIL_COUNT++))
        return 1
    else
        echo "✓ PASS: Pattern removed - $description"
        ((PASS_COUNT++))
        return 0
    fi
}

# Test 1: Phase 3 header removed
check_pattern_removed "## Phase 3" "Phase 3 header"

# Test 2: Verify Skill Completion section removed
check_pattern_removed "Verify Skill Completion" "Verify Skill Completion section"

# Test 3: epic_files variable assignment removed
check_pattern_removed "epic_files =" "epic_files variable assignment"

# Test 4: req_files variable assignment removed
check_pattern_removed "req_files =" "req_files variable assignment"

# Test 5: len(epic_files) check removed
check_pattern_removed "len(epic_files)" "len(epic_files) check"

# Test 6: "artifacts not found" message removed
check_pattern_removed "artifacts not found" "artifacts not found message"

# Test 7: No validation CODE (grep for patterns that indicate validation LOGIC, not documentation)
# Looking for patterns like "validate_frontmatter" or "id field matches" which indicate actual validation code
if grep -q "validate_frontmatter\|id field matches filename" "$IDEATE_FILE" 2>/dev/null; then
    echo "✗ FAIL: Validation logic still found"
    ((FAIL_COUNT++))
else
    echo "✓ PASS: No validation logic (code) in command"
    ((PASS_COUNT++))
fi

# Test 8: No "expected artifacts" counting logic
if grep -q "Expected artifacts" "$IDEATE_FILE" 2>/dev/null; then
    echo "✗ FAIL: Artifact counting logic still found"
    ((FAIL_COUNT++))
else
    echo "✓ PASS: No artifact counting logic"
    ((PASS_COUNT++))
fi

# Test 9: No "3.1" or "3.2" subsections (Phase 3 subsections)
if grep -q "### 3\\.1\|### 3\\.2" "$IDEATE_FILE" 2>/dev/null; then
    echo "✗ FAIL: Phase 3 subsections still found"
    ((FAIL_COUNT++))
else
    echo "✓ PASS: Phase 3 subsections removed"
    ((PASS_COUNT++))
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Results: $PASS_COUNT/$TOTAL_TESTS passed"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ $FAIL_COUNT -gt 0 ]; then
    echo "  Status: FAILED ($FAIL_COUNT patterns still present)"
    exit 1
else
    echo "  Status: PASSED (all Phase 3 patterns removed)"
    exit 0
fi
