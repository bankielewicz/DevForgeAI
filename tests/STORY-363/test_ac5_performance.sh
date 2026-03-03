#!/usr/bin/env bash
# =============================================================================
# STORY-363 AC#5: Performance Validation for Treelint Searches
# =============================================================================
# Validates that test-automator.md contains:
#   1. Performance target (<100ms) documented
#   2. Reference to stats.elapsed_ms field in Treelint JSON output
#   3. Total discovery overhead target (<200ms) documented
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
echo "  AC#5: Performance Validation"
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
    echo "  AC#5 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
    echo "=============================================="
    echo "  STATUS: FAILED"
    exit 1
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: Performance target (<100ms) documented
# -----------------------------------------------------------------------------
echo "--- Test 2: Performance Target Documented ---"
if grep -qE '(100.*ms|100ms|< ?100|under 100)' "$TARGET_FILE" 2>/dev/null; then
    pass "Performance target (<100ms) documented"
else
    fail "Missing performance target (<100ms) in Treelint search instructions"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: stats.elapsed_ms field referenced
# -----------------------------------------------------------------------------
echo "--- Test 3: stats.elapsed_ms Field Referenced ---"
if grep -qE 'stats\.elapsed_ms|elapsed_ms' "$TARGET_FILE" 2>/dev/null; then
    pass "stats.elapsed_ms field referenced for performance verification"
else
    fail "Missing stats.elapsed_ms field reference (required for performance validation)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: Total overhead target mentioned
# -----------------------------------------------------------------------------
echo "--- Test 4: Total Discovery Overhead Target ---"
if grep -qE '(200.*ms|200ms|overhead|total.*latency)' "$TARGET_FILE" 2>/dev/null; then
    pass "Total discovery overhead target documented"
else
    fail "Missing total discovery overhead target (<200ms per AC#5)"
fi
echo ""

# =============================================================================
# Summary
# =============================================================================
echo "=============================================="
echo "  AC#5 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
echo "=============================================="

if [[ "$FAIL_COUNT" -gt 0 ]]; then
    echo "  STATUS: FAILED"
    exit 1
else
    echo "  STATUS: PASSED"
    exit 0
fi
