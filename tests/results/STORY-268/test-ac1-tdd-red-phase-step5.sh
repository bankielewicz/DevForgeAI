#!/bin/bash
# =============================================================================
# STORY-268 AC#1: tdd-red-phase.md contains Step 5 for AC Checklist update
# =============================================================================
# Status: SHOULD PASS (already implemented)
#
# Acceptance Criteria:
#   Given Phase 02 (Red Phase - Test Generation) completes successfully
#   When the workflow executes Step 5 (Update AC Checklist)
#   Then all AC items marked with **Phase:** 1 are validated and checked off
#   And progress summary displayed showing "AC Progress: X/Y"
# =============================================================================

# Note: Using explicit arithmetic to avoid set -e issues with ((var++))

TEST_FILE=".claude/skills/devforgeai-development/references/tdd-red-phase.md"
RESULTS_DIR="tests/results/STORY-268"
TEST_PASSED=0
TEST_FAILED=0

echo "=========================================="
echo "STORY-268 AC#1: tdd-red-phase.md Step 5"
echo "=========================================="
echo ""

# Test 1.1: Step 5 header exists
echo "[Test 1.1] Step 5 header exists in tdd-red-phase.md..."
if grep -q "### Step 5.*Update AC.*Checklist" "$TEST_FILE" 2>/dev/null || \
   grep -q "### Step 5.*AC Verification Checklist" "$TEST_FILE" 2>/dev/null; then
    echo "  PASS: Step 5 header found"
    TEST_PASSED=$((TEST_PASSED + 1))
else
    echo "  FAIL: Step 5 header NOT found"
    echo "  Expected pattern: '### Step 5.*AC.*Checklist'"
    TEST_FAILED=$((TEST_FAILED + 1))
fi

# Test 1.2: Reference to ac-checklist-update-workflow.md
echo "[Test 1.2] Reference to ac-checklist-update-workflow.md..."
if grep -q "ac-checklist-update-workflow.md" "$TEST_FILE" 2>/dev/null; then
    echo "  PASS: Reference to ac-checklist-update-workflow.md found"
    TEST_PASSED=$((TEST_PASSED + 1))
else
    echo "  FAIL: No reference to ac-checklist-update-workflow.md"
    echo "  Expected: Read() call to ac-checklist-update-workflow.md"
    TEST_FAILED=$((TEST_FAILED + 1))
fi

# Test 1.3: Graceful skip logic for stories without AC Checklist
echo "[Test 1.3] Graceful skip logic (DoD-only tracking)..."
if grep -q "DoD-only tracking" "$TEST_FILE" 2>/dev/null || \
   grep -q "AC Checklist not present" "$TEST_FILE" 2>/dev/null; then
    echo "  PASS: Graceful skip text found"
    TEST_PASSED=$((TEST_PASSED + 1))
else
    echo "  FAIL: No graceful skip logic found"
    echo "  Expected: 'DoD-only tracking' or 'AC Checklist not present'"
    TEST_FAILED=$((TEST_FAILED + 1))
fi

# Test 1.4: Progress display pattern
echo "[Test 1.4] Progress display pattern (AC Progress: X/Y)..."
if grep -q "AC Progress" "$TEST_FILE" 2>/dev/null; then
    echo "  PASS: AC Progress display pattern found"
    TEST_PASSED=$((TEST_PASSED + 1))
else
    echo "  FAIL: No AC Progress display pattern"
    echo "  Expected: 'AC Progress: X/Y items complete'"
    TEST_FAILED=$((TEST_FAILED + 1))
fi

# Test 1.5: Phase marker reference (Phase: 1)
echo "[Test 1.5] Phase marker reference for Phase 02 items..."
if grep -q "Phase.*: 1" "$TEST_FILE" 2>/dev/null || \
   grep -q "Phase 02" "$TEST_FILE" 2>/dev/null; then
    echo "  PASS: Phase marker reference found"
    TEST_PASSED=$((TEST_PASSED + 1))
else
    echo "  FAIL: No Phase marker reference for Phase 02 items"
    echo "  Expected: Reference to '**Phase:** 1' items"
    TEST_FAILED=$((TEST_FAILED + 1))
fi

echo ""
echo "=========================================="
echo "AC#1 Test Summary"
echo "=========================================="
echo "Passed: $TEST_PASSED"
echo "Failed: $TEST_FAILED"
echo ""

if [ $TEST_FAILED -gt 0 ]; then
    echo "RESULT: FAIL - AC#1 not fully satisfied"
    exit 1
else
    echo "RESULT: PASS - AC#1 fully satisfied"
    exit 0
fi
