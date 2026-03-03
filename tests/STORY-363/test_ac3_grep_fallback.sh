#!/usr/bin/env bash
# =============================================================================
# STORY-363 AC#3: Grep Fallback for Unsupported Languages
# =============================================================================
# Validates that test-automator.md contains:
#   1. A fallback section for when Treelint is unavailable or unsupported
#   2. Uses native Grep tool (Grep(pattern=...), NOT Bash grep)
#   3. Warning-level messaging (not error/HALT) on fallback
#   4. Distinction between empty results and command failure (BR-002)
#
# TDD Phase: RED - Tests expected to FAIL until implementation complete.
# =============================================================================

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/mnt/c/Projects/DevForgeAI2}"
TARGET_FILE="${PROJECT_ROOT}/src/claude/agents/test-automator.md"

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
echo "  AC#3: Grep Fallback for Unsupported Languages"
echo "=============================================="
echo ""

# -----------------------------------------------------------------------------
# Test 1: Target file exists
# -----------------------------------------------------------------------------
echo "--- Test 1: File Existence ---"
if [[ -r "$TARGET_FILE" ]]; then
    pass "test-automator.md exists and is readable"
else
    fail "test-automator.md not found"
    echo ""
    echo "=============================================="
    echo "  AC#3 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
    echo "=============================================="
    echo "  STATUS: FAILED"
    exit 1
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: Fallback section heading exists
# -----------------------------------------------------------------------------
echo "--- Test 2: Fallback Section Heading ---"
if grep -qiE '^#{1,4}.*(fallback|unsupported)' "$TARGET_FILE" 2>/dev/null; then
    pass "Fallback section heading found"
else
    fail "Missing fallback section heading (e.g., '### Fallback: Grep for Unsupported Languages')"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: Uses native Grep tool (not Bash grep)
# Must contain Grep(pattern= style invocation
# -----------------------------------------------------------------------------
echo "--- Test 3: Native Grep Tool Usage ---"
if grep -qE 'Grep\(pattern=' "$TARGET_FILE" 2>/dev/null; then
    pass "Uses native Grep tool (Grep(pattern=...)) for fallback"
else
    fail "Missing native Grep tool usage (must use Grep(pattern=...), not Bash grep)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: Warning-level messaging (not error/HALT)
# Must mention 'warning' in fallback context, must NOT use HALT for Treelint failures
# -----------------------------------------------------------------------------
echo "--- Test 4: Warning-Level Messaging ---"
if grep -qiE 'warning' "$TARGET_FILE" 2>/dev/null; then
    pass "Warning-level messaging present in fallback context"
else
    fail "Missing 'warning' level messaging for Treelint fallback"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: No HALT on Treelint failure (BR-003)
# The file should NOT instruct HALT when Treelint fails
# We check that there is no pattern like "Treelint...HALT" or "fallback...HALT"
# -----------------------------------------------------------------------------
echo "--- Test 5: No HALT on Treelint Failure (BR-003) ---"
# Search for HALT in proximity to treelint/fallback context
# The file should NOT contain instructions to HALT when Treelint fails
treelint_halt_found=false
if grep -iE 'treelint.*(HALT|halt|error.*block)' "$TARGET_FILE" 2>/dev/null | grep -qiv 'not.*halt\|no.*halt\|never.*halt\|without.*halt'; then
    treelint_halt_found=true
fi

if [[ "$treelint_halt_found" == "false" ]]; then
    pass "No HALT instruction on Treelint failure (BR-003 compliant)"
else
    fail "Found HALT instruction associated with Treelint failure (violates BR-003)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 6: Empty results vs command failure distinction (BR-002)
# Must document that exit code 0 with empty results is NOT a failure
# -----------------------------------------------------------------------------
echo "--- Test 6: Empty Results vs Failure Distinction (BR-002) ---"
if grep -qiE '(empty.*result|exit.code.0|zero.*match)' "$TARGET_FILE" 2>/dev/null; then
    pass "Documents distinction between empty results and command failure"
else
    fail "Missing documentation for empty results vs command failure distinction (BR-002)"
fi
echo ""

# =============================================================================
# Summary
# =============================================================================
echo "=============================================="
echo "  AC#3 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
echo "=============================================="

if [[ "$FAIL_COUNT" -gt 0 ]]; then
    echo "  STATUS: FAILED"
    exit 1
else
    echo "  STATUS: PASSED"
    exit 0
fi
