#!/bin/bash
# =============================================================================
# STORY-268 AC#5: phase-06-deferral-challenge.md contains Step 7 for AC Checklist
# =============================================================================
# Status: SHOULD FAIL (NEEDS IMPLEMENTATION - only has checkpoint mention)

TEST_FILE=".claude/skills/devforgeai-development/references/phase-06-deferral-challenge.md"
TEST_PASSED=0
TEST_FAILED=0

echo "=========================================="
echo "STORY-268 AC#5: phase-06-deferral-challenge.md"
echo "=========================================="
echo ""

echo "[Test 5.1] AC Checklist update section exists..."
# Look for any AC Checklist update section (Step 7, 8, or 9)
if grep -qE "^### Step [789].*Update AC.*Checklist" "$TEST_FILE" 2>/dev/null || \
   grep -qE "^### Step [789].*AC Verification Checklist" "$TEST_FILE" 2>/dev/null; then
    echo "  PASS: AC Checklist section found"
    TEST_PASSED=$((TEST_PASSED + 1))
else
    echo "  FAIL: No AC Checklist update section found"
    echo "  Expected: Step 7, 8, or 9 with AC Checklist update"
    TEST_FAILED=$((TEST_FAILED + 1))
fi

echo "[Test 5.2] Reference to ac-checklist-update-workflow.md..."
if grep -q "ac-checklist-update-workflow.md" "$TEST_FILE" 2>/dev/null; then
    echo "  PASS: Reference to ac-checklist-update-workflow.md found"
    TEST_PASSED=$((TEST_PASSED + 1))
else
    echo "  FAIL: No reference to ac-checklist-update-workflow.md"
    TEST_FAILED=$((TEST_FAILED + 1))
fi

echo "[Test 5.3] Graceful skip logic (DoD-only tracking)..."
if grep -q "DoD-only tracking" "$TEST_FILE" 2>/dev/null || \
   grep -q "AC Checklist not present" "$TEST_FILE" 2>/dev/null; then
    echo "  PASS: Graceful skip text found"
    TEST_PASSED=$((TEST_PASSED + 1))
else
    echo "  FAIL: No graceful skip logic found"
    TEST_FAILED=$((TEST_FAILED + 1))
fi

echo "[Test 5.4] Progress display pattern (AC Progress)..."
if grep -q "AC Progress" "$TEST_FILE" 2>/dev/null; then
    echo "  PASS: AC Progress display pattern found"
    TEST_PASSED=$((TEST_PASSED + 1))
else
    echo "  FAIL: No AC Progress display pattern"
    TEST_FAILED=$((TEST_FAILED + 1))
fi

echo ""
echo "=========================================="
echo "AC#5 Test Summary: Passed=$TEST_PASSED Failed=$TEST_FAILED"
echo "=========================================="

if [ $TEST_FAILED -gt 0 ]; then
    echo "RESULT: FAIL - Implementation needed for AC Checklist section"
    exit 1
else
    echo "RESULT: PASS"
    exit 0
fi
