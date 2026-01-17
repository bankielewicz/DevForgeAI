#!/bin/bash
# =============================================================================
# STORY-268 AC#8: Progress Display with Running Total
# =============================================================================

REFS_DIR=".claude/skills/devforgeai-development/references"
WORKFLOW_FILE="$REFS_DIR/ac-checklist-update-workflow.md"
TEST_PASSED=0
TEST_FAILED=0

echo "=========================================="
echo "STORY-268 AC#8: Progress Display"
echo "=========================================="
echo ""

echo "[Test 8.1] Workflow defines progress display format..."
if grep -q "AC Progress" "$WORKFLOW_FILE" 2>/dev/null && \
   grep -q "items complete" "$WORKFLOW_FILE" 2>/dev/null; then
    echo "  PASS: Progress display format defined"
    TEST_PASSED=$((TEST_PASSED + 1))
else
    echo "  FAIL: Progress display format not fully defined"
    TEST_FAILED=$((TEST_FAILED + 1))
fi

echo "[Test 8.2] Workflow includes percentage display..."
if grep -q "percentage" "$WORKFLOW_FILE" 2>/dev/null || \
   grep -q "%" "$WORKFLOW_FILE" 2>/dev/null; then
    echo "  PASS: Percentage display found"
    TEST_PASSED=$((TEST_PASSED + 1))
else
    echo "  FAIL: No percentage display"
    TEST_FAILED=$((TEST_FAILED + 1))
fi

echo "[Test 8.3] tdd-red-phase.md has progress display..."
if grep -q "AC Progress" "$REFS_DIR/tdd-red-phase.md" 2>/dev/null; then
    echo "  PASS: Progress display found in tdd-red-phase.md"
    TEST_PASSED=$((TEST_PASSED + 1))
else
    echo "  FAIL: No progress display in tdd-red-phase.md"
    TEST_FAILED=$((TEST_FAILED + 1))
fi

echo "[Test 8.4] git-workflow-conventions.md has final summary..."
if grep -q "AC Verification Checklist Complete" "$REFS_DIR/git-workflow-conventions.md" 2>/dev/null || \
   grep -q "100%" "$REFS_DIR/git-workflow-conventions.md" 2>/dev/null; then
    echo "  PASS: Final summary found"
    TEST_PASSED=$((TEST_PASSED + 1))
else
    echo "  FAIL: No final summary"
    TEST_FAILED=$((TEST_FAILED + 1))
fi

echo ""
echo "=========================================="
echo "AC#8 Test Summary: Passed=$TEST_PASSED Failed=$TEST_FAILED"
echo "=========================================="

if [ $TEST_FAILED -gt 0 ]; then
    echo "RESULT: FAIL"
    exit 1
else
    echo "RESULT: PASS"
    exit 0
fi
