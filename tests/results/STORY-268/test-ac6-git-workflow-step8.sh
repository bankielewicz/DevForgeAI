#!/bin/bash
# =============================================================================
# STORY-268 AC#6: git-workflow-conventions.md contains AC Checklist section
# =============================================================================

TEST_FILE=".claude/skills/devforgeai-development/references/git-workflow-conventions.md"
TEST_PASSED=0
TEST_FAILED=0

echo "=========================================="
echo "STORY-268 AC#6: git-workflow-conventions.md"
echo "=========================================="
echo ""

echo "[Test 6.1] AC Verification Checklist section exists..."
if grep -q "## AC Verification Checklist Updates" "$TEST_FILE" 2>/dev/null || \
   grep -q "### Step 8.*Update AC.*Checklist" "$TEST_FILE" 2>/dev/null; then
    echo "  PASS: AC Checklist section header found"
    TEST_PASSED=$((TEST_PASSED + 1))
else
    echo "  FAIL: AC Checklist section header NOT found"
    TEST_FAILED=$((TEST_FAILED + 1))
fi

echo "[Test 6.2] Reference to ac-checklist-update-workflow.md..."
if grep -q "ac-checklist-update-workflow.md" "$TEST_FILE" 2>/dev/null; then
    echo "  PASS: Reference to ac-checklist-update-workflow.md found"
    TEST_PASSED=$((TEST_PASSED + 1))
else
    echo "  FAIL: No reference to ac-checklist-update-workflow.md"
    TEST_FAILED=$((TEST_FAILED + 1))
fi

echo "[Test 6.3] Progress display pattern..."
if grep -q "AC Progress" "$TEST_FILE" 2>/dev/null || \
   grep -q "100%" "$TEST_FILE" 2>/dev/null || \
   grep -q "items checked" "$TEST_FILE" 2>/dev/null; then
    echo "  PASS: Progress display pattern found"
    TEST_PASSED=$((TEST_PASSED + 1))
else
    echo "  FAIL: No progress display pattern"
    TEST_FAILED=$((TEST_FAILED + 1))
fi

echo ""
echo "=========================================="
echo "AC#6 Test Summary: Passed=$TEST_PASSED Failed=$TEST_FAILED"
echo "=========================================="

if [ $TEST_FAILED -gt 0 ]; then
    echo "RESULT: FAIL"
    exit 1
else
    echo "RESULT: PASS"
    exit 0
fi
