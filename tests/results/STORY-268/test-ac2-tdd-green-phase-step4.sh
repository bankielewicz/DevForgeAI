#!/bin/bash
# =============================================================================
# STORY-268 AC#2: tdd-green-phase.md contains Step 4 for AC Checklist update
# =============================================================================

TEST_FILE=".claude/skills/devforgeai-development/references/tdd-green-phase.md"
TEST_PASSED=0
TEST_FAILED=0

echo "=========================================="
echo "STORY-268 AC#2: tdd-green-phase.md Step 4"
echo "=========================================="
echo ""

echo "[Test 2.1] Step 4 header exists for AC Checklist update..."
if grep -q "### Step 4.*Update AC.*Checklist" "$TEST_FILE" 2>/dev/null || \
   grep -q "### Step 4.*AC Verification Checklist" "$TEST_FILE" 2>/dev/null; then
    echo "  PASS: Step 4 AC Checklist header found"
    TEST_PASSED=$((TEST_PASSED + 1))
else
    echo "  FAIL: Step 4 AC Checklist header NOT found"
    TEST_FAILED=$((TEST_FAILED + 1))
fi

echo "[Test 2.2] Reference to ac-checklist-update-workflow.md..."
if grep -q "ac-checklist-update-workflow.md" "$TEST_FILE" 2>/dev/null; then
    echo "  PASS: Reference to ac-checklist-update-workflow.md found"
    TEST_PASSED=$((TEST_PASSED + 1))
else
    echo "  FAIL: No reference to ac-checklist-update-workflow.md"
    TEST_FAILED=$((TEST_FAILED + 1))
fi

echo "[Test 2.3] Graceful skip logic (DoD-only tracking)..."
if grep -q "DoD-only tracking" "$TEST_FILE" 2>/dev/null || \
   grep -q "AC Checklist not present" "$TEST_FILE" 2>/dev/null; then
    echo "  PASS: Graceful skip text found"
    TEST_PASSED=$((TEST_PASSED + 1))
else
    echo "  FAIL: No graceful skip logic found"
    TEST_FAILED=$((TEST_FAILED + 1))
fi

echo "[Test 2.4] Progress display pattern (AC Progress)..."
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
echo "AC#2 Test Summary: Passed=$TEST_PASSED Failed=$TEST_FAILED"
echo "=========================================="

if [ $TEST_FAILED -gt 0 ]; then
    echo "RESULT: FAIL"
    exit 1
else
    echo "RESULT: PASS"
    exit 0
fi
