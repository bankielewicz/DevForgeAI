#!/bin/bash
# =============================================================================
# STORY-268 AC#3: tdd-refactor-phase.md contains Step 6 for AC Checklist update
# =============================================================================
# Status: SHOULD FAIL (NEEDS IMPLEMENTATION - only has checkpoint mention)

TEST_FILE=".claude/skills/devforgeai-development/references/tdd-refactor-phase.md"
TEST_PASSED=0
TEST_FAILED=0

echo "=========================================="
echo "STORY-268 AC#3: tdd-refactor-phase.md Step 6"
echo "=========================================="
echo ""

echo "[Test 3.1] Step 6 DEDICATED SECTION exists for AC Checklist update..."
if grep -qE "^### Step 6.*Update AC.*Checklist" "$TEST_FILE" 2>/dev/null || \
   grep -qE "^### Step 6.*AC Verification Checklist" "$TEST_FILE" 2>/dev/null; then
    echo "  PASS: Step 6 dedicated section header found"
    TEST_PASSED=$((TEST_PASSED + 1))
else
    echo "  FAIL: Step 6 DEDICATED SECTION NOT found"
    echo "  Expected: '### Step 6: Update AC Verification Checklist' as section header"
    TEST_FAILED=$((TEST_FAILED + 1))
fi

echo "[Test 3.2] Reference to ac-checklist-update-workflow.md in Step 6 context..."
if grep -q "ac-checklist-update-workflow.md" "$TEST_FILE" 2>/dev/null; then
    echo "  PASS: Reference to ac-checklist-update-workflow.md found"
    TEST_PASSED=$((TEST_PASSED + 1))
else
    echo "  FAIL: No reference to ac-checklist-update-workflow.md"
    TEST_FAILED=$((TEST_FAILED + 1))
fi

echo "[Test 3.3] Graceful skip logic (DoD-only tracking)..."
if grep -q "DoD-only tracking" "$TEST_FILE" 2>/dev/null || \
   grep -q "AC Checklist not present" "$TEST_FILE" 2>/dev/null; then
    echo "  PASS: Graceful skip text found"
    TEST_PASSED=$((TEST_PASSED + 1))
else
    echo "  FAIL: No graceful skip logic found"
    TEST_FAILED=$((TEST_FAILED + 1))
fi

echo "[Test 3.4] Progress display pattern (AC Progress)..."
if grep -q "AC Progress" "$TEST_FILE" 2>/dev/null; then
    echo "  PASS: AC Progress display pattern found"
    TEST_PASSED=$((TEST_PASSED + 1))
else
    echo "  FAIL: No AC Progress display pattern"
    TEST_FAILED=$((TEST_FAILED + 1))
fi

echo ""
echo "=========================================="
echo "AC#3 Test Summary: Passed=$TEST_PASSED Failed=$TEST_FAILED"
echo "=========================================="

if [ $TEST_FAILED -gt 0 ]; then
    echo "RESULT: FAIL - Implementation needed for Step 6 section"
    exit 1
else
    echo "RESULT: PASS"
    exit 0
fi
