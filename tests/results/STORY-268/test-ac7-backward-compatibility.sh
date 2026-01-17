#!/bin/bash
# =============================================================================
# STORY-268 AC#7: Backward Compatibility with Stories Without AC Checklist
# =============================================================================

REFS_DIR=".claude/skills/devforgeai-development/references"
WORKFLOW_FILE="$REFS_DIR/ac-checklist-update-workflow.md"
TEST_PASSED=0
TEST_FAILED=0

echo "=========================================="
echo "STORY-268 AC#7: Backward Compatibility"
echo "=========================================="
echo ""

echo "[Test 7.1] ac-checklist-update-workflow.md has graceful skip section..."
if grep -q "DoD-only tracking" "$WORKFLOW_FILE" 2>/dev/null; then
    echo "  PASS: Graceful skip text found in workflow"
    TEST_PASSED=$((TEST_PASSED + 1))
else
    echo "  FAIL: No 'DoD-only tracking' in workflow"
    TEST_FAILED=$((TEST_FAILED + 1))
fi

echo "[Test 7.2] Workflow has Backward Compatibility section..."
if grep -q "## Backward Compatibility" "$WORKFLOW_FILE" 2>/dev/null; then
    echo "  PASS: Backward Compatibility section found"
    TEST_PASSED=$((TEST_PASSED + 1))
else
    echo "  FAIL: No Backward Compatibility section"
    TEST_FAILED=$((TEST_FAILED + 1))
fi

echo "[Test 7.3] Workflow has error handling for missing checklist..."
if grep -q "checklist section not found" "$WORKFLOW_FILE" 2>/dev/null || \
   grep -q "AC Checklist not present" "$WORKFLOW_FILE" 2>/dev/null; then
    echo "  PASS: Missing checklist error handling found"
    TEST_PASSED=$((TEST_PASSED + 1))
else
    echo "  FAIL: No error handling for missing checklist"
    TEST_FAILED=$((TEST_FAILED + 1))
fi

echo "[Test 7.4] Phase files reference workflow for inherited behavior..."
REF_COUNT=0
for file in tdd-red-phase.md tdd-green-phase.md integration-testing.md git-workflow-conventions.md; do
    if grep -q "ac-checklist-update-workflow.md" "$REFS_DIR/$file" 2>/dev/null; then
        REF_COUNT=$((REF_COUNT + 1))
    fi
done
if [ $REF_COUNT -ge 3 ]; then
    echo "  PASS: $REF_COUNT/4 files reference workflow"
    TEST_PASSED=$((TEST_PASSED + 1))
else
    echo "  FAIL: Only $REF_COUNT/4 files reference workflow"
    TEST_FAILED=$((TEST_FAILED + 1))
fi

echo ""
echo "=========================================="
echo "AC#7 Test Summary: Passed=$TEST_PASSED Failed=$TEST_FAILED"
echo "=========================================="

if [ $TEST_FAILED -gt 0 ]; then
    echo "RESULT: FAIL"
    exit 1
else
    echo "RESULT: PASS"
    exit 0
fi
