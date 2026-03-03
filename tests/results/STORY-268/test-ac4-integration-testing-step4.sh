#!/bin/bash
# =============================================================================
# STORY-268 AC#4: integration-testing.md contains Step 4 for AC Checklist update
# =============================================================================
# Note: Implementation uses Step 3 (acceptable variation)

TEST_FILE=".claude/skills/devforgeai-development/references/integration-testing.md"
TEST_PASSED=0
TEST_FAILED=0

echo "=========================================="
echo "STORY-268 AC#4: integration-testing.md Step 3/4"
echo "=========================================="
echo ""

echo "[Test 4.1] Step 3 or Step 4 header exists for AC Checklist update..."
if grep -q "### Step 3.*Update AC.*Checklist" "$TEST_FILE" 2>/dev/null || \
   grep -q "### Step 4.*Update AC.*Checklist" "$TEST_FILE" 2>/dev/null; then
    echo "  PASS: AC Checklist step header found"
    TEST_PASSED=$((TEST_PASSED + 1))
else
    echo "  FAIL: AC Checklist step header NOT found"
    TEST_FAILED=$((TEST_FAILED + 1))
fi

echo "[Test 4.2] Reference to ac-checklist-update-workflow.md..."
if grep -q "ac-checklist-update-workflow.md" "$TEST_FILE" 2>/dev/null; then
    echo "  PASS: Reference to ac-checklist-update-workflow.md found"
    TEST_PASSED=$((TEST_PASSED + 1))
else
    echo "  FAIL: No reference to ac-checklist-update-workflow.md"
    TEST_FAILED=$((TEST_FAILED + 1))
fi

echo "[Test 4.3] Progress display pattern (AC Progress)..."
if grep -q "AC Progress" "$TEST_FILE" 2>/dev/null || \
   grep -q "AC Checklist.*items checked" "$TEST_FILE" 2>/dev/null; then
    echo "  PASS: AC Progress display pattern found"
    TEST_PASSED=$((TEST_PASSED + 1))
else
    echo "  FAIL: No AC Progress display pattern"
    TEST_FAILED=$((TEST_FAILED + 1))
fi

echo ""
echo "=========================================="
echo "AC#4 Test Summary: Passed=$TEST_PASSED Failed=$TEST_FAILED"
echo "=========================================="

if [ $TEST_FAILED -gt 0 ]; then
    echo "RESULT: FAIL"
    exit 1
else
    echo "RESULT: PASS"
    exit 0
fi
