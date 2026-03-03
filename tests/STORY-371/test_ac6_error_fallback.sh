#!/usr/bin/env bash
# =============================================================================
# STORY-371 AC#6: Error Handling for Unavailable Treelint
# =============================================================================
# Validates that code-quality-auditor.md documents:
#   1. Fallback logic when Treelint not installed (exit code 127)
#   2. Fallback to radon for Python
#   3. Fallback to eslint for JS/TS
#   4. Warning log with fallback reason
#   5. Workflow continues (no HALT) on Treelint failure
#   6. Final report complete even without Treelint
#   7. Unsupported file type handling
#
# TDD Phase: RED - Target file does not contain Treelint fallback logic.
# =============================================================================

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/mnt/c/Projects/DevForgeAI2}"
TARGET_FILE="${PROJECT_ROOT}/src/claude/agents/code-quality-auditor.md"

PASS_COUNT=0
FAIL_COUNT=0
TOTAL_COUNT=0

pass() {
    PASS_COUNT=$((PASS_COUNT + 1))
    TOTAL_COUNT=$((TOTAL_COUNT + 1))
    echo "  PASS: $1"
}

fail() {
    FAIL_COUNT=$((FAIL_COUNT + 1))
    TOTAL_COUNT=$((TOTAL_COUNT + 1))
    echo "  FAIL: $1"
}

echo "=============================================="
echo "  AC#6: Error Handling and Fallback"
echo "=============================================="
echo ""

# -----------------------------------------------------------------------------
# Test 1: Target file exists
# -----------------------------------------------------------------------------
echo "--- Test 1: File Existence ---"
if [[ -r "$TARGET_FILE" ]]; then
    pass "code-quality-auditor.md exists"
else
    fail "code-quality-auditor.md not found"
    echo ""
    echo "=============================================="
    echo "  AC#6 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
    echo "=============================================="
    echo "  STATUS: FAILED"
    exit 1
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: Documents Treelint fallback logic
# -----------------------------------------------------------------------------
echo "--- Test 2: Treelint Fallback Logic ---"
if grep -qiE 'treelint.*fallback|fallback.*treelint|treelint.*unavailable.*fall|treelint.*not.*installed.*fall' "$TARGET_FILE" 2>/dev/null; then
    pass "Documents Treelint fallback logic"
else
    fail "Missing Treelint fallback logic documentation"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: Fallback to radon for Python
# -----------------------------------------------------------------------------
echo "--- Test 3: Radon Fallback for Python ---"
if grep -qiE 'fallback.*radon|radon.*fallback|python.*radon.*fallback|radon.*python' "$TARGET_FILE" 2>/dev/null; then
    pass "Documents radon fallback for Python"
else
    fail "Missing radon fallback for Python documentation"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: Fallback to eslint for JS/TS
# -----------------------------------------------------------------------------
echo "--- Test 4: ESLint Fallback for JS/TS ---"
if grep -qiE 'fallback.*eslint|eslint.*fallback|javascript.*eslint.*fallback|eslint.*js' "$TARGET_FILE" 2>/dev/null; then
    pass "Documents eslint fallback for JS/TS"
else
    fail "Missing eslint fallback for JS/TS documentation"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: Warning log with fallback reason
# -----------------------------------------------------------------------------
echo "--- Test 5: Warning Log with Reason ---"
if grep -qiE 'warning.*fallback.*reason|log.*warning.*fallback|warn.*treelint.*reason|warning.*reason' "$TARGET_FILE" 2>/dev/null; then
    pass "Documents warning log with fallback reason"
else
    fail "Missing warning log with fallback reason documentation"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 6: No HALT on Treelint failure (workflow continues)
# -----------------------------------------------------------------------------
echo "--- Test 6: No HALT on Treelint Failure ---"
if grep -qiE 'without.*halt|no.*halt.*treelint|continue.*without.*treelint|does not.*halt|workflow.*continue' "$TARGET_FILE" 2>/dev/null; then
    pass "Documents workflow continues without halting on Treelint failure"
else
    fail "Missing no-halt documentation for Treelint failure"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 7: Final report complete without Treelint
# -----------------------------------------------------------------------------
echo "--- Test 7: Complete Report Without Treelint ---"
if grep -qiE 'report.*complete.*without|complete.*report.*fallback|all.*metrics.*sections|report.*still.*contain' "$TARGET_FILE" 2>/dev/null; then
    pass "Documents report completeness without Treelint"
else
    fail "Missing report completeness without Treelint documentation"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 8: Unsupported file type handling
# -----------------------------------------------------------------------------
echo "--- Test 8: Unsupported File Type Handling ---"
if grep -qiE 'unsupported.*file|unsupported.*language|file.*not.*supported|skip.*unsupported' "$TARGET_FILE" 2>/dev/null; then
    pass "Documents unsupported file type handling"
else
    fail "Missing unsupported file type handling documentation"
fi
echo ""

# =============================================================================
# Summary
# =============================================================================
echo "=============================================="
echo "  AC#6 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
echo "=============================================="

if [[ "$FAIL_COUNT" -gt 0 ]]; then
    echo "  STATUS: FAILED"
    exit 1
else
    echo "  STATUS: PASSED"
    exit 0
fi
