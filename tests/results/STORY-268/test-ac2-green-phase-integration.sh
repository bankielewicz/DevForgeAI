#!/usr/bin/env bash
# Test: AC#2 - tdd-green-phase.md Integration (Phase 03)
# Story: STORY-268 - Integrate AC Verification Checklist Real-Time Updates
# Phase: TDD Red (Test Generation)
# Pattern: AAA (Arrange-Act-Assert)

set -e

# ============================================================================
# TEST CONFIGURATION
# ============================================================================
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TARGET_FILE="${PROJECT_ROOT}/.claude/skills/devforgeai-development/references/tdd-green-phase.md"
TEST_NAME="AC#2: tdd-green-phase.md contains Step 4 for AC Checklist update"
PASS_COUNT=0
FAIL_COUNT=0

# ============================================================================
# TEST HELPERS
# ============================================================================
pass() {
    echo "[PASS] $1"
    ((PASS_COUNT++))
}

fail() {
    echo "[FAIL] $1"
    ((FAIL_COUNT++))
}

# ============================================================================
# ARRANGE: Verify target file exists
# ============================================================================
echo ""
echo "=========================================="
echo "TEST: ${TEST_NAME}"
echo "=========================================="
echo ""
echo "[ARRANGE] Verifying target file exists..."

if [[ ! -f "${TARGET_FILE}" ]]; then
    fail "Target file does not exist: ${TARGET_FILE}"
    echo ""
    echo "SUMMARY: 0 passed, 1 failed"
    exit 1
fi

echo "[ARRANGE] Target file exists: ${TARGET_FILE}"
echo ""

# ============================================================================
# ACT & ASSERT: Test 1 - Step 4 header exists for AC Checklist
# ============================================================================
echo "[ACT] Testing: Step 4 header exists for AC Checklist update..."

# Note: Step 4 exists but may have different naming - looking for AC Checklist mention
if grep -qE "^### Step 4:.*AC.*Checklist" "${TARGET_FILE}" 2>/dev/null || \
   grep -qE "^### Step 4:.*AC Verification Checklist" "${TARGET_FILE}" 2>/dev/null; then
    pass "Step 4 header exists with AC Checklist mention"
else
    fail "Step 4 header missing or does not mention AC Checklist"
fi

# ============================================================================
# ACT & ASSERT: Test 2 - Reference to ac-checklist-update-workflow.md
# ============================================================================
echo "[ACT] Testing: Reference to ac-checklist-update-workflow.md exists..."

if grep -q "ac-checklist-update-workflow.md" "${TARGET_FILE}" 2>/dev/null; then
    pass "Reference to ac-checklist-update-workflow.md found"
else
    fail "Missing reference to ac-checklist-update-workflow.md"
fi

# ============================================================================
# ACT & ASSERT: Test 3 - Read() call to workflow file
# ============================================================================
echo "[ACT] Testing: Read() call to ac-checklist-update-workflow.md..."

if grep -qE 'Read\(.*ac-checklist-update-workflow' "${TARGET_FILE}" 2>/dev/null; then
    pass "Read() call to ac-checklist-update-workflow.md found"
else
    fail "Missing Read() call to ac-checklist-update-workflow.md"
fi

# ============================================================================
# ACT & ASSERT: Test 4 - Graceful skip logic (DoD-only tracking)
# ============================================================================
echo "[ACT] Testing: Graceful skip logic for stories without AC Checklist..."

if grep -q "DoD-only tracking" "${TARGET_FILE}" 2>/dev/null; then
    pass "Graceful skip text 'DoD-only tracking' found"
else
    fail "Missing graceful skip text 'DoD-only tracking'"
fi

# ============================================================================
# ACT & ASSERT: Test 5 - Progress display pattern
# ============================================================================
echo "[ACT] Testing: Progress display pattern with 'AC Progress'..."

if grep -q "AC Progress" "${TARGET_FILE}" 2>/dev/null; then
    pass "Progress display pattern 'AC Progress' found"
else
    fail "Missing progress display pattern 'AC Progress'"
fi

# ============================================================================
# ACT & ASSERT: Test 6 - Phase marker reference (Phase: 2)
# ============================================================================
echo "[ACT] Testing: Phase marker reference for Phase 03 items..."

if grep -qE "Phase.*:.*2" "${TARGET_FILE}" 2>/dev/null; then
    pass "Phase marker reference (Phase: 2) found"
else
    fail "Missing Phase marker reference for Phase 03 (Phase: 2)"
fi

# ============================================================================
# ACT & ASSERT: Test 7 - Grep pattern for identifying AC items
# ============================================================================
echo "[ACT] Testing: Grep pattern for identifying Phase 03 AC items..."

if grep -qE 'Grep\(.*pattern.*Phase' "${TARGET_FILE}" 2>/dev/null; then
    pass "Grep pattern for identifying Phase AC items found"
else
    fail "Missing Grep pattern for identifying Phase AC items"
fi

# ============================================================================
# ACT & ASSERT: Test 8 - Implementation metrics mentioned
# ============================================================================
echo "[ACT] Testing: Implementation metrics mentioned (code written, business logic)..."

if grep -qEi "(implementation|code written|business logic)" "${TARGET_FILE}" 2>/dev/null; then
    pass "Implementation metrics mentioned in Phase 03 AC items"
else
    fail "Missing implementation metrics in Phase 03 AC items"
fi

# ============================================================================
# SUMMARY
# ============================================================================
echo ""
echo "=========================================="
echo "TEST SUMMARY: ${TEST_NAME}"
echo "=========================================="
echo "Passed: ${PASS_COUNT}"
echo "Failed: ${FAIL_COUNT}"
echo ""

if [[ ${FAIL_COUNT} -gt 0 ]]; then
    echo "RESULT: FAILED (${FAIL_COUNT} tests failed)"
    exit 1
else
    echo "RESULT: PASSED (all ${PASS_COUNT} tests passed)"
    exit 0
fi
