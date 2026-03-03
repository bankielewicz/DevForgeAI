#!/usr/bin/env bash
# =============================================================================
# STORY-371 AC#3: Metrics Compared Against Configurable Thresholds
# =============================================================================
# Validates that code-quality-auditor.md documents:
#   1. Loading thresholds from quality-metrics.md
#   2. Three classification levels: ACCEPTABLE, WARNING, CRITICAL
#   3. Method max 100 lines threshold reference
#   4. Complexity max 10 threshold reference
#   5. Default threshold fallback when config missing (BR-002)
#   6. Classification logic (threshold comparison rules)
#
# TDD Phase: RED - Target file does not contain Treelint threshold classification.
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
echo "  AC#3: Threshold Classification"
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
    echo "  AC#3 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
    echo "=============================================="
    echo "  STATUS: FAILED"
    exit 1
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: References quality-metrics.md for thresholds
# -----------------------------------------------------------------------------
echo "--- Test 2: Quality Metrics Reference ---"
if grep -q 'quality-metrics.md' "$TARGET_FILE" 2>/dev/null; then
    pass "References quality-metrics.md for threshold loading"
else
    fail "Missing reference to quality-metrics.md"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: Documents ACCEPTABLE classification level
# -----------------------------------------------------------------------------
echo "--- Test 3: ACCEPTABLE Classification ---"
if grep -q 'ACCEPTABLE' "$TARGET_FILE" 2>/dev/null; then
    pass "Documents ACCEPTABLE classification level"
else
    fail "Missing ACCEPTABLE classification level"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: Documents WARNING classification level
# -----------------------------------------------------------------------------
echo "--- Test 4: WARNING Classification ---"
if grep -q 'WARNING' "$TARGET_FILE" 2>/dev/null; then
    pass "Documents WARNING classification level"
else
    fail "Missing WARNING classification level"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: Documents CRITICAL classification level
# -----------------------------------------------------------------------------
echo "--- Test 5: CRITICAL Classification ---"
if grep -q 'CRITICAL' "$TARGET_FILE" 2>/dev/null; then
    pass "Documents CRITICAL classification level"
else
    fail "Missing CRITICAL classification level"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 6: Treelint-specific threshold for function length (max 100 lines)
# -----------------------------------------------------------------------------
echo "--- Test 6: Function Length Threshold (100 lines) ---"
if grep -qE '100.*lines|method.*max.*100|function.*length.*100|max_length.*100' "$TARGET_FILE" 2>/dev/null; then
    pass "Documents method/function max 100 lines threshold"
else
    fail "Missing method/function max 100 lines threshold"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 7: Treelint-specific classification logic linking metrics to levels
# AC#3 requires: "Each function is classified as ACCEPTABLE/WARNING/CRITICAL"
# This must be NEW Treelint-specific classification, not existing complexity thresholds
# -----------------------------------------------------------------------------
echo "--- Test 7: Treelint Metrics Classification Logic ---"
if grep -qiE 'treelint.*classif|classif.*treelint|function.*length.*ACCEPTABLE|function.*length.*WARNING|function.*length.*CRITICAL|treelint.*ACCEPTABLE.*WARNING.*CRITICAL' "$TARGET_FILE" 2>/dev/null; then
    pass "Documents Treelint metrics classification logic"
else
    fail "Missing Treelint metrics classification logic (functions classified by Treelint output)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 8: Default thresholds when config missing (BR-002)
# -----------------------------------------------------------------------------
echo "--- Test 8: Default Threshold Fallback (BR-002) ---"
if grep -qiE 'default.*threshold|fallback.*threshold|threshold.*default|missing.*config.*default' "$TARGET_FILE" 2>/dev/null; then
    pass "Documents default threshold fallback behavior"
else
    fail "Missing default threshold fallback behavior (BR-002)"
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
